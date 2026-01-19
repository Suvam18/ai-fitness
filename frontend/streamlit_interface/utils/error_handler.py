"""
Error Handler Utility
Provides centralized error handling and user-friendly error messages
"""
import streamlit as st
from typing import Optional, Callable, Any
import logging

from styles.theme import COLORS, TYPOGRAPHY, SPACING, BORDER_RADIUS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorHandler:
    """Centralized error handling for the application"""
    
    @staticmethod
    def render_error_message(
        title: str,
        message: str,
        icon: str = "error_outline",
        error_type: str = "error",
        show_retry: bool = False,
        retry_callback: Optional[Callable] = None
    ) -> None:
        """
        Render a user-friendly error message with optional retry button
        
        Args:
            title: Error title
            message: Detailed error message
            icon: Material icon name
            error_type: Type of error (error, warning, info)
            show_retry: Whether to show retry button
            retry_callback: Function to call when retry is clicked
        """
        # Determine color based on error type
        color_map = {
            'error': COLORS['error'],
            'warning': COLORS['warning'],
            'info': COLORS['info'],
        }
        color = color_map.get(error_type, COLORS['error'])
        
        st.markdown(
            f"""
            <div style="
                background-color: {color}15;
                border-left: 4px solid {color};
                border-radius: {BORDER_RADIUS['md']};
                padding: {SPACING['lg']};
                margin: {SPACING['xl']} 0;
            ">
                <div style="
                    display: flex;
                    align-items: start;
                    gap: {SPACING['md']};
                ">
                    <span class="material-icons" style="
                        font-size: 32px;
                        color: {color};
                        flex-shrink: 0;
                    ">{icon}</span>
                    <div style="flex-grow: 1;">
                        <h3 style="
                            font-family: {TYPOGRAPHY['font_family_primary']};
                            font-size: {TYPOGRAPHY['font_size_lg']};
                            font-weight: {TYPOGRAPHY['font_weight_semibold']};
                            color: {COLORS['text_primary']};
                            margin: 0 0 {SPACING['sm']} 0;
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
                            {message}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if show_retry and retry_callback:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔄 Retry", use_container_width=True):
                    retry_callback()
    
    @staticmethod
    def render_data_load_error(error_info: dict) -> None:
        """
        Render error message for data loading failures
        
        Args:
            error_info: Dictionary with error details
        """
        if not error_info.get('directory_exists'):
            ErrorHandler.render_error_message(
                title="Data Directory Not Found",
                message="The workout data directory does not exist yet. Complete your first workout to create it.",
                icon="folder_off",
                error_type="info"
            )
        elif not error_info.get('is_directory'):
            ErrorHandler.render_error_message(
                title="Invalid Data Path",
                message="The workout data path exists but is not a directory. Please check your configuration.",
                icon="error",
                error_type="error"
            )
        elif not error_info.get('has_permission'):
            ErrorHandler.render_error_message(
                title="Permission Denied",
                message="Unable to access the workout data directory due to insufficient permissions. Please check file permissions.",
                icon="lock",
                error_type="error"
            )
        else:
            ErrorHandler.render_error_message(
                title="Data Loading Error",
                message="An unexpected error occurred while loading workout data. Please try refreshing the page.",
                icon="error_outline",
                error_type="error",
                show_retry=True,
                retry_callback=lambda: st.rerun()
            )
    
    @staticmethod
    def render_api_error(error_context: str = "API request") -> None:
        """
        Render error message for API communication failures
        
        Args:
            error_context: Context of the API call that failed
        """
        ErrorHandler.render_error_message(
            title="Backend Communication Error",
            message=f"Failed to communicate with the backend service during {error_context}. "
                   "Please ensure the FastAPI backend is running and try again.",
            icon="cloud_off",
            error_type="error",
            show_retry=True,
            retry_callback=lambda: st.rerun()
        )
    
    @staticmethod
    def render_camera_error(error_message: str) -> None:
        """
        Render error message for camera access issues
        
        Args:
            error_message: Specific error message from camera
        """
        ErrorHandler.render_error_message(
            title="Camera Access Error",
            message=f"Unable to access your camera: {error_message}. "
                   "Please ensure camera permissions are granted and no other application is using the camera.",
            icon="videocam_off",
            error_type="error"
        )
        
        # Add troubleshooting tips
        st.markdown(
            f"""
            <div style="
                background-color: {COLORS['info']}10;
                border-radius: {BORDER_RADIUS['md']};
                padding: {SPACING['md']};
                margin-top: {SPACING['md']};
            ">
                <h4 style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_base']};
                    font-weight: {TYPOGRAPHY['font_weight_semibold']};
                    color: {COLORS['text_primary']};
                    margin: 0 0 {SPACING['sm']} 0;
                ">
                    💡 Troubleshooting Tips:
                </h4>
                <ul style="
                    font-family: {TYPOGRAPHY['font_family_primary']};
                    font-size: {TYPOGRAPHY['font_size_sm']};
                    color: {COLORS['text_secondary']};
                    line-height: {TYPOGRAPHY['line_height_relaxed']};
                    margin: 0;
                    padding-left: {SPACING['lg']};
                ">
                    <li>Check that your browser has permission to access the camera</li>
                    <li>Close other applications that might be using the camera</li>
                    <li>Try refreshing the page and granting camera access when prompted</li>
                    <li>Ensure your camera is properly connected (for external cameras)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    @staticmethod
    def render_session_error(operation: str) -> None:
        """
        Render error message for session operation failures
        
        Args:
            operation: The operation that failed (e.g., "start", "end")
        """
        ErrorHandler.render_error_message(
            title=f"Session {operation.title()} Failed",
            message=f"Unable to {operation} the workout session. This may be due to a backend connection issue. "
                   "Please check that the backend is running and try again.",
            icon="error",
            error_type="error",
            show_retry=True,
            retry_callback=lambda: st.rerun()
        )
    
    @staticmethod
    def render_corrupted_data_warning(count: int) -> None:
        """
        Render warning message for corrupted data files
        
        Args:
            count: Number of corrupted files
        """
        if count > 0:
            st.warning(
                f"⚠️ {count} workout file{'s' if count != 1 else ''} could not be loaded due to corruption or invalid format. "
                "These files have been skipped.",
                icon="⚠️"
            )
    
    @staticmethod
    def handle_exception(
        exception: Exception,
        context: str,
        show_to_user: bool = True,
        fallback_message: Optional[str] = None
    ) -> None:
        """
        Handle an exception with logging and optional user notification
        
        Args:
            exception: The exception that occurred
            context: Context where the exception occurred
            show_to_user: Whether to show error to user
            fallback_message: Custom message to show user
        """
        # Log the exception
        logger.error(f"Exception in {context}: {str(exception)}", exc_info=True)
        
        # Show to user if requested
        if show_to_user:
            message = fallback_message or f"An error occurred: {str(exception)}"
            ErrorHandler.render_error_message(
                title="Unexpected Error",
                message=message,
                icon="error",
                error_type="error"
            )
    
    @staticmethod
    def safe_execute(
        func: Callable,
        context: str,
        fallback_value: Any = None,
        show_error: bool = True
    ) -> Any:
        """
        Safely execute a function with error handling
        
        Args:
            func: Function to execute
            context: Context description for logging
            fallback_value: Value to return on error
            show_error: Whether to show error to user
            
        Returns:
            Function result or fallback value on error
        """
        try:
            return func()
        except Exception as e:
            ErrorHandler.handle_exception(
                e,
                context,
                show_to_user=show_error
            )
            return fallback_value
