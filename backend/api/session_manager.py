"""
SessionManager service class for managing workout sessions
Handles session creation, retrieval, ending, and resetting with thread-safe operations
"""
import threading
import uuid
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass, field

from backend.api.exercise_analyzer import EnhancedExerciseAnalyzer
from backend.api.workout_session import WorkoutSession


@dataclass
class SessionData:
    """Data structure for storing active session information"""
    session_id: str
    exercise_type: str
    analyzer: EnhancedExerciseAnalyzer
    workout_session: WorkoutSession
    user_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    status: str = "active"  # "active", "completed", "expired"


class SessionManager:
    """
    Manages active workout sessions and their associated analyzers.
    Provides thread-safe operations for creating, retrieving, ending, and resetting sessions.
    
    Requirements:
    - 3.1: Create sessions with unique identifiers
    - 6.1: Associate Exercise Analyzer instances with session IDs
    - 6.3: Reset session state to initial values
    - 6.4: Clean up ended sessions
    """
    
    def __init__(self):
        """Initialize SessionManager with empty session storage and thread lock"""
        self.active_sessions: Dict[str, SessionData] = {}
        self.session_lock = threading.Lock()
    
    def create_session(self, exercise_type: str, user_id: Optional[str] = None) -> str:
        """
        Create a new workout session with a unique identifier.
        
        Args:
            exercise_type: Type of exercise for this session (e.g., "bicep_curl", "squat")
            user_id: Optional user identifier for tracking
            
        Returns:
            str: Unique session ID (UUID)
            
        Requirements:
        - 3.1: WHEN a client initiates a workout session with an exercise type 
               THEN the FastAPI Service SHALL create a new Workout Session with 
               a unique identifier and timestamp
        - 6.1: WHEN a client starts a session THEN the FastAPI Service SHALL create 
               an Exercise Analyzer instance associated with that session identifier
        """
        with self.session_lock:
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Create analyzer and workout session instances
            analyzer = EnhancedExerciseAnalyzer(exercise_type)
            workout_session = WorkoutSession()
            workout_session.start_session(exercise_type)
            
            # Store session data
            session_data = SessionData(
                session_id=session_id,
                exercise_type=exercise_type,
                analyzer=analyzer,
                workout_session=workout_session,
                user_id=user_id,
                created_at=datetime.now(),
                last_activity=datetime.now(),
                status="active"
            )
            
            self.active_sessions[session_id] = session_data
            
            return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Retrieve an active session by its ID.
        
        Args:
            session_id: UUID of the session to retrieve
            
        Returns:
            SessionData if session exists and is active, None otherwise
            
        Requirements:
        - 6.2: WHEN a client submits frames for analysis with a session ID 
               THEN the FastAPI Service SHALL use the existing Exercise Analyzer 
               to maintain rep count and stage
        """
        with self.session_lock:
            session_data = self.active_sessions.get(session_id)
            
            if session_data:
                # Update last activity timestamp
                session_data.last_activity = datetime.now()
            
            return session_data
    
    def end_session(self, session_id: str) -> Optional[SessionData]:
        """
        End a workout session and clean up associated resources.
        
        Args:
            session_id: UUID of the session to end
            
        Returns:
            SessionData with final statistics if session exists, None otherwise
            
        Requirements:
        - 3.2: WHEN a client ends a workout session THEN the FastAPI Service SHALL 
               persist the session data including reps, duration, calories, and 
               timestamps to storage
        - 6.4: WHEN a session is ended THEN the FastAPI Service SHALL clean up 
               the associated Exercise Analyzer instance
        """
        with self.session_lock:
            session_data = self.active_sessions.get(session_id)
            
            if not session_data:
                return None
            
            # Get final analysis result
            final_analysis = session_data.analyzer.analyze_form({})
            
            # End the workout session (this persists data)
            session_data.workout_session.end_session(final_analysis)
            
            # Update session status
            session_data.status = "completed"
            
            # Remove from active sessions (cleanup)
            del self.active_sessions[session_id]
            
            return session_data
    
    def reset_session(self, session_id: str) -> bool:
        """
        Reset a session's state to initial values (zero reps, zero calories).
        
        Args:
            session_id: UUID of the session to reset
            
        Returns:
            bool: True if session was reset successfully, False if session not found
            
        Requirements:
        - 6.3: WHEN a client resets a session THEN the FastAPI Service SHALL 
               reset the Exercise Analyzer state to initial values
        """
        with self.session_lock:
            session_data = self.active_sessions.get(session_id)
            
            if not session_data:
                return False
            
            # Reset analyzer state to initial values
            session_data.analyzer.rep_count = 0
            session_data.analyzer.current_stage = "start"
            session_data.analyzer.calories_burned = 0
            session_data.analyzer.rep_history = []
            
            # Update last activity
            session_data.last_activity = datetime.now()
            
            return True
    
    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists in active sessions.
        
        Args:
            session_id: UUID of the session to check
            
        Returns:
            bool: True if session exists, False otherwise
        """
        with self.session_lock:
            return session_id in self.active_sessions
    
    def get_all_sessions(self) -> Dict[str, SessionData]:
        """
        Get all active sessions (for debugging/monitoring purposes).
        
        Returns:
            Dict mapping session IDs to SessionData objects
        """
        with self.session_lock:
            return self.active_sessions.copy()
