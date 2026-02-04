"""
Workout History Formatter Service
Formats workout data for display in the UI
"""
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkoutHistoryFormatter:
    """Formats workout data for display in the UI"""
    
    @staticmethod
    def format_date(timestamp: str) -> str:
        """
        Convert ISO timestamp to human-readable format
        
        Args:
            timestamp: ISO format timestamp string (e.g., "2024-01-15T14:30:00")
            
        Returns:
            Human-readable date string (e.g., "Jan 15, 2024 2:30 PM")
        """
        try:
            # Parse the ISO format timestamp
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            # Format as human-readable string
            # Example: "Jan 15, 2024 2:30 PM"
            return dt.strftime("%b %d, %Y %I:%M %p")
        except (ValueError, AttributeError) as e:
            logger.warning(f"Error formatting date {timestamp}: {str(e)}")
            # Return the original timestamp if parsing fails
            return timestamp
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Convert seconds to "Xm Ys" format
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string (e.g., "5m 30s")
        """
        try:
            # Handle negative values by treating them as 0
            if seconds < 0:
                seconds = 0
            
            # Convert to integer seconds
            total_seconds = int(seconds)
            
            # Calculate minutes and remaining seconds
            minutes = total_seconds // 60
            remaining_seconds = total_seconds % 60
            
            # Format the string
            if minutes > 0:
                return f"{minutes}m {remaining_seconds}s"
            else:
                return f"{remaining_seconds}s"
        except (ValueError, TypeError) as e:
            logger.warning(f"Error formatting duration {seconds}: {str(e)}")
            return "0s"
    
    @staticmethod
    def format_exercise_name(exercise_type: str) -> str:
        """
        Convert exercise type to display name
        
        Args:
            exercise_type: Exercise type identifier (e.g., "bicep_curl", "squat")
            
        Returns:
            Human-readable exercise name (e.g., "Bicep Curl", "Squat")
        """
        # Mapping of exercise types to display names
        exercise_name_map = {
            'bicep_curl': 'Bicep Curl',
            'squat': 'Squat',
            'push_up': 'Push Up',
            'pushup': 'Push Up',
            'pull_up': 'Pull Up',
            'pullup': 'Pull Up',
            'plank': 'Plank',
            'lunge': 'Lunge',
            'jumping_jack': 'Jumping Jack',
            'burpee': 'Burpee',
            'sit_up': 'Sit Up',
            'situp': 'Sit Up',
        }
        
        # Convert to lowercase for lookup
        exercise_lower = exercise_type.lower()
        
        # Return mapped name if available, otherwise format the raw type
        if exercise_lower in exercise_name_map:
            return exercise_name_map[exercise_lower]
        else:
            # Convert underscores to spaces and capitalize each word
            return exercise_type.replace('_', ' ').title()
    
    @staticmethod
    def get_exercise_icon(exercise_type: str) -> str:
        """
        Get emoji icon for exercise type
        
        Args:
            exercise_type: Exercise type identifier (e.g., "bicep_curl", "squat")
            
        Returns:
            Emoji icon string for the exercise type
        """
        # Mapping of exercise types to emoji icons
        exercise_icon_map = {
            'bicep_curl': '💪',
            'squat': '🦵',
            'push_up': '🤸',
            'pushup': '🤸',
            'pull_up': '🏋️',
            'pullup': '🏋️',
            'plank': '🧘',
            'lunge': '🏃',
            'jumping_jack': '🤾',
            'burpee': '🔥',
            'sit_up': '🧘',
            'situp': '🧘',
        }
        
        # Convert to lowercase for lookup
        exercise_lower = exercise_type.lower()
        
        # Return mapped icon if available, otherwise return a default icon
        return exercise_icon_map.get(exercise_lower, '🏋️')
