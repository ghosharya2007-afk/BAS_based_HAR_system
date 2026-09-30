import ollama
import cv2
import base64
import numpy as np

def frame_to_base64(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def detect_action(frame):
    img_b64 = frame_to_base64(frame)
    
    response = ollama.chat(
        model='llava',
        messages=[{
            'role': 'user',
            'content': '''Look at this image. What is the person doing with their hands?
Choose ONLY one from these options and reply with just that text, nothing else:
- picking container
- opening container
- extracting with spatula
- closing container
- none''',
            'images': [img_b64]
        }]
    )
    
    result = response['message']['content'].strip().lower()
    print(f"LLaVA detected: {result}")
    return result

ACTION_MAP = {
    "picking container": 0,
    "opening container": 1,
    "extracting with spatula": 2,
    "closing container": 3,
}

def get_step_index(action):
    for key, idx in ACTION_MAP.items():
        if key in action:
            return idx
    return -1