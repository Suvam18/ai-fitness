"""
Utility functions and helpers for the Streamlit application
"""

from .icons import (
    inject_material_icons_cdn,
    get_icon_name,
    render_icon,
    render_icon_with_text,
    render_metric_card_icon,
    render_feedback_icon,
    render_exercise_card_icon,
    render_navigation_icon,
    get_icon_html_with_alignment,
    NAVIGATION_ICONS,
    EXERCISE_ICONS,
    METRIC_ICONS,
    FEEDBACK_ICONS,
    ACTION_ICONS,
    ICON_SIZES,
)

from .responsive import (
    get_responsive_columns,
    create_responsive_columns,
    inject_responsive_container_css,
    get_chart_height,
    inject_responsive_chart_css,
    add_viewport_meta_tag,
    create_responsive_card,
    inject_responsive_utilities,
)

from .state_manager import StateManager

__all__ = [
    "inject_material_icons_cdn",
    "get_icon_name",
    "render_icon",
    "render_icon_with_text",
    "render_metric_card_icon",
    "render_feedback_icon",
    "render_exercise_card_icon",
    "render_navigation_icon",
    "get_icon_html_with_alignment",
    "NAVIGATION_ICONS",
    "EXERCISE_ICONS",
    "METRIC_ICONS",
    "FEEDBACK_ICONS",
    "ACTION_ICONS",
    "ICON_SIZES",
    "get_responsive_columns",
    "create_responsive_columns",
    "inject_responsive_container_css",
    "get_chart_height",
    "inject_responsive_chart_css",
    "add_viewport_meta_tag",
    "create_responsive_card",
    "inject_responsive_utilities",
    "StateManager",
]
