"""
Responsive design utilities for the AI Fitness Trainer Streamlit application.

This module provides helper functions for creating responsive layouts and
handling different viewport sizes.
"""

import streamlit as st
from typing import Tuple, List


def get_responsive_columns(
    num_columns: int,
    mobile_columns: int = 1,
    tablet_columns: int = 2
) -> Tuple[int, int, int]:
    """
    Get responsive column configuration based on viewport size.
    
    Args:
        num_columns: Number of columns for desktop
        mobile_columns: Number of columns for mobile (default: 1)
        tablet_columns: Number of columns for tablet (default: 2)
        
    Returns:
        Tuple of (desktop_cols, tablet_cols, mobile_cols)
    """
    return (num_columns, tablet_columns, mobile_columns)


def create_responsive_columns(
    desktop_cols: int = 3,
    tablet_cols: int = 2,
    mobile_cols: int = 1
) -> List:
    """
    Create responsive columns that adapt to viewport size.
    
    Note: Streamlit doesn't support dynamic column counts based on viewport,
    so this creates columns optimized for desktop with CSS handling responsiveness.
    
    Args:
        desktop_cols: Number of columns for desktop
        tablet_cols: Number of columns for tablet
        mobile_cols: Number of columns for mobile
        
    Returns:
        List of Streamlit column objects
    """
    # Create columns for desktop layout
    # CSS media queries will handle stacking on smaller screens
    return st.columns(desktop_cols)


def inject_responsive_container_css() -> None:
    """
    Inject CSS for responsive container behavior.
    
    Ensures containers adapt properly to different viewport sizes.
    """
    st.markdown(
        """
        <style>
        /* Responsive container utilities */
        .responsive-container {
            width: 100%;
            max-width: 100%;
            padding: 0 1rem;
            margin: 0 auto;
        }
        
        @media (min-width: 640px) {
            .responsive-container {
                max-width: 640px;
            }
        }
        
        @media (min-width: 768px) {
            .responsive-container {
                max-width: 768px;
            }
        }
        
        @media (min-width: 1024px) {
            .responsive-container {
                max-width: 1024px;
            }
        }
        
        @media (min-width: 1280px) {
            .responsive-container {
                max-width: 1280px;
            }
        }
        
        /* Responsive grid */
        .responsive-grid {
            display: grid;
            gap: 1rem;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
        
        @media (max-width: 640px) {
            .responsive-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Responsive flex */
        .responsive-flex {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .responsive-flex > * {
            flex: 1 1 300px;
        }
        
        @media (max-width: 640px) {
            .responsive-flex {
                flex-direction: column;
            }
            
            .responsive-flex > * {
                flex: 1 1 100%;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def get_chart_height(
    desktop_height: int = 400,
    tablet_height: int = 350,
    mobile_height: int = 300
) -> int:
    """
    Get responsive chart height based on viewport.
    
    Note: Since we can't detect viewport size in Streamlit server-side,
    this returns the desktop height. CSS will handle chart responsiveness.
    
    Args:
        desktop_height: Height for desktop viewports
        tablet_height: Height for tablet viewports
        mobile_height: Height for mobile viewports
        
    Returns:
        Chart height in pixels
    """
    # Return desktop height as default
    # Plotly's autosize will handle responsiveness
    return desktop_height


def inject_responsive_chart_css() -> None:
    """
    Inject CSS to ensure charts are responsive.
    
    Makes Plotly charts scale properly to container width.
    """
    st.markdown(
        """
        <style>
        /* Ensure charts are responsive */
        .js-plotly-plot,
        .plotly,
        .plotly-graph-div {
            width: 100% !important;
        }
        
        /* Responsive chart container */
        .chart-container {
            width: 100%;
            max-width: 100%;
            overflow-x: auto;
        }
        
        @media (max-width: 768px) {
            .js-plotly-plot .plotly .modebar {
                display: none !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def add_viewport_meta_tag() -> None:
    """
    Add viewport meta tag for proper mobile rendering.
    
    Note: Streamlit handles this automatically, but this function
    is provided for completeness.
    """
    st.markdown(
        """
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        """,
        unsafe_allow_html=True
    )


def create_responsive_card(
    content: str,
    mobile_padding: str = "0.5rem",
    tablet_padding: str = "1rem",
    desktop_padding: str = "1.5rem"
) -> None:
    """
    Create a responsive card with adaptive padding.
    
    Args:
        content: HTML content for the card
        mobile_padding: Padding for mobile viewports
        tablet_padding: Padding for tablet viewports
        desktop_padding: Padding for desktop viewports
    """
    st.markdown(
        f"""
        <style>
        .responsive-card {{
            padding: {desktop_padding};
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            background-color: white;
            border: 1px solid #e5e7eb;
        }}
        
        @media (max-width: 768px) {{
            .responsive-card {{
                padding: {tablet_padding};
            }}
        }}
        
        @media (max-width: 640px) {{
            .responsive-card {{
                padding: {mobile_padding};
            }}
        }}
        </style>
        <div class="responsive-card">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


def inject_responsive_utilities() -> None:
    """
    Inject all responsive utility CSS at once.
    
    Call this function once per page to enable all responsive features.
    """
    inject_responsive_container_css()
    inject_responsive_chart_css()
