import cv2
import numpy as np

def visualize(frame, results, cls=["face", "plate"], conf=0.25, mapping={0: "face", 1: "plate"}):
    frame_copy = frame.copy()

    number_cls_list = [num_cls for num_cls, name in mapping.items() if name in cls]

    for i, result in enumerate(results):
        if result.conf >= conf and result.cls in number_cls_list:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            roi = frame[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (55, 55), 11)
            frame_copy[y1:y2, x1:x2] = blurred_roi
    
    return frame_copy
