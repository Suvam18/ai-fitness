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
    
    /* Main Container */
    .main {{
        background-color: {COLORS['background']};
        padding: {SPACING['lg']};
    }}
    
    /* Streamlit Header */
    header {{
        background-color: {COLORS['background']} !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Typography Styles */
    h1 {{
        font-size: clamp({TYPOGRAPHY['font_size_2xl']}, 4vw, {TYPOGRAPHY['font_size_4xl']});
        font-weight: {TYPOGRAPHY['font_weight_bold']};
        color: {COLORS['text_primary']};
        line-height: {TYPOGRAPHY['line_height_tight']};
        margin-bottom: {SPACING['lg']};
        letter-spacing: {TYPOGRAPHY['letter_spacing_tight']};
    }}
    
    h2 {{
        font-size: clamp({TYPOGRAPHY['font_size_xl']}, 3vw, {TYPOGRAPHY['font_size_3xl']});
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        color: {COLORS['text_primary']};
        line-height: {TYPOGRAPHY['line_height_tight']};
        margin-bottom: {SPACING['md']};
    }}
    
    h3 {{
        font-size: clamp({TYPOGRAPHY['font_size_lg']}, 2.5vw, {TYPOGRAPHY['font_size_2xl']});
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        color: {COLORS['text_primary']};
        line-height: {TYPOGRAPHY['line_height_normal']};
        margin-bottom: {SPACING['md']};
    }}
    
    h4 {{
        font-size: clamp({TYPOGRAPHY['font_size_base']}, 2vw, {TYPOGRAPHY['font_size_xl']});
        font-weight: {TYPOGRAPHY['font_weight_medium']};
        color: {COLORS['text_primary']};
        margin-bottom: {SPACING['sm']};
    }}
    
    p {{
        font-size: clamp({TYPOGRAPHY['font_size_sm']}, 1.5vw, {TYPOGRAPHY['font_size_base']});
        font-weight: {TYPOGRAPHY['font_weight_normal']};
        color: {COLORS['text_secondary']};
        line-height: {TYPOGRAPHY['line_height_relaxed']};
        margin-bottom: {SPACING['md']};
    }}
    
    /* Button Styles */
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_inverse']};
        border: none;
        border-radius: {BORDER_RADIUS['md']};
        padding: {SPACING['sm']} {SPACING['lg']};
        font-size: {TYPOGRAPHY['font_size_base']};
        font-weight: {TYPOGRAPHY['font_weight_medium']};
        font-family: {TYPOGRAPHY['font_family_primary']};
        cursor: pointer;
        transition: all {TRANSITIONS['normal']};
        box-shadow: {SHADOWS['sm']};
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['primary_dark']};
        box-shadow: {SHADOWS['md']};
        transform: translateY(-1px);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: {SHADOWS['sm']};
    }}
    
    .stButton > button:focus {{
        outline: 2px solid {COLORS['primary_light']};
        outline-offset: 2px;
    }}
    
    /* Secondary Button */
    .stButton.secondary > button {{
        background-color: {COLORS['background_secondary']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
    }}
    
    .stButton.secondary > button:hover {{
        background-color: {COLORS['background_tertiary']};
        border-color: {COLORS['border_dark']};
    }}
    
    /* Card Styles */
    .card {{
        background-color: {COLORS['card_background']};
        border-radius: {BORDER_RADIUS['lg']};
        padding: {SPACING['lg']};
        box-shadow: {SHADOWS['md']};
        transition: all {TRANSITIONS['normal']};
        border: 1px solid {COLORS['border']};
        margin-bottom: {SPACING['md']};
    }}
    
    .card:hover {{
        box-shadow: {SHADOWS['lg']};
        transform: translateY(-2px);
        border-color: {COLORS['primary_light']};
    }}
    
    .card-clickable {{
        cursor: pointer;
    }}
    
    .card-clickable:active {{
        transform: translateY(0);
    }}
    
    /* Metric Card Styles */
    [data-testid="stMetricValue"] {{
        font-size: {TYPOGRAPHY['font_size_3xl']};
        font-weight: {TYPOGRAPHY['font_weight_bold']};
        color: {COLORS['primary']};
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: {TYPOGRAPHY['font_size_sm']};
        font-weight: {TYPOGRAPHY['font_weight_medium']};
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: {TYPOGRAPHY['letter_spacing_wide']};
    }}
    
    [data-testid="stMetricDelta"] {{
        font-size: {TYPOGRAPHY['font_size_sm']};
    }}
    
    /* Input Styles */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {{
        border-radius: {BORDER_RADIUS['md']};
        border: 1px solid {COLORS['border']};
        padding: {SPACING['sm']} {SPACING['md']};
        font-family: {TYPOGRAPHY['font_family_primary']};
        font-size: {TYPOGRAPHY['font_size_base']};
        transition: all {TRANSITIONS['fast']};
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {{
        border-color: {COLORS['primary']};
        outline: none;
        box-shadow: 0 0 0 3px {COLORS['primary_light']}33;
    }}
    
    /* Selectbox Styles */
    .stSelectbox > div > div {{
        border-radius: {BORDER_RADIUS['md']};
    }}
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {{
        background-color: {COLORS['background_secondary']};
        padding: {SPACING['lg']} {SPACING['md']};
    }}
    
    [data-testid="stSidebar"] .stButton > button {{
        background-color: transparent;
        color: {COLORS['text_primary']};
        border: none;
        box-shadow: none;
        text-align: left;
        padding: {SPACING['md']};
        border-radius: {BORDER_RADIUS['md']};
        margin-bottom: {SPACING['xs']};
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover {{
        background-color: {COLORS['card_hover']};
        transform: none;
    }}
    
    [data-testid="stSidebar"] .stButton.active > button {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_inverse']};
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
    }}
    
    /* Tabs Styles */
    .stTabs [data-baseweb="tab-list"] {{
        gap: {SPACING['sm']};
        border-bottom: 2px solid {COLORS['border']};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: {SPACING['sm']} {SPACING['lg']};
        font-weight: {TYPOGRAPHY['font_weight_medium']};
        color: {COLORS['text_secondary']};
        border-radius: {BORDER_RADIUS['md']} {BORDER_RADIUS['md']} 0 0;
        transition: all {TRANSITIONS['fast']};
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {COLORS['background_secondary']};
        color: {COLORS['text_primary']};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['primary']};
        color: {COLORS['text_inverse']} !important;
    }}
    
    /* Expander Styles */
    .streamlit-expanderHeader {{
        background-color: {COLORS['background_secondary']};
        border-radius: {BORDER_RADIUS['md']};
        padding: {SPACING['md']};
        font-weight: {TYPOGRAPHY['font_weight_medium']};
        transition: all {TRANSITIONS['fast']};
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {COLORS['background_tertiary']};
    }}
    
    /* Alert/Info Box Styles */
    .stAlert {{
        border-radius: {BORDER_RADIUS['md']};
        padding: {SPACING['md']};
        border-left: 4px solid;
    }}
    
    .stAlert[data-baseweb="notification"] {{
        background-color: {COLORS['background_secondary']};
    }}
    
    /* Success Alert */
    .stSuccess {{
        border-left-color: {COLORS['success']};
        background-color: {COLORS['success']}15;
    }}
    
    /* Warning Alert */
    .stWarning {{
        border-left-color: {COLORS['warning']};
        background-color: {COLORS['warning']}15;
    }}
    
    /* Error Alert */
    .stError {{
        border-left-color: {COLORS['error']};
        background-color: {COLORS['error']}15;
    }}
    
    /* Info Alert */
    .stInfo {{
        border-left-color: {COLORS['info']};
        background-color: {COLORS['info']}15;
    }}
    
    /* Dataframe Styles */
    .stDataFrame {{
        border-radius: {BORDER_RADIUS['md']};
        overflow: hidden;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div {{
        background-color: {COLORS['primary']};
        border-radius: {BORDER_RADIUS['full']};
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {COLORS['primary']};
    }}
    
    /* Divider */
    hr {{
        border: none;
        border-top: 1px solid {COLORS['border']};
        margin: {SPACING['lg']} 0;
    }}
    
    /* Link Styles */
    a {{
        color: {COLORS['primary']};
        text-decoration: none;
        transition: color {TRANSITIONS['fast']};
    }}
    
    a:hover {{
        color: {COLORS['primary_dark']};
        text-decoration: underline;
    }}
    
    /* Code Block Styles */
    code {{
        background-color: {COLORS['background_secondary']};
        padding: {SPACING['xs']} {SPACING['sm']};
        border-radius: {BORDER_RADIUS['sm']};
        font-family: {TYPOGRAPHY['font_family_mono']};
        font-size: {TYPOGRAPHY['font_size_sm']};
        color: {COLORS['accent']};
    }}
    
    pre {{
        background-color: {COLORS['background_secondary']};
        padding: {SPACING['md']};
        border-radius: {BORDER_RADIUS['md']};
        overflow-x: auto;
    }}
    
    /* Responsive Design - Enhanced */
    
    /* Prevent horizontal scrolling */
    html, body {{
        overflow-x: hidden;
        max-width: 100vw;
    }}
    
    .main {{
        max-width: 100%;
        overflow-x: hidden;
    }}
    
    /* Responsive containers */
    [data-testid="stHorizontalBlock"] {{
        flex-wrap: wrap;
        gap: {SPACING['md']};
    }}
    
    /* Responsive columns */
    [data-testid="column"] {{
        min-width: 0;
        flex-shrink: 1;
    }}
    
    /* Tablet breakpoint (768px and below) */
    @media (max-width: {BREAKPOINTS['tablet']}) {{
        .main {{
            padding: {SPACING['md']};
        }}
        
        /* Adjust card padding */
        .card {{
            padding: {SPACING['md']};
            margin-bottom: {SPACING['sm']};
        }}
        
        /* Adjust metric sizes */
        [data-testid="stMetricValue"] {{
            font-size: clamp({TYPOGRAPHY['font_size_xl']}, 3vw, {TYPOGRAPHY['font_size_2xl']});
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: {TYPOGRAPHY['font_size_xs']};
        }}
        
        /* Stack columns on tablet */
        [data-testid="column"] {{
            width: 100% !important;
            flex: 1 1 100% !important;
        }}
        
        /* Adjust button sizes */
        .stButton > button {{
            padding: {SPACING['sm']} {SPACING['md']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Sidebar adjustments */
        [data-testid="stSidebar"] {{
            padding: {SPACING['md']} {SPACING['sm']};
        }}
        
        /* Reduce spacing */
        .mt-lg {{ margin-top: {SPACING['md']}; }}
        .mb-lg {{ margin-bottom: {SPACING['md']}; }}
        .p-lg {{ padding: {SPACING['md']}; }}
    }}
    
    /* Mobile breakpoint (640px and below) */
    @media (max-width: {BREAKPOINTS['mobile']}) {{
        .main {{
            padding: {SPACING['sm']};
        }}
        
        /* Further reduce card padding */
        .card {{
            padding: {SPACING['sm']};
            margin-bottom: {SPACING['xs']};
        }}
        
        /* Smaller buttons */
        .stButton > button {{
            padding: {SPACING['xs']} {SPACING['sm']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Compact metrics */
        [data-testid="stMetricValue"] {{
            font-size: clamp({TYPOGRAPHY['font_size_lg']}, 4vw, {TYPOGRAPHY['font_size_xl']});
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: {TYPOGRAPHY['font_size_xs']};
        }}
        
        /* Compact sidebar */
        [data-testid="stSidebar"] {{
            padding: {SPACING['sm']} {SPACING['xs']};
        }}
        
        [data-testid="stSidebar"] .stButton > button {{
            padding: {SPACING['xs']} {SPACING['sm']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Reduce icon sizes */
        .icon {{
            width: 1.25rem;
            height: 1.25rem;
        }}
        
        .icon-lg {{
            width: 2rem;
            height: 2rem;
        }}
        
        .icon-xl {{
            width: 3rem;
            height: 3rem;
        }}
        
        /* Compact spacing */
        .mt-md {{ margin-top: {SPACING['sm']}; }}
        .mt-lg {{ margin-top: {SPACING['md']}; }}
        .mb-md {{ margin-bottom: {SPACING['sm']}; }}
        .mb-lg {{ margin-bottom: {SPACING['md']}; }}
        .p-md {{ padding: {SPACING['sm']}; }}
        .p-lg {{ padding: {SPACING['md']}; }}
        
        /* Adjust input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {{
            padding: {SPACING['xs']} {SPACING['sm']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Compact tabs */
        .stTabs [data-baseweb="tab"] {{
            padding: {SPACING['xs']} {SPACING['sm']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Compact expander */
        .streamlit-expanderHeader {{
            padding: {SPACING['sm']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Compact alerts */
        .stAlert {{
            padding: {SPACING['sm']};
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
        
        /* Compact empty state */
        .empty-state {{
            padding: {SPACING['xl']} {SPACING['sm']};
        }}
        
        .empty-state-icon {{
            font-size: {TYPOGRAPHY['font_size_3xl']};
        }}
        
        .empty-state-title {{
            font-size: {TYPOGRAPHY['font_size_lg']};
        }}
        
        .empty-state-description {{
            font-size: {TYPOGRAPHY['font_size_sm']};
        }}
    }}
    
    /* Large desktop breakpoint (1280px and above) */
    @media (min-width: {BREAKPOINTS['wide']}) {{
        .main {{
            max-width: 1400px;
            margin: 0 auto;
        }}
    }}
    
    /* Responsive images and media */
    img, video {{
        max-width: 100%;
        height: auto;
    }}
    
    /* Responsive tables */
    .stDataFrame {{
        overflow-x: auto;
        max-width: 100%;
    }}
    
    /* Responsive charts - ensure they fit container */
    .js-plotly-plot {{
        width: 100% !important;
    }}
    
    .plotly {{
        width: 100% !important;
    }}
    
    /* Mobile navigation enhancements */
    @media (max-width: {BREAKPOINTS['mobile']}) {{
        /* Collapsible sidebar on mobile */
        [data-testid="stSidebar"][aria-expanded="false"] {{
            display: none;
        }}
        
        /* Hamburger menu button styling */
        [data-testid="collapsedControl"] {{
            background-color: {COLORS['primary']};
            color: {COLORS['text_inverse']};
            border-radius: {BORDER_RADIUS['md']};
            padding: {SPACING['sm']};
        }}
    }}
    
    /* Custom Utility Classes */
    .text-center {{
        text-align: center;
    }}
    
    .text-right {{
        text-align: right;
    }}
    
    .mt-sm {{ margin-top: {SPACING['sm']}; }}
    .mt-md {{ margin-top: {SPACING['md']}; }}
    .mt-lg {{ margin-top: {SPACING['lg']}; }}
    
    .mb-sm {{ margin-bottom: {SPACING['sm']}; }}
    .mb-md {{ margin-bottom: {SPACING['md']}; }}
    .mb-lg {{ margin-bottom: {SPACING['lg']}; }}
    
    .p-sm {{ padding: {SPACING['sm']}; }}
    .p-md {{ padding: {SPACING['md']}; }}
    .p-lg {{ padding: {SPACING['lg']}; }}
    
    /* Icon Styles */
    .icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 1.5rem;
        height: 1.5rem;
        margin-right: {SPACING['sm']};
    }}
    
    .icon-lg {{
        width: 2.5rem;
        height: 2.5rem;
    }}
    
    .icon-xl {{
        width: 4rem;
        height: 4rem;
    }}
    
    /* Empty State Styles */
    .empty-state {{
        text-align: center;
        padding: {SPACING['4xl']} {SPACING['lg']};
        color: {COLORS['text_tertiary']};
    }}
    
    .empty-state-icon {{
        font-size: {TYPOGRAPHY['font_size_5xl']};
        margin-bottom: {SPACING['lg']};
        opacity: 0.5;
    }}
    
    .empty-state-title {{
        font-size: {TYPOGRAPHY['font_size_xl']};
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        color: {COLORS['text_secondary']};
        margin-bottom: {SPACING['sm']};
    }}
    
    .empty-state-description {{
        font-size: {TYPOGRAPHY['font_size_base']};
        color: {COLORS['text_tertiary']};
    }}
    
    /* Loading State */
    .loading-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: {SPACING['3xl']};
    }}
    
    /* Badge Styles */
    .badge {{
        display: inline-block;
        padding: {SPACING['xs']} {SPACING['sm']};
        border-radius: {BORDER_RADIUS['full']};
        font-size: {TYPOGRAPHY['font_size_xs']};
        font-weight: {TYPOGRAPHY['font_weight_semibold']};
        text-transform: uppercase;
        letter-spacing: {TYPOGRAPHY['letter_spacing_wide']};
    }}
    
    .badge-success {{
        background-color: {COLORS['success']}20;
        color: {COLORS['success']};
    }}
    
    .badge-warning {{
        background-color: {COLORS['warning']}20;
        color: {COLORS['warning']};
    }}
    
    .badge-error {{
        background-color: {COLORS['error']}20;
        color: {COLORS['error']};
    }}
    
    .badge-info {{
        background-color: {COLORS['info']}20;
        color: {COLORS['info']};
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
