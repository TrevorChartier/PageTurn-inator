"""Provides visualization utilities for overlaying image processing 
results on a frame
"""

import numpy as np
import cv2


def visualize(
    frame: np.ndarray, face_landmarks
) -> np.ndarray:
    output_frame = frame.copy()

    if face_landmarks is None:
        return output_frame
    
    for face in face_landmarks:
        for lm in face:
            x = int(lm.x * frame.shape[1])
            y = int(lm.y * frame.shape[0])
            # Draw a small circle at each landmark
            cv2.circle(output_frame, (x, y), radius=1, color=(0, 255, 0), thickness=-1)
    return output_frame