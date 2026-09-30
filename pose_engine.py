import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
pose = mp_pose.Pose()

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # Print wrist landmarks (key for hand tracking)
        lw = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        rw = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        print(f"L_Wrist: ({lw.x:.2f}, {lw.y:.2f}) | R_Wrist: ({rw.x:.2f}, {rw.y:.2f})")

    cv2.imshow("Pose", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()