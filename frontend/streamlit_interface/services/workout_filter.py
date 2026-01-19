"""
Workout History Filter Service
Handles filtering and sorting of workout session data
"""
from typing import List, Dict


class WorkoutHistoryFilter:
    """Filters and sorts workout session data"""
    
    @staticmethod
    def filter_by_exercise(sessions: List[Dict], exercise_type: str) -> List[Dict]:
        """
        Filter sessions by exercise type
        
        Args:
            sessions: List of workout session dictionaries
            exercise_type: Exercise type to filter by (e.g., "bicep_curl", "squat")
                          Use "all" or empty string to return all sessions
            
        Returns:
            List of sessions matching the exercise type
        """
        # If exercise_type is "all" or empty, return all sessions
        if not exercise_type or exercise_type.lower() == "all":
            return sessions
        
        # Filter sessions by exercise type
        filtered_sessions = []
        for session in sessions:
            # Check both 'exercise' and 'exercise_type' fields for compatibility
            session_exercise = session.get('exercise', session.get('exercise_type', ''))
            
            if session_exercise.lower() == exercise_type.lower():
                filtered_sessions.append(session)
        
        return filtered_sessions
    
    @staticmethod
    def sort_by_date(sessions: List[Dict], reverse: bool = True) -> List[Dict]:
        """
        Sort sessions chronologically by start time
        
        Args:
            sessions: List of workout session dictionaries
            reverse: If True, sort in reverse chronological order (newest first)
                    If False, sort in chronological order (oldest first)
            
        Returns:
            Sorted list of sessions
        """
        # Create a copy to avoid modifying the original list
        sorted_sessions = sessions.copy()
        
        # Sort by start_time (ISO format strings sort correctly lexicographically)
        # If start_time is not available, try start_timestamp
        def get_sort_key(session: Dict) -> str:
            # Try to get start_time first (ISO format)
            start_time = session.get('start_time', '')
            
            # If start_time is not available, try start_timestamp
            if not start_time and 'start_timestamp' in session:
                # Convert timestamp to string for sorting
                start_time = str(session['start_timestamp'])
            
            return start_time
        
        sorted_sessions.sort(key=get_sort_key, reverse=reverse)
        
        return sorted_sessions
    
    @staticmethod
    def get_unique_exercise_types(sessions: List[Dict]) -> List[str]:
        """
        Extract unique exercise types from sessions
        
        Args:
            sessions: List of workout session dictionaries
            
        Returns:
            Sorted list of unique exercise types
        """
        exercise_types = set()
        
        for session in sessions:
            # Check both 'exercise' and 'exercise_type' fields for compatibility
            exercise = session.get('exercise', session.get('exercise_type', ''))
            
            if exercise:  # Only add non-empty exercise types
                exercise_types.add(exercise)
        
        # Return sorted list for consistent ordering
        return sorted(list(exercise_types))
