import cv2
import time
from llava_engine import detect_action, get_step_index

cap = cv2.VideoCapture(0)
time.sleep(2)  # let camera warm up
ret, frame = cap.read()
cap.release()

cv2.imshow("Captured Frame", frame)
cv2.waitKey(3000)  # show for 3 seconds so you can see what was captured
cv2.destroyAllWindows()

action = detect_action(frame)
step = get_step_index(action)
print(f"Action: {action} | Step index: {step}")