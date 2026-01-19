"""
State management utility for the AI Fitness Trainer Streamlit application.

This module provides centralized state management functions to ensure
consistent session_state usage across all pages, proper state preservation
during page transitions, and appropriate state cleanup.
"""

import streamlit as st
from typing import Any, Optional, Dict
from datetime import datetime


class StateManager:
    """
    Centralized state management for the Streamlit application.
    
    Provides methods for initializing, accessing, updating, and cleaning up
    session state variables consistently across all pages.
    """
    
    # Define all state keys with their default values
    STATE_DEFAULTS = {
        # Navigation state
        "current_page": "home",
        
        # Workout session state
        "active_exercise": None,
        "session_id": None,
        "session_start": None,
        "rep_count": 0,
        "calories": 0.0,
        "current_feedback": [],
        "quality_score": 0.0,
        "camera_active": False,
        
        # History page state
        "selected_exercise_filter": "all",
        "loaded_sessions": None,
        
        # Stats page state
        "stats_time_range": "all",
        "stats_exercise_filter": "all",
    }
    
    @staticmethod
    def initialize_all() -> None:
        """
        Initialize all session state variables with default values.
        
        This should be called once at application startup to ensure all
        required state variables exist with appropriate defaults.
        """
        for key, default_value in StateManager.STATE_DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @staticmethod
    def initialize_navigation() -> None:
        """
        Initialize navigation-related state variables.
        
        Ensures current_page is set with a default value.
        """
        if "current_page" not in st.session_state:
            st.session_state.current_page = "home"
    
    @staticmethod
    def initialize_workout() -> None:
        """
        Initialize workout session-related state variables.
        
        Ensures all workout state variables exist with default values.
        """
        workout_keys = [
            "active_exercise",
            "session_id",
            "session_start",
            "rep_count",
            "calories",
            "current_feedback",
            "quality_score",
            "camera_active",
        ]
        
        for key in workout_keys:
            if key not in st.session_state:
                st.session_state[key] = StateManager.STATE_DEFAULTS[key]
    
    @staticmethod
    def initialize_history() -> None:
        """
        Initialize history page-related state variables.
        
        Ensures history state variables exist with default values.
        """
        history_keys = ["selected_exercise_filter", "loaded_sessions"]
        
        for key in history_keys:
            if key not in st.session_state:
                st.session_state[key] = StateManager.STATE_DEFAULTS[key]
    
    @staticmethod
    def initialize_stats() -> None:
        """
        Initialize stats page-related state variables.
        
        Ensures stats state variables exist with default values.
        """
        stats_keys = ["stats_time_range", "stats_exercise_filter", "loaded_sessions"]
        
        for key in stats_keys:
            if key not in st.session_state:
                st.session_state[key] = StateManager.STATE_DEFAULTS[key]
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """
        Get a value from session state with optional default.
        
        Args:
            key: State variable key
            default: Default value if key doesn't exist
            
        Returns:
            Value from session state or default
        """
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        Set a value in session state.
        
        Args:
            key: State variable key
            value: Value to set
        """
        st.session_state[key] = value
    
    @staticmethod
    def update(updates: Dict[str, Any]) -> None:
        """
        Update multiple state variables at once.
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        for key, value in updates.items():
            st.session_state[key] = value
    
    @staticmethod
    def clear_workout_session() -> None:
        """
        Clear all workout session-related state variables.
        
        This should be called when ending a workout session to ensure
        clean state for the next session.
        """
        workout_keys = [
            "active_exercise",
            "session_id",
            "session_start",
            "rep_count",
            "calories",
            "current_feedback",
            "quality_score",
            "camera_active",
        ]
        
        for key in workout_keys:
            st.session_state[key] = StateManager.STATE_DEFAULTS[key]
    
    @staticmethod
    def clear_history_cache() -> None:
        """
        Clear cached history data.
        
        This should be called when history data needs to be refreshed
        (e.g., after completing a new workout).
        """
        st.session_state["loaded_sessions"] = None
    
    @staticmethod
    def clear_stats_cache() -> None:
        """
        Clear cached stats data.
        
        This should be called when stats data needs to be refreshed
        (e.g., after completing a new workout).
        """
        st.session_state["loaded_sessions"] = None
    
    @staticmethod
    def clear_all_caches() -> None:
        """
        Clear all cached data (history and stats).
        
        This should be called after completing a workout to ensure
        fresh data is loaded on the next page visit.
        """
        st.session_state["loaded_sessions"] = None
    
    @staticmethod
    def is_workout_active() -> bool:
        """
        Check if there is an active workout session.
        
        Returns:
            True if a workout session is active, False otherwise
        """
        return (
            st.session_state.get("session_id") is not None
            and st.session_state.get("active_exercise") is not None
        )
    
    @staticmethod
    def get_current_page() -> str:
        """
        Get the current page identifier.
        
        Returns:
            Current page key (e.g., 'home', 'workout', 'history', 'stats')
        """
        StateManager.initialize_navigation()
        return st.session_state["current_page"]
    
    @staticmethod
    def set_current_page(page_key: str) -> None:
        """
        Set the current page identifier.
        
        Args:
            page_key: Page identifier to set as active
        """
        StateManager.initialize_navigation()
        st.session_state["current_page"] = page_key
    
    @staticmethod
    def start_workout_session(
        exercise_type: str, session_id: str, session_start: Optional[datetime] = None
    ) -> None:
        """
        Initialize state for a new workout session.
        
        Args:
            exercise_type: Type of exercise being performed
            session_id: Unique session identifier from API
            session_start: Session start timestamp (defaults to now)
        """
        StateManager.update({
            "active_exercise": exercise_type,
            "session_id": session_id,
            "session_start": session_start or datetime.now(),
            "rep_count": 0,
            "calories": 0.0,
            "current_feedback": [],
            "quality_score": 0.0,
            "camera_active": False,
        })
    
    @staticmethod
    def end_workout_session() -> None:
        """
        Clean up state after ending a workout session.
        
        Clears all workout-related state and invalidates cached data
        so that history and stats pages will reload fresh data.
        """
        StateManager.clear_workout_session()
        StateManager.clear_all_caches()
    
    @staticmethod
    def update_workout_metrics(
        rep_count: Optional[int] = None,
        calories: Optional[float] = None,
        quality_score: Optional[float] = None,
        feedback: Optional[list] = None,
    ) -> None:
        """
        Update workout session metrics.
        
        Args:
            rep_count: Current rep count
            calories: Calories burned
            quality_score: Current quality score
            feedback: List of feedback messages
        """
        updates = {}
        
        if rep_count is not None:
            updates["rep_count"] = rep_count
        if calories is not None:
            updates["calories"] = calories
        if quality_score is not None:
            updates["quality_score"] = quality_score
        if feedback is not None:
            updates["current_feedback"] = feedback
        
        StateManager.update(updates)
    
    @staticmethod
    def preserve_state_on_navigation() -> None:
        """
        Ensure state is preserved during page transitions.
        
        This is a no-op in Streamlit since session_state automatically
        persists across page transitions, but it's provided for
        explicit documentation and potential future enhancements.
        """
        # Streamlit's session_state automatically persists across pages
        # This method is provided for explicit state preservation logic
        # if needed in the future
        pass
    
    @staticmethod
    def get_state_snapshot() -> Dict[str, Any]:
        """
        Get a snapshot of all current state variables.
        
        Useful for debugging and testing.
        
        Returns:
            Dictionary containing all state variables and their values
        """
        snapshot = {}
        for key in StateManager.STATE_DEFAULTS.keys():
            snapshot[key] = st.session_state.get(key)
        return snapshot
    
    @staticmethod
    def reset_to_defaults() -> None:
        """
        Reset all state variables to their default values.
        
        This should be used with caution as it clears all application state.
        Primarily useful for testing or explicit user-initiated reset.
        """
        for key, default_value in StateManager.STATE_DEFAULTS.items():
            st.session_state[key] = default_value
