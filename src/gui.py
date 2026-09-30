"""Tkinter monitoring GUI."""
import tkinter as tk
from PIL import Image, ImageTk
import cv2

class MonitorGUI:
    def __init__(self, title="HAR-BAS Monitor"):
        self.root = tk.Tk()
        self.root.title(title)
        self.video_label = tk.Label(self.root)
        self.video_label.pack(side=tk.LEFT)
        panel = tk.Frame(self.root)
        panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        self.exp_label  = tk.Label(panel, text="Experiment: -", font=("Segoe UI", 13, "bold"))
        self.next_label = tk.Label(panel, text="Next step: -", font=("Segoe UI", 11))
        self.prog_label = tk.Label(panel, text="Progress: 0/0", font=("Segoe UI", 11))
        self.status_label = tk.Label(panel, text="Status: idle", font=("Segoe UI", 11), fg="blue")
        self.log_box = tk.Text(panel, width=42, height=20, state=tk.DISABLED)
        for w in (self.exp_label, self.next_label, self.prog_label, self.status_label, self.log_box):
            w.pack(anchor="w", pady=3)

    def set_experiment(self, name):       self.exp_label.config(text=f"Experiment: {name}")
    def set_next(self, text):             self.next_label.config(text=f"Next step: {text}")
    def set_progress(self, text):         self.prog_label.config(text=f"Progress: {text}")
    def set_status(self, text, color="blue"): self.status_label.config(text=f"Status: {text}", fg=color)

    def log(self, msg):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def show_frame(self, frame_bgr):
        img = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        try: self.root.destroy()
        except Exception: pass