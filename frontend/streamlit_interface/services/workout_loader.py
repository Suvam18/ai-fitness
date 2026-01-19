"""
Workout History Loader Service
Handles loading workout session data from the backend data directory
"""
import json
import os
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkoutHistoryLoader:
    """Loads workout session data from the backend data directory"""
    
    def __init__(self, data_dir: str = "backend/data/reports"):
        """
        Initialize the WorkoutHistoryLoader
        
        Args:
            data_dir: Path to the directory containing workout session JSON files
        """
        self.data_dir = data_dir
        self.corrupted_files = []  # Track corrupted files
        self.load_errors = {}  # Track load errors
    
    def load_all_sessions(self) -> List[Dict]:
        """
        Load all workout session JSON files from the data directory
        
        Returns:
            List of workout session dictionaries
        """
        sessions = []
        self.corrupted_files = []  # Reset corrupted files list
        
        # Check if data directory exists
        if not os.path.exists(self.data_dir):
            logger.warning(f"Data directory does not exist: {self.data_dir}")
            self.load_errors['directory_exists'] = False
            return sessions
        
        # Check if it's a directory
        if not os.path.isdir(self.data_dir):
            logger.error(f"Path is not a directory: {self.data_dir}")
            self.load_errors['is_directory'] = False
            return sessions
        
        # Iterate through all files in the directory
        try:
            for filename in os.listdir(self.data_dir):
                # Only process JSON files
                if filename.endswith('.json'):
                    filepath = os.path.join(self.data_dir, filename)
                    session = self.parse_session_file(filepath)
                    
                    # Only add valid sessions
                    if session is not None:
                        sessions.append(session)
                    else:
                        self.corrupted_files.append(filename)
        except PermissionError:
            logger.error(f"Permission denied accessing directory: {self.data_dir}")
            self.load_errors['has_permission'] = False
        except Exception as e:
            logger.error(f"Error reading directory {self.data_dir}: {str(e)}")
            self.load_errors['general_error'] = str(e)
        
        logger.info(f"Loaded {len(sessions)} workout sessions from {self.data_dir}")
        if self.corrupted_files:
            logger.warning(f"Skipped {len(self.corrupted_files)} corrupted or invalid files: {', '.join(self.corrupted_files)}")
        
        return sessions
    
    def get_corrupted_file_count(self) -> int:
        """
        Get the number of corrupted files encountered during last load
        
        Returns:
            Number of corrupted files
        """
        return len(self.corrupted_files)
    
    def has_load_errors(self) -> bool:
        """
        Check if there were any load errors
        
        Returns:
            True if errors occurred, False otherwise
        """
        return len(self.load_errors) > 0
    
    def get_load_errors(self) -> Dict[str, any]:
        """
        Get information about any errors encountered during loading
        
        Returns:
            Dictionary with error information
        """
        errors = {
            'directory_exists': os.path.exists(self.data_dir),
            'is_directory': os.path.isdir(self.data_dir) if os.path.exists(self.data_dir) else False,
            'has_permission': True,  # Will be set to False if permission error occurs
        }
        
        try:
            if errors['is_directory']:
                # Try to list directory to check permissions
                os.listdir(self.data_dir)
        except PermissionError:
            errors['has_permission'] = False
        except Exception:
            pass
        
        return errors
    
    def parse_session_file(self, filepath: str) -> Optional[Dict]:
        """
        Parse a single JSON file and return session data
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Session dictionary if valid, None if invalid or corrupted
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Validate the session data
            if self.validate_session_data(session_data):
                return session_data
            else:
                logger.warning(f"Invalid session data in file: {filepath}")
                return None
                
        except json.JSONDecodeError as e:
            logger.warning(f"Corrupted JSON file {filepath}: {str(e)}")
            return None
        except FileNotFoundError:
            logger.warning(f"File not found: {filepath}")
            return None
        except PermissionError:
            logger.warning(f"Permission denied reading file: {filepath}")
            return None
        except Exception as e:
            logger.warning(f"Error parsing file {filepath}: {str(e)}")
            return None
    
    def validate_session_data(self, session: Dict) -> bool:
        """
        Validate that a session contains required fields
        
        Args:
            session: Session dictionary to validate
            
        Returns:
            True if session is valid, False otherwise
        """
        # Define required fields based on the data model
        required_fields = [
            'session_id',
            'exercise',
            'start_time',
            'reps',
            'duration',
            'calories',
            'status'
        ]
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in session:
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Additional validation: check data types
        try:
            # session_id should be a string
            if not isinstance(session['session_id'], str):
                logger.warning(f"Invalid session_id type: {type(session['session_id'])}")
                return False
            
            # exercise should be a string
            if not isinstance(session['exercise'], str):
                logger.warning(f"Invalid exercise type: {type(session['exercise'])}")
                return False
            
            # start_time should be a string
            if not isinstance(session['start_time'], str):
                logger.warning(f"Invalid start_time type: {type(session['start_time'])}")
                return False
            
            # reps should be a number (int or float)
            if not isinstance(session['reps'], (int, float)):
                logger.warning(f"Invalid reps type: {type(session['reps'])}")
                return False
            
            # duration should be a number
            if not isinstance(session['duration'], (int, float)):
                logger.warning(f"Invalid duration type: {type(session['duration'])}")
                return False
            
            # calories should be a number
            if not isinstance(session['calories'], (int, float)):
                logger.warning(f"Invalid calories type: {type(session['calories'])}")
                return False
            
            # status should be a string
            if not isinstance(session['status'], str):
                logger.warning(f"Invalid status type: {type(session['status'])}")
                return False
            
        except Exception as e:
            logger.warning(f"Error validating session data: {str(e)}")
            return False
        
        return True
