"""
Workout page for the AI Fitness Trainer Streamlit application.

This page allows users to select an exercise type and start a workout session.
It handles exercise selection, session initialization, and error handling for API failures.
"""

import streamlit as st
import sys
from pathlib import Path
import cv2
import numpy as np
from datetime import datetime, timedelta
import time

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from styles.custom_css import inject_custom_css, apply_page_config
from styles.theme import COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS
from utils.icons import (
    inject_material_icons_cdn,
    render_exercise_card_icon,
    get_icon_name,
)
from utils.state_manager import StateManager
from components.navigation import Navigation
from services.api_client import APIClient, get_api_client
from utils.error_handler import ErrorHandler


def check_backend_health() -> bool:
    """
    Check if the backend API is available.
    
    Returns:
        True if backend is healthy, False otherwise
    """
    return APIClient.check_health()


def render_backend_error():
    """Render error message when backend is unavailable."""
    st.markdown(
        f"""
        <div style="
            background-color: {COLORS['error']}15;
            border-left: 4px solid {COLORS['error']};
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['lg']};
            margin: {SPACING['xl']} 0;
            text-align: center;
        ">
            <div style="
                display: flex;
                justify-content: center;
                margin-bottom: {SPACING['md']};
            ">
                <span class="material-icons" style="
                    font-size: 48px;
                    color: {COLORS['error']};
                ">error_outline</span>
            </div>
            <h3 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['sm']};
            ">
                Backend Service Unavailable
            </h3>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_secondary']};
                line-height: {TYPOGRAPHY['line_height_relaxed']};
                margin-bottom: {SPACING['md']};
            ">
                The AI Fitness Trainer backend service is not running or cannot be reached.
                Please ensure the FastAPI backend is started before using the workout feature.
            </p>
            <p style="
                font-family: {TYPOGRAPHY['font_family_mono']};
                font-size: {TYPOGRAPHY['font_size_sm']};
                color: {COLORS['text_tertiary']};
                background-color: {COLORS['background_secondary']};
                padding: {SPACING['sm']};
                border-radius: {BORDER_RADIUS['sm']};
                display: inline-block;
            ">
                Expected backend at: http://localhost:8000
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Add retry button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Retry Connection", use_container_width=True):
            # Clear health check cache and rerun
            APIClient._health_check_cache = None
            APIClient._health_check_timestamp = None
            st.rerun()


def start_workout_session(exercise_type: str) -> bool:
    """
    Start a new workout session via API.
    
    Args:
        exercise_type: Type of exercise to start
        
    Returns:
        True if session started successfully, False otherwise
    """
    api_client = get_api_client()
    
    # Map internal exercise type to display name for API
    exercise_display_map = {
        "bicep_curl": "Bicep Curls",
        "squat": "Squats",
        "push_up": "Push-ups",
    }
    
    display_name = exercise_display_map.get(exercise_type, exercise_type)
    
    # Start session via API
    session_id = api_client.start_session(display_name)
    
    if session_id:
        # Use StateManager to initialize workout session state
        StateManager.start_workout_session(
            exercise_type=exercise_type,
            session_id=session_id,
            session_start=datetime.now()
        )
        return True
    else:
        return False


def render_session_start_error(exercise_name: str):
    """
    Render error message when session fails to start.
    
    Args:
        exercise_name: Name of the exercise that failed to start
    """
    ErrorHandler.render_session_error("start")


def render_page_header():
    """Render the workout page header."""
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: {SPACING['2xl']} {SPACING['lg']} {SPACING['xl']};
            margin-bottom: {SPACING['xl']};
        ">
            <h1 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_4xl']};
                font-weight: {TYPOGRAPHY['font_weight_bold']};
                color: var(--text-color);
                line-height: {TYPOGRAPHY['line_height_tight']};
                margin-bottom: {SPACING['sm']};
                letter-spacing: {TYPOGRAPHY['letter_spacing_tight']};
            ">
                Start Your Workout
            </h1>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_lg']};
                font-weight: {TYPOGRAPHY['font_weight_normal']};
                color: var(--text-secondary);
                line-height: {TYPOGRAPHY['line_height_relaxed']};
                max-width: 600px;
                margin: 0 auto;
            ">
                Select an exercise to begin your AI-powered workout session with real-time form analysis
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_exercise_selection():
    """Render exercise selection view with icon-based cards."""
    # Exercise definitions
    exercises = [
        {
            "type": "bicep_curl",
            "display_name": "Bicep Curls",
            "description": "Build arm strength with proper curl form and technique",
            "icon_color": COLORS['primary'],
            "benefits": ["Strengthens biceps", "Improves arm definition", "Enhances grip strength"],
        },
        {
            "type": "squat",
            "display_name": "Squats",
            "description": "Strengthen legs and core with perfect squat technique",
            "icon_color": COLORS['secondary'],
            "benefits": ["Builds leg muscles", "Strengthens core", "Improves mobility"],
        },
        {
            "type": "push_up",
            "display_name": "Push-ups",
            "description": "Develop upper body strength with controlled push-ups",
            "icon_color": COLORS['accent'],
            "benefits": ["Strengthens chest", "Builds shoulders", "Engages core"],
        },
    ]
    
    # Create columns for exercise cards
    col1, col2, col3 = st.columns(3)
    
    for col, exercise in zip([col1, col2, col3], exercises):
        with col:
            # Get icon for exercise
            icon_name = get_icon_name("exercise", exercise["type"])
            
            # Create card container
            st.markdown(
                f"""
                <div style="
                    background-color: {COLORS['card_background']};
                    border-radius: {BORDER_RADIUS['xl']};
                    padding: {SPACING['xl']};
                    box-shadow: {SHADOWS['md']};
                    border: 2px solid {COLORS['border']};
                    text-align: center;
                    transition: all 0.3s ease;
                    margin-bottom: {SPACING['md']};
                    height: 100%;
                " class="exercise-card">
                    <div style="
                        display: flex;
                        justify-content: center;
                        margin-bottom: {SPACING['lg']};
                    ">
                        <span class="material-icons" style="
                            font-size: 72px;
                            color: {exercise['icon_color']};
                        ">{icon_name}</span>
                    </div>
                    <h3 style="
                        font-family: {TYPOGRAPHY['font_family_primary']};
                        font-size: {TYPOGRAPHY['font_size_2xl']};
                        font-weight: {TYPOGRAPHY['font_weight_semibold']};
                        color: {COLORS['text_primary']};
                        margin-bottom: {SPACING['sm']};
                    ">
                        {exercise['display_name']}
                    </h3>
                    <p style="
                        font-family: {TYPOGRAPHY['font_family_primary']};
                        font-size: {TYPOGRAPHY['font_size_base']};
                        color: {COLORS['text_secondary']};
                        line-height: {TYPOGRAPHY['line_height_relaxed']};
                        margin-bottom: {SPACING['lg']};
                    ">
                        {exercise['description']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            # Button for starting workout
            if st.button(
                f"▶️ Start {exercise['display_name']}",
                key=f"start_{exercise['type']}",
                use_container_width=True,
            ):
                # Show loading spinner while starting session
                with st.spinner(f"Starting {exercise['display_name']} session..."):
                    success = start_workout_session(exercise["type"])
                    
                    if success:
                        st.success(
                            f"✅ {exercise['display_name']} session started successfully!",
                            icon="🎉"
                        )
                        time.sleep(1)
                        st.rerun()
                    else:
                        render_session_start_error(exercise['display_name'])


def inject_hover_styles():
    """Inject CSS for hover effects on exercise cards and dark mode support."""
    st.markdown(
        f"""
        <style>
        /* Dark mode CSS variables */
        :root {{
            --text-color: #111827;
            --text-secondary: #6b7280;
            --card-bg: #f9fafb;
            --border-color: #e5e7eb;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --text-color: #f9fafb;
                --text-secondary: #9ca3af;
                --card-bg: #1f2937;
                --border-color: #374151;
            }}
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] {{
            --text-color: #f9fafb;
            --text-secondary: #9ca3af;
            --card-bg: #1f2937;
            --border-color: #374151;
        }}
        
        /* Force all headings and text to use proper colors */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-color) !important;
        }}
        
        p {{
            color: var(--text-secondary) !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] h1,
        [data-testid="stAppViewContainer"][data-theme="dark"] h2,
        [data-testid="stAppViewContainer"][data-theme="dark"] h3 {{
            color: #f9fafb !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] p {{
            color: #9ca3af !important;
        }}
        
        /* Remove white space at top */
        [data-testid="stHeader"] {{
            background-color: transparent !important;
        }}
        
        [data-testid="stToolbar"] {{
            background-color: transparent !important;
        }}
        
        [data-testid="stToolbar"] > div:not(:first-child) {{
            display: none !important;
        }}
        
        .main .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }}
        
        section[data-testid="stSidebar"] > div:first-child {{
            padding-top: 1rem !important;
        }}
        
        /* Fix button text color to white - FORCE IT */
        .stButton > button {{
            color: #ffffff !important;
        }}
        
        .stButton > button:hover {{
            color: #ffffff !important;
        }}
        
        .stButton > button p {{
            color: #ffffff !important;
        }}
        
        .stButton > button span {{
            color: #ffffff !important;
        }}
        
        .stButton > button div {{
            color: #ffffff !important;
        }}
        
        /* Fix button text in dark mode */
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button {{
            color: #ffffff !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button:hover {{
            color: #ffffff !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button p {{
            color: #ffffff !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button span {{
            color: #ffffff !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button div {{
            color: #ffffff !important;
        }}
        
        /* Hover effects */
        .exercise-card:hover {{
            transform: translateY(-5px);
            box-shadow: {SHADOWS['lg']};
            border-color: {COLORS['primary']};
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .exercise-card {{
                margin-bottom: {SPACING['lg']};
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def end_workout_session() -> bool:
    """
    End the current workout session via API.
    
    Returns:
        True if session ended successfully, False otherwise
    """
    session_id = StateManager.get("session_id")
    if not session_id:
        return False
    
    api_client = get_api_client()
    result = api_client.end_session(session_id)
    
    if result:
        # Use StateManager to clean up workout session state
        StateManager.end_workout_session()
        return True
    else:
        return False


def render_session_metrics():
    """Render session metrics in metric cards."""
    # Calculate duration
    duration_seconds = 0
    session_start = StateManager.get("session_start")
    if session_start:
        duration = datetime.now() - session_start
        duration_seconds = int(duration.total_seconds())
    
    # Format duration as MM:SS
    minutes = duration_seconds // 60
    seconds = duration_seconds % 60
    duration_str = f"{minutes:02d}:{seconds:02d}"
    
    # Get metrics from state
    rep_count = StateManager.get("rep_count", 0)
    calories = StateManager.get("calories", 0.0)
    quality_score = StateManager.get("quality_score", 0.0)
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: {COLORS['card_background']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['lg']};
                box-shadow: {SHADOWS['sm']};
                border: 2px solid {COLORS['border']};
                text-align: center;
            ">
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-bottom: {SPACING['sm']};
                ">
                    <span class="material-icons" style="
                        font-size: 32px;
                        color: {COLORS['primary']};
                    ">fitness_center</span>
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_3xl']};
                    font-weight: {TYPOGRAPHY['font_weight_bold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']};
                ">
                    {rep_count}
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_sm']};
                    color: {COLORS['text_secondary']};
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    Reps
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="
                background-color: {COLORS['card_background']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['lg']};
                box-shadow: {SHADOWS['sm']};
                border: 2px solid {COLORS['border']};
                text-align: center;
            ">
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-bottom: {SPACING['sm']};
                ">
                    <span class="material-icons" style="
                        font-size: 32px;
                        color: {COLORS['secondary']};
                    ">timer</span>
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_3xl']};
                    font-weight: {TYPOGRAPHY['font_weight_bold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']};
                ">
                    {duration_str}
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_sm']};
                    color: {COLORS['text_secondary']};
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    Duration
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="
                background-color: {COLORS['card_background']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['lg']};
                box-shadow: {SHADOWS['sm']};
                border: 2px solid {COLORS['border']};
                text-align: center;
            ">
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-bottom: {SPACING['sm']};
                ">
                    <span class="material-icons" style="
                        font-size: 32px;
                        color: {COLORS['accent']};
                    ">local_fire_department</span>
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_3xl']};
                    font-weight: {TYPOGRAPHY['font_weight_bold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']};
                ">
                    {calories:.1f}
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_sm']};
                    color: {COLORS['text_secondary']};
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    Calories
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col4:
        # Determine quality color based on score
        if quality_score >= 80:
            quality_color = COLORS['success']
        elif quality_score >= 60:
            quality_color = COLORS['warning']
        else:
            quality_color = COLORS['error']
        
        st.markdown(
            f"""
            <div style="
                background-color: {COLORS['card_background']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['lg']};
                box-shadow: {SHADOWS['sm']};
                border: 2px solid {COLORS['border']};
                text-align: center;
            ">
                <div style="
                    display: flex;
                    justify-content: center;
                    margin-bottom: {SPACING['sm']};
                ">
                    <span class="material-icons" style="
                        font-size: 32px;
                        color: {quality_color};
                    ">grade</span>
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_3xl']};
                    font-weight: {TYPOGRAPHY['font_weight_bold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['xs']};
                ">
                    {quality_score:.0f}%
                </div>
                <div style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_sm']};
                    color: {COLORS['text_secondary']};
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    Quality
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_feedback_messages():
    """Render real-time feedback messages."""
    current_feedback = StateManager.get("current_feedback", [])
    
    if not current_feedback:
        # Show default message when no feedback
        st.markdown(
            f"""
            <div style="
                background-color: {COLORS['info']}15;
                border-left: 4px solid {COLORS['info']};
                border-radius: {BORDER_RADIUS['md']};
                padding: {SPACING['md']};
                margin: {SPACING['lg']} 0;
            ">
                <div style="
                    display: flex;
                    align-items: center;
                    gap: {SPACING['sm']};
                ">
                    <span class="material-icons" style="
                        font-size: 24px;
                        color: {COLORS['info']};
                    ">info</span>
                    <span style="
                        font-family: {TYPOGRAPHY['font_family_primary']};
                        font-size: {TYPOGRAPHY['font_size_base']};
                        color: var(--text-color);
                    ">
                        Position yourself in frame and start exercising to receive feedback
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Display feedback messages
        for feedback in current_feedback:
            # Determine feedback type and color
            feedback_lower = feedback.lower()
            if "good" in feedback_lower or "great" in feedback_lower or "excellent" in feedback_lower:
                feedback_color = COLORS['success']
                icon = "check_circle"
            elif "warning" in feedback_lower or "careful" in feedback_lower or "watch" in feedback_lower:
                feedback_color = COLORS['warning']
                icon = "warning"
            else:
                feedback_color = COLORS['error']
                icon = "error"
            
            st.markdown(
                f"""
                <div style="
                    background-color: {feedback_color}15;
                    border-left: 4px solid {feedback_color};
                    border-radius: {BORDER_RADIUS['md']};
                    padding: {SPACING['md']};
                    margin: {SPACING['sm']} 0;
                ">
                    <div style="
                        display: flex;
                        align-items: center;
                        gap: {SPACING['sm']};
                    ">
                        <span class="material-icons" style="
                            font-size: 24px;
                            color: {feedback_color};
                        ">{icon}</span>
                        <span style="
                            font-family: {TYPOGRAPHY['font_family_primary']};
                            font-size: {TYPOGRAPHY['font_size_base']};
                            color: var(--text-color);
                        ">
                            {feedback}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_camera_feed_with_feedback():
    """Render camera feed component with pose detection and feedback inside the loop."""
    st.markdown(
        f"""
        <div style="
            text-align: center;
            margin: {SPACING['xl']} 0;
        ">
            <h3 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_2xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['md']};
            ">
                Live Camera Feed
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Create placeholder for camera feed
    camera_placeholder = st.empty()
    
    # Create placeholder for feedback (will be updated inside camera loop)
    st.markdown(
        f"""
        <h3 style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_xl']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['text_primary']};
            margin: {SPACING['lg']} 0 {SPACING['md']} 0;
        ">
            Real-Time Feedback
        </h3>
        """,
        unsafe_allow_html=True,
    )
    feedback_placeholder = st.empty()
    
    # Camera control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        camera_active = StateManager.get("camera_active", False)
        if st.button("📹 Start Camera", use_container_width=True, disabled=camera_active):
            StateManager.set("camera_active", True)
            st.rerun()
    
    with col2:
        camera_active = StateManager.get("camera_active", False)
        if st.button("⏸️ Stop Camera", use_container_width=True, disabled=not camera_active):
            StateManager.set("camera_active", False)
            st.rerun()
    
    # If camera is active, show live feed
    if StateManager.get("camera_active", False):
        try:
            # Open camera
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                ErrorHandler.render_camera_error("Camera device not found or already in use")
                StateManager.set("camera_active", False)
                return
            
            # Get API client
            api_client = get_api_client()
            
            # Process frames
            frame_count = 0
            max_frames = 300  # Process for ~10 seconds at 30fps
            
            while StateManager.get("camera_active", False) and frame_count < max_frames:
                ret, frame = cap.read()
                
                if not ret:
                    ErrorHandler.render_camera_error("Failed to read frame from camera")
                    break
                
                # Detect pose every frame
                pose_result = api_client.detect_pose(frame, draw_landmarks=True)
                
                if pose_result and pose_result.get('detected'):
                    # Get annotated image
                    if 'annotated_image' in pose_result:
                        annotated_frame = api_client.decode_frame(pose_result['annotated_image'])
                    else:
                        annotated_frame = frame
                    
                    # Analyze exercise
                    key_points = pose_result.get('key_points', {})
                    
                    # Map exercise type to display name
                    exercise_display_map = {
                        "bicep_curl": "Bicep Curls",
                        "squat": "Squats",
                        "push_up": "Push-ups",
                    }
                    active_exercise = StateManager.get("active_exercise")
                    display_name = exercise_display_map.get(active_exercise, active_exercise)
                    
                    session_id = StateManager.get("session_id")
                    analysis_result = api_client.analyze_exercise(
                        session_id,
                        display_name,
                        key_points
                    )
                    
                    if analysis_result:
                        # Extract all feedback types from API response
                        feedback_list = []
                        
                        # Add errors
                        if analysis_result.get('errors'):
                            feedback_list.extend(analysis_result.get('errors', []))
                        
                        # Add warnings
                        if analysis_result.get('warnings'):
                            feedback_list.extend(analysis_result.get('warnings', []))
                        
                        # Add positive feedback
                        if analysis_result.get('feedback'):
                            feedback_list.extend(analysis_result.get('feedback', []))
                        
                        # Add real-time feedback message if available
                        if analysis_result.get('real_time_feedback'):
                            feedback_list.append(analysis_result.get('real_time_feedback'))
                        
                        # Update session state with analysis results using StateManager
                        StateManager.update_workout_metrics(
                            rep_count=analysis_result.get('rep_count'),
                            calories=analysis_result.get('calories'),
                            quality_score=analysis_result.get('quality_score'),
                            feedback=feedback_list
                        )
                        
                        # Update feedback display dynamically INSIDE the loop
                        with feedback_placeholder.container():
                            render_feedback_messages()
                    else:
                        # API call failed - show warning but continue
                        if frame_count % 30 == 0:  # Show warning every second
                            st.warning("⚠️ Temporary connection issue with backend. Retrying...", icon="⚠️")
                    
                    # Display annotated frame
                    camera_placeholder.image(annotated_frame, channels="BGR", use_container_width=True)
                elif pose_result is None:
                    # API call failed completely
                    if frame_count % 30 == 0:  # Show error every second
                        st.error("❌ Lost connection to backend. Please check backend status.", icon="🚨")
                    # Still show the frame
                    camera_placeholder.image(frame, channels="BGR", use_container_width=True)
                else:
                    # No pose detected - show overlay message
                    overlay_frame = frame.copy()
                    h, w = overlay_frame.shape[:2]
                    cv2.putText(
                        overlay_frame,
                        "Step into frame",
                        (w // 2 - 150, h // 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        3
                    )
                    camera_placeholder.image(overlay_frame, channels="BGR", use_container_width=True)
                
                frame_count += 1
                time.sleep(0.033)  # ~30 fps
            
            # Release camera
            cap.release()
            
            if frame_count >= max_frames:
                st.info("ℹ️ Camera feed stopped after timeout. Click 'Start Camera' to continue.", icon="ℹ️")
                StateManager.set("camera_active", False)
                
        except cv2.error as e:
            ErrorHandler.render_camera_error(f"OpenCV error: {str(e)}")
            StateManager.set("camera_active", False)
        except Exception as e:
            ErrorHandler.render_camera_error(f"Unexpected error: {str(e)}")
            StateManager.set("camera_active", False)
    else:
        # Show placeholder when camera is not active
        camera_placeholder.markdown(
            f"""
            <div style="
                background-color: {COLORS['background_secondary']};
                border: 2px dashed {COLORS['border']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['3xl']};
                text-align: center;
                min-height: 400px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            ">
                <span class="material-icons" style="
                    font-size: 72px;
                    color: {COLORS['text_tertiary']};
                    margin-bottom: {SPACING['lg']};
                ">videocam_off</span>
                <p style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_lg']};
                    color: {COLORS['text_secondary']};
                ">
                    Camera is not active. Click "Start Camera" to begin.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Show initial feedback message when camera is off
        with feedback_placeholder.container():
            render_feedback_messages()


def render_active_session():
    """Render the active workout session view."""
    # Get exercise display name
    exercise_display_map = {
        "bicep_curl": "Bicep Curls",
        "squat": "Squats",
        "push_up": "Push-ups",
    }
    active_exercise = StateManager.get("active_exercise")
    exercise_name = exercise_display_map.get(
        active_exercise,
        active_exercise.replace('_', ' ').title() if active_exercise else "Unknown"
    )
    
    session_id = StateManager.get("session_id", "")
    
    # Page header
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: {SPACING['xl']} {SPACING['lg']} {SPACING['md']};
            margin-bottom: {SPACING['lg']};
        ">
            <h1 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_3xl']};
                font-weight: {TYPOGRAPHY['font_weight_bold']};
                color: {COLORS['text_primary']};
                line-height: {TYPOGRAPHY['line_height_tight']};
                margin-bottom: {SPACING['xs']};
            ">
                {exercise_name} Session
            </h1>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_secondary']};
            ">
                Session ID: <code style="
                    font-family: {TYPOGRAPHY['font_family_mono']};
                    background-color: {COLORS['background_secondary']};
                    padding: 2px 6px;
                    border-radius: {BORDER_RADIUS['sm']};
                ">{session_id}</code>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Session metrics
    render_session_metrics()
    
    st.markdown(f"<div style='margin: {SPACING['xl']} 0;'></div>", unsafe_allow_html=True)
    
    # Camera feed (includes feedback inside the loop)
    render_camera_feed_with_feedback()
    
    st.markdown(f"<div style='margin: {SPACING['2xl']} 0;'></div>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🔙 Back to Exercise Selection", use_container_width=True):
            # Stop camera if active
            StateManager.set("camera_active", False)
            
            # End session
            with st.spinner("Ending session..."):
                try:
                    success = end_workout_session()
                    
                    if success:
                        st.success("✅ Session ended successfully!", icon="🎉")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("⚠️ Session ended but backend communication failed. Data may not be saved.", icon="⚠️")
                        # Clear state anyway using StateManager
                        StateManager.end_workout_session()
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    ErrorHandler.handle_exception(
                        e,
                        "ending workout session",
                        show_to_user=True,
                        fallback_message="Failed to end session properly. Returning to exercise selection."
                    )
                    # Clear state anyway
                    StateManager.end_workout_session()
                    time.sleep(1)
                    st.rerun()
    
    with col3:
        if st.button("🏁 End Workout", use_container_width=True, type="primary"):
            # Stop camera if active
            StateManager.set("camera_active", False)
            
            # Get current metrics before ending
            rep_count = StateManager.get("rep_count", 0)
            calories = StateManager.get("calories", 0.0)
            
            # End session
            with st.spinner("Saving workout session..."):
                try:
                    success = end_workout_session()
                    
                    if success:
                        st.success(
                            f"🎉 Great workout! You completed {rep_count} reps "
                            f"and burned {calories:.1f} calories!",
                            icon="🏆"
                        )
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.warning(
                            f"⚠️ Workout completed ({rep_count} reps, {calories:.1f} calories) "
                            "but failed to save to backend. Data may not be persisted.",
                            icon="⚠️"
                        )
                        time.sleep(2)
                        st.rerun()
                except Exception as e:
                    ErrorHandler.handle_exception(
                        e,
                        "saving workout session",
                        show_to_user=True,
                        fallback_message="Failed to save workout session. Your progress may not be recorded."
                    )
                    time.sleep(1)
                    st.rerun()


def main():
    """Main function to render the Workout page."""
    # Apply page configuration
    apply_page_config(
        page_title="Workout - AI Fitness Trainer",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Inject custom CSS and Material Icons
    inject_custom_css()
    inject_material_icons_cdn()
    inject_hover_styles()
    
    # Initialize session state
    StateManager.initialize_all()
    
    # Set current page
    Navigation.set_current_page("workout")
    
    # Render navigation
    Navigation.render_sidebar_nav()
    
    # Check backend health
    if not check_backend_health():
        render_backend_error()
        return
    
    # Check if there's an active session using StateManager
    if StateManager.is_workout_active():
        # Render active session view
        render_active_session()
    else:
        # Render page header
        render_page_header()
        
        # Render exercise selection view
        render_exercise_selection()
        
        # Footer
        st.markdown(
            f"""
            <div style="
                text-align: center;
                padding: {SPACING['2xl']} {SPACING['lg']} {SPACING['lg']};
                margin-top: {SPACING['3xl']};
                border-top: 1px solid {COLORS['border']};
            ">
                <p style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_sm']};
                    color: {COLORS['text_tertiary']};
                    margin: 0;
                ">
                    💡 Tip: Ensure good lighting and position yourself fully in frame for best results
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
