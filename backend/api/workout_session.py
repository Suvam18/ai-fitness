"""
Workout Session management for API use
Refactored from app.py - added session ID support and load_sessions method
"""
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


class WorkoutSession:
    """
    Manages workout session data with persistence.
    Refactored for API use with session ID support.
    """
    
    def __init__(self, data_dir: str = "backend/data/reports"):
        """
        Initialize the workout session manager.
        
        Args:
            data_dir: Directory to store session data files
        """
        self.data_dir = data_dir
        self.sessions = []
        self.current_session = None
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing sessions
        self.load_sessions()

    def start_session(self, exercise_type: str, session_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
        """
        Start a new workout session.
        
        Args:
            exercise_type: Type of exercise for this session
            session_id: Optional session ID (generates UUID if not provided)
            user_id: Optional user identifier
            
        Returns:
            Session ID (UUID string)
        """
        if session_id is None:
            session_id = str(uuid4())
            
        self.current_session = {
            'session_id': session_id,
            'id': len(self.sessions) + 1,  # Legacy numeric ID
            'exercise': exercise_type,
            'exercise_type': exercise_type,  # Alias for consistency
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'start_timestamp': time.time(),
            'end_time': None,
            'reps': 0,
            'duration': 0,
            'calories': 0,
            'status': 'active'
        }
        
        return session_id

    def update_session(self, rep_count: int, calories: float):
        """
        Update the current session with latest stats.
        
        Args:
            rep_count: Current repetition count
            calories: Current calories burned
        """
        if self.current_session:
            self.current_session['reps'] = rep_count
            self.current_session['calories'] = calories
            self.current_session['duration'] = time.time() - self.current_session['start_timestamp']

    def end_session(self, analysis_result: Optional[Dict] = None) -> Optional[Dict]:
        """
        End the current workout session and save it.
        
        Args:
            analysis_result: Final analysis result containing rep_count, calories, etc.
            
        Returns:
            The completed session data or None if no active session
        """
        if not self.current_session:
            return None

        self.current_session['end_time'] = datetime.now().isoformat()
        
        if analysis_result:
            self.current_session['reps'] = analysis_result.get('rep_count', 0)
            self.current_session['calories'] = analysis_result.get('calories', 0)
            
        self.current_session['duration'] = (
            time.time() - self.current_session['start_timestamp']
        )
        self.current_session['status'] = 'completed'

        # Add to sessions list
        self.sessions.append(self.current_session)
        
        # Save to file
        self.save_session(self.current_session)
        
        completed_session = self.current_session
        self.current_session = None
        
        return completed_session

    def get_session_by_id(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve a session by its ID.
        
        Args:
            session_id: UUID of the session to retrieve
            
        Returns:
            Session data dictionary or None if not found
        """
        # Check current session first
        if self.current_session and self.current_session.get('session_id') == session_id:
            return self.current_session
            
        # Search in completed sessions
        for session in self.sessions:
            if session.get('session_id') == session_id:
                return session
                
        return None

    def save_session(self, session: Dict):
        """
        Save a single session to a JSON file.
        
        Args:
            session: Session data dictionary
        """
        try:
            # Create filename with exercise type and timestamp
            exercise_type = session.get('exercise', 'unknown')
            timestamp = int(session.get('start_timestamp', time.time()))
            filename = f"workout_{exercise_type}_{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(session, f, indent=2)
        except Exception as e:
            # Silently fail - don't crash the application
            pass

    def save_sessions(self):
        """
        Save all sessions to individual JSON files.
        This method maintains compatibility with the original implementation.
        """
        for session in self.sessions:
            if session.get('status') == 'completed':
                self.save_session(session)

    def load_sessions(self) -> List[Dict]:
        """
        Load all workout sessions from the data directory.
        
        Returns:
            List of session dictionaries
        """
        self.sessions = []
        
        try:
            if not os.path.exists(self.data_dir):
                return self.sessions
                
            # Load all JSON files from the data directory
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.data_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            session = json.load(f)
                            self.sessions.append(session)
                    except Exception as e:
                        # Skip corrupted files
                        continue
                        
            # Sort sessions by start time
            self.sessions.sort(key=lambda x: x.get('start_time', ''), reverse=False)
            
        except Exception as e:
            # Return empty list on error
            pass
            
        return self.sessions

    def get_all_sessions(self, user_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        """
        Get all workout sessions with optional filtering and pagination.
        
        Args:
            user_id: Optional user ID to filter sessions
            limit: Maximum number of sessions to return
            offset: Number of sessions to skip
            
        Returns:
            List of session dictionaries
        """
        sessions = self.sessions
        
        # Filter by user_id if provided
        if user_id:
            sessions = [s for s in sessions if s.get('user_id') == user_id]
            
        # Apply pagination
        return sessions[offset:offset + limit]

    def reset_current_session(self):
        """
        Reset the current session's rep count and calories to zero.
        Does not reset the session ID or start time.
        """
        if self.current_session:
            self.current_session['reps'] = 0
            self.current_session['calories'] = 0
