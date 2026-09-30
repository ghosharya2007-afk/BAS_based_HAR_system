import cv2
import mediapipe as mp
import numpy as np
import os
from config import EXPERIMENT_STEPS

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)
output_dir = "keypoint_data"
os.makedirs(output_dir, exist_ok=True)

step_idx = 0
recording = False
keypoints_buffer = []

print(f"Steps: {EXPERIMENT_STEPS}")
print("Press number keys 0-4 to select step, SPACE to record, Q to quit\n")

while True:
    ret, frame = cap.read()
    if not ret: break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    cv2.putText(frame, f"Step: {EXPERIMENT_STEPS[step_idx]} | Recording: {recording}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0) if not recording else (0,0,255), 2)

    if results.pose_landmarks:
        kpts = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
        
        if recording:
            keypoints_buffer.append(kpts)
            cv2.putText(frame, f"Frames: {len(keypoints_buffer)}", (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv2.imshow("Data Collection", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord(' '):
        if not recording:
            recording = True
            keypoints_buffer = []
            print(f"Recording {EXPERIMENT_STEPS[step_idx]}...")
        else:
            recording = False
            if len(keypoints_buffer) > 20:
                fname = f"{output_dir}/step_{step_idx}_{len(os.listdir(output_dir))}.npy"
                np.save(fname, np.array(keypoints_buffer))
                print(f"Saved {fname} ({len(keypoints_buffer)} frames)")
            keypoints_buffer = []
    elif ord('0') <= key <= ord('4'):
        step_idx = key - ord('0')

cap.release()
cv2.destroyAllWindows()