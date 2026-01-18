"""
Enhanced Pose Detector for API use
Refactored from app.py - removed print statements and CV2 display logic
"""
import mediapipe as mp
import cv2
import numpy as np
from typing import Optional, Dict, List, Tuple


class EnhancedPoseDetector:
    """
    Detects human pose landmarks from images using MediaPipe.
    Refactored for API use without console output or display logic.
    """
    
    def __init__(self, min_detection_confidence: float = 0.7, min_tracking_confidence: float = 0.5):
        """
        Initialize the pose detector with MediaPipe.
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.initialized = True

    def detect_pose(self, image: np.ndarray, draw_landmarks: bool = False) -> Tuple[Optional[any], np.ndarray]:
        """
        Detect pose landmarks in an image.
        
        Args:
            image: Input image as numpy array (BGR format)
            draw_landmarks: Whether to draw landmarks on the image
            
        Returns:
            Tuple of (landmarks, processed_image)
            - landmarks: MediaPipe pose landmarks or None if no person detected
            - processed_image: Image with landmarks drawn (if draw_landmarks=True) or original
        """
        try:
            # Convert BGR to RGB for MediaPipe
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = self.pose.process(image_rgb)
            image_rgb.flags.writeable = True
            
            # Convert back to BGR
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            
            landmarks = None
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                
                # Draw landmarks if requested
                if draw_landmarks:
                    self.mp_drawing.draw_landmarks(
                        image_bgr,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                        self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                    )
            
            return landmarks, image_bgr
        except Exception as e:
            # Return None for landmarks and original image on error
            return None, image

    def extract_key_points(self, landmarks) -> Optional[Dict[str, Tuple[float, float, float, float]]]:
        """
        Extract key body landmarks as a dictionary.
        
        Args:
            landmarks: MediaPipe pose landmarks
            
        Returns:
            Dictionary mapping landmark names to (x, y, z, visibility) tuples
            Returns None if landmarks is None
        """
        if not landmarks:
            return None
            
        key_points = {}
        landmark_indices = {
            'nose': 0, 'left_eye': 1, 'right_eye': 2,
            'left_ear': 7, 'right_ear': 8,
            'left_shoulder': 11, 'right_shoulder': 12,
            'left_elbow': 13, 'right_elbow': 14,
            'left_wrist': 15, 'right_wrist': 16,
            'left_hip': 23, 'right_hip': 24,
            'left_knee': 25, 'right_knee': 26,
            'left_ankle': 27, 'right_ankle': 28,
            'left_heel': 29, 'right_heel': 30,
            'left_foot_index': 31, 'right_foot_index': 32
        }
        
        for name, idx in landmark_indices.items():
            if idx < len(landmarks):
                landmark = landmarks[idx]
                key_points[name] = (landmark.x, landmark.y, landmark.z, landmark.visibility)
                
        return key_points
