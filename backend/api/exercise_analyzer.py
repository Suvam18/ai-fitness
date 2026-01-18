"""
Enhanced Exercise Analyzer for API use
Refactored from app.py - removed print statements and console output
"""
import numpy as np
import time
from typing import Dict, List, Tuple, Optional


class EnhancedExerciseAnalyzer:
    """
    Analyzes exercise form and counts repetitions based on body landmarks.
    Refactored for API use without console output.
    """
    
    def __init__(self, exercise_type: str = "bicep_curl"):
        """
        Initialize the exercise analyzer.
        
        Args:
            exercise_type: Type of exercise to analyze (bicep_curl, squat, etc.)
        """
        self.exercise_type = exercise_type
        self.rep_count = 0
        self.set_count = 1
        self.current_stage = "start"
        self.start_time = time.time()
        self.rep_history = []
        self.calories_burned = 0.0
        self.rep_start_time = None

    def calculate_angle(self, a: Tuple[float, ...], b: Tuple[float, ...], c: Tuple[float, ...]) -> float:
        """
        Calculate the angle between three points.
        
        Args:
            a: First point (x, y, z, visibility)
            b: Middle point (vertex of angle)
            c: Third point
            
        Returns:
            Angle in degrees
        """
        try:
            # Use only x,y for 2D angle calculation
            a = np.array(a[:2])
            b = np.array(b[:2])
            c = np.array(c[:2])
            
            ba = a - b
            bc = c - b
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1, 1)
            
            return np.degrees(np.arccos(cosine_angle))
        except:
            return 0.0

    def calculate_distance(self, point1: Tuple[float, ...], point2: Tuple[float, ...]) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            point1: First point (x, y, ...)
            point2: Second point (x, y, ...)
            
        Returns:
            Distance between points
        """
        try:
            return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
        except:
            return 0.0

    def analyze_bicep_curl(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict:
        """
        Analyze bicep curl form and count reps.
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary containing analysis results
        """
        feedback = []
        errors = []
        warnings = []
        
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        elbow = key_points.get('right_elbow', (0, 0, 0, 0))
        wrist = key_points.get('right_wrist', (0, 0, 0, 0))
        
        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Rep counting with time tracking
        current_time = time.time()
        
        if self.current_stage == "start" and elbow_angle < 80:
            self.current_stage = "up"
            self.rep_start_time = current_time
        elif self.current_stage == "up" and elbow_angle > 160:
            self.current_stage = "down"
            self.rep_count += 1
            rep_duration = current_time - self.rep_start_time if self.rep_start_time else 0
            self.rep_history.append(rep_duration)
            self.calories_burned += 0.5  # Approximate calories per rep
            
            feedback.append(f"Rep {self.rep_count} completed! ({rep_duration:.1f}s)")
            
            # Check for consistent tempo
            if len(self.rep_history) > 1:
                avg_duration = np.mean(self.rep_history)
                if rep_duration > avg_duration * 1.5:
                    warnings.append("Slow down - maintain consistent tempo")
                elif rep_duration < avg_duration * 0.5:
                    warnings.append("Speed up - don't rush the movement")
                    
        elif self.current_stage == "down" and elbow_angle < 80:
            self.current_stage = "up"
            self.rep_start_time = current_time
            
        # Form checks
        elbow_shoulder_distance = abs(elbow[0] - shoulder[0])
        if elbow_shoulder_distance > 0.12:
            errors.append("Keep elbows tight to your body")
        elif elbow_shoulder_distance > 0.08:
            warnings.append("Elbows starting to drift out")
            
        if elbow_angle > 170 and self.current_stage != "start":
            warnings.append("Fully extend arms for maximum range")
            
        return {
            'angles': {'elbow': elbow_angle},
            'rep_count': self.rep_count,
            'set_count': self.set_count,
            'feedback': feedback,
            'errors': errors,
            'warnings': warnings,
            'stage': self.current_stage,
            'calories': self.calories_burned
        }

    def analyze_squat(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict:
        """
        Analyze squat form and count reps.
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary containing analysis results
        """
        feedback = []
        errors = []
        warnings = []
        
        hip = key_points.get('right_hip', (0, 0, 0, 0))
        knee = key_points.get('right_knee', (0, 0, 0, 0))
        ankle = key_points.get('right_ankle', (0, 0, 0, 0))
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        
        knee_angle = self.calculate_angle(hip, knee, ankle)
        hip_angle = self.calculate_angle(shoulder, hip, knee)
        
        # Squat rep counting
        if self.current_stage == "start" and knee_angle < 150:
            self.current_stage = "down"
        elif self.current_stage == "down" and knee_angle > 160:
            self.current_stage = "up"
            self.rep_count += 1
            self.calories_burned += 1.0  # More calories for squats
            feedback.append(f"Squat {self.rep_count} completed!")
        elif self.current_stage == "up" and knee_angle < 150:
            self.current_stage = "down"
            
        # Depth analysis
        if knee_angle < 90:
            feedback.append("Great depth!")
        elif knee_angle < 110:
            warnings.append("Go deeper for better results")
        else:
            errors.append("Not deep enough - aim for 90°")
            
        # Knee alignment
        if abs(knee[0] - ankle[0]) > 0.1:
            errors.append("Keep knees aligned with ankles")
            
        # Back position
        if hip_angle < 150:
            errors.append("Keep your back straight")
            
        return {
            'angles': {'knee': knee_angle, 'hip': hip_angle},
            'rep_count': self.rep_count,
            'feedback': feedback,
            'errors': errors,
            'warnings': warnings,
            'stage': self.current_stage,
            'calories': self.calories_burned
        }

    def analyze_shoulder_press(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict:
        """
        Analyze shoulder press form and count reps.
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary containing analysis results
        """
        feedback = []
        errors = []
        warnings = []
        
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        elbow = key_points.get('right_elbow', (0, 0, 0, 0))
        wrist = key_points.get('right_wrist', (0, 0, 0, 0))
        
        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        if self.current_stage == "start" and elbow_angle < 100:
            self.current_stage = "up"
        elif self.current_stage == "up" and elbow_angle > 160:
            self.current_stage = "down"
            self.rep_count += 1
            self.calories_burned += 0.6
            feedback.append(f"Shoulder Press {self.rep_count} completed!")
        elif self.current_stage == "down" and elbow_angle < 100:
            self.current_stage = "up"
            
        # Form checks
        if elbow_angle < 90:
            warnings.append("Good depth - keep elbows at 90°")
        if abs(elbow[0] - shoulder[0]) > 0.15:
            errors.append("Keep elbows in front of shoulders")
            
        return {
            'angles': {'elbow': elbow_angle},
            'rep_count': self.rep_count,
            'feedback': feedback,
            'errors': errors,
            'warnings': warnings,
            'stage': self.current_stage,
            'calories': self.calories_burned
        }

    def analyze_plank(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict:
        """
        Analyze plank form and track duration.
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary containing analysis results
        """
        feedback = []
        errors = []
        warnings = []
        
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        hip = key_points.get('right_hip', (0, 0, 0, 0))
        ankle = key_points.get('right_ankle', (0, 0, 0, 0))
        
        # Calculate body alignment angle
        body_angle = self.calculate_angle(shoulder, hip, ankle)
        
        # Plank is time-based, not rep-based
        current_time = time.time()
        plank_duration = current_time - self.start_time
        
        # Update calories based on time (approx 3 calories per minute)
        self.calories_burned = plank_duration * (3/60)
        
        # Form checks
        if body_angle < 160:
            errors.append("Keep your body straight - don't sag")
        elif body_angle > 175:
            warnings.append("Don't raise hips too high")
        else:
            feedback.append(f"Perfect plank form! {int(plank_duration)}s")
            
        # Check hip height relative to shoulders
        if hip[1] > shoulder[1] + 0.1:
            errors.append("Hips are too low - engage core")
            
        return {
            'angles': {'body': body_angle},
            'duration': plank_duration,
            'feedback': feedback,
            'errors': errors,
            'warnings': warnings,
            'stage': 'hold',
            'calories': self.calories_burned
        }

    def analyze_form(self, key_points: Optional[Dict[str, Tuple[float, ...]]]) -> Dict:
        """
        Analyze exercise form based on the exercise type.
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary containing analysis results
        """
        if not key_points:
            return {
                'errors': ['No person detected'],
                'rep_count': self.rep_count,
                'stage': self.current_stage,
                'angles': {},
                'feedback': [],
                'warnings': [],
                'calories': self.calories_burned
            }
            
        if self.exercise_type == "bicep_curl":
            return self.analyze_bicep_curl(key_points)
        elif self.exercise_type == "squat":
            return self.analyze_squat(key_points)
        elif self.exercise_type == "shoulder_press":
            return self.analyze_shoulder_press(key_points)
        elif self.exercise_type == "plank":
            return self.analyze_plank(key_points)
        elif self.exercise_type == "push_up":
            # Push-ups use similar mechanics to bicep curls
            return self.analyze_bicep_curl(key_points)
        else:
            return {
                'errors': ['Exercise not supported'],
                'rep_count': self.rep_count,
                'stage': self.current_stage,
                'angles': {},
                'feedback': [],
                'warnings': [],
                'calories': self.calories_burned
            }

    def reset(self):
        """Reset the analyzer state to initial values."""
        self.rep_count = 0
        self.current_stage = "start"
        self.calories_burned = 0.0
        self.rep_history = []
        self.rep_start_time = None
