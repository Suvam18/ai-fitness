"""
Exercise configuration infrastructure for pose quality evaluation.

This module defines the configuration structure for exercise-specific
threshold-based feedback, including metric weights and feedback templates.
"""

from dataclasses import dataclass
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class ThresholdConfig:
    """Configuration for pose quality thresholds.
    
    Attributes:
        poor_threshold: Score below this indicates poor form (default: 60.0)
        good_threshold: Score at or above this indicates excellent form (default: 85.0)
    """
    poor_threshold: float = 60.0
    good_threshold: float = 85.0
    
    def validate(self) -> bool:
        """Validate that poor_threshold < good_threshold.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if self.poor_threshold >= self.good_threshold:
            logger.error(
                f"Invalid threshold configuration: poor_threshold ({self.poor_threshold}) "
                f"must be less than good_threshold ({self.good_threshold})"
            )
            return False
        return True


@dataclass
class MetricWeight:
    """Weight configuration for a form metric.
    
    Attributes:
        name: Name of the form metric
        weight: Weight value (0.0 to 1.0) for this metric
        is_critical: Whether this is a safety-critical metric (gets 1.5x multiplier)
    """
    name: str
    weight: float
    is_critical: bool


@dataclass
class ExerciseConfig:
    """Complete configuration for an exercise type.
    
    Attributes:
        exercise_type: Name of the exercise (e.g., 'bicep_curl', 'squat')
        thresholds: Threshold configuration for feedback categorization
        metric_weights: List of weighted metrics for quality score calculation
        feedback_templates: Dict mapping category to list of feedback messages
    """
    exercise_type: str
    thresholds: ThresholdConfig
    metric_weights: List[MetricWeight]
    feedback_templates: Dict[str, List[str]]
    
    def validate(self) -> bool:
        """Validate the exercise configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Validate thresholds
        if not self.thresholds.validate():
            return False
        
        # Validate that feedback templates exist for all categories
        required_categories = {'poor', 'average', 'excellent'}
        if not required_categories.issubset(self.feedback_templates.keys()):
            logger.error(
                f"Missing feedback templates for {self.exercise_type}. "
                f"Required: {required_categories}, Found: {set(self.feedback_templates.keys())}"
            )
            return False
        
        return True


# Feedback message templates for bicep curls
BICEP_CURL_FEEDBACK = {
    "poor": [
        "Lock those elbows in! Keep them tight to your sides.",
        "Slow down and control the movement. Quality over speed!",
        "Extend your arms fully at the bottom - get that full range!",
    ],
    "average": [
        "Good effort! Try keeping your elbows even closer to your body.",
        "Nice work! Focus on that full extension at the bottom.",
        "You're getting there! Maintain a steady, controlled tempo.",
    ],
    "excellent": [
        "Perfect form! Keep it up!",
        "Excellent control! That's how it's done!",
        "Outstanding technique! You're crushing it!",
    ]
}

# Feedback message templates for squats
SQUAT_FEEDBACK = {
    "poor": [
        "Go deeper! Aim to get your thighs parallel to the ground.",
        "Keep your knees aligned with your feet - don't let them cave in!",
        "Straighten that back! Engage your core for stability.",
    ],
    "average": [
        "Good depth! Try going just a bit lower for maximum benefit.",
        "Nice form! Keep focusing on that knee alignment.",
        "Solid work! Remember to push through your heels.",
    ],
    "excellent": [
        "Perfect squat! That's textbook form!",
        "Incredible depth and control! Keep it going!",
        "Flawless technique! You're a squat master!",
    ]
}

# Feedback message templates for push-ups
PUSHUP_FEEDBACK = {
    "poor": [
        "Keep your body straight! Don't let those hips sag.",
        "Lower yourself more - aim for a 90-degree elbow bend.",
        "Engage your core! Your body should be a straight line.",
    ],
    "average": [
        "Good form! Try to keep your body even straighter.",
        "Nice work! Focus on that full range of motion.",
        "You're doing well! Keep that core tight throughout.",
    ],
    "excellent": [
        "Perfect push-up! Textbook form!",
        "Excellent alignment and control! Keep it up!",
        "Outstanding! That's how push-ups are done!",
    ]
}

# Exercise-specific configurations
EXERCISE_CONFIGS = {
    "bicep_curl": ExerciseConfig(
        exercise_type="bicep_curl",
        thresholds=ThresholdConfig(poor_threshold=60.0, good_threshold=85.0),
        metric_weights=[
            MetricWeight(name="elbow_angle_score", weight=0.5, is_critical=True),
            MetricWeight(name="elbow_stability_score", weight=0.5, is_critical=True),
        ],
        feedback_templates=BICEP_CURL_FEEDBACK
    ),
    "squat": ExerciseConfig(
        exercise_type="squat",
        thresholds=ThresholdConfig(poor_threshold=60.0, good_threshold=85.0),
        metric_weights=[
            MetricWeight(name="depth_score", weight=0.33, is_critical=False),
            MetricWeight(name="knee_alignment_score", weight=0.33, is_critical=True),
            MetricWeight(name="back_position_score", weight=0.34, is_critical=True),
        ],
        feedback_templates=SQUAT_FEEDBACK
    ),
    "push_up": ExerciseConfig(
        exercise_type="push_up",
        thresholds=ThresholdConfig(poor_threshold=60.0, good_threshold=85.0),
        metric_weights=[
            MetricWeight(name="body_alignment_score", weight=0.5, is_critical=True),
            MetricWeight(name="elbow_angle_score", weight=0.5, is_critical=False),
        ],
        feedback_templates=PUSHUP_FEEDBACK
    ),
}

# Default configuration for unknown exercise types
DEFAULT_CONFIG = ExerciseConfig(
    exercise_type="default",
    thresholds=ThresholdConfig(poor_threshold=60.0, good_threshold=85.0),
    metric_weights=[],
    feedback_templates={
        "poor": ["Focus on your form!"],
        "average": ["Good work! Keep improving!"],
        "excellent": ["Perfect! Keep it up!"]
    }
)


def get_exercise_config(exercise_type: str) -> ExerciseConfig:
    """Get configuration for a specific exercise type.
    
    Handles edge cases:
    - Unknown exercise type: returns DEFAULT_CONFIG with warning log
    - Invalid configuration: returns DEFAULT_CONFIG with error log
    
    Args:
        exercise_type: Name of the exercise
        
    Returns:
        ExerciseConfig for the specified exercise, or DEFAULT_CONFIG if not found
    """
    config = EXERCISE_CONFIGS.get(exercise_type)
    
    if config is None:
        logger.warning(
            f"Unknown exercise type '{exercise_type}', using default configuration. "
            f"Available types: {list(EXERCISE_CONFIGS.keys())}"
        )
        return DEFAULT_CONFIG
    
    # Validate configuration
    if not config.validate():
        logger.error(
            f"Invalid configuration for '{exercise_type}': "
            f"poor_threshold={config.thresholds.poor_threshold}, "
            f"good_threshold={config.thresholds.good_threshold}. "
            f"Using default configuration instead."
        )
        return DEFAULT_CONFIG
    
    return config
