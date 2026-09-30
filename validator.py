from config import EXPERIMENT_STEPS, DAG
import pyttsx3
import threading

engine = pyttsx3.init()
current_step = 0

def speak(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

def validate_step(detected_step_index):
    global current_step

    if detected_step_index == current_step:
        print(f"✅ Step {current_step+1} complete: {EXPERIMENT_STEPS[current_step]}")
        next_text = EXPERIMENT_STEPS[current_step+1] if current_step+1 < len(EXPERIMENT_STEPS) else "Experiment Done"
        speak(f"Step {current_step+1} complete. Next: {next_text}")
        current_step += 1

    elif detected_step_index > current_step:
        print(f"⚠ Step skipped! Expected: {EXPERIMENT_STEPS[current_step]}")
        speak(f"Warning! Please complete {EXPERIMENT_STEPS[current_step]} first.")

    elif detected_step_index < current_step:
        print(f"⚠ Out of sequence!")
        speak(f"Out of sequence! Already completed {EXPERIMENT_STEPS[detected_step_index]}.")

    if current_step >= len(EXPERIMENT_STEPS):
        print("✅ Experiment complete!")
        speak("Experiment complete. All steps done.")
        current_step = 0