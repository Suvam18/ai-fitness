"""
Stats page for the AI Fitness Trainer Streamlit application.

This page displays aggregated workout statistics with visualizations,
performance trends, and personal bests.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from styles.custom_css import inject_custom_css, apply_page_config
from styles.theme import COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS
from utils.icons import (
    inject_material_icons_cdn,
    get_icon_name,
    render_icon,
)
from utils.state_manager import StateManager
from components.navigation import Navigation
from components.charts import ChartComponents
from services.workout_loader import WorkoutHistoryLoader
from services.stats_calculator import StatsCalculator
from utils.error_handler import ErrorHandler


def load_workout_sessions():
    """Load workout sessions from the backend data directory."""
    # Use cached sessions if available
    loaded_sessions = StateManager.get("loaded_sessions")
    loader_state = StateManager.get("loader_state")
    
    if loaded_sessions is not None and loader_state is not None:
        return loaded_sessions, loader_state
    
    # Load sessions using WorkoutHistoryLoader
    loader = WorkoutHistoryLoader()
    
    try:
        sessions = loader.load_all_sessions()
        
        # Store loader state for error reporting
        loader_state = {
            'corrupted_count': loader.get_corrupted_file_count(),
            'has_errors': loader.has_load_errors(),
            'errors': loader.load_errors
        }
        
        # Cache sessions and loader state in session state
        StateManager.set("loaded_sessions", sessions)
        StateManager.set("loader_state", loader_state)
        
        return sessions, loader_state
    except Exception as e:
        ErrorHandler.handle_exception(
            e,
            "loading workout statistics",
            show_to_user=True,
            fallback_message="Failed to load workout data for statistics. Please try refreshing the page."
        )
        return [], {'corrupted_count': 0, 'has_errors': True, 'errors': {}}


def render_page_header():
    """Render the stats page header."""
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
                Workout Statistics
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
                Analyze your performance trends and track your fitness journey
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview_metrics(sessions):
    """
    Render overview metrics section with total workouts, reps, calories, duration.
    
    Args:
        sessions: List of workout sessions
    """
    # Calculate aggregate statistics
    total_workouts = len(sessions)
    total_reps = sum(session.get('reps', 0) for session in sessions)
    total_calories = sum(session.get('calories', 0.0) for session in sessions)
    total_duration = sum(session.get('duration', 0.0) for session in sessions)
    
    # Format duration for display
    duration_hours = int(total_duration // 3600)
    duration_minutes = int((total_duration % 3600) // 60)
    
    if duration_hours > 0:
        duration_formatted = f"{duration_hours}h {duration_minutes}m"
    else:
        duration_formatted = f"{duration_minutes}m"
    
    # Render section header
    st.markdown(
        f"""
        <div style="
            margin-bottom: {SPACING['xl']};
        ">
            <h2 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_2xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['lg']};
            ">
                Overview
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Create columns for metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        {
            "icon": "fitness_center",
            "value": str(total_workouts),
            "label": "Total Workouts",
            "color": COLORS['primary'],
        },
        {
            "icon": "repeat",
            "value": str(total_reps),
            "label": "Total Reps",
            "color": COLORS['secondary'],
        },
        {
            "icon": "local_fire_department",
            "value": f"{total_calories:.0f}",
            "label": "Total Calories",
            "color": COLORS['error'],
        },
        {
            "icon": "schedule",
            "value": duration_formatted,
            "label": "Total Duration",
            "color": COLORS['info'],
        },
    ]
    
    for col, metric in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div style="
                    background-color: {COLORS['card_background']};
                    border-radius: {BORDER_RADIUS['lg']};
                    padding: {SPACING['xl']};
                    box-shadow: {SHADOWS['md']};
                    border: 2px solid {COLORS['border']};
                    text-align: center;
                    transition: all 0.3s ease;
                    height: 100%;
                " class="metric-card">
                    <div style="
                        display: flex;
                        justify-content: center;
                        margin-bottom: {SPACING['md']};
                    ">
                        <span class="material-icons" style="
                            font-size: 48px;
                            color: {metric['color']};
                        ">{metric['icon']}</span>
                    </div>
                    <div style="
                        font-family: {TYPOGRAPHY['font_family_primary']};
                        font-size: {TYPOGRAPHY['font_size_4xl']};
                        font-weight: {TYPOGRAPHY['font_weight_bold']};
                        color: {COLORS['text_primary']};
                        margin-bottom: {SPACING['sm']};
                        line-height: 1;
                    ">
                        {metric['value']}
                    </div>
                    <div style="
                        font-family: {TYPOGRAPHY['font_family_primary']};
                        font-size: {TYPOGRAPHY['font_size_sm']};
                        color: {COLORS['text_secondary']};
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                        font-weight: {TYPOGRAPHY['font_weight_medium']};
                    ">
                        {metric['label']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_empty_state():
    """Render empty state when no workout data exists."""
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: {SPACING['4xl']} {SPACING['lg']};
            margin: {SPACING['3xl']} 0;
        ">
            <div style="
                display: flex;
                justify-content: center;
                margin-bottom: {SPACING['xl']};
                opacity: 0.5;
            ">
                <span class="material-icons" style="
                    font-size: 96px;
                    color: {COLORS['text_tertiary']};
                ">bar_chart</span>
            </div>
            <h3 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_2xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_secondary']};
                margin-bottom: {SPACING['md']};
            ">
                No Statistics Available
            </h3>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_tertiary']};
                line-height: {TYPOGRAPHY['line_height_relaxed']};
                max-width: 500px;
                margin: 0 auto {SPACING['xl']} auto;
            ">
                Complete your first workout to start tracking your performance and viewing detailed statistics about your fitness journey.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Add action button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏋️ Start Your First Workout", use_container_width=True):
            StateManager.set_current_page("workout")
            st.switch_page("pages/2_💪_Workout.py")


def render_workout_frequency_chart(sessions):
    """
    Render workout frequency chart showing workouts over time.
    
    Args:
        sessions: List of workout sessions
    """
    # Render section header
    st.markdown(
        f"""
        <div style="
            margin-bottom: {SPACING['lg']};
            margin-top: {SPACING['2xl']};
        ">
            <h2 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_2xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['md']};
            ">
                Workout Frequency
            </h2>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_secondary']};
                margin-bottom: {SPACING['lg']};
            ">
                Track your workout consistency over time
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    try:
        # Calculate frequency data using StatsCalculator with auto interval selection
        frequency_data = StatsCalculator.calculate_workout_frequency(sessions, interval="auto")
        
        if not frequency_data:
            st.info("No workout frequency data available.")
            return
        
        # Prepare data for line chart
        dates = list(frequency_data.keys())
        counts = list(frequency_data.values())
        
        # Format dates for better display
        formatted_dates = []
        for date_str in dates:
            try:
                # Handle different date formats (YYYY-MM-DD or YYYY-MM)
                if len(date_str) == 10:  # YYYY-MM-DD format (daily)
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_dates.append(dt.strftime("%b %d"))
                elif len(date_str) == 7:  # YYYY-MM format (monthly)
                    dt = datetime.strptime(date_str, "%Y-%m")
                    formatted_dates.append(dt.strftime("%b %Y"))
                else:
                    formatted_dates.append(date_str)
            except ValueError:
                formatted_dates.append(date_str)
        
        # Create chart data structure
        chart_data = {
            'x': formatted_dates,
            'y': counts,
            'name': 'Workouts'
        }
        
        # Determine interval type for axis label
        date_range_days = 0
        if len(dates) >= 2:
            try:
                first_date = datetime.strptime(dates[0][:10], "%Y-%m-%d")
                last_date = datetime.strptime(dates[-1][:10], "%Y-%m-%d")
                date_range_days = (last_date - first_date).days
            except ValueError:
                pass
        
        # Set appropriate x-axis label based on interval
        if date_range_days < 14:
            x_label = "Date"
        elif date_range_days <= 90:
            x_label = "Week"
        else:
            x_label = "Month"
        
        # Create line chart using ChartComponents
        fig = ChartComponents.create_line_chart(
            data=chart_data,
            title="Workout Frequency Over Time",
            x_label=x_label,
            y_label="Number of Workouts",
            show_legend=False,
            height=450
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        ErrorHandler.handle_exception(
            e,
            "rendering workout frequency chart",
            show_to_user=True,
            fallback_message="Unable to display workout frequency chart. Data may be incomplete."
        )


def render_exercise_distribution_chart(sessions):
    """
    Render exercise distribution chart showing breakdown of exercises by type.
    
    Args:
        sessions: List of workout sessions
    """
    # Calculate exercise distribution using StatsCalculator
    distribution_data = StatsCalculator.calculate_exercise_distribution(sessions)
    
    if not distribution_data:
        st.info("No exercise distribution data available.")
        return
    
    # Only display chart when multiple exercise types exist
    if len(distribution_data) < 2:
        return
    
    # Render section header
    st.markdown(
        f"""
        <div style="
            margin-bottom: {SPACING['lg']};
            margin-top: {SPACING['2xl']};
        ">
            <h2 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_2xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['md']};
            ">
                Exercise Distribution
            </h2>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_secondary']};
                margin-bottom: {SPACING['lg']};
            ">
                Breakdown of your workouts by exercise type
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Format exercise names for display (convert snake_case to Title Case)
    formatted_labels = []
    for exercise in distribution_data.keys():
        formatted_name = exercise.replace('_', ' ').title()
        formatted_labels.append(formatted_name)
    
    # Prepare data for chart
    chart_data = {
        'labels': formatted_labels,
        'values': list(distribution_data.values())
    }
    
    # Create two columns for side-by-side charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Create pie chart using ChartComponents
        pie_fig = ChartComponents.create_pie_chart(
            data=chart_data,
            title="Exercise Distribution (Pie Chart)",
            show_legend=True,
            height=450
        )
        
        # Display the pie chart
        st.plotly_chart(pie_fig, use_container_width=True)
    
    with col2:
        # Create bar chart using ChartComponents
        bar_data = {
            'categories': formatted_labels,
            'values': list(distribution_data.values())
        }
        
        bar_fig = ChartComponents.create_bar_chart(
            data=bar_data,
            title="Exercise Distribution (Bar Chart)",
            x_label="Exercise Type",
            y_label="Number of Workouts",
            orientation='v',
            show_legend=False,
            height=450
        )
        
        # Display the bar chart
        st.plotly_chart(bar_fig, use_container_width=True)


def render_performance_trends(sessions):
    """
    Render performance trends chart showing quality scores over time.
    
    Args:
        sessions: List of workout sessions
    """
    # Calculate trend data using StatsCalculator
    trends = StatsCalculator.calculate_performance_trends(sessions)
    
    if not trends:
        st.info("No performance trend data available. Quality scores will be tracked in future workouts.")
        return
    
    # Render section header
    st.markdown(
        f"""
        <div style="
            margin-bottom: {SPACING['lg']};
            margin-top: {SPACING['2xl']};
        ">
            <h2 style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_2xl']};
                font-weight: {TYPOGRAPHY['font_weight_semibold']};
                color: {COLORS['text_primary']};
                margin-bottom: {SPACING['md']};
            ">
                Performance Trends
            </h2>
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_secondary']};
                margin-bottom: {SPACING['lg']};
            ">
                Track your form quality and performance improvements over time
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Identify personal bests
    personal_bests = StatsCalculator.identify_personal_bests(sessions)
    
    # Format dates for display
    formatted_dates = []
    for trend in trends:
        try:
            dt = datetime.strptime(trend['date'], "%Y-%m-%d")
            formatted_dates.append(dt.strftime("%b %d"))
        except ValueError:
            formatted_dates.append(trend['date'])
    
    # Prepare data for line chart
    quality_scores = [trend['quality_score'] for trend in trends]
    
    # Create chart data structure
    chart_data = {
        'x': formatted_dates,
        'y': quality_scores,
        'name': 'Quality Score'
    }
    
    # Create line chart using ChartComponents
    fig = ChartComponents.create_line_chart(
        data=chart_data,
        title="Average Quality Score Over Time",
        x_label="Date",
        y_label="Quality Score (%)",
        show_legend=False,
        height=450
    )
    
    # Highlight personal best if available
    if personal_bests.get('best_quality'):
        best_quality = personal_bests['best_quality']
        best_date = best_quality['date']
        best_value = best_quality['value']
        
        # Find the index of the best quality date in trends
        for idx, trend in enumerate(trends):
            if trend['date'] == best_date:
                # Add annotation for personal best
                fig.add_annotation(
                    x=formatted_dates[idx],
                    y=best_value,
                    text=f"🏆 Personal Best<br>{best_value:.1f}%",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor=COLORS['warning'],
                    ax=0,
                    ay=-60,
                    font=dict(
                        size=12,
                        color=COLORS['warning'],
                        family=TYPOGRAPHY['font_family_primary']
                    ),
                    bgcolor=COLORS['background'],
                    bordercolor=COLORS['warning'],
                    borderwidth=2,
                    borderpad=4,
                    opacity=0.9
                )
                
                # Add a marker for the personal best
                fig.add_trace(go.Scatter(
                    x=[formatted_dates[idx]],
                    y=[best_value],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color=COLORS['warning'],
                        symbol='star',
                        line=dict(color=COLORS['background'], width=2)
                    ),
                    showlegend=False,
                    hovertemplate=f'<b>Personal Best</b><br>{best_value:.1f}%<extra></extra>'
                ))
                break
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Add comparison by exercise type if multiple types exist
    exercise_distribution = StatsCalculator.calculate_exercise_distribution(sessions)
    
    if len(exercise_distribution) > 1:
        st.markdown(
            f"""
            <div style="
                margin-top: {SPACING['2xl']};
                margin-bottom: {SPACING['lg']};
            ">
                <h3 style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_xl']};
                    font-weight: {TYPOGRAPHY['font_weight_semibold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['md']};
                ">
                    Performance by Exercise Type
                </h3>
                <p style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_base']};
                    color: {COLORS['text_secondary']};
                    margin-bottom: {SPACING['lg']};
                ">
                    Compare your quality scores across different exercises
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Group sessions by exercise type and calculate trends for each
        exercise_trends = {}
        for session in sessions:
            exercise_type = session.get('exercise', 'unknown')
            if exercise_type not in exercise_trends:
                exercise_trends[exercise_type] = []
            exercise_trends[exercise_type].append(session)
        
        # Prepare data for multi-series line chart
        chart_series = []
        colors = [
            COLORS['primary'],
            COLORS['secondary'],
            COLORS['accent'],
            COLORS['warning'],
            COLORS['info']
        ]
        
        for idx, (exercise_type, exercise_sessions) in enumerate(exercise_trends.items()):
            exercise_trend_data = StatsCalculator.calculate_performance_trends(exercise_sessions)
            
            if exercise_trend_data:
                # Format dates
                ex_formatted_dates = []
                for trend in exercise_trend_data:
                    try:
                        dt = datetime.strptime(trend['date'], "%Y-%m-%d")
                        ex_formatted_dates.append(dt.strftime("%b %d"))
                    except ValueError:
                        ex_formatted_dates.append(trend['date'])
                
                # Format exercise name
                exercise_name = exercise_type.replace('_', ' ').title()
                
                chart_series.append({
                    'x': ex_formatted_dates,
                    'y': [trend['quality_score'] for trend in exercise_trend_data],
                    'name': exercise_name
                })
        
        if chart_series:
            # Create multi-series line chart
            comparison_fig = ChartComponents.create_line_chart(
                data=chart_series,
                title="Quality Score Comparison by Exercise",
                x_label="Date",
                y_label="Quality Score (%)",
                show_legend=True,
                height=450
            )
            
            # Display the comparison chart
            st.plotly_chart(comparison_fig, use_container_width=True)
    
    # Display personal bests summary
    if any(personal_bests.values()):
        st.markdown(
            f"""
            <div style="
                margin-top: {SPACING['2xl']};
                margin-bottom: {SPACING['lg']};
            ">
                <h3 style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_xl']};
                    font-weight: {TYPOGRAPHY['font_weight_semibold']};
                    color: {COLORS['text_primary']};
                    margin-bottom: {SPACING['md']};
                ">
                    🏆 Personal Bests
                </h3>
                <p style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_base']};
                    color: {COLORS['text_secondary']};
                    margin-bottom: {SPACING['lg']};
                ">
                    Your best achievements across all workouts
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Create columns for personal best cards
        cols = st.columns(4)
        
        best_records = [
            {
                "key": "max_reps",
                "icon": "repeat",
                "label": "Most Reps",
                "format": lambda v: f"{int(v)}",
                "color": COLORS['primary']
            },
            {
                "key": "longest_duration",
                "icon": "schedule",
                "label": "Longest Duration",
                "format": lambda v: f"{int(v//60)}m {int(v%60)}s" if v >= 60 else f"{int(v)}s",
                "color": COLORS['info']
            },
            {
                "key": "best_quality",
                "icon": "star",
                "label": "Best Quality",
                "format": lambda v: f"{v:.1f}%",
                "color": COLORS['warning']
            },
            {
                "key": "most_calories",
                "icon": "local_fire_department",
                "label": "Most Calories",
                "format": lambda v: f"{v:.0f}",
                "color": COLORS['error']
            }
        ]
        
        for col, record_info in zip(cols, best_records):
            record = personal_bests.get(record_info['key'])
            
            if record:
                with col:
                    exercise_name = record['exercise'].replace('_', ' ').title()
                    formatted_value = record_info['format'](record['value'])
                    
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {COLORS['card_background']};
                            border-radius: {BORDER_RADIUS['lg']};
                            padding: {SPACING['lg']};
                            box-shadow: {SHADOWS['md']};
                            border: 2px solid {record_info['color']};
                            text-align: center;
                            height: 100%;
                        ">
                            <div style="
                                display: flex;
                                justify-content: center;
                                margin-bottom: {SPACING['sm']};
                            ">
                                <span class="material-icons" style="
                                    font-size: 36px;
                                    color: {record_info['color']};
                                ">{record_info['icon']}</span>
                            </div>
                            <div style="
                                font-family: {TYPOGRAPHY['font_family_primary']};
                                font-size: {TYPOGRAPHY['font_size_3xl']};
                                font-weight: {TYPOGRAPHY['font_weight_bold']};
                                color: {COLORS['text_primary']};
                                margin-bottom: {SPACING['xs']};
                                line-height: 1;
                            ">
                                {formatted_value}
                            </div>
                            <div style="
                                font-family: {TYPOGRAPHY['font_family_primary']};
                                font-size: {TYPOGRAPHY['font_size_xs']};
                                color: {COLORS['text_secondary']};
                                text-transform: uppercase;
                                letter-spacing: 0.05em;
                                font-weight: {TYPOGRAPHY['font_weight_medium']};
                                margin-bottom: {SPACING['xs']};
                            ">
                                {record_info['label']}
                            </div>
                            <div style="
                                font-family: {TYPOGRAPHY['font_family_primary']};
                                font-size: {TYPOGRAPHY['font_size_xs']};
                                color: {COLORS['text_tertiary']};
                                margin-top: {SPACING['sm']};
                            ">
                                {exercise_name}<br>{record['date']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


def inject_hover_styles():
    """Inject CSS for hover effects on metric cards and dark mode support."""
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
        
        [data-testid="stAppViewContainer"][data-theme="dark"] h1,
        [data-testid="stAppViewContainer"][data-theme="dark"] h2,
        [data-testid="stAppViewContainer"][data-theme="dark"] h3 {{
            color: var(--text-color) !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] p {{
            color: var(--text-secondary) !important;
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
        
        /* Fix button text visibility in both light and dark mode */
        .stButton > button {{
            color: #ffffff !important;
            background-color: #2563eb !important;
        }}
        
        .stButton > button:hover {{
            background-color: #1e40af !important;
            color: #ffffff !important;
        }}
        
        /* Fix button text in dark mode */
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button {{
            color: #ffffff !important;
            background-color: #2563eb !important;
        }}
        
        [data-testid="stAppViewContainer"][data-theme="dark"] .stButton > button:hover {{
            background-color: #1e40af !important;
            color: #ffffff !important;
        }}
        
        /* Hover effects */
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: {SHADOWS['lg']};
            border-color: {COLORS['primary_light']};
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .metric-card {{
                padding: {SPACING['md']};
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    """Main function to render the Stats page."""
    # Apply page configuration
    apply_page_config(
        page_title="Stats - AI Fitness Trainer",
        page_icon="📊",
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
    Navigation.set_current_page("stats")
    
    # Render navigation
    Navigation.render_sidebar_nav()
    
    # Render page header
    render_page_header()
    
    # Load workout sessions
    sessions, loader_state = load_workout_sessions()
    
    # Show warning for corrupted files if any
    if loader_state.get('corrupted_count', 0) > 0:
        ErrorHandler.render_corrupted_data_warning(loader_state['corrupted_count'])
    
    # Check if any sessions exist
    if not sessions:
        # Display empty state
        render_empty_state()
    else:
        # Render overview metrics
        render_overview_metrics(sessions)
        
        # Add divider
        st.markdown(
            f"""
            <div style="margin: {SPACING['3xl']} 0;">
                <hr style="
                    border: none;
                    border-top: 1px solid {COLORS['border']};
                ">
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Render workout frequency chart
        render_workout_frequency_chart(sessions)
        
        # Add divider
        st.markdown(
            f"""
            <div style="margin: {SPACING['3xl']} 0;">
                <hr style="
                    border: none;
                    border-top: 1px solid {COLORS['border']};
                ">
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Render exercise distribution chart
        render_exercise_distribution_chart(sessions)
        
        # Add divider
        st.markdown(
            f"""
            <div style="margin: {SPACING['3xl']} 0;">
                <hr style="
                    border: none;
                    border-top: 1px solid {COLORS['border']};
                ">
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Render performance trends
        render_performance_trends(sessions)
        
        # Remove the placeholder message since we now have performance trends
        # (The "More detailed statistics coming soon" message)
    
    # Footer
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: {SPACING['3xl']} {SPACING['lg']} {SPACING['xl']};
            margin-top: {SPACING['4xl']};
            border-top: 1px solid {COLORS['border']};
        ">
            <p style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_sm']};
                color: {COLORS['text_tertiary']};
                margin: 0;
            ">
                AI Fitness Trainer © 2024 | Track Your Progress
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
