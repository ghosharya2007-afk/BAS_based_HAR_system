"""Step-condition tracker with frame debounce."""

class StepTracker:
    def __init__(self, steps, confirm_frames=5, cooldown_frames=40):
        self.step_ids = [s["id"] for s in steps]
        self.confirm_frames = confirm_frames
        self.cooldown = cooldown_frames
        self.streak = {sid: 0 for sid in self.step_ids}
        self.cool = 0

    def update(self, active_id):
        if self.cool > 0:
            self.cool -= 1
            return None
        confirmed = None
        for sid in self.step_ids:
            if sid == active_id:
                self.streak[sid] += 1
                if self.streak[sid] >= self.confirm_frames:
                    confirmed = sid
            else:
                self.streak[sid] = 0
        if confirmed is not None:
            self.streak = {k: 0 for k in self.streak}
            self.cool = self.cooldown
        return confirmed