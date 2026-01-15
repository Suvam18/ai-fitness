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
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced CSS
    st.markdown("""
    <style>
        .main { padding: 2rem 1rem; }
        .block-container { padding-top: 2rem; max-width: 1400px; }
        h1 { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: clamp(2rem, 5vw, 3rem);
            font-weight: 700;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .subtitle { text-align: center; color: #666; margin-bottom: 2rem; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; }
        section[data-testid="stSidebar"] { background-color: #f8f9fa; }
        @media (max-width: 768px) { .block-container { padding: 1rem; } }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🏋️ AI Fitness Trainer")
    st.markdown('<p class="subtitle">Real-time exercise form analysis using computer vision</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'camera_on' not in st.session_state:
        st.session_state.camera_on = False
    if 'rep_count' not in st.session_state:
        st.session_state.rep_count = 0
    
    # Sidebar with improved layout
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        st.markdown("")
        
        exercise = st.selectbox(
            "Choose Exercise",
            ["Bicep Curls", "Squats", "Push-ups", "Shoulder Press"],
            help="Select your workout exercise"
        )
        
        st.slider("Target Reps", 5, 20, 10, key="target_reps", help="Set your rep goal")
        
        st.markdown("---")
        st.markdown("### 🎬 Controls")
        st.markdown("")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start" if not st.session_state.camera_on else "⏹️ Stop", use_container_width=True):
                st.session_state.camera_on = not st.session_state.camera_on
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.rep_count = 0
        
        st.markdown("---")
        st.markdown("### 📊 Stats")
        st.markdown("")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Completed", st.session_state.rep_count)
        with col_b:
            st.metric("Target", st.session_state.target_reps)
        
        # Progress bar with label
        progress = min(st.session_state.rep_count / st.session_state.target_reps, 1.0)
        st.progress(progress)
        st.caption(f"Progress: {progress*100:.0f}%")
    
    # Main area with better spacing
    col1, col2 = st.columns([2.5, 1.5], gap="large")
    
    with col1:
        st.markdown("### 📹 Live Feed")
        st.markdown("")
        
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
            st.info("👆 Click 'Start' to begin your workout")
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 150px 20px; border-radius: 12px; text-align: center; color: white;">
                <h2 style="margin: 0; color: white;">🎥 Camera Feed</h2>
                <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9);">Will appear here</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 💡 Form Guide")
        st.markdown("")
        
        if exercise == "Bicep Curls":
            st.info("""
            **Bicep Curl Form:**
            
            ✓ Keep elbows close to body  
            ✓ Fully extend at bottom  
            ✓ Control the movement  
            ✓ Don't swing torso
            """)
            
            # Simulate form detection
            st.markdown("")
            st.markdown("#### 🔍 Form Check")
            col_a, col_b = st.columns(2)
            with col_a:
                st.success("✅ Elbow")
                st.warning("⚠️ Extension")
            with col_b:
                st.success("✅ Wrist")
                st.error("❌ Sway")
                
        elif exercise == "Squats":
            st.info("""
            **Squat Form:**
            
            ✓ Feet shoulder-width apart  
            ✓ Knees aligned with toes  
            ✓ Back straight  
            ✓ Go to parallel
            """)
        
        elif exercise == "Push-ups":
            st.info("""
            **Push-up Form:**
            
            ✓ Keep body straight  
            ✓ Elbows at 45°  
            ✓ Full range of motion  
            ✓ Engage core
            """)
            
        st.markdown("")
        st.markdown("#### 🎯 Quick Tips")
        st.markdown("""
        • Warm up before starting  
        • Maintain proper form  
        • Breathe consistently  
        • Stay hydrated
        """)

if __name__ == "__main__":
    main()