import cv2
import cv2.aruco as aruco
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, params)

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils
pose = mp_pose.Pose()

def get_rack_origin(corners, ids):
    if ids is None: return None
    for i, mid in enumerate(ids.flatten()):
        if mid == 0:
            c = corners[i][0]
            return np.mean(c, axis=0)  # center of marker 0 as origin
    return None

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    
    rack_origin = get_rack_origin(corners, ids)
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks and rack_origin is not None:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        h, w, _ = frame.shape
        rw = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        lw = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]

        rw_px = np.array([rw.x * w, rw.y * h])
        lw_px = np.array([lw.x * w, lw.y * h])

        # Rack-relative positions
        rw_rel = rw_px - rack_origin
        lw_rel = lw_px - rack_origin

        print(f"R_Wrist_rack: ({rw_rel[0]:.1f}, {rw_rel[1]:.1f}) | L_Wrist_rack: ({lw_rel[0]:.1f}, {lw_rel[1]:.1f})")

        cv2.circle(frame, tuple(rack_origin.astype(int)), 8, (0,255,0), -1)
        cv2.putText(frame, "Rack Origin", tuple(rack_origin.astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    cv2.imshow("Rack + Pose", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()