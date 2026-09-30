from flask import Flask, Response, render_template_string
import cv2
import threading

app = Flask(__name__)
cap = cv2.VideoCapture(0)

HTML = """
<!DOCTYPE html><html>
<head><title>HAR-BAS Monitor</title>
<style>body{background:#111;color:#0f0;font-family:monospace;text-align:center;}
h1{color:#0f0;} img{border:2px solid #0f0;width:640px;}</style></head>
<body>
<h1>HAR-BAS Experiment Monitor</h1>
<img src="/video"><br>
<h2 id="step">Current Step: Waiting...</h2>
<h3 id="alert" style="color:red;"></h3>
</body></html>
"""

def generate():
    while True:
        ret, frame = cap.read()
        if not ret: break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)