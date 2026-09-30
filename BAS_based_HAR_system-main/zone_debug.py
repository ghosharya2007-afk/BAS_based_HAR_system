import cv2
import cv2.aruco as aruco
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, params)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def get_rack_origin(corners, ids):
    if ids is None: return None
    for i, mid in enumerate(ids.flatten()):
        if mid == 0:
            return np.mean(corners[i][0], axis=0)
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
        h, w, _ = frame.shape
        rw = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        rw_px = np.array([rw.x * w, rw.y * h])
        rw_rel = rw_px - rack_origin

        cv2.putText(frame, f"Wrist_rel: ({rw_rel[0]:.0f}, {rw_rel[1]:.0f})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.imshow("Zone Debug", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
