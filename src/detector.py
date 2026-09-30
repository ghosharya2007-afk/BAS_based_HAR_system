"""Pose (YOLOv8) + object detection (Roboflow RF-DETR, local)."""
import numpy as np
from ultralytics import YOLO

WRIST_L, WRIST_R = 9, 10

class Detector:
    def __init__(self, pose_path, api_key, model_id, conf=0.30):
        self.pose = YOLO(pose_path)
        from inference import get_model
        print("Loading RF-DETR (first run downloads once, then offline)...")
        self.obj = get_model(model_id=model_id, api_key=api_key)
        self.conf = conf

    def detect(self, frame, wanted_objects=None):
        wrists, objects = [], {}

        pr = self.pose(frame, verbose=False, conf=0.40)[0]
        if pr.keypoints is not None and len(pr.keypoints.xy):
            kpts = pr.keypoints.xy[0].cpu().numpy()
            for idx in (WRIST_L, WRIST_R):
                if idx < len(kpts):
                    wrists.append((float(kpts[idx][0]), float(kpts[idx][1])))

        res = self.obj.infer(frame, confidence=self.conf)[0]
        for p in res.predictions:
            label = p.class_name.lower()
            label = {"lead": "lid"}.get(label, label) 
            if wanted_objects and label not in wanted_objects:
                continue
            x1, y1 = p.x - p.width / 2, p.y - p.height / 2
            x2, y2 = p.x + p.width / 2, p.y + p.height / 2
            objects.setdefault(label, (float(x1), float(y1), float(x2), float(y2),
                                       float(p.confidence)))
        return {"wrists": wrists, "objects": objects}

    @staticmethod
    def hand_holds_object(wrists, obj_box, max_dist):
        if not wrists or obj_box is None:
            return False
        x1, y1, x2, y2, _ = obj_box
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        return any(np.hypot(wx - cx, wy - cy) <= max_dist for wx, wy in wrists)