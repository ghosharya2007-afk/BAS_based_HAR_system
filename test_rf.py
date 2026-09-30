"""Test: run your Roboflow model locally, print what it sees."""
from inference import get_model
import cv2

API_KEY  = "ZjrcDk63NntAo98TC63j"   # ← replace
MODEL_ID = "arya-ghosh/bas-dgyu0-2-rfdetr-seg-small-t1"               # ← verify this matches the Current Model chip

print("Downloading weights (first time only)...")
model = get_model(model_id=MODEL_ID, api_key=API_KEY)

cap = cv2.VideoCapture(0)
print("Show your objects. Press Q to quit.")

while True:
    ok, frame = cap.read()
    if not ok:
        break
    results = model.infer(frame)[0]
    if results.predictions:
        for p in results.predictions:
            print(f"  {p.class_name}: {p.confidence:.2f}")
            x1, y1 = int(p.x - p.width/2), int(p.y - p.height/2)
            x2, y2 = int(p.x + p.width/2), int(p.y + p.height/2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{p.class_name} {p.confidence:.2f}",
                        (x1, y1-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow("RF local test", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()