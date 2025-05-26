import numpy as np
from PIL import Image
import mediapipe as mp

mp_pose = mp.solutions.pose


def get_pose_landmarks(pil_image: Image.Image):
    """
    Process a PIL image and return the names of pose landmarks detected using MediaPipe.

    Args:
        pil_image (Image.Image): The input image in PIL format.

    Returns:
        List[str]: A list of pose landmark names detected in the image.
    """
    image_np = np.array(pil_image.convert("RGB"))
    
    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(image_np)

        if not results.pose_landmarks:
            return []

        landmark_names = [
            mp_pose.PoseLandmark(idx).name
            for idx, landmark in enumerate(results.pose_landmarks.landmark)
            if landmark.visibility > 0.5
        ]

        return landmark_names