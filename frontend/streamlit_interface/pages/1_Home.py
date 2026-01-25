"""
Home page for the AI Fitness Trainer Streamlit application.

This page serves as the main landing page with a hero section, feature overview,
and quick action cards for starting workouts.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from styles.custom_css import inject_custom_css, apply_page_config
from utils.icons import inject_material_icons_cdn, get_icon_name
from utils.state_manager import StateManager
from components.navigation import Navigation
from components.hero_carousel import render_hero_carousel


def inject_dark_mode_support():
    """Inject CSS variables for dark mode support and remove top white space."""
    st.markdown(
        """
        <style>
        :root {
            --text-color: #111827;
            --text-secondary: #6b7280;
            --card-bg: #f9fafb;
            --border-color: #e5e7eb;
        }
        
        /* Dark mode support via media query */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #f9fafb;
                --text-secondary: #9ca3af;
                --card-bg: #1f2937;
                --border-color: #374151;
            }
        }
        
        /* Dark mode support via Streamlit's data-theme attribute */
        [data-testid="stAppViewContainer"][data-theme="dark"] {
            --text-color: #f9fafb;
            --text-secondary: #9ca3af;
            --card-bg: #1f2937;
            --border-color: #374151;
        }
        
        /* Ensure dark mode styles apply to all elements */
        [data-testid="stAppViewContainer"][data-theme="dark"] h1,
        [data-testid="stAppViewContainer"][data-theme="dark"] h2,
        [data-testid="stAppViewContainer"][data-theme="dark"] h3 {
            color: var(--text-color) !important;
        }
        
        [data-testid="stAppViewContainer"][data-theme="dark"] p {
            color: var(--text-secondary) !important;
        }
        
        /* Remove top white space */
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        
        [data-testid="stToolbar"] {
            background-color: transparent !important;
        }
        
        /* Hide the toolbar buttons but keep the hamburger menu */
        [data-testid="stToolbar"] > div:not(:first-child) {
            display: none !important;
        }
        
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem !important;
        }
        
        /* Fix button text visibility in both light and dark mode */
        .stButton > button {
            color: #ffffff !important;
            background-color: #2563eb !important;
        }
        
        .stButton > button:hover {
            background-color: #1e40af !important;
            color: #ffffff !important;
        }
        
        /* Fix button text in dark mode */
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button {
            color: #ffffff !important;
            background-color: #2563eb !important;
        }
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button:hover {
            background-color: #1e40af !important;
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    """Main function to render the Home page."""
    # Apply page configuration
    apply_page_config(
        page_title="Home - AI Fitness Trainer",
        page_icon="home",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Inject custom CSS and Material Icons
    inject_custom_css()
    inject_material_icons_cdn()
    inject_dark_mode_support()

    # Initialize session state
    StateManager.initialize_all()

    # Set current page
    Navigation.set_current_page("home")

    # Render navigation
    Navigation.render_sidebar_nav()



    # Hero Carousel Section
    render_hero_carousel()

    # Features section
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 0.5rem; margin: 2rem 0 1.5rem 0;'>
            <span class="material-icons" style='color: #2563eb;'>auto_awesome</span>
            <h2 style='margin: 0; color: var(--text-color);'>Features</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style='padding: 1.5rem; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); text-align: center;'>
                <span class="material-icons" style='font-size: 3rem; color: #2563eb; margin-bottom: 0.5rem;'>videocam</span>
                <h3 style='font-weight: 600; color: var(--text-color); margin: 0.5rem 0;'>Real-Time Analysis</h3>
                <p style='font-size: 0.875rem; color: var(--text-secondary); margin: 0;'>
                    Get instant feedback on your form using advanced pose detection
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='padding: 1.5rem; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); text-align: center;'>
                <span class="material-icons" style='font-size: 3rem; color: #10b981; margin-bottom: 0.5rem;'>trending_up</span>
                <h3 style='font-weight: 600; color: var(--text-color); margin: 0.5rem 0;'>Track Progress</h3>
                <p style='font-size: 0.875rem; color: var(--text-secondary); margin: 0;'>
                    Monitor your workout history and performance trends over time
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style='padding: 1.5rem; background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border-color); text-align: center;'>
                <span class="material-icons" style='font-size: 3rem; color: #f59e0b; margin-bottom: 0.5rem;'>emoji_events</span>
                <h3 style='font-weight: 600; color: var(--text-color); margin: 0.5rem 0;'>Achieve Goals</h3>
                <p style='font-size: 0.875rem; color: var(--text-secondary); margin: 0;'>
                    Set targets, track achievements, and celebrate milestones
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Start Workout section
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 0.5rem; margin: 2rem 0 1.5rem 0;'>
            <span class="material-icons" style='color: #2563eb;'>fitness_center</span>
            <h2 style='margin: 0; color: var(--text-color);'>Start Your Workout</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    exercises = [
        {
            "type": "bicep_curl",
            "display_name": "Bicep Curls",
            "description": "Build arm strength with proper curl form",
            "icon": "fitness_center",
            "color": "#2563eb"
        },
        {
            "type": "squat",
            "display_name": "Squats",
            "description": "Strengthen legs and core with perfect technique",
            "icon": "accessibility",
            "color": "#10b981"
        },
        {
            "type": "push_up",
            "display_name": "Push-ups",
            "description": "Develop upper body strength with control",
            "icon": "self_improvement",
            "color": "#8b5cf6"
        },
    ]

    col1, col2, col3 = st.columns(3)

    for col, exercise in zip([col1, col2, col3], exercises):
        with col:
            st.markdown(
                f"""
                <div style='padding: 1.5rem; background: var(--card-bg); border-radius: 12px; border: 2px solid var(--border-color); text-align: center;'>
                    <span class="material-icons" style='font-size: 4rem; color: {exercise['color']}; margin-bottom: 0.5rem;'>{exercise['icon']}</span>
                    <h3 style='font-weight: 600; color: var(--text-color); margin: 0.5rem 0;'>{exercise['display_name']}</h3>
                    <p style='font-size: 0.875rem; color: var(--text-secondary); margin-bottom: 1rem;'>
                        {exercise['description']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"Start {exercise['display_name']}",
                key=f"start_{exercise['type']}",
                use_container_width=True,
            ):
                StateManager.set("active_exercise", exercise["type"])
                StateManager.set_current_page("workout")
                st.switch_page("pages/2_Workout.py")


if __name__ == "__main__":
    main()
