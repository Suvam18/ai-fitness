"""
Pydantic data models for FastAPI Fitness Backend
Defines request/response schemas for all API endpoints
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List
from uuid import UUID
from enum import Enum
import base64


def validate_session_id(session_id: str) -> str:
    """Validate and return session ID if it's a valid UUID"""
    try:
        UUID(session_id)
        return session_id
    except ValueError:
        raise ValueError(f"Invalid session ID format: {session_id}. Must be a valid UUID")


def validate_base64_image(image_data: str) -> str:
    """Validate base64 encoded image data"""
    if not image_data or len(image_data.strip()) == 0:
        raise ValueError("Image data cannot be empty")
    
    # Remove data URI prefix if present
    if ',' in image_data:
        image_data = image_data.split(',', 1)[1]
    
    # Remove whitespace
    image_data = image_data.strip()
    
    # Check if it's valid base64
    try:
        # Remove padding characters and check length is multiple of 4
        image_data_no_padding = image_data.rstrip('=')
        if len(image_data_no_padding) % 4 != 0:
            raise ValueError("Invalid base64 string length")
        
        # Try to decode to validate
        base64.b64decode(image_data)
    except Exception:
        raise ValueError("Invalid base64 encoded image data")
    
    # Check minimum size (very small images are likely corrupted)
    if len(image_data) < 100:  # Base64 encoded 64x64 RGB image is about 12KB, so 100 chars is very small
        raise ValueError("Image data appears to be too small or corrupted")
    
    return image_data


# Enums for validation
class ExerciseType(str, Enum):
    """Supported exercise types"""
    BICEP_CURL = "bicep_curl"
    SQUAT = "squat"
    PUSH_UP = "push_up"
    SHOULDER_PRESS = "shoulder_press"
    LUNGE = "lunge"
    PLANK = "plank"


