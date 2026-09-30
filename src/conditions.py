"""Step-condition logic: hand_distance, motion_pickup, separation, enter_exit, proximity."""
import numpy as np

def bbox_center(b):
    return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)

def dist(a, b):
    return float(np.hypot(a[0] - b[0], a[1] - b[1]))

def inside(pt, box, margin=0):
    return (box[0]-margin <= pt[0] <= box[2]+margin
            and box[1]-margin <= pt[1] <= box[3]+margin)
def overlap_ratio(a, b):
    """Fraction of the smaller box covered by the other (0..1)."""
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    if x2 <= x1 or y2 <= y1:
        return 0.0
    inter = (x2 - x1) * (y2 - y1)
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / min(area_a, area_b)
class ConditionChecker:
    def __init__(self, conditions, dist_thresh, separation_dist,
                 motion_thresh, proximity_dist):
        self.conditions = conditions
        self.dist_thresh = dist_thresh
        self.sep = separation_dist
        self.motion = motion_thresh
        self.prox = proximity_dist
        self.prev_bbox = {}
        self.rest_pos = {}
        self.warmup = 40       # ~first few seconds: always learn rest position
        self.spoon_was_inside = False
    def _dist_to_box_edge(self, pt, box):
        """Distance from a point to the nearest edge of the box (0 if inside)."""
        x = min(max(pt[0], box[0]), box[2])
        y = min(max(pt[1], box[1]), box[3])
        return float(np.hypot(pt[0] - x, pt[1] - y))

    def _hand_near(self, wrists, box):
        if not wrists or box is None:
            return False
        return any(self._dist_to_box_edge(w, box) <= self.dist_thresh for w in wrists)    

    def _hand_near(self, wrists, box):
        if not wrists or box is None:
            return False
        c = bbox_center(box)
        return any(np.hypot(w[0]-c[0], w[1]-c[1]) <= self.dist_thresh for w in wrists)

    def active_step(self, idx, det):
        """True if step idx's condition holds this frame."""
        c = self.conditions[idx]
        kind = c["interaction"]
        objs = det["objects"]
        if kind in ("hand_distance", "motion_pickup"):
            oid = c["objects"][0]
            cur = objs.get(oid)
            if cur is None:
                return False
            near = self._hand_near(det["wrists"], cur)
            if kind == "hand_distance":
                return near
            if self.warmup > 0 or not near:
                self.rest_pos[oid] = bbox_center(cur)
                self.warmup = max(0, self.warmup - 1)
                return False
            rest = self.rest_pos.get(oid)
            if rest is None:
                return False
            return dist(rest, bbox_center(cur)) > self.motion

        if kind in ("separation", "proximity"):
            lid, cont = objs.get("lid"), objs.get("container")
            if lid is None or cont is None:
                return False
            if kind == "separation":
                return dist(bbox_center(lid), bbox_center(cont)) > self.sep
            # proximity = lid actually ON the jar (overlap), not just resting nearby
            return (inside(bbox_center(lid), cont)
                    or overlap_ratio(lid, cont) > 0.25)

        if kind == "enter_exit":
            spoon, cont = objs.get("spoon"), objs.get("container")
            if spoon is None or cont is None:
                return False
            if inside(bbox_center(spoon), cont, margin=30):
                self.spoon_was_inside = True
                return False
            return self.spoon_was_inside

        return False

    def on_confirmed(self, idx):
        if self.conditions[idx]["interaction"] == "enter_exit":
            self.spoon_was_inside = False
   