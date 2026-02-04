"""
Reusable page styling components for the AI Fitness Trainer Streamlit application.

This module provides consistent styling functions that can be used across all pages
to ensure uniform appearance and behavior. It centralizes common styling patterns
to reduce code duplication and maintain consistency.
"""

from .theme import COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS


def get_page_header_style(
    title: str,
    subtitle: str,
    center: bool = True
) -> str:
    """
    Generate consistent page header HTML with styling.
    
    Args:
        title: Main page title
        subtitle: Subtitle or description text
        center: Whether to center-align the header
        
    Returns:
        HTML string for the page header
    """
    text_align = "center" if center else "left"
    max_width = "max-width: 600px; margin: 0 auto;" if center else ""
    
    return f"""
    <div style="
        text-align: {text_align};
        padding: {SPACING['2xl']} {SPACING['lg']} {SPACING['xl']};
        margin-bottom: {SPACING['xl']};
    ">
        <h1 style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_4xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
            color: {COLORS['text_primary']};
            line-height: {TYPOGRAPHY['line_height_tight']};
            margin-bottom: {SPACING['sm']};
            letter-spacing: {TYPOGRAPHY['letter_spacing_tight']};
        ">
            {title}
        </h1>
        <p style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_lg']};
            font-weight: {TYPOGRAPHY['font_weight_normal']};
            color: {COLORS['text_secondary']};
            line-height: {TYPOGRAPHY['line_height_relaxed']};
            {max_width}
        ">
            {subtitle}
        </p>
    </div>
    """


