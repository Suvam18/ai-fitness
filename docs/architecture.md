# 🏋️ AI Fitness Trainer — Project Overview & Architecture

## 1. Project Overview
The **AI Fitness Trainer** is a computer-vision–based application that uses a webcam and pose estimation to analyze human exercises in real time. It provides live feedback, repetition counting, form correction, quality scoring, calorie estimation, and workout session persistence.

The project is designed to be:
- Beginner-friendly
- Modular and extensible
- Suitable for desktop, API-based, and modern web-based interfaces
- Production-ready with comprehensive testing

---

## 2. High-Level Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
├─────────────────────────────────────────────────────────────┤
│  Desktop App (OpenCV)  │  Web App (Streamlit Multi-page)    │
│  - Direct integration  │  - Modern UI with navigation       │
│  - Real-time display   │  - Workout history & analytics     │
│                        │  - Responsive design               │
└────────────┬───────────┴──────────────┬─────────────────────┘
             │                          │
             │                          │ HTTP/REST API
             v                          v
┌─────────────────────────────────────────────────────────────┐
│                        Backend Layer                         │
├─────────────────────────────────────────────────────────────┤
│                     FastAPI REST API                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Session Manager  │  Pose Detector  │  Analyzer      │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Quality Evaluator  │  Exercise Config  │  Models    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────┐
│                      Data Persistence                        │
├─────────────────────────────────────────────────────────────┤
│  JSON Reports  │  Session History  │  Workout Metrics       │
└─────────────────────────────────────────────────────────────┘
```

### Frontend Architecture (Streamlit)

```
streamlit_interface/
├── app.py (Entry Point)
│   └── Multi-page Router
│
├── Pages Layer
│   ├── Home (Welcome & Quick Start)
│   ├── Workout (Live Session)
│   ├── History (Past Sessions)
│   └── Stats (Analytics)
│
├── Components Layer (Reusable UI)
│   ├── Charts
│   └── Navigation
│
├── Services Layer (Business Logic)
│   ├── API Client (Backend Communication)
│   ├── Workout Loader (Data Loading)
│   ├── Workout Filter (Filtering & Sorting)
│   ├── Workout Formatter (Display Formatting)
│   └── Workout Aggregator (Statistics)
│
├── Styles Layer (Theming)
│   ├── Theme (Design Tokens)
│   ├── Custom CSS
│   └── Page Styles
│
└── Utils Layer (Helpers)
    ├── State Manager (Session State)
    ├── Error Handler (Error Management)
    ├── Icons (Icon Utilities)
    └── Responsive (Responsive Design)
```

---

## 3. Execution Flow

### 3.1 Web Application Startup (Streamlit)
1. User navigates to `http://localhost:8501`
2. `app.py` initializes the application
3. Page configuration and styling are applied
4. Session state is initialized via `StateManager`
5. Backend health check is performed
6. Welcome page is rendered with navigation

---

### 3.2 Workout Session Flow
1. User selects exercise type from Home or Workout page
2. Frontend sends `POST /api/v1/sessions/start` to backend
3. Backend creates session and returns `session_id`
4. Camera feed starts capturing frames
5. For each frame:
   - Frame encoded to base64
   - Sent to `POST /api/v1/pose/detect`
   - Backend returns landmarks and annotated image
   - Sent to `POST /api/v1/analyze` with session context
   - Backend returns:
     - Rep count and calories
     - Quality score (0-100)
     - Real-time feedback messages
     - Historical quality average
6. UI displays:
   - Annotated video feed
   - Live metrics (reps, calories, quality)
   - Color-coded feedback (🟢 🟡 🔴)
   - Progress tracking

---

### 3.3 Session End & Data Persistence
1. User stops camera or navigates away
2. Frontend sends `POST /api/v1/sessions/{session_id}/end`
3. Backend finalizes session:
   - Calculates final statistics
   - Saves to `backend/data/reports/{session_id}.json`
4. Session state is cleared
5. User can view history in History page

---

