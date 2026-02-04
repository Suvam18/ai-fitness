# Streamlit Interface Setup

The Streamlit interface is a modern, modular web application that communicates with the FastAPI backend for pose detection and exercise analysis.

## Architecture

- **Frontend**: Multi-page Streamlit web application with modular components
- **Backend**: FastAPI REST API (handles pose detection and exercise analysis)
- **Communication**: HTTP requests with base64-encoded video frames

## New Modular Structure

The interface has been refactored into a clean, maintainable architecture:

```
frontend/streamlit_interface/
├── app.py                    # Main application entry point
├── pages/                    # Multi-page navigation
│   ├── 1_Home.py            # Welcome page
│   ├── 2_Workout.py         # Live workout session
│   ├── 3_History.py         # Workout history viewer
│   └── 4_Stats.py           # Analytics dashboard
├── components/              # Reusable UI components
│   ├── charts.py           # Chart components
│   └── navigation.py       # Navigation system
├── services/               # Business logic layer
│   ├── api_client.py       # Backend API communication
│   ├── workout_loader.py   # Load workout data
│   ├── workout_filter.py   # Filter and sort sessions
│   ├── workout_formatter.py # Format data for display
│   └── workout_aggregator.py # Calculate statistics
├── styles/                 # Styling and theming
│   ├── theme.py           # Design tokens
│   ├── custom_css.py      # Custom CSS injection
│   └── page_styles.py     # Page-specific styles
└── utils/                  # Utility functions
    ├── state_manager.py   # Session state management
    ├── error_handler.py   # Error handling
    ├── icons.py           # Icon utilities
    └── responsive.py      # Responsive design helpers
```

## Setup Instructions

### 1. Start the FastAPI Backend

First, start the backend server:

```bash
# From the project root directory
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Start the Streamlit Frontend

In a separate terminal, start the Streamlit interface:

```bash
# From the project root directory
streamlit run frontend/streamlit_interface/app.py
```

The Streamlit app will open in your browser at `http://localhost:8501`

## Features

### Multi-Page Application

- **Home Page**: Welcome screen with quick start options
- **Workout Page**: Live exercise session with real-time feedback
- **History Page**: View past workout sessions with filtering
- **Stats Page**: Analytics dashboard with progress tracking

### Backend Integration

- **Health Check**: Automatically checks if backend is available on startup
- **Session Management**: Creates and manages workout sessions via API
- **Pose Detection**: Sends video frames to backend for pose landmark detection
- **Exercise Analysis**: Receives real-time form feedback, rep counting, and calorie tracking

### Supported Exercises

- 💪 Bicep Curls
- 🦵 Squats
- 🏃 Push-ups

### Real-time Feedback

- 🟢 Excellent form feedback with quality scores
- 🟡 Average form with improvement suggestions
- 🔴 Poor form with corrective guidance
- 📊 Live rep counting and calorie tracking
- 📈 Historical quality score comparison

### Workout History

- **Session Filtering**: Filter by exercise type
- **Summary Statistics**: Total workouts, reps, calories, and duration
- **Session Details**: View individual workout metrics
- **Data Persistence**: All sessions saved to JSON files

## API Endpoints Used

- `GET /health` - Check backend availability
- `POST /api/v1/sessions/start` - Start workout session
- `POST /api/v1/sessions/{session_id}/end` - End workout session
- `POST /api/v1/pose/detect` - Detect pose landmarks in frame
- `POST /api/v1/analyze` - Analyze exercise form and count reps

## Configuration

The API base URL can be changed in `frontend/streamlit_interface/services/api_client.py`:

```python
API_BASE_URL = "http://localhost:8000"
```

### Customizing Styles

Modify design tokens in `frontend/streamlit_interface/styles/theme.py`:

```python
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    # ... more colors
}
```

### Adding New Pages

1. Create a new file in `pages/` (e.g., `5_NewPage.py`)
2. Import required components and services
3. Implement the page logic
4. Update navigation in `components/navigation.py`

## Troubleshooting

### Backend Not Available

If you see "Backend API is not available", ensure:
1. FastAPI server is running on port 8000
2. No firewall blocking localhost connections
3. All dependencies are installed (`pip install -r config/requirements.txt`)

### Camera Not Working

- Ensure your webcam is not being used by another application
- Check browser permissions for camera access
- Try restarting the Streamlit app

### Slow Performance

- The interface sends frames to the backend every ~50ms
- Adjust the `time.sleep(0.05)` value in `pages/2_Workout.py` to change frame rate
- Consider running backend and frontend on the same machine to reduce latency

### Workout History Not Loading

- Check that `backend/data/reports/` directory exists
- Verify JSON files are properly formatted
- Check file permissions for the reports directory

### State Management Issues

- Clear browser cache and cookies
- Restart the Streamlit server
- Check `utils/state_manager.py` for state initialization

## Development

### Running Tests

```bash
# Run all tests
pytest frontend/streamlit_interface/tests/

# Run specific test file
pytest frontend/streamlit_interface/tests/test_state_management.py
```

### Code Organization

- **Services**: Business logic and API communication
- **Components**: Reusable UI elements
- **Pages**: Individual page implementations
- **Utils**: Helper functions and utilities
- **Styles**: Theming and CSS

### Best Practices

1. Use `StateManager` for all session state operations
2. Handle errors with `ErrorHandler` utilities
3. Keep API calls in `services/api_client.py`
4. Use design tokens from `styles/theme.py`
5. Follow the existing component structure
