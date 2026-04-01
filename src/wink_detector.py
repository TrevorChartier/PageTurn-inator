import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

class WinkDetector:
    def __init__(self, model_path="model/face_landmarker.task"):
        BaseOptions = mp.tasks.BaseOptions
        FaceLandmarker = mp.tasks.vision.FaceLandmarker
        FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE
        )

        self.__current_face_landmarks = None
        self.NO_WINK = 0
        self.LEFT_WINK = 1
        self.RIGHT_WINK = 2
        self.__detector = vision.FaceLandmarker.create_from_options(options)
        
    def detect_wink(self, frame: np.ndarray) -> int:
        """Detect the presence of a wink in the frame
        
        Returns: int (between 0 or 2)
            0: No Wink
            1: Left Eye Wink
            2: Right Eye Wink
        """
        mp_image = mp.Image(mp.ImageFormat.SRGB, frame)
        face_landmarker_result = self.__detector.detect(mp_image)
        
        if face_landmarker_result.face_landmarks:
            self.__current_face_landmarks = face_landmarker_result.face_landmarks
            return self.__detect_wink(
                face_landmarker_result.face_landmarks[0],
                frame.shape[1], frame.shape[0]
                )
        else:
            # No Face Detected in Frame
            self.__current_face_landmarks = None
            return  self.NO_WINK

    def get_face_landmarks(self):
        return self.__current_face_landmarks
        
    def __eye_aspect_ratio(self, eye_landmarks, frame_width, frame_height):
        eye_pts = np.array([[lm.x * frame_width, lm.y * frame_height] for lm in eye_landmarks])
        
        A = np.linalg.norm(eye_pts[1] - eye_pts[5])
        B = np.linalg.norm(eye_pts[2] - eye_pts[4])
        C = np.linalg.norm(eye_pts[0] - eye_pts[3])
        
        ear = (A + B) / (2.0 * C)
        return ear
    
    def __detect_wink(self, face_landmarks, frame_width, frame_height):
    
        right_eye_indices = [33, 160, 158, 133, 153, 144]
        left_eye_indices = [362, 387, 385, 263, 380, 373]

        left_eye_landmarks = [face_landmarks[i] for i in left_eye_indices]
        right_eye_landmarks = [face_landmarks[i] for i in right_eye_indices]

        left_ear = self.__eye_aspect_ratio(left_eye_landmarks, frame_width, frame_height)
        right_ear = self.__eye_aspect_ratio(right_eye_landmarks, frame_width, frame_height)

        EAR_THRESHOLD = 0.18
        if left_ear < EAR_THRESHOLD and right_ear >= EAR_THRESHOLD:
            return self.LEFT_WINK
        elif right_ear < EAR_THRESHOLD and left_ear >= EAR_THRESHOLD:
            return self.RIGHT_WINK
        else:
            return self.NO_WINK