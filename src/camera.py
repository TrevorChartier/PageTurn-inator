from picamera2 import Picamera2
import numpy as np

class Camera:
    """Manages PiCamera initialization and frame capture."""

    def __init__(self):
        self.__camera = Picamera2()

        camera_config = self.__camera.create_video_configuration(
            main={
                "size": (640, 480),
                "format": "RGB888"
            },
            controls={
                # Request 50 FPS
                "FrameDurationLimits": (int(1e6 / 50), int(1e6 / 50))  
            }
        )

        self.__camera.configure(camera_config)
        self.__camera.start()

    def get_latest_frame(self) -> np.ndarray:
        """Retrieve the most recent frame.

        Returns: 
            np.ndarray: Copy of latest frame as a numpy array in RGB
        """
        return self.__camera.capture_array()[:, :, ::].copy()
    
    def cleanup(self):
        self.__camera.stop()
        self.__camera.close()