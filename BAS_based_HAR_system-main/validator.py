from config import EXPERIMENT_STEPS, DAG
import threading

current_step = 0

def speak(text):
    import pyttsx3
    def _speak():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

def validate_step(detected_step_index):
    global current_step

    if current_step >= len(EXPERIMENT_STEPS):
        return

    if detected_step_index == current_step:
        print(f"✅ Step {current_step+1} complete: {EXPERIMENT_STEPS[current_step]}")
        current_step += 1
        if current_step >= len(EXPERIMENT_STEPS):
            speak("Experiment complete! All steps done.")
            print("✅ Experiment complete!")

    elif detected_step_index > current_step:
        msg = f"Step skipped. Please complete {EXPERIMENT_STEPS[current_step]} first."
        print(f"⚠ {msg}")
        speak(msg)

    elif detected_step_index < current_step:
        msg = f"Already completed {EXPERIMENT_STEPS[detected_step_index]}."
        print(f"⚠ {msg}")
        speak(msg)