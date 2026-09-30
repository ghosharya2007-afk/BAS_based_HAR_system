import cv2
cap = cv2.VideoCapture(0)  # 0 = laptop cam
while True:
    ret, frame = cap.read()
    cv2.imshow("Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break