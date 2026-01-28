"""
Custom CSS styling for the AI Fitness Trainer Streamlit application.

This module provides CSS injection functionality to apply professional
styling including hover states, responsive design, and custom components.
"""

import streamlit as st
from .theme import (
    COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, 
    SHADOWS, TRANSITIONS, BREAKPOINTS, GOOGLE_FONTS_URL
)


def get_custom_css() -> str:
    """
    Generate custom CSS for the application.
    
    Returns:
        str: Complete CSS string to be injected into Streamlit pages
    """
    css = f"""
    <style>
    /* Import Google Fonts */
    @import url('{GOOGLE_FONTS_URL}');
    
    /* Global Styles */
    * {{
        box-sizing: border-box;
    }}
    
    html, body, [class*="css"] {{
        font-family: {TYPOGRAPHY['font_family_primary']};
        color: {COLORS['text_primary']};
    }}
    
    /* Main Container with Gradient Background */
    .main {{
        background: {COLORS['background']};
        background-image: {COLORS['background_gradient']};
        background-attachment: fixed;
        padding: {SPACING['lg']};
        min-height: 100vh;
    }}
    
    /* Streamlit Header - Transparent */
    header {{
        background-color: transparent !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Typography Styles */
    h1 {{
        font-size: clamp({TYPOGRAPHY['font_size_3xl']}, 5vw, {TYPOGRAPHY['font_size_5xl']});
        font-weight: {TYPOGRAPHY['font_weight_bold']};
        color: {COLORS['text_primary']};
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        margin-bottom: {SPACING['xl']};
        letter-spacing: {TYPOGRAPHY['letter_spacing_tight']};
    }}
    
    h2 {{
        font-size: clamp({TYPOGRAPHY['font_size_xl']}, 3vw, {TYPOGRAPHY['font_size_3xl']});
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['lg']};
    }}
    
    h3 {{
        font-size: clamp({TYPOGRAPHY['font_size_lg']}, 2.5vw, {TYPOGRAPHY['font_size_2xl']});
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['md']};
    }}
    
    p {{
        font-size: clamp({TYPOGRAPHY['font_size_sm']}, 1.5vw, {TYPOGRAPHY['font_size_base']});
        font-weight: {TYPOGRAPHY['font_weight_normal']};
        color: {COLORS['text_secondary']};
        line-height: {TYPOGRAPHY['line_height_relaxed']};
        margin-bottom: {SPACING['md']};
    }}
    
    /* Button Styles - Neon Glow */
    .stButton > button {{
        background: linear-gradient(135deg, #c2410c, #dc2626);
        color: {COLORS['text_inverse']};
        border: none;
        border-radius: {BORDER_RADIUS['full']};
        padding: {SPACING['md']} {SPACING['xl']};
        font-size: {TYPOGRAPHY['font_size_base']};
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        cursor: pointer;
        transition: all {TRANSITIONS['normal']};
        box-shadow: 0 0 15px rgba(194, 65, 12, 0.3);
        text-transform: uppercase;
        letter-spacing: {TYPOGRAPHY['letter_spacing_wide']};
        width: 100%;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(194, 65, 12, 0.5);
        filter: brightness(1.15);
    }}
    
    /* Glassmorphism Card Styles */
    .glass-card {{
        background: {COLORS['card_background']};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {COLORS['border']};
        border-radius: {BORDER_RADIUS['2xl']};
        padding: {SPACING['xl']};
        box-shadow: {SHADOWS['lg']};
        transition: all {TRANSITIONS['normal']};
    }}
    
    .glass-card:hover {{
        background: {COLORS['card_hover']};
        border-color: {COLORS['border_glow']};
        box-shadow: {COLORS['primary_glow']}, {SHADOWS['xl']};
        transform: translateY(-5px);
    }}
    
    /* Metric Card Styles */
    [data-testid="stMetricValue"] {{
        color: {COLORS['primary_light']};
        text-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {COLORS['text_tertiary']};
    }}
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['background']} !important;
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.8s ease-out forwards;
    }}
    
    .animate-slide-up {{
        animation: slideUp 0.6s ease-out forwards;
    }}
    
    /* Material Icon Styles */
    .material-icons {{
        font-family: 'Material Icons';
        font-weight: normal;
        font-style: normal;
        display: inline-block;
        line-height: 1;
        text-transform: none;
        letter-spacing: normal;
        word-wrap: normal;
        white-space: nowrap;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }}
    
    .icon-glow-primary {{
        text-shadow: {COLORS['primary_glow']};
    }}
    
    .icon-glow-secondary {{
        text-shadow: {COLORS['secondary_glow']};
    }}
    
    .icon-glow-accent {{
        text-shadow: {COLORS['accent_glow']};
    }}
    
    /* Responsive Adjustments */
    @media (max-width: {BREAKPOINTS['tablet']}) {{
        .main {{
            padding: {SPACING['md']};
        }}
        .glass-card {{
            padding: {SPACING['lg']};
        }}
    }}
    </style>
    """
    return css


def inject_custom_css() -> None:
    """
    Inject custom CSS into the current Streamlit page.
    
    This function should be called at the beginning of each page
    to apply consistent styling across the application.
    """
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    # Also inject responsive utilities
    try:
        from utils.responsive import inject_responsive_utilities
        inject_responsive_utilities()
    except ImportError:
        # Fallback for when running from different contexts
        import sys
        from pathlib import Path
        parent_dir = Path(__file__).parent.parent
        if str(parent_dir) not in sys.path:
            sys.path.insert(0, str(parent_dir))
        from utils.responsive import inject_responsive_utilities
        inject_responsive_utilities()



def apply_page_config(
    page_title: str = "AI Fitness Trainer",
    page_icon: str = "💪",
    layout: str = "wide",
    initial_sidebar_state: str = "expanded"
) -> None:
    """
    Apply Streamlit page configuration with custom settings.
    
    Args:
        page_title: Title displayed in browser tab
        page_icon: Icon displayed in browser tab
        layout: Page layout ("centered" or "wide")
        initial_sidebar_state: Initial sidebar state ("expanded" or "collapsed")
    """
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state=initial_sidebar_state
    )
