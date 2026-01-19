"""
Pose quality evaluation for real-time feedback.

This module implements the PoseQualityEvaluator class which calculates
pose quality scores, tracks historical performance, and generates
trainer-like feedback messages.
"""

from typing import Dict, List, Optional, Tuple
import logging
import random
import numpy as np
from backend.api.exercise_config import ExerciseConfig, get_exercise_config

logger = logging.getLogger(__name__)


class PoseQualityEvaluator:
    """Evaluates pose quality and generates real-time feedback.
    
    This class calculates pose quality scores based on exercise-specific
    form metrics, maintains historical averages, and generates contextual
    feedback messages for users.
    
    Attributes:
        exercise_type: Name of the exercise being evaluated
        config: Exercise-specific configuration
        history: List of quality scores from the current session
    """
    
    def __init__(self, exercise_type: str):
        """Initialize evaluator with exercise-specific configuration.
        
        Args:
            exercise_type: Name of the exercise (e.g., 'bicep_curl', 'squat')
        """
        self.exercise_type = exercise_type
        self.config: ExerciseConfig = get_exercise_config(exercise_type)
        self.history: List[float] = []
        
        logger.info(f"Initialized PoseQualityEvaluator for {exercise_type}")
    
    def calculate_quality_score(
        self, 
        form_metrics: Dict[str, float],
        analysis_result: Dict
    ) -> float:
        """Calculate pose quality score (0-100) from form metrics.
        
        Uses weighted average of form metrics with critical metrics
        receiving a 1.5x weight multiplier.
        
        Args:
            form_metrics: Dict of metric_name -> score (0-100)
            analysis_result: Full analysis result dict (for future use)
            
        Returns:
            Overall quality score between 0 and 100
        """
        # Handle empty metrics
        if not form_metrics and not self.config.metric_weights:
            return 50.0  # Neutral score for no metrics
        
        total_score = 0.0
        total_weight = 0.0
        
        for weight_config in self.config.metric_weights:
            # Get metric score, default to neutral 50.0 if missing
            metric_score = form_metrics.get(weight_config.name, 50.0)
            
            # Clamp metric score to 0-100 range
            metric_score = max(0.0, min(100.0, metric_score))
            
            # Critical metrics have 1.5x weight multiplier
            effective_weight = weight_config.weight * (1.5 if weight_config.is_critical else 1.0)
            
            total_score += metric_score * effective_weight
            total_weight += effective_weight
        
        # Calculate final score
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            # No configured metrics, use average of provided metrics
            if form_metrics:
                final_score = sum(form_metrics.values()) / len(form_metrics)
            else:
                final_score = 50.0
        
        # Ensure score is within bounds
        final_score = max(0.0, min(100.0, final_score))
        
        return final_score
    
    def get_feedback_category(self, quality_score: float) -> str:
        """Determine feedback category based on quality score.
        
        Categories:
        - 'poor': score < poor_threshold (default 60)
        - 'average': poor_threshold <= score < good_threshold (default 60-85)
        - 'excellent': score >= good_threshold (default 85+)
        
        Args:
            quality_score: Pose quality score (0-100)
            
        Returns:
            Feedback category: 'poor', 'average', or 'excellent'
        """
        if quality_score < self.config.thresholds.poor_threshold:
            return 'poor'
        elif quality_score < self.config.thresholds.good_threshold:
            return 'average'
        else:
            return 'excellent'
    
    def update_history(self, quality_score: float):
        """Add score to historical average.
        
        Maintains a sliding window of the last 100 scores to prevent
        memory growth in long sessions.
        
        Args:
            quality_score: Pose quality score to add to history
        """
        self.history.append(quality_score)
        
        # Keep only last 100 scores (sliding window)
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def get_historical_average(self) -> Optional[float]:
        """Get average quality score for session.
        
        Returns:
            Average of all recorded scores, or None if no history
        """
        if not self.history:
            return None
        
        return sum(self.history) / len(self.history)
    
    def reset(self):
        """Reset historical data for new session.
        
        Clears the history list to start fresh tracking for a new session.
        """
        self.history = []
        logger.info(f"Reset history for {self.exercise_type}")
    
    def generate_feedback_message(
        self,
        quality_score: float,
        category: str,
        form_metrics: Dict[str, float],
        analysis_result: Dict
    ) -> str:
        """Generate trainer-like feedback message.
        
        Generates contextual feedback based on quality category, with specific
        correction hints for poor form, improvement suggestions for average form,
        and encouragement for excellent form. Includes historical comparison when
        sufficient data is available (3+ reps).
        
        Args:
            quality_score: Current pose quality score (0-100)
            category: Feedback category ('poor', 'average', or 'excellent')
            form_metrics: Dict of metric_name -> score (0-100)
            analysis_result: Full analysis result (for future use)
            
        Returns:
            Trainer-like feedback message string
        """
        # Get base message template for category
        templates = self.config.feedback_templates.get(category, ["Keep going!"])
        base_message = random.choice(templates)
        
        # For poor category, add metric-specific correction hints
        if category == 'poor' and form_metrics:
            correction_hint = self._get_correction_hint(form_metrics)
            if correction_hint:
                base_message = correction_hint
        
        # Add historical comparison if we have enough data (3+ reps)
        historical_avg = self.get_historical_average()
        if historical_avg is not None and len(self.history) >= 3:
            # Check for significant regression or progress
            difference = quality_score - historical_avg
            
            if difference < -10:  # Significant regression
                base_message += " You're slipping a bit - refocus on form!"
            elif difference > 10:  # Significant progress
                base_message += " You're improving - great progress!"
        
        return base_message
    
    def _get_correction_hint(self, form_metrics: Dict[str, float]) -> Optional[str]:
        """Get specific correction hint based on worst-performing metric.
        
        Prioritizes critical (safety-related) metrics over non-critical ones.
        
        Args:
            form_metrics: Dict of metric_name -> score (0-100)
            
        Returns:
            Correction hint string, or None if no specific hint available
        """
        if not form_metrics:
            return None
        
        # Separate metrics into critical and non-critical
        critical_metrics = []
        non_critical_metrics = []
        
        for weight_config in self.config.metric_weights:
            metric_score = form_metrics.get(weight_config.name)
            if metric_score is not None:
                if weight_config.is_critical:
                    critical_metrics.append((weight_config.name, metric_score))
                else:
                    non_critical_metrics.append((weight_config.name, metric_score))
        
        # Prioritize critical issues
        if critical_metrics:
            # Find worst critical metric
            worst_metric_name, worst_score = min(critical_metrics, key=lambda x: x[1])
        elif non_critical_metrics:
            # Find worst non-critical metric
            worst_metric_name, worst_score = min(non_critical_metrics, key=lambda x: x[1])
        else:
            return None
        
        # Generate exercise-specific correction hints
        return self._get_metric_specific_hint(worst_metric_name, worst_score)
    
    def _get_metric_specific_hint(self, metric_name: str, score: float) -> Optional[str]:
        """Get exercise-specific correction hint for a metric.
        
        Args:
            metric_name: Name of the metric that needs correction
            score: Current score for the metric
            
        Returns:
            Exercise-specific correction hint, or None if not available
        """
        # Bicep curl hints
        if self.exercise_type == "bicep_curl":
            if metric_name == "elbow_angle_score":
                return "Extend your arms fully at the bottom - get that full range!"
            elif metric_name == "elbow_stability_score":
                return "Lock those elbows in! Keep them tight to your sides."
        
        # Squat hints
        elif self.exercise_type == "squat":
            if metric_name == "depth_score":
                return "Go deeper! Aim to get your thighs parallel to the ground."
            elif metric_name == "knee_alignment_score":
                return "Keep your knees aligned with your feet - don't let them cave in!"
            elif metric_name == "back_position_score":
                return "Straighten that back! Engage your core for stability."
        
        # Push-up hints
        elif self.exercise_type == "push_up":
            if metric_name == "body_alignment_score":
                return "Keep your body straight! Don't let those hips sag."
            elif metric_name == "elbow_angle_score":
                return "Lower yourself more - aim for a 90-degree elbow bend."
        
        # Fallback to generic message from templates
        return None
    
    def calculate_angle(self, a: Tuple[float, ...], b: Tuple[float, ...], c: Tuple[float, ...]) -> float:
        """Calculate the angle between three points.
        
        Args:
            a: First point (x, y, z, visibility)
            b: Middle point (vertex of angle)
            c: Third point
            
        Returns:
            Angle in degrees
        """
        try:
            # Use only x,y for 2D angle calculation
            a_arr = np.array(a[:2])
            b_arr = np.array(b[:2])
            c_arr = np.array(c[:2])
            
            ba = a_arr - b_arr
            bc = c_arr - b_arr
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1, 1)
            
            return np.degrees(np.arccos(cosine_angle))
        except:
            return 0.0
    
    def calculate_distance(self, point1: Tuple[float, ...], point2: Tuple[float, ...]) -> float:
        """Calculate Euclidean distance between two points.
        
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
    
    def calculate_form_metrics(
        self,
        analysis_result: Dict,
        key_points: Dict[str, Tuple[float, ...]]
    ) -> Dict[str, float]:
        """Calculate exercise-specific form metrics.
        
        Handles edge cases:
        - Empty key_points: returns empty metrics dict
        - Missing key points: individual metric calculations handle gracefully
        - Unknown exercise type: returns empty metrics dict
        
        Args:
            analysis_result: Full analysis result from EnhancedExerciseAnalyzer
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary of metric_name -> score (0-100)
        """
        # Handle no pose detected (empty key_points)
        if not key_points:
            logger.warning(f"No key points provided for {self.exercise_type}, returning empty metrics")
            return {}
        
        if self.exercise_type == "bicep_curl":
            return self._calculate_bicep_curl_metrics(key_points)
        elif self.exercise_type == "squat":
            return self._calculate_squat_metrics(key_points)
        elif self.exercise_type == "push_up":
            return self._calculate_pushup_metrics(key_points)
        else:
            # Unknown exercise type, return empty metrics
            logger.warning(f"Unknown exercise type '{self.exercise_type}', returning empty metrics")
            return {}
    
    def _calculate_bicep_curl_metrics(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict[str, float]:
        """Calculate form metrics for bicep curls.
        
        Metrics:
        - elbow_angle_score: Penalize if angle doesn't reach full range (< 80° or > 170°)
        - elbow_stability_score: Penalize if elbows drift from body (distance > 0.12)
        
        Handles missing key points by using default coordinates (0, 0, 0, 0).
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary of metric scores (0-100)
        """
        metrics = {}
        
        # Get key points with defaults for missing landmarks
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        elbow = key_points.get('right_elbow', (0, 0, 0, 0))
        wrist = key_points.get('right_wrist', (0, 0, 0, 0))
        
        # Check if we have valid key points (not all zeros)
        if shoulder == (0, 0, 0, 0) or elbow == (0, 0, 0, 0) or wrist == (0, 0, 0, 0):
            logger.warning("Missing key points for bicep curl metrics, using neutral scores")
            return {
                "elbow_angle_score": 50.0,
                "elbow_stability_score": 50.0
            }
        
        # Calculate elbow angle
        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Elbow angle score: penalize if not reaching full range
        # Ideal range: 80° (flexed) to 170° (extended)
        if elbow_angle < 80:
            # Too flexed
            angle_score = max(0, 100 - (80 - elbow_angle) * 2)
        elif elbow_angle > 170:
            # Good extension
            angle_score = 100.0
        elif elbow_angle > 160:
            # Decent extension
            angle_score = 80 + (elbow_angle - 160) * 2
        else:
            # Mid-range, score based on proximity to ideal range
            angle_score = 60.0
        
        metrics['elbow_angle_score'] = angle_score
        
        # Elbow stability score: penalize if elbows drift from body
        elbow_shoulder_distance = abs(elbow[0] - shoulder[0])
        
        if elbow_shoulder_distance <= 0.08:
            # Excellent stability
            stability_score = 100.0
        elif elbow_shoulder_distance <= 0.12:
            # Acceptable stability
            stability_score = 100 - ((elbow_shoulder_distance - 0.08) / 0.04) * 30
        else:
            # Poor stability
            stability_score = max(0, 70 - (elbow_shoulder_distance - 0.12) * 200)
        
        metrics['elbow_stability_score'] = stability_score
        
        return metrics
    
    def _calculate_squat_metrics(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict[str, float]:
        """Calculate form metrics for squats.
        
        Metrics:
        - depth_score: Reward deeper squats (knee angle < 90° = 100, > 110° = 0)
        - knee_alignment_score: Penalize if knees extend past ankles
        - back_position_score: Penalize if back angle indicates rounding
        
        Handles missing key points by using default coordinates (0, 0, 0, 0).
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary of metric scores (0-100)
        """
        metrics = {}
        
        # Get key points with defaults for missing landmarks
        hip = key_points.get('right_hip', (0, 0, 0, 0))
        knee = key_points.get('right_knee', (0, 0, 0, 0))
        ankle = key_points.get('right_ankle', (0, 0, 0, 0))
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        
        # Check if we have valid key points (not all zeros)
        if (hip == (0, 0, 0, 0) or knee == (0, 0, 0, 0) or 
            ankle == (0, 0, 0, 0) or shoulder == (0, 0, 0, 0)):
            logger.warning("Missing key points for squat metrics, using neutral scores")
            return {
                "depth_score": 50.0,
                "knee_alignment_score": 50.0,
                "back_position_score": 50.0
            }
        
        # Calculate angles
        knee_angle = self.calculate_angle(hip, knee, ankle)
        hip_angle = self.calculate_angle(shoulder, hip, knee)
        
        # Depth score: reward deeper squats
        if knee_angle <= 90:
            # Excellent depth
            depth_score = 100.0
        elif knee_angle <= 110:
            # Good depth, linear decrease
            depth_score = 100 - ((knee_angle - 90) / 20) * 40
        elif knee_angle <= 140:
            # Acceptable depth
            depth_score = 60 - ((knee_angle - 110) / 30) * 40
        else:
            # Poor depth
            depth_score = max(0, 20 - (knee_angle - 140))
        
        metrics['depth_score'] = depth_score
        
        # Knee alignment score: penalize if knees extend past ankles
        knee_ankle_horizontal_distance = abs(knee[0] - ankle[0])
        
        if knee_ankle_horizontal_distance <= 0.05:
            # Excellent alignment
            alignment_score = 100.0
        elif knee_ankle_horizontal_distance <= 0.10:
            # Good alignment
            alignment_score = 100 - ((knee_ankle_horizontal_distance - 0.05) / 0.05) * 20
        else:
            # Poor alignment
            alignment_score = max(0, 80 - (knee_ankle_horizontal_distance - 0.10) * 300)
        
        metrics['knee_alignment_score'] = alignment_score
        
        # Back position score: penalize if back angle indicates rounding
        # Hip angle should be > 150° for straight back
        if hip_angle >= 150:
            # Excellent back position
            back_score = 100.0
        elif hip_angle >= 130:
            # Acceptable back position
            back_score = 100 - ((150 - hip_angle) / 20) * 30
        else:
            # Poor back position (rounding)
            back_score = max(0, 70 - (130 - hip_angle) * 2)
        
        metrics['back_position_score'] = back_score
        
        return metrics
    
    def _calculate_pushup_metrics(self, key_points: Dict[str, Tuple[float, ...]]) -> Dict[str, float]:
        """Calculate form metrics for push-ups.
        
        Metrics:
        - body_alignment_score: Penalize if body isn't straight (hip sag or pike)
        - elbow_angle_score: Reward full range of motion
        
        Handles missing key points by using default coordinates (0, 0, 0, 0).
        
        Args:
            key_points: Dictionary of body landmarks
            
        Returns:
            Dictionary of metric scores (0-100)
        """
        metrics = {}
        
        # Get key points with defaults for missing landmarks
        shoulder = key_points.get('right_shoulder', (0, 0, 0, 0))
        elbow = key_points.get('right_elbow', (0, 0, 0, 0))
        wrist = key_points.get('right_wrist', (0, 0, 0, 0))
        hip = key_points.get('right_hip', (0, 0, 0, 0))
        ankle = key_points.get('right_ankle', (0, 0, 0, 0))
        
        # Check if we have valid key points (not all zeros)
        if (shoulder == (0, 0, 0, 0) or elbow == (0, 0, 0, 0) or 
            wrist == (0, 0, 0, 0) or hip == (0, 0, 0, 0) or ankle == (0, 0, 0, 0)):
            logger.warning("Missing key points for push-up metrics, using neutral scores")
            return {
                "body_alignment_score": 50.0,
                "elbow_angle_score": 50.0
            }
        
        # Body alignment score: check if body is straight
        body_angle = self.calculate_angle(shoulder, hip, ankle)
        
        if body_angle >= 160 and body_angle <= 180:
            # Excellent alignment (straight body)
            alignment_score = 100.0
        elif body_angle >= 150:
            # Good alignment
            alignment_score = 100 - ((160 - body_angle) / 10) * 20
        elif body_angle >= 140:
            # Acceptable alignment
            alignment_score = 80 - ((150 - body_angle) / 10) * 30
        else:
            # Poor alignment (sagging or piking)
            alignment_score = max(0, 50 - (140 - body_angle))
        
        metrics['body_alignment_score'] = alignment_score
        
        # Elbow angle score: reward full range of motion
        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # In push-up down position, elbow should be around 90°
        # In up position, elbow should be around 170°+
        if elbow_angle <= 100 and elbow_angle >= 80:
            # Good depth (down position)
            angle_score = 100.0
        elif elbow_angle >= 170:
            # Good extension (up position)
            angle_score = 100.0
        elif elbow_angle >= 160:
            # Decent extension
            angle_score = 80 + (elbow_angle - 160) * 2
        elif elbow_angle <= 110:
            # Acceptable depth
            angle_score = 80.0
        else:
            # Mid-range (transitioning)
            angle_score = 60.0
        
        metrics['elbow_angle_score'] = angle_score
        
        return metrics