def get_section_header_style(
    title: str,
    subtitle: str = "",
    margin_top: str = SPACING['2xl']
) -> str:
    """
    Generate consistent section header HTML with styling.
    
    Args:
        title: Section title
        subtitle: Optional subtitle text
        margin_top: Top margin spacing
        
    Returns:
        HTML string for the section header
    """
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_base']};
            color: {COLORS['text_secondary']};
            margin-bottom: {SPACING['lg']};
        ">
            {subtitle}
        </p>
        """
    
    return f"""
    <div style="
        margin-bottom: {SPACING['lg']};
        margin-top: {margin_top};
    ">
        <h2 style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_2xl']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['md']};
        ">
            {title}
        </h2>
        {subtitle_html}
    </div>
    """


def get_metric_card_style(
    icon: str,
    value: str,
    label: str,
    icon_color: str,
    card_class: str = "metric-card"
) -> str:
    """
    Generate consistent metric card HTML with styling.
    
    Args:
        icon: Material icon name
        value: Metric value to display
        label: Metric label
        icon_color: Color for the icon
        card_class: CSS class for the card
        
    Returns:
        HTML string for the metric card
    """
    return f"""
    <div style="
        background-color: {COLORS['card_background']};
        border-radius: {BORDER_RADIUS['lg']};
        padding: {SPACING['xl']};
        box-shadow: {SHADOWS['md']};
        border: 2px solid {COLORS['border']};
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    " class="{card_class}">
        <div style="
            display: flex;
            justify-content: center;
            margin-bottom: {SPACING['md']};
        ">
            <span class="material-icons" style="
                font-size: 48px;
                color: {icon_color};
            ">{icon}</span>
        </div>
        <div style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_4xl']};
            font-weight: {TYPOGRAPHY['font_weight_bold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['sm']};
            line-height: 1;
        ">
            {value}
        </div>
        <div style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_sm']};
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: {TYPOGRAPHY['font_weight_medium']};
        ">
            {label}
        </div>
    </div>
    """


def get_feature_card_style(
    icon: str,
    title: str,
    description: str,
    icon_color: str = COLORS['primary']
) -> str:
    """
    Generate consistent feature card HTML with styling.
    
    Args:
        icon: Material icon name
        title: Feature title
        description: Feature description
        icon_color: Color for the icon
        
    Returns:
        HTML string for the feature card
    """
    return f"""
    <div style="
        background-color: {COLORS['card_background']};
        border-radius: {BORDER_RADIUS['lg']};
        padding: {SPACING['xl']};
        box-shadow: {SHADOWS['md']};
        border: 1px solid {COLORS['border']};
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    ">
        <div style="
            display: flex;
            justify-content: center;
            margin-bottom: {SPACING['lg']};
        ">
            <span class="material-icons" style="
                font-size: 48px;
                color: {icon_color};
            ">{icon}</span>
        </div>
        <h3 style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_xl']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['sm']};
        ">
            {title}
        </h3>
        <p style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_base']};
            color: {COLORS['text_secondary']};
            line-height: {TYPOGRAPHY['line_height_relaxed']};
            margin: 0;
        ">
            {description}
        </p>
    </div>
    """


def get_exercise_card_style(
    icon: str,
    title: str,
    description: str,
    icon_color: str
) -> str:
    """
    Generate consistent exercise selection card HTML with styling.
    
    Args:
        icon: Material icon name
        title: Exercise name
        description: Exercise description
        icon_color: Color for the icon
        
    Returns:
        HTML string for the exercise card
    """
    return f"""
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
                color: {icon_color};
            ">{icon}</span>
        </div>
        <h3 style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_2xl']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['text_primary']};
            margin-bottom: {SPACING['sm']};
        ">
            {title}
        </h3>
        <p style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_base']};
            color: {COLORS['text_secondary']};
            line-height: {TYPOGRAPHY['line_height_relaxed']};
            margin-bottom: {SPACING['lg']};
        ">
            {description}
        </p>
    </div>
    """


def get_empty_state_style(
    icon: str,
    title: str,
    description: str
) -> str:
    """
    Generate consistent empty state HTML with styling.
    
    Args:
        icon: Material icon name
        title: Empty state title
        description: Empty state description
        
    Returns:
        HTML string for the empty state
    """
    return f"""
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
            ">{icon}</span>
        </div>
        <h3 style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_2xl']};
            font-weight: {TYPOGRAPHY['font_weight_semibold']};
            color: {COLORS['text_secondary']};
            margin-bottom: {SPACING['md']};
        ">
            {title}
        </h3>
        <p style="
            font-family: {TYPOGRAPHY['font_family_primary']};
            font-size: {TYPOGRAPHY['font_size_base']};
            color: {COLORS['text_tertiary']};
            line-height: {TYPOGRAPHY['line_height_relaxed']};
            max-width: 500px;
            margin: 0 auto {SPACING['xl']} auto;
        ">
            {description}
        </p>
    </div>
    """


def get_footer_style(text: str) -> str:
    """
    Generate consistent footer HTML with styling.
    
    Args:
        text: Footer text content
        
    Returns:
        HTML string for the footer
    """
    return f"""
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
            {text}
        </p>
    </div>
    """


def get_divider_style(margin: str = SPACING['3xl']) -> str:
    """
    Generate consistent divider HTML with styling.
    
    Args:
        margin: Vertical margin spacing
        
    Returns:
        HTML string for the divider
    """
    return f"""
    <div style="margin: {margin} 0;">
        <hr style="
            border: none;
            border-top: 1px solid {COLORS['border']};
        ">
    </div>
    """


def get_alert_style(
    message: str,
    alert_type: str = "info",
    icon: str = None
) -> str:
    """
    Generate consistent alert/notification HTML with styling.
    
    Args:
        message: Alert message text
        alert_type: Type of alert ('success', 'warning', 'error', 'info')
        icon: Optional custom icon name
        
    Returns:
        HTML string for the alert
    """
    # Map alert types to colors and default icons
    alert_config = {
        "success": {"color": COLORS['success'], "icon": "check_circle"},
        "warning": {"color": COLORS['warning'], "icon": "warning"},
        "error": {"color": COLORS['error'], "icon": "error"},
        "info": {"color": COLORS['info'], "icon": "info"},
    }
    
    config = alert_config.get(alert_type, alert_config["info"])
    icon_name = icon or config["icon"]
    color = config["color"]
    
    return f"""
    <div style="
        background-color: {color}15;
        border-left: 4px solid {color};
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
                color: {color};
            ">{icon_name}</span>
            <span style="
                font-family: {TYPOGRAPHY['font_family_primary']};
                font-size: {TYPOGRAPHY['font_size_base']};
                color: {COLORS['text_primary']};
            ">
                {message}
            </span>
        </div>
    </div>
    """


def inject_card_hover_styles() -> str:
    """
    Generate CSS for consistent card hover effects.
    
    Returns:
        CSS string for card hover styles
    """
    return f"""
    <style>
    .exercise-card:hover {{
        transform: translateY(-5px);
        box-shadow: {SHADOWS['lg']};
        border-color: {COLORS['primary']};
    }}
    
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: {SHADOWS['lg']};
        border-color: {COLORS['primary_light']};
    }}
    
    .session-card:hover {{
        transform: translateY(-2px);
        box-shadow: {SHADOWS['lg']};
        border-color: {COLORS['primary_light']};
    }}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .exercise-card,
        .metric-card,
        .session-card {{
            margin-bottom: {SPACING['lg']};
        }}
        
        .metric-card,
        .session-card {{
            padding: {SPACING['md']};
        }}
    }}
    
    @media (max-width: 640px) {{
        .exercise-card,
        .metric-card,
        .session-card {{
            padding: {SPACING['sm']};
        }}
    }}
    </style>
    """
