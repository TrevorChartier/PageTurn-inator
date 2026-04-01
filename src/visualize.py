"""Provides visualization utilities for overlaying image processing 
results on a frame
"""

import numpy as np
import cv2

class Visualize:
    def __init__(self):
        self.__curr_wink_text = ""
        self.__frames_left_for_text = 0
        self.__NUM_FRAMES_TO_LOG_PER_WINK =  48
        
    def visualize(
        self, frame: np.ndarray, face_landmarks
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

        cv2.putText(
            output_frame, self.__curr_wink_text , (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA
        )
        self.__decrement_counter()
        return output_frame
    
    def log_left_wink(self):
        self.__curr_wink_text = "Left Wink Detected"
        self.__frames_left_for_text = self.__NUM_FRAMES_TO_LOG_PER_WINK
        
    def log_right_wink(self):
        self.__curr_wink_text = "Right Wink Detected"
        self.__frames_left_for_text = self.__NUM_FRAMES_TO_LOG_PER_WINK
        
    def __decrement_counter(self):
        self.__frames_left_for_text -= 1
        if self.__frames_left_for_text <= 0:
            self.__curr_wink_text = ""