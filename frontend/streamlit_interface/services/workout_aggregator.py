"""
Workout History Aggregator Service
Calculates summary statistics from workout session data
"""
from typing import List, Dict


class WorkoutHistoryAggregator:
    """Calculates summary statistics from workout session data"""
    
    @staticmethod
    def calculate_total_workouts(sessions: List[Dict]) -> int:
        """
        Calculate the total number of workout sessions
        
        Args:
            sessions: List of workout session dictionaries
            
        Returns:
            Total number of workout sessions
        """
        return len(sessions)
    
    @staticmethod
    def calculate_total_reps(sessions: List[Dict]) -> int:
        """
        Calculate the total number of reps across all sessions
        
        Args:
            sessions: List of workout session dictionaries
            
        Returns:
            Total number of reps performed
        """
        total_reps = 0
        
        for session in sessions:
            # Get reps from session, default to 0 if not present
            reps = session.get('reps', 0)
            
            # Handle negative values by treating them as 0
            if isinstance(reps, (int, float)) and reps > 0:
                total_reps += int(reps)
        
        return total_reps
    
    @staticmethod
    def calculate_total_calories(sessions: List[Dict]) -> float:
        """
        Calculate the total calories burned across all sessions
        
        Args:
            sessions: List of workout session dictionaries
            
        Returns:
            Total calories burned
        """
        total_calories = 0.0
        
        for session in sessions:
            # Get calories from session, default to 0 if not present
            calories = session.get('calories', 0)
            
            # Handle negative values by treating them as 0
            if isinstance(calories, (int, float)) and calories > 0:
                total_calories += float(calories)
        
        return total_calories
    
    @staticmethod
    def calculate_total_duration(sessions: List[Dict]) -> float:
        """
        Calculate the total workout time across all sessions
        
        Args:
            sessions: List of workout session dictionaries
            
        Returns:
            Total duration in seconds
        """
        total_duration = 0.0
        
        for session in sessions:
            # Get duration from session, default to 0 if not present
            duration = session.get('duration', 0)
            
            # Handle negative values by treating them as 0
            if isinstance(duration, (int, float)) and duration > 0:
                total_duration += float(duration)
        
        return total_duration
