import cv2
import mediapipe as mp
import numpy as np
import time

class Config:
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.5

class ExerciseAnalyzer:
    def __init__(self, exercise_type="Bicep Curls"):
        self.exercise_type = exercise_type
        self.rep_count = 0
        self.current_stage = "start"
        self.last_rep_time = time.time()
        self.mp_pose = mp.solutions.pose
        
    def calculate_angle(self, a, b, c):
        """Calculates the angle between three joints."""
        a = np.array(a) # First (e.g., Shoulder)
        b = np.array(b) # Mid (e.g., Elbow)
        c = np.array(c) # End (e.g., Wrist)
        
        ba = a - b
        bc = c - b
        
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(np.clip(cosine_angle, -1, 1)))
        return angle

    def analyze_form(self, landmarks):
        """Analyzes landmarks based on the exercise selected in the UI."""
        if not landmarks:
            return {'rep_count': self.rep_count, 'errors': ['No pose detected'], 'stage': self.current_stage}

        # Extract landmark coordinates
        l = landmarks
        # Helper to map landmarks to (x, y)
        def get_pt(idx): return [l[idx].x, l[idx].y]

        feedback = []
        errors = []
        current_angle = 0

        # --- BICEP CURLS LOGIC ---
        if self.exercise_type == "Bicep Curls":
            shoulder = get_pt(11); elbow = get_pt(13); wrist = get_pt(15)
            current_angle = self.calculate_angle(shoulder, elbow, wrist)
            
            if current_angle < 35:
                self.current_stage = "up"
            if current_angle > 160 and self.current_stage == "up":
                self.current_stage = "down"
                self.rep_count += 1
            if abs(elbow[0] - shoulder[0]) > 0.15:
                errors.append("Keep elbow close to body")

        # --- SQUATS LOGIC ---
        elif self.exercise_type == "Squats":
            hip = get_pt(23); knee = get_pt(25); ankle = get_pt(27)
            current_angle = self.calculate_angle(hip, knee, ankle)
            
            if current_angle < 100:
                self.current_stage = "down"
            if current_angle > 160 and self.current_stage == "down":
                self.current_stage = "up"
                self.rep_count += 1
            if abs(knee[0] - ankle[0]) > 0.2:
                errors.append("Align knees with feet")

        # --- PUSH-UPS LOGIC ---
        elif self.exercise_type == "Push-ups":
            shoulder = get_pt(11); elbow = get_pt(13); wrist = get_pt(15)
            current_angle = self.calculate_angle(shoulder, elbow, wrist)
            
            if current_angle < 90:
                self.current_stage = "down"
            if current_angle > 160 and self.current_stage == "down":
                self.current_stage = "up"
                self.rep_count += 1
            # Check for straight back using shoulder and hip y-coordinates
            hip = get_pt(23)
            if abs(shoulder[1] - hip[1]) > 0.4:
                errors.append("Keep your back straight")

        return {
            'rep_count': self.rep_count,
            'angle': current_angle,
            'stage': self.current_stage,
            'errors': errors,
            'exercise': self.exercise_type
        }