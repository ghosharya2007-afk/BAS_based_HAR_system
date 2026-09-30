"""Global configuration for the HAR-BAS system."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Paths ---
MODELS_DIR   = os.path.join(BASE_DIR, "models")
LOGS_DIR     = os.path.join(BASE_DIR, "data", "logs")
VIDEOS_DIR   = os.path.join(BASE_DIR, "data", "videos")
POSE_MODEL   = os.path.join(MODELS_DIR, "yolov8n-pose.pt")

# --- Roboflow RF-DETR ---
ROBOFLOW_API_KEY  = "DkZjrc63NntAo98TC63j"   # ← your Roboflow private key
ROBOFLOW_MODEL_ID = "arya-ghosh/bas-dgyu0-2-rfdetr-seg-small-t1"                       # ← check "Current Model" chip!

# --- Thresholds ---
CONF_THRES      = 0.20
DIST_THRESH     = 300
CONFIRM_FRAMES  = 3
COOLDOWN_FRAMES = 40
SEPARATION_DIST = 80
MOTION_THRESH   = 25
PROXIMITY_DIST  = 100
ALERT_COOLDOWN  = 6.0

# --- Experiment (5 steps) ---
EXPERIMENT_STEPS = [
    "Pick Up Container",
    "Open Container",
    "Use Spoon to Extract",
    "Place Contents in Rack",
    "Close Container",
]

STEP_CONDITIONS = [
    {"objects": ["container"],           "interaction": "hand_distance"},
    {"objects": ["lid", "container"],    "interaction": "separation"},
    {"objects": ["spoon", "container"],  "interaction": "enter_exit"},
    {"objects": ["spoon"],               "interaction": "hand_distance"},
    {"objects": ["lid", "container"],    "interaction": "proximity"},
]

DAG = {0: [1], 1: [2], 2: [3], 3: [4]}
current_step = 0

# --- Camera ---
CAMERA_INDEX = 0
FRAME_WIDTH, FRAME_HEIGHT = 1280, 720
RECORD_LOCAL = True