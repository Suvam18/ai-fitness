"""
Enhanced Exercise Analyzer for API use
Refactored from app.py - removed print statements and console output
"""
import numpy as np
import time
from typing import Dict, List, Tuple, Optional
from enum import Enum


class RepState(Enum):
    """States for the repetition state machine."""
    START = "start"
    IN_PROGRESS = "in_progress"
    PEAK_REACHED = "peak_reached"
    COMPLETED = "completed"


class RepCounter:
    """
    Robust repetition counter using Finite State Machine.
    Prevents double-counting and phantom reps by requiring full movement cycles.
    """
    
    def __init__(self, bottom_threshold: float = 80.0, peak_threshold: float = 160.0, 
                 hysteresis: float = 5.0):
        """
        Initialize the rep counter.
        
        Args:
            bottom_threshold: Angle threshold for bottom position (degrees)
            peak_threshold: Angle threshold for peak position (degrees)
            hysteresis: Hysteresis buffer to prevent jittery transitions
        """
        self.bottom_threshold = bottom_threshold
        self.peak_threshold = peak_threshold
        self.hysteresis = hysteresis
        
        self.state = RepState.START
        self.rep_count = 0
        self.rep_history = []
        self.last_angle = None
        self.angle_history = []  # Track recent angles for smoothing
        self.rep_start_time = None
        
    def _is_at_bottom(self, angle: float) -> bool:
        """Check if angle indicates bottom position with hysteresis."""
        if self.state == RepState.START:
            return angle <= self.bottom_threshold
        elif self.state == RepState.PEAK_REACHED:
            return angle <= self.bottom_threshold + self.hysteresis
        return False
        
    def _is_at_peak(self, angle: float) -> bool:
        """Check if angle indicates peak position with hysteresis."""
        if self.state == RepState.IN_PROGRESS:
            return angle >= self.peak_threshold
        return False
        
    def _is_moving_up(self, angle: float) -> bool:
        """Check if movement is upward (angle increasing)."""
        if self.last_angle is None:
            return False
        return angle > self.last_angle + 2.0  # Minimum movement threshold
        
    def _is_moving_down(self, angle: float) -> bool:
        """Check if movement is downward (angle decreasing)."""
        if self.last_angle is None:
            return False
        return angle < self.last_angle - 2.0  # Minimum movement threshold
        
    def update(self, angle: float, timestamp: float = None) -> Dict:
        """
        Update the state machine with new angle measurement.
        
        Args:
            angle: Current joint angle in degrees
            timestamp: Current timestamp (uses time.time() if None)
            
        Returns:
            Dictionary with rep count and state information
        """
        if timestamp is None:
            timestamp = time.time()
            
        # Store angle history for potential future smoothing
        self.angle_history.append(angle)
        if len(self.angle_history) > 5:
            self.angle_history.pop(0)
            
        # Use raw angle for now - smoothing can be added with more sophisticated logic
        smoothed_angle = angle
        
        rep_completed = False
        feedback = []
        
        # State machine transitions
        if self.state == RepState.START:
            # Wait for movement to begin (angle decreases to bottom)
            if self._is_at_bottom(smoothed_angle):
                self.state = RepState.IN_PROGRESS
                self.rep_start_time = timestamp
                feedback.append("Movement started")
                
        elif self.state == RepState.IN_PROGRESS:
            # Moving up towards peak
            if self._is_at_peak(smoothed_angle):
                self.state = RepState.PEAK_REACHED
                self.rep_count += 1
                rep_duration = timestamp - self.rep_start_time if self.rep_start_time else 0
                self.rep_history.append(rep_duration)
                feedback.append(f"Rep {self.rep_count} completed! ({rep_duration:.1f}s)")
                rep_completed = True
                
        elif self.state == RepState.PEAK_REACHED:
            # At peak, wait for movement back down
            if self._is_at_bottom(smoothed_angle):
                self.state = RepState.IN_PROGRESS
                self.rep_start_time = timestamp
                
        self.last_angle = smoothed_angle
        
        return {
            'rep_count': self.rep_count,
            'state': self.state.value,
            'rep_completed': rep_completed,
            'feedback': feedback,
            'smoothed_angle': smoothed_angle
        }
        
    def reset(self):
        """Reset the counter to initial state."""
        self.state = RepState.START
        self.rep_count = 0
        self.rep_history = []
        self.last_angle = None
        self.angle_history = []
        self.rep_start_time = None


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
        self.start_time = time.time()
        self.rep_history = []
        self.calories_burned = 0.0
        
        # Initialize rep counters for different exercises with appropriate thresholds
        self.rep_counters = {
            "bicep_curl": RepCounter(bottom_threshold=80.0, peak_threshold=160.0),
            "squat": RepCounter(bottom_threshold=90.0, peak_threshold=170.0),
            "shoulder_press": RepCounter(bottom_threshold=90.0, peak_threshold=160.0),
            "push_up": RepCounter(bottom_threshold=70.0, peak_threshold=160.0),  # Elbow angle
        }
        
        # Get the appropriate rep counter for current exercise
        self.rep_counter = self.rep_counters.get(exercise_type, RepCounter())

    @property
    def current_stage(self):
        """Get the current stage for backward compatibility."""
        state_mapping = {
            RepState.START: "start",
            RepState.IN_PROGRESS: "up", 
            RepState.PEAK_REACHED: "down",
            RepState.COMPLETED: "start"  # Should not happen with new logic
        }
        return state_mapping.get(self.rep_counter.state, "start")
        
    @current_stage.setter 
    def current_stage(self, value):
        """Set the current stage for backward compatibility."""
        # Map old stage names to new enum values
        stage_mapping = {
            "start": RepState.START,
            "up": RepState.IN_PROGRESS,
            "down": RepState.PEAK_REACHED,
        }
        if value in stage_mapping:
            self.rep_counter.state = stage_mapping[value]

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
        
        # Use robust state machine for rep counting
        rep_result = self.rep_counter.update(elbow_angle)
        self.rep_count = rep_result['rep_count']
        
        # Add rep counter feedback
        feedback.extend(rep_result['feedback'])
        
        # Update calories
        if rep_result['rep_completed']:
            self.calories_burned += 0.5  # Approximate calories per rep
            
            # Check for consistent tempo
            if len(self.rep_counter.rep_history) > 1:
                avg_duration = np.mean(self.rep_counter.rep_history)
                last_duration = self.rep_counter.rep_history[-1]
                if last_duration > avg_duration * 1.5:
                    warnings.append("Slow down - maintain consistent tempo")
                elif last_duration < avg_duration * 0.5:
                    warnings.append("Speed up - don't rush the movement")
                    
        # Form checks
        elbow_shoulder_distance = abs(elbow[0] - shoulder[0])
        if elbow_shoulder_distance > 0.12:
            errors.append("Keep elbows tight to your body")
        elif elbow_shoulder_distance > 0.08:
            warnings.append("Elbows starting to drift out")
            
        if elbow_angle > 170 and rep_result['state'] != "start":
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
        
        # Use robust state machine for rep counting
        rep_result = self.rep_counter.update(knee_angle)
        self.rep_count = rep_result['rep_count']
        
        # Add rep counter feedback
        feedback.extend(rep_result['feedback'])
        
        # Update calories
        if rep_result['rep_completed']:
            self.calories_burned += 1.0  # More calories for squats
            
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
        
        # Use robust state machine for rep counting
        rep_result = self.rep_counter.update(elbow_angle)
        self.rep_count = rep_result['rep_count']
        
        # Add rep counter feedback
        feedback.extend(rep_result['feedback'])
        
        # Update calories
        if rep_result['rep_completed']:
            self.calories_burned += 0.6
            
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
        self.calories_burned = 0.0
        self.rep_history = []
        
        # Reset the rep counter
        if hasattr(self, 'rep_counter'):
            self.rep_counter.reset()
