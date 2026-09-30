import cv2
import mediapipe as mp
import numpy as np
import json
import datetime
import threading
import time
import ollama
import base64
from flask import Flask, Response, render_template_string, request, redirect
from validator import validate_step, EXPERIMENT_STEPS
import validator

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html>
<head><title>HAR-BAS Monitor</title>
<meta http-equiv="refresh" content="3">
<style>
body{background:#111;color:#0f0;font-family:monospace;text-align:center;}
h1{color:#0f0;} img{border:2px solid #0f0;width:640px;}
.alert{color:red;font-size:1.5em;}
.step{color:#0f0;font-size:1.3em;}
.btn{background:#0f0;color:#111;border:none;padding:10px 30px;font-size:1.2em;cursor:pointer;margin-top:10px;}
</style></head>
<body>
<h1>HAR-BAS Experiment Monitor</h1>
<img src="/video"><br>
<div class="step">Current Step: {{ step }}</div>
<div class="step">Next Step: {{ next_step }}</div>
<div class="alert">{{ alert }}</div>
<form action="/reset" method="post">
<button class="btn" type="submit">🔄 Reset Experiment</button>
</form>
<h3>Log:</h3>
<pre style="color:#aaa;text-align:left;margin:auto;width:640px;">{{ log }}</pre>
</body></html>
"""

state = {"current_step": 0, "alert": "", "log": []}
frame_global = None

ACTION_MAP = {
    "picking container": 0,
    "opening container": 1,
    "extracting with spatula": 2,
    "closing container": 3,
}

def frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def detect_action(frame):
    try:
        img_b64 = frame_to_base64(frame)
        response = ollama.chat(
            model='llava',
            messages=[{
                'role': 'user',
                'content': '''Look at this image. What is the person doing with their hands?
Choose ONLY one from these options and reply with just that text, nothing else:
- picking container
- opening container
- extracting with spatula
- closing container
- none''',
                'images': [img_b64]
            }]
        )
        result = response['message']['content'].strip().lower()
        print(f"LLaVA: {result}")
        return result
    except Exception as e:
        print(f"LLaVA error: {e}")
        return "none"

def get_step_index(action):
    for key, idx in ACTION_MAP.items():
        if key in action:
            return idx
    return -1

def log_event(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"[{ts}] {msg}"
    state["log"].append(entry)
    with open("experiment_log.jsonl", "a") as f:
        f.write(json.dumps({"time": ts, "event": msg}) + "\n")

def speak(text):
    import pyttsx3
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

def generate():
    while True:
        if frame_global is not None:
            _, buffer = cv2.imencode('.jpg', frame_global)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def index():
    cs = state["current_step"]
    step_name = EXPERIMENT_STEPS[cs] if cs < len(EXPERIMENT_STEPS) else "Done"
    next_name = EXPERIMENT_STEPS[cs+1] if cs+1 < len(EXPERIMENT_STEPS) else "Experiment Complete"
    log_text = "\n".join(state["log"][-10:])
    return render_template_string(HTML, step=step_name, next_step=next_name, alert=state["alert"], log=log_text)

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset', methods=['POST'])
def reset():
    validator.current_step = 0
    state["current_step"] = 0
    state["alert"] = ""
    state["log"] = []
    log_event("Experiment reset")
    speak("Experiment reset. Starting from Step 1.")
    return redirect('/')

def llava_loop():
    global frame_global
    while True:
        if frame_global is not None:
            action = detect_action(frame_global)
            step_idx = get_step_index(action)

            if step_idx != -1:
                prev = validator.current_step
                validate_step(step_idx)
                state["current_step"] = validator.current_step

                if validator.current_step > prev:
                    msg = f"Step {prev+1} complete: {EXPERIMENT_STEPS[prev]}"
                    log_event(msg)
                    state["alert"] = ""
                    next_txt = EXPERIMENT_STEPS[validator.current_step] if validator.current_step < len(EXPERIMENT_STEPS) else "Experiment Complete"
                    speak(f"Step {prev+1} complete. Next: {next_txt}")
                elif step_idx < validator.current_step:
                    state["alert"] = f"⚠ Already completed: {EXPERIMENT_STEPS[step_idx]}"
                    log_event(f"Already completed: {EXPERIMENT_STEPS[step_idx]}")
                elif step_idx > validator.current_step:
                    state["alert"] = f"⚠ Skipped! Do: {EXPERIMENT_STEPS[validator.current_step]} first"
                    log_event(f"Skip alert at step {step_idx}")
                    speak(f"Step skipped. Please do {EXPERIMENT_STEPS[validator.current_step]} first")

        time.sleep(3)

def run_camera():
    global frame_global
    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(0)
    time.sleep(2)

    while True:
        ret, frame = cap.read()
        if not ret: break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        if results.pose_landmarks:
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cs = state["current_step"]
        label = EXPERIMENT_STEPS[cs] if cs < len(EXPERIMENT_STEPS) else "Done"
        cv2.putText(frame, f"Step: {label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        frame_global = frame.copy()
        cv2.imshow("HAR-BAS", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    threading.Thread(target=run_camera, daemon=True).start()
    threading.Thread(target=llava_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)