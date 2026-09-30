"""Timestamped JSONL event log."""
import json, os, time, datetime

class EventLogger:
    def __init__(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.path = os.path.join(log_dir, f"experiment_{ts}.jsonl")

    def log(self, event_type, **data):
        rec = {"t": time.time(),
               "time": datetime.datetime.now().isoformat(timespec="seconds"),
               "event": event_type, **data}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        return rec