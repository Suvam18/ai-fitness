"""
Icon utility system for the AI Fitness Trainer Streamlit application.

This module provides icon mapping functions and rendering utilities using
Material Design Icons via HTML/CSS. It ensures consistent icon usage across
all pages for navigation, exercises, metrics, and feedback.
"""

from typing import Optional
import streamlit as st


# Material Design Icons CDN URL
MATERIAL_ICONS_CDN = "https://fonts.googleapis.com/icon?family=Material+Icons"


# Icon constants for navigation pages
NAVIGATION_ICONS = {
    "home": "home",
    "workout": "fitness_center",
    "history": "history",
    "stats": "bar_chart",
}


# Icon constants for exercise types
EXERCISE_ICONS = {
    "bicep_curl": "fitness_center",
    "squat": "accessibility",
    "push_up": "self_improvement",
    "default": "sports_gymnastics",
}


# Icon constants for metrics
METRIC_ICONS = {
    "reps": "repeat",
    "duration": "schedule",
    "calories": "local_fire_department",
    "quality": "star",
    "heart_rate": "favorite",
    "distance": "straighten",
    "weight": "fitness_center",
    "sets": "format_list_numbered",
}


# Icon constants for feedback and status
FEEDBACK_ICONS = {
    "success": "check_circle",
    "warning": "warning",
    "error": "error",
    "info": "info",
    "excellent": "emoji_events",
    "good": "thumb_up",
    "average": "trending_flat",
    "poor": "trending_down",
}


# Icon constants for actions
ACTION_ICONS = {
    "start": "play_arrow",
    "stop": "stop",
    "pause": "pause",
    "resume": "play_arrow",
    "refresh": "refresh",
    "filter": "filter_list",
    "search": "search",
    "settings": "settings",
    "close": "close",
    "delete": "delete",
    "edit": "edit",
    "save": "save",
    "download": "download",
    "upload": "upload",
}


# Default icon sizes (in pixels)
ICON_SIZES = {
    "xs": 16,
    "sm": 20,
    "md": 24,
    "lg": 32,
    "xl": 40,
    "2xl": 48,
}


def inject_material_icons_cdn() -> None:
    """
    Inject Material Icons CDN link into the Streamlit app.
    
    This function should be called once at app initialization to load
    the Material Icons font from Google's CDN.
    """
    st.markdown(
        f'<link href="{MATERIAL_ICONS_CDN}" rel="stylesheet">',
        unsafe_allow_html=True
    )


def get_icon_name(category: str, key: str) -> str:
    """
    Get the Material Design icon name for a given category and key.
    
    Args:
        category: Icon category ('navigation', 'exercise', 'metric', 'feedback', 'action')
        key: Specific key within the category
        
    Returns:
        Material Design icon name, or 'help_outline' if not found
        
    Examples:
        >>> get_icon_name('navigation', 'home')
        'home'
        >>> get_icon_name('exercise', 'bicep_curl')
        'fitness_center'
        >>> get_icon_name('metric', 'calories')
        'local_fire_department'
    """
    icon_maps = {
        "navigation": NAVIGATION_ICONS,
        "exercise": EXERCISE_ICONS,
        "metric": METRIC_ICONS,
        "feedback": FEEDBACK_ICONS,
        "action": ACTION_ICONS,
    }
    
    icon_map = icon_maps.get(category, {})
    return icon_map.get(key, "help_outline")


def render_icon(
    icon_name: str,
    size: str = "md",
    color: Optional[str] = None,
    style: Optional[str] = None,
    title: Optional[str] = None,
) -> str:
    """
    Render a Material Design icon as HTML.
    
    Args:
        icon_name: Material Design icon name (e.g., 'home', 'fitness_center')
        size: Icon size ('xs', 'sm', 'md', 'lg', 'xl', '2xl') or custom pixel value
        color: CSS color value (hex, rgb, or named color)
        style: Additional CSS styles to apply
        title: Tooltip text for the icon
        
    Returns:
        HTML string for the icon
        
    Examples:
        >>> render_icon('home', size='lg', color='#2563eb')
        '<span class="material-icons" style="font-size: 32px; color: #2563eb; ...">home</span>'
    """
    # Determine icon size in pixels
    if size in ICON_SIZES:
        size_px = ICON_SIZES[size]
    else:
        # Assume size is already in pixels or a valid CSS value
        size_px = size
    
    # Build style string
    styles = [
        f"font-size: {size_px}px" if isinstance(size_px, int) else f"font-size: {size_px}",
        "vertical-align: middle",
        "display: inline-flex",
        "align-items: center",
        "justify-content: center",
    ]
    
    if color:
        styles.append(f"color: {color}")
    
    if style:
        styles.append(style)
    
    style_str = "; ".join(styles)
    
    # Build title attribute
    title_attr = f' title="{title}"' if title else ""
    
    return f'<span class="material-icons" style="{style_str}"{title_attr}>{icon_name}</span>'


