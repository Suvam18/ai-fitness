"""
Web Interface for AI Fitness Trainer
"""
import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="AI Fitness Trainer",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Responsive CSS (Restored from your original) ---
st.markdown("""
<style>
    /* Global Styles */
    * { box-sizing: border-box; }
    .main { padding: 2rem 1rem; }
    .block-container { padding-top: 2rem; max-width: 1400px; margin: 0 auto; }
    
    /* Typography */
    .main-header {
        font-size: clamp(1.5rem, 4vw, 3.5rem);
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0 0 1rem 0;
        padding: 0.5rem 0;
        line-height: 1.2;
    }
    
    /* Workout Selection Cards */
    .workout-card {
        background: #f8f9fa;
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #eee;
        text-align: center;
        transition: all 0.3s ease;
    }
    .workout-card:hover {
        transform: translateY(-5px);
        border-color: #764ba2;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    
    /* Metrics & Info Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .info-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class FitnessTrainer:
    def __init__(self, exercise):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.exercise = exercise
        self.rep_count = 0
        self.current_stage = "start"
        
    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba, bc = a - b, c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(np.clip(cosine_angle, -1, 1)))
    
    def analyze_frame(self, landmarks):
        if not landmarks: return {'rep_count': self.rep_count, 'errors': ['No pose detected']}
        l = landmarks
        errors = []
        
        # Select joints based on session type
        if self.exercise == "Bicep Curls" or self.exercise == "Push-ups":
            p1, p2, p3 = [l[11].x, l[11].y], [l[13].x, l[13].y], [l[15].x, l[15].y]
        else: # Squats
            p1, p2, p3 = [l[23].x, l[23].y], [l[25].x, l[25].y], [l[27].x, l[27].y]

        angle = self.calculate_angle(p1, p2, p3)
        
        # Core Counting Logic
        if self.exercise == "Bicep Curls":
            if angle < 40: self.current_stage = "up"
            if angle > 160 and self.current_stage == "up":
                self.current_stage = "down"; self.rep_count += 1
            if abs(l[13].x - l[11].x) > 0.15: errors.append("Keep elbow close to body")
        elif self.exercise == "Squats":
            if angle < 100: self.current_stage = "down"
            if angle > 160 and self.current_stage == "down":
                self.current_stage = "up"; self.rep_count += 1
        else: # Push-ups
            if angle < 90: self.current_stage = "down"
            if angle > 160 and self.current_stage == "down":
                self.current_stage = "up"; self.rep_count += 1
                
        return {'rep_count': self.rep_count, 'stage': self.current_stage, 'angle': angle, 'errors': errors}

def main():
    st.markdown('<h1 class="main-header">🏋️ AI Fitness Trainer</h1>', unsafe_allow_html=True)

    # --- UI COMPONENT: WORKOUT SELECTION MENU (PRE-SESSION) ---
    if 'active_exercise' not in st.session_state:
        st.markdown("<h3 style='text-align: center;'>Pick your workout to start the session</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        workouts = [("💪 Bicep Curls", "Bicep Curls"), ("🦵 Squats", "Squats"), ("🏃 Push-ups", "Push-ups")]
        for i, (label, key) in enumerate(workouts):
            with [col1, col2, col3][i]:
                st.markdown('<div class="workout-card">', unsafe_allow_html=True)
                if st.button(label, key=f"btn_{key}", use_container_width=True):
                    st.session_state.active_exercise = key
                    st.session_state.session_start = datetime.now()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # --- MAIN SESSION DASHBOARD ---
    else:
        exercise = st.session_state.active_exercise
        
        with st.sidebar:
            st.markdown(f"### ⚙️ Mode: {exercise}")
            if st.button("🔄 Back to Menu"):
                del st.session_state.active_exercise
                st.rerun()
            st.markdown("---")
            target_reps = st.slider("Target Reps", 5, 20, 10)
            
            st.markdown("### 📹 Camera Controls")
            col_a, col_b = st.columns(2)
            start_camera = col_a.button("▶️ Start", use_container_width=True)
            stop_camera = col_b.button("⏹️ Stop", use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📊 Session Stats")
            current_reps = st.session_state.get('rep_count', 0)
            col1, col2 = st.columns(2)
            col1.metric("Current", current_reps)
            col2.metric("Target", target_reps)

        # Main Layout
        col_video, col_analytics = st.columns([2.5, 1.5], gap="medium")

        with col_video:
            st.markdown("### 📹 Live Camera Feed")
            video_placeholder = st.empty()
            feedback_placeholder = st.empty()
            
            if start_camera:
                cap = cv2.VideoCapture(0)
                trainer = FitnessTrainer(exercise)
                while cap.isOpened() and not stop_camera:
                    ret, frame = cap.read()
                    if not ret: break
                    
                    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    res = trainer.pose.process(img_rgb)
                    
                    if res.pose_landmarks:
                        mp.solutions.drawing_utils.draw_landmarks(frame, res.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                        analysis = trainer.analyze_frame(res.pose_landmarks.landmark)
                        st.session_state.rep_count = analysis['rep_count']
                        
                        # Overlays
                        cv2.putText(frame, f"Reps: {analysis['rep_count']}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        with feedback_placeholder.container():
                            if analysis.get('errors'):
                                for error in analysis['errors']: st.error(f"⚠️ {error}")
                    
                    video_placeholder.image(frame, channels="BGR", use_column_width=True)
                cap.release()

        with col_analytics:
            st.markdown("### 📈 Workout Analytics")
            reps = st.session_state.get('rep_count', 0)
            progress = min(reps / target_reps, 1.0)
            st.progress(progress)
            st.metric("Completion", f"{progress*100:.1f}%")

            # --- RESTORED FORM GUIDE ---
            st.markdown("### 💡 Form Guide")
            if exercise == "Bicep Curls":
                st.info("""
                        **Bicep Curl Tips:**
                        
                        ✓ Keep elbows close to body  
                        ✓ Fully extend arms at bottom  
                        ✓ Control the movement  
                        ✓ Avoid swinging torso
                    """)
            elif exercise == "Squats":
                st.info("""
                        **Squat Tips:**
                       
                        ✓ Knees aligned with feet  
                        ✓ Maintain straight back  
                        ✓ Go parallel to floor  
                        ✓ Push through heels
                    """)

            elif exercise == "Push-ups":
                st.info("""
                        **Push-up Tips:**
                        
                        ✓ Keep body straight  
                        ✓ Elbows at 45° angle  
                        ✓ Full range of motion  
                        ✓ Engage core muscles
                    """)
                st.markdown("")

        

            # --- RESTORED SUMMARY ---
            st.markdown("### ⏱️ Session Summary")
            duration = datetime.now() - st.session_state.session_start
            st.metric("Duration", f"{duration.seconds // 60}m {duration.seconds % 60}s")

if __name__ == "__main__":
    main()