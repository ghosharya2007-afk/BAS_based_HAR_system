"""Camera capture and local video recording."""
import cv2

class CameraSystem:
    def __init__(self, index=0, width=1280, height=720,
                 stream_ip=None, stream_port=5000, record_path=None):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera.")
        self.writer = None
        if record_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(record_path, fourcc, 20.0, (width, height))

    def read(self):
        ok, frame = self.cap.read()
        if not ok:
            return None
        if self.writer:
            self.writer.write(frame)
        return frame

    def release(self):
        self.cap.release()
        if self.writer:
            self.writer.release()