def render_icon_with_text(
    icon_name: str,
    text: str,
    size: str = "md",
    color: Optional[str] = None,
    icon_position: str = "left",
    gap: str = "8px",
    style: Optional[str] = None,
) -> str:
    """
    Render an icon with adjacent text in a flex container.
    
    Args:
        icon_name: Material Design icon name
        text: Text to display next to the icon
        size: Icon size ('xs', 'sm', 'md', 'lg', 'xl', '2xl')
        color: CSS color value for both icon and text
        icon_position: Position of icon relative to text ('left' or 'right')
        gap: CSS gap value between icon and text
        style: Additional CSS styles for the container
        
    Returns:
        HTML string for the icon-text combination
        
    Examples:
        >>> render_icon_with_text('home', 'Home', size='md', color='#2563eb')
        '<div style="display: flex; ..."><span>home</span><span>Home</span></div>'
    """
    icon_html = render_icon(icon_name, size=size, color=color)
    
    # Build container styles
    container_styles = [
        "display: inline-flex",
        "align-items: center",
        f"gap: {gap}",
    ]
    
    if color:
        container_styles.append(f"color: {color}")
    
    if style:
        container_styles.append(style)
    
    container_style_str = "; ".join(container_styles)
    
    # Arrange icon and text based on position
    if icon_position == "right":
        content = f'<span>{text}</span>{icon_html}'
    else:
        content = f'{icon_html}<span>{text}</span>'
    
    return f'<div style="{container_style_str}">{content}</div>'


def render_metric_card_icon(
    metric_type: str,
    value: str,
    label: str,
    color: Optional[str] = None,
    icon_size: str = "lg",
) -> str:
    """
    Render a metric card with an icon, value, and label.
    
    This is a specialized function for displaying metrics in a card format
    commonly used on the Stats and History pages.
    
    Args:
        metric_type: Type of metric ('reps', 'duration', 'calories', 'quality')
        value: Metric value to display
        label: Label text for the metric
        color: CSS color value for the icon
        icon_size: Size of the icon
        
    Returns:
        HTML string for the metric card
        
    Examples:
        >>> render_metric_card_icon('calories', '250', 'Calories Burned', color='#ef4444')
        '<div style="..."><span>local_fire_department</span><div>...</div></div>'
    """
    icon_name = get_icon_name("metric", metric_type)
    icon_html = render_icon(icon_name, size=icon_size, color=color)
    
    card_html = f"""
    <div style="display: flex; align-items: center; gap: 12px;">
        {icon_html}
        <div style="display: flex; flex-direction: column;">
            <span style="font-size: 1.5rem; font-weight: 600; line-height: 1.2;">{value}</span>
            <span style="font-size: 0.875rem; color: #6b7280; line-height: 1.2;">{label}</span>
        </div>
    </div>
    """
    
    return card_html


def render_feedback_icon(
    feedback_type: str,
    message: str,
    size: str = "md",
) -> str:
    """
    Render a feedback message with an appropriate status icon.
    
    Args:
        feedback_type: Type of feedback ('success', 'warning', 'error', 'info', 
                       'excellent', 'good', 'average', 'poor')
        message: Feedback message text
        size: Icon size
        
    Returns:
        HTML string for the feedback message with icon
        
    Examples:
        >>> render_feedback_icon('success', 'Great form!', size='md')
        '<div style="..."><span>check_circle</span><span>Great form!</span></div>'
    """
    icon_name = get_icon_name("feedback", feedback_type)
    
    # Map feedback types to colors
    color_map = {
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6",
        "excellent": "#10b981",
        "good": "#10b981",
        "average": "#f59e0b",
        "poor": "#ef4444",
    }
    
    color = color_map.get(feedback_type, "#6b7280")
    
    return render_icon_with_text(
        icon_name=icon_name,
        text=message,
        size=size,
        color=color,
        gap="8px",
    )


def render_exercise_card_icon(
    exercise_type: str,
    size: str = "2xl",
    color: Optional[str] = None,
) -> str:
    """
    Render an exercise icon for use in exercise selection cards.
    
    Args:
        exercise_type: Type of exercise ('bicep_curl', 'squat', 'push_up')
        size: Icon size
        color: CSS color value
        
    Returns:
        HTML string for the exercise icon
        
    Examples:
        >>> render_exercise_card_icon('bicep_curl', size='2xl', color='#2563eb')
        '<span class="material-icons" style="...">fitness_center</span>'
    """
    icon_name = get_icon_name("exercise", exercise_type)
    return render_icon(icon_name, size=size, color=color)


def render_navigation_icon(
    page: str,
    size: str = "md",
    color: Optional[str] = None,
) -> str:
    """
    Render a navigation icon for use in the sidebar menu.
    
    Args:
        page: Page name ('home', 'workout', 'history', 'stats')
        size: Icon size
        color: CSS color value
        
    Returns:
        HTML string for the navigation icon
        
    Examples:
        >>> render_navigation_icon('home', size='md', color='#2563eb')
        '<span class="material-icons" style="...">home</span>'
    """
    icon_name = get_icon_name("navigation", page)
    return render_icon(icon_name, size=size, color=color)


def get_icon_html_with_alignment(
    icon_name: str,
    size: str = "md",
    color: Optional[str] = None,
    vertical_align: str = "middle",
) -> str:
    """
    Render an icon with specific vertical alignment for inline use.
    
    This is useful when embedding icons within text or buttons where
    precise alignment is needed.
    
    Args:
        icon_name: Material Design icon name
        size: Icon size
        color: CSS color value
        vertical_align: CSS vertical-align value ('top', 'middle', 'bottom', 'text-top', etc.)
        
    Returns:
        HTML string for the aligned icon
    """
    style = f"vertical-align: {vertical_align}"
    return render_icon(icon_name, size=size, color=color, style=style)