### 3.4 History & Analytics Flow
1. User navigates to History page
2. `WorkoutHistoryLoader` scans `backend/data/reports/`
3. JSON files are parsed and validated
4. `WorkoutHistoryFilter` applies user filters
5. `WorkoutHistoryAggregator` calculates statistics
6. `WorkoutHistoryFormatter` formats data for display
7. UI renders:
   - Summary statistics cards
   - Filterable session list
   - Individual session details

---

## 4. Core Components

### 4.1 Backend Components

#### Pose Detector (`backend/api/pose_detector.py`)
**Responsibility:**
- Detects human pose using MediaPipe
- Extracts 33 landmark coordinates and visibility
- Draws landmarks on frames
- Returns structured key points

**Key Methods:**
- `detect_pose()` - Process frame and extract landmarks
- `draw_landmarks()` - Annotate frame with pose overlay

---

#### Exercise Analyzer (`backend/api/exercise_analyzer.py`)
**Responsibility:**
- Interprets pose landmarks
- Calculates joint angles
- Tracks repetitions or hold duration
- Detects incorrect form
- Manages exercise state machines

**Supported Exercises:**
- Bicep curls
- Squats
- Push-ups

**Key Methods:**
- `analyze()` - Main analysis entry point
- `_analyze_bicep_curl()` - Bicep curl logic
- `_analyze_squat()` - Squat logic
- `_analyze_push_up()` - Push-up logic

---

#### Pose Quality Evaluator (`backend/api/pose_quality_evaluator.py`)
**Responsibility:**
- Evaluates exercise form quality (0-100 score)
- Provides real-time feedback messages
- Categorizes quality (excellent/average/poor)
- Tracks historical quality averages

**Key Methods:**
- `evaluate_quality()` - Calculate quality score
- `get_real_time_feedback()` - Generate feedback message
- `get_quality_category()` - Categorize score

---

#### Session Manager (`backend/api/session_manager.py`)
**Responsibility:**
- Manages workout session lifecycle
- Tracks session state and metrics
- Persists session data to JSON
- Handles concurrent sessions

**Key Class:**
- `SessionManager` - Singleton session manager
- `WorkoutSession` - Individual session data

---

### 4.2 Frontend Components

#### API Client (`services/api_client.py`)
**Responsibility:**
- Communicates with FastAPI backend
- Encodes/decodes video frames
- Handles HTTP requests and errors
- Provides caching for health checks

**Key Methods:**
- `start_session()` - Start workout session
- `end_session()` - End workout session
- `detect_pose()` - Send frame for pose detection
- `analyze_exercise()` - Send landmarks for analysis

---

#### State Manager (`utils/state_manager.py`)
**Responsibility:**
- Manages Streamlit session state
- Provides type-safe state access
- Handles workout session state
- Preserves state across page navigation

**Key Methods:**
- `initialize_all()` - Initialize default state
- `start_workout_session()` - Set workout state
- `end_workout_session()` - Clear workout state
- `get()` / `set()` - Type-safe state access

---

#### Workout History Services (`services/`)
**Components:**
- `WorkoutHistoryLoader` - Load and validate JSON files
- `WorkoutHistoryFilter` - Filter and sort sessions
- `WorkoutHistoryFormatter` - Format data for display
- `WorkoutHistoryAggregator` - Calculate statistics

**Data Flow:**
```
JSON Files → Loader → Filter → Aggregator → Formatter → UI
```

---

### 4.3 Data Persistence

**Session Data Format:**
```json
{
  "session_id": "abc123...",
  "exercise": "bicep_curl",
  "start_time": "2026-01-19T14:30:00",
  "end_time": "2026-01-19T14:35:00",
  "reps": 15,
  "duration": 300,
  "calories": 25.5,
  "status": "completed",
  "quality_scores": [85, 90, 88, 92],
  "average_quality": 88.75
}
```

**Storage Location:**
- `backend/data/reports/{session_id}.json`

---

## 5. Folder Structure

