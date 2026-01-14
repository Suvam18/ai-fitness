"""
Simple Web Interface for AI Fitness Trainer
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

def main():
    st.set_page_config(
        page_title="AI Fitness Trainer",
        page_icon="🏋️",
        layout="wide"
    )
    
    st.title("🏋️ AI Fitness Trainer")
    st.markdown("Real-time exercise form analysis using computer vision")
    
    # Initialize session state
    if 'camera_on' not in st.session_state:
        st.session_state.camera_on = False
    if 'rep_count' not in st.session_state:
        st.session_state.rep_count = 0
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        exercise = st.selectbox(
            "Choose Exercise",
            ["Bicep Curls", "Squats", "Push-ups", "Shoulder Press"]
        )
        
        st.slider("Target Reps", 5, 20, 10, key="target_reps")
        
        if st.button("🎥 Start Camera" if not st.session_state.camera_on else "🛑 Stop Camera"):
            st.session_state.camera_on = not st.session_state.camera_on
            
        if st.button("🔄 Reset Counter"):
            st.session_state.rep_count = 0
            
        st.header("Stats")
        st.metric("Reps Completed", st.session_state.rep_count)
        st.metric("Progress", f"{st.session_state.rep_count}/{st.session_state.target_reps}")
        
        # Progress bar
        progress = min(st.session_state.rep_count / st.session_state.target_reps, 1.0)
        st.progress(progress)
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Live Feed")
        
        if st.session_state.camera_on:
            # Camera placeholder
            camera_placeholder = st.empty()
            
            # Start camera
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Could not access camera. Please check if it's being used by another application.")
            else:
                st.success("✅ Camera connected successfully!")
                
                # Simple exercise simulation (since we can't run MediaPipe in this simplified version)
                while st.session_state.camera_on and cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        st.error("Failed to capture frame")
                        break
                    
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Add workout overlay
                    cv2.putText(frame_rgb, f"Exercise: {exercise}", (50, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(frame_rgb, f"Reps: {st.session_state.rep_count}", (50, 100), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame_rgb, "Placeholder - Desktop version has full AI", (50, 150), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
                    # Display frame
                    camera_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                    
                    # Simulate rep counting (in real app, this would come from pose detection)
                    time.sleep(0.1)
                
                cap.release()
        else:
            st.info("👆 Click 'Start Camera' to begin your workout")
            st.image("https://via.placeholder.com/600x400/667eea/ffffff?text=Camera+Feed+Will+Appear+Here", 
                    use_column_width=True)
    
    with col2:
        st.header("Form Guide")
        
        if exercise == "Bicep Curls":
            st.info("""
            **💡 Bicep Curl Form:**
            - Keep elbows close to body
            - Fully extend at bottom
            - Control the movement
            - Don't swing torso
            """)
            
            # Simulate form detection
            st.subheader("Form Check")
            col_a, col_b = st.columns(2)
            with col_a:
                st.success("✅ Elbow Position")
                st.warning("⚠️ Arm Extension")
            with col_b:
                st.success("✅ Wrist Stability")
                st.error("❌ Body Sway")
                
        elif exercise == "Squats":
            st.info("""
            **💡 Squat Form:**
            - Feet shoulder-width apart
            - Knees aligned with toes
            - Back straight
            - Go to parallel
            """)
            
        st.header("Workout Tips")
        st.write("• Warm up before starting")
        st.write("• Maintain proper form")
        st.write("• Breathe consistently")
        st.write("• Stay hydrated")

if __name__ == "__main__":
    main()