# Backend Structure

This directory contains the AI Fitness Trainer backend components.

## Directory Structure

```
backend/
├── api/                    # FastAPI REST API components
│   ├── __init__.py
│   ├── main.py            # FastAPI application and endpoints
│   ├── models.py          # Pydantic data models for API
│   ├── pose_detector.py   # Pose detection service (API version)
│   ├── exercise_analyzer.py  # Exercise analysis service (API version)
│   ├── workout_session.py    # Workout session management (API version)
│   └── session_manager.py    # Session state manager
│
├── core/                  # Standalone desktop application
│   └── app.py            # Desktop app with CV2 GUI
│
├── utils/                 # Shared utilities
│   ├── __init__.py
│   └── image_processor.py # Image encoding/decoding utilities
│
├── tests/                 # Test suite
│   ├── test_*.py         # Unit tests
│   └── dependencies_test.py
│
└── data/                  # Data storage
    └── reports/          # Workout session reports (JSON)
```

## Components

### API Package (`backend/api/`)

The API package contains all components for the FastAPI REST service:

- **main.py**: FastAPI application with all HTTP endpoints
- **models.py**: Pydantic models for request/response validation
- **pose_detector.py**: MediaPipe-based pose detection (refactored for API use)
- **exercise_analyzer.py**: Exercise form analysis and rep counting (refactored for API use)
- **workout_session.py**: Session persistence and management (refactored for API use)
- **session_manager.py**: Thread-safe session state management

These components are refactored versions of the original classes, with:
- No console output (print statements removed)
- No CV2 display logic
- API-friendly interfaces
- Proper error handling

### Core Package (`backend/core/`)

Contains the standalone desktop application:

- **app.py**: Interactive desktop application with camera and CV2 GUI

This is the original application that provides a complete desktop experience with:
- Live camera feed
- Visual overlays and menus
- Keyboard controls
- Real-time feedback

### Utils Package (`backend/utils/`)

Shared utilities used by both API and core:

- **image_processor.py**: Image encoding/decoding (base64, multipart)

## Running the API

### Development Mode

```bash
# From project root
python3 -m backend.api.main

# Or using uvicorn directly
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn backend.api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running the Desktop App

```bash
# From project root
python3 backend/core/app.py
```

## Running Tests

```bash
# Run all tests
python3 -m pytest backend/tests/ -v

# Run specific test file
python3 -m pytest backend/tests/test_error_handlers.py -v

# Run with coverage
python3 -m pytest backend/tests/ --cov=backend --cov-report=html
```

## Import Paths

When importing from the backend:

```python
# API components
from backend.api.main import app
from backend.api.models import AnalysisRequest, AnalysisResponse
from backend.api.pose_detector import EnhancedPoseDetector
from backend.api.exercise_analyzer import EnhancedExerciseAnalyzer
from backend.api.session_manager import SessionManager

# Utilities
from backend.utils.image_processor import ImageProcessor

# Desktop app (if needed)
# Note: app.py is meant to be run standalone, not imported
```

## Architecture

The backend follows a clean separation of concerns:

1. **API Layer** (`main.py`): HTTP endpoints, request/response handling
2. **Service Layer** (`session_manager.py`): Business logic, session management
3. **Core Layer** (`pose_detector.py`, `exercise_analyzer.py`): Domain logic
4. **Data Layer** (`workout_session.py`): Persistence and storage
5. **Utilities** (`image_processor.py`): Shared helper functions

This structure allows:
- Easy testing of individual components
- Clear separation between API and desktop app
- Reusable core logic
- Scalable architecture
