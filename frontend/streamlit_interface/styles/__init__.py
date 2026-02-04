"""
Styles package for the AI Fitness Trainer Streamlit application.

This package provides theme configuration and CSS styling utilities
for consistent visual design across all pages.
"""

from .theme import (
    COLORS,
    TYPOGRAPHY,
    SPACING,
    BORDER_RADIUS,
    SHADOWS,
    TRANSITIONS,
    BREAKPOINTS,
    Z_INDEX,
    GOOGLE_FONTS_URL
)

from .custom_css import (
    get_custom_css,
    inject_custom_css,
    apply_page_config
)

from .page_styles import (
    get_page_header_style,
    get_section_header_style,
    get_metric_card_style,
    get_feature_card_style,
    get_exercise_card_style,
    get_empty_state_style,
    get_footer_style,
    get_divider_style,
    get_alert_style,
    inject_card_hover_styles
)

__all__ = [
    # Theme constants
    'COLORS',
    'TYPOGRAPHY',
    'SPACING',
    'BORDER_RADIUS',
    'SHADOWS',
    'TRANSITIONS',
    'BREAKPOINTS',
    'Z_INDEX',
    'GOOGLE_FONTS_URL',
    
    # CSS functions
    'get_custom_css',
    'inject_custom_css',
    'apply_page_config',
    
    # Page styling functions
    'get_page_header_style',
    'get_section_header_style',
    'get_metric_card_style',
    'get_feature_card_style',
    'get_exercise_card_style',
    'get_empty_state_style',
    'get_footer_style',
    'get_divider_style',
    'get_alert_style',
    'inject_card_hover_styles',
]
