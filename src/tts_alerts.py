"""Offline text-to-speech alerts (pyttsx3)."""
import threading, queue, time

class TTSAlerts:
    def __init__(self, cooldown=6.0, enabled=True):
        self.enabled = enabled
        self.cooldown = cooldown
        self.q = queue.Queue()
        self._last = {}
        self._engine = None
        if enabled:
            try:
                import pyttsx3
                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", 170)
                threading.Thread(target=self._worker, daemon=True).start()
            except Exception as e:
                print(f"[TTS ERROR] {e} - voice alerts disabled")
                self.enabled = False

    def speak(self, text, key=None):
        if not self.enabled:
            return
        key = key or text
        now = time.time()
        if now - self._last.get(key, 0) < self.cooldown:
            return
        self._last[key] = now
        self.q.put(text)

    def _worker(self):
        while True:
            text = self.q.get()
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception as e:
                print(f"[TTS ERROR] {e}")

    def step_done(self, name):      self.speak(f"{name} done", key="step_done")
    def step_skipped(self, names):  self.speak(f"Alert: step missed. {names}", key="skip")
    def out_of_order(self, name):   self.speak(f"Alert: out of sequence. {name}", key="ooo")
    def next_step(self, name):      self.speak(f"Next step: {name}", key="next")
    def experiment_complete(self):  self.speak("All steps complete. Experiment finished.", key="done")