```
ai-fitness-trainer/
│
├── backend/                   # Backend Components
│   ├── api/                   # FastAPI REST API
│   │   ├── main.py           # API endpoints
│   │   ├── models.py         # Data models
│   │   ├── pose_detector.py  # Pose detection
│   │   ├── exercise_analyzer.py  # Exercise analysis
│   │   ├── pose_quality_evaluator.py  # Quality scoring
│   │   ├── workout_session.py    # Session data
│   │   └── session_manager.py    # Session management
│   │
│   ├── core/                  # Desktop App
│   │   └── app.py            # OpenCV GUI
│   │
│   ├── data/                  # Data storage
│   │   └── reports/          # JSON workout reports
│   │
│   └── tests/                 # Test suite
│
├── frontend/                  # User Interfaces
│   ├── streamlit_interface/   # Modern web app
│   │   ├── app.py            # Entry point
│   │   ├── pages/            # Multi-page navigation
│   │   ├── components/       # Reusable UI
│   │   ├── services/         # Business logic
│   │   ├── styles/           # Theming
│   │   └── utils/            # Helpers
│   │
│   └── web-interface/         # Landing pages
│
├── config/                    # Configuration
│   └── requirements.txt       # Dependencies
│
└── docs/                      # Documentation
    ├── CONTRIBUTING.md
    ├── CODE_OF_CONDUCT.md
    └── architecture.md
```

---

## 6. How to Extend the Project

### Add a New Exercise

**Backend:**
1. Add exercise configuration to `backend/api/exercise_config.py`
2. Implement analysis method in `backend/api/exercise_analyzer.py`:
```python
def _analyze_new_exercise(self, key_points: Dict) -> Dict:
    # Extract landmarks
    # Calculate angles
    # Detect movement stage
    # Count reps
    # Return analysis result
```
3. Add quality evaluation logic in `backend/api/pose_quality_evaluator.py`
4. Update `EXERCISE_TYPE_MAP` in `frontend/streamlit_interface/services/api_client.py`

**Frontend:**
1. Add exercise to workout selection in `pages/2_Workout.py`
2. Add form guide tips for the new exercise
3. Update exercise icon mapping in `services/workout_formatter.py`

---

### Add a New Page

1. Create `pages/X_NewPage.py` following the existing structure
2. Import required services and components
3. Implement page logic with proper state management
4. Update navigation in `components/navigation.py`
5. Add page-specific styles if needed

---

### Improve Analytics

- Add weekly/monthly aggregation in `services/workout_aggregator.py`
- Create chart components in `components/charts.py`
- Implement data export functionality
- Add progress tracking visualizations in `pages/4_Stats.py`

---

### Enhance Quality Evaluation

- Add more granular form checks in `pose_quality_evaluator.py`
- Implement exercise-specific quality metrics
- Add video recording for form review
- Create detailed feedback explanations

---

## 7. Intended Audience

- **Developers:** Building computer vision applications
- **Students:** Learning AI, pose estimation, and web development
- **Contributors:** Extending fitness tech with open source
- **Fitness Enthusiasts:** Using AI for form improvement
- **Researchers:** Studying human movement analysis

---

## 8. Development Best Practices

### Backend
- Keep API endpoints RESTful and stateless
- Use Pydantic models for data validation
- Implement comprehensive error handling
- Write unit tests for all analysis logic

### Frontend
- Use `StateManager` for all session state
- Handle errors with `ErrorHandler` utilities
- Keep business logic in services layer
- Use design tokens from `styles/theme.py`
- Ensure responsive design for all pages

### Testing
- Write tests for new features
- Test edge cases (no pose detected, poor lighting)
- Validate data persistence
- Test API error scenarios

---

## 9. Summary

This project demonstrates a production-ready architecture for AI-powered fitness applications, combining:
- **Computer Vision:** MediaPipe pose estimation
- **Real-time Analysis:** Exercise form evaluation and quality scoring
- **Modern Web UI:** Multi-page Streamlit application with clean architecture
- **Data Persistence:** Structured workout history and analytics
- **Modular Design:** Easy to extend, test, and maintain

The separation of concerns (backend API, frontend services, UI components) makes the system scalable and maintainable for both learning and production use.