class SessionStatus(str, Enum):
    """Workout session status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"


class ExerciseStage(str, Enum):
    """Exercise movement stages"""
    START = "start"
    UP = "up"
    DOWN = "down"
    HOLD = "hold"


# Pose Detection Models
class PoseDetectionRequest(BaseModel):
    """Request model for pose detection endpoint"""
    image: str = Field(..., description="Base64 encoded image string")
    draw_landmarks: bool = Field(default=False, description="Whether to return annotated image with landmarks")

    @field_validator('image')
    @classmethod
    def validate_image(cls, v: str) -> str:
        """Validate that image string is valid base64"""
        validate_base64_image(v)
        return v


class PoseDetectionResponse(BaseModel):
    """Response model for pose detection endpoint"""
    detected: bool = Field(..., description="Whether a person was detected in the image")
    key_points: Optional[Dict[str, List[float]]] = Field(
        default=None,
        description="Dictionary of body landmarks with [x, y, z, visibility] coordinates"
    )
    annotated_image: Optional[str] = Field(
        default=None,
        description="Base64 encoded image with drawn landmarks (if requested)"
    )


# Exercise Analysis Models
class AnalysisRequest(BaseModel):
    """Request model for exercise analysis endpoint"""
    session_id: str = Field(..., description="UUID of the active workout session")
    exercise_type: ExerciseType = Field(..., description="Type of exercise being performed")
    key_points: Dict[str, List[float]] = Field(..., description="Body landmark coordinates from pose detection")
    image: Optional[str] = Field(default=None, description="Optional base64 encoded image for additional processing")

    @field_validator('image')
    @classmethod
    def validate_optional_image(cls, v: Optional[str]) -> Optional[str]:
        """Validate optional image if provided"""
        if v is not None:
            validate_base64_image(v)
        return v

    @field_validator('session_id')
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """Validate session ID format (UUID)"""
        try:
            UUID(v)
        except ValueError:
            raise ValueError("session_id must be a valid UUID")
        return v

    @field_validator('key_points')
    @classmethod
    def validate_key_points(cls, v: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """Validate key points structure and coordinate ranges"""
        if not v:
            raise ValueError("key_points cannot be empty")
        
        # Expected joints for pose detection (MediaPipe pose landmarks)
        expected_joints = {
            'nose', 'left_eye_inner', 'left_eye', 'left_eye_outer', 'right_eye_inner', 'right_eye', 
            'right_eye_outer', 'left_ear', 'right_ear', 'mouth_left', 'mouth_right', 'left_shoulder', 
            'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_pinky', 
            'right_pinky', 'left_index', 'right_index', 'left_thumb', 'right_thumb', 'left_hip', 
            'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle', 'left_heel', 
            'right_heel', 'left_foot_index', 'right_foot_index'
        }
        
        # Validate that each key point has 4 values [x, y, z, visibility]
        for joint, coords in v.items():
            if not isinstance(coords, list) or len(coords) != 4:
                raise ValueError(f"Each key point must have exactly 4 values [x, y, z, visibility], got {len(coords)} for {joint}")
            
            x, y, z, visibility = coords
            
            # Validate coordinate types
            if not all(isinstance(coord, (int, float)) for coord in coords):
                raise ValueError(f"All coordinates must be numbers for {joint}")
            
            # Validate ranges (assuming normalized coordinates 0-1)
            if not (0 <= x <= 1):
                raise ValueError(f"X coordinate for {joint} must be between 0 and 1, got {x}")
            if not (0 <= y <= 1):
                raise ValueError(f"Y coordinate for {joint} must be between 0 and 1, got {y}")
            if not (-1 <= z <= 1):  # Z can be negative for depth
                raise ValueError(f"Z coordinate for {joint} must be between -1 and 1, got {z}")
            if not (0 <= visibility <= 1):
                raise ValueError(f"Visibility for {joint} must be between 0 and 1, got {visibility}")
        
        # Check for minimum required joints
        present_joints = set(v.keys())
        if len(present_joints) < 10:  # At least some basic joints should be present
            raise ValueError(f"Too few joints detected. Expected at least 10, got {len(present_joints)}")
        
        return v


class AnalysisResponse(BaseModel):
    """Response model for exercise analysis endpoint"""
    session_id: str = Field(..., description="UUID of the workout session")
    rep_count: int = Field(..., description="Current repetition count")
    stage: ExerciseStage = Field(..., description="Current stage of the exercise movement")
    angles: Dict[str, float] = Field(..., description="Joint angles in degrees")
    feedback: List[str] = Field(default_factory=list, description="Positive feedback messages")
    warnings: List[str] = Field(default_factory=list, description="Form warning messages")
    errors: List[str] = Field(default_factory=list, description="Form error messages")
    calories: float = Field(..., description="Calories burned in this session")
    duration: Optional[float] = Field(default=None, description="Duration in seconds (for time-based exercises like plank)")
    
    # Real-time quality feedback fields
    quality_score: float = Field(
        ...,
        description="Pose quality score (0-100)",
        ge=0.0,
        le=100.0
    )
    quality_category: str = Field(
        ...,
        description="Feedback category: 'poor', 'average', or 'excellent'"
    )
    real_time_feedback: str = Field(
        ...,
        description="Trainer-like feedback message"
    )
    historical_average: Optional[float] = Field(
        default=None,
        description="Average quality score for this session"
    )


# Session Management Models
class SessionStartRequest(BaseModel):
    """Request model for starting a workout session"""
    exercise_type: ExerciseType = Field(..., description="Type of exercise for this session")
    user_id: Optional[str] = Field(default=None, description="Optional user identifier for tracking")

    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v: Optional[str]) -> Optional[str]:
        """Validate user_id if provided"""
        if v is not None and len(v.strip()) == 0:
            raise ValueError("user_id cannot be empty if provided")
        return v


class SessionResponse(BaseModel):
    """Response model for session information"""
    session_id: str = Field(..., description="Unique session identifier (UUID)")
    exercise_type: ExerciseType = Field(..., description="Type of exercise")
    start_time: str = Field(..., description="ISO8601 timestamp when session started")
    end_time: Optional[str] = Field(default=None, description="ISO8601 timestamp when session ended")
    duration: float = Field(..., description="Session duration in seconds")
    total_reps: int = Field(..., description="Total repetitions completed")
    calories_burned: float = Field(..., description="Total calories burned")
    status: SessionStatus = Field(..., description="Current session status")


class SessionResetResponse(BaseModel):
    """Response model for session reset operation"""
    session_id: str = Field(..., description="UUID of the reset session")
    message: str = Field(..., description="Success message")
    rep_count: int = Field(default=0, description="Rep count after reset (should be 0)")
    calories: float = Field(default=0.0, description="Calories after reset (should be 0)")


class SessionListResponse(BaseModel):
    """Response model for listing sessions"""
    sessions: List[SessionResponse] = Field(..., description="List of workout sessions")
    total: int = Field(..., description="Total number of sessions")
    limit: int = Field(..., description="Maximum sessions per page")
    offset: int = Field(..., description="Offset for pagination")


# Exercise Configuration Models
class ExerciseInfo(BaseModel):
    """Information about a supported exercise"""
    id: str = Field(..., description="Exercise identifier")
    name: str = Field(..., description="Display name of the exercise")
    muscle: str = Field(..., description="Primary muscle group targeted")
    type: str = Field(..., description="Exercise type (rep_based or time_based)")


class ExerciseListResponse(BaseModel):
    """Response model for listing available exercises"""
    exercises: List[ExerciseInfo] = Field(..., description="List of supported exercises")


# Error Response Models
class ErrorResponse(BaseModel):
    """Standard error response format"""
    error: str = Field(..., description="Error category or type")
    detail: str = Field(..., description="Detailed error description")
    status_code: int = Field(..., description="HTTP status code")


# Health Check Models
class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")
    pose_detector_initialized: bool = Field(..., description="Whether pose detector is ready")
