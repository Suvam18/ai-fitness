"""
AI Fitness Trainer - Complete Working Version
"""
import cv2
import mediapipe as mp
import numpy as np
import time
import os
import json
from datetime import datetime

print("🚀 Initializing AI Fitness Trainer...")

# Configuration
class Config:
    CAMERA_WIDTH = 1280
    CAMERA_HEIGHT = 720
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.5
    SUPPORTED_EXERCISES = ["bicep_curl", "squat", "push_up"]

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=Config.MIN_TRACKING_CONFIDENCE
        )
        print("✅ Pose detector initialized")

    def detect_pose(self, image):
        try:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = self.pose.process(image_rgb)
            image_rgb.flags.writeable = True
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            
            landmarks = None
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                self.mp_drawing.draw_landmarks(
                    image_bgr,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
            
            return landmarks, image_bgr
        except Exception as e:
            print(f"❌ Pose detection error: {e}")
            return None, image

    def extract_key_points(self, landmarks):
        if not landmarks:
            return None
            
        key_points = {}
        landmark_indices = {
            'nose': 0, 'left_eye': 1, 'right_eye': 2,
            'left_shoulder': 11, 'right_shoulder': 12,
            'left_elbow': 13, 'right_elbow': 14,
            'left_wrist': 15, 'right_wrist': 16,
            'left_hip': 23, 'right_hip': 24,
            'left_knee': 25, 'right_knee': 26,
            'left_ankle': 27, 'right_ankle': 28,
        }
        
        for name, idx in landmark_indices.items():
            if idx < len(landmarks):
                landmark = landmarks[idx]
                key_points[name] = (landmark.x, landmark.y, landmark.visibility)
                
        return key_points

class ExerciseAnalyzer:
    def __init__(self, exercise_type="bicep_curl"):
        self.exercise_type = exercise_type
        self.rep_count = 0
        self.current_stage = "start"
        self.last_rep_time = time.time()
        print(f"✅ Exercise analyzer initialized for {exercise_type}")

    def calculate_angle(self, a, b, c):
        try:
            a = np.array(a)
            b = np.array(b)
            c = np.array(c)
            
            ba = a - b
            bc = c - b
            
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            cosine_angle = np.clip(cosine_angle, -1, 1)
            
            return np.degrees(np.arccos(cosine_angle))
        except:
            return 0

    def analyze_bicep_curl(self, key_points):
        feedback = []
        errors = []
        
        # Use right arm by default
        shoulder = key_points.get('right_shoulder', (0, 0, 0))[:2]
        elbow = key_points.get('right_elbow', (0, 0, 0))[:2]
        wrist = key_points.get('right_wrist', (0, 0, 0))[:2]
        
        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Rep counting logic
        if self.current_stage == "start" and elbow_angle < 80:
            self.current_stage = "up"
        elif self.current_stage == "up" and elbow_angle > 160:
            self.current_stage = "down"
            self.rep_count += 1
            self.last_rep_time = time.time()
            feedback.append(f"💪 Rep {self.rep_count} completed!")
        elif self.current_stage == "down" and elbow_angle < 80:
            self.current_stage = "up"
            
        # Form checks
        if elbow_angle > 170 and self.current_stage != "start":
            errors.append("Fully extend your arm")
            
        if abs(elbow[0] - shoulder[0]) > 0.15:
            errors.append("Keep elbow close to body")
            
        return {
            'angles': {'elbow': elbow_angle},
            'rep_count': self.rep_count,
            'feedback': feedback,
            'errors': errors,
            'stage': self.current_stage
        }

    def analyze_squat(self, key_points):
        feedback = []
        errors = []
        
        hip = key_points.get('right_hip', (0, 0, 0))[:2]
        knee = key_points.get('right_knee', (0, 0, 0))[:2]
        ankle = key_points.get('right_ankle', (0, 0, 0))[:2]
        
        knee_angle = self.calculate_angle(hip, knee, ankle)
        
        # Squat rep counting
        if self.current_stage == "start" and knee_angle < 140:
            self.current_stage = "down"
        elif self.current_stage == "down" and knee_angle > 160:
            self.current_stage = "up"
            self.rep_count += 1
            feedback.append(f"🦵 Rep {self.rep_count} completed!")
        elif self.current_stage == "up" and knee_angle < 140:
            self.current_stage = "down"
            
        # Form checks
        if knee_angle < 90:
            errors.append("Good depth! Keep going")
        elif knee_angle > 170 and self.current_stage != "start":
            errors.append("Stand up straight")
            
        return {
            'angles': {'knee': knee_angle},
            'rep_count': self.rep_count,
            'feedback': feedback,
            'errors': errors,
            'stage': self.current_stage
        }

    def analyze_push_up(self, key_points):
        feedback = []
        errors = []
        
        shoulder = key_points.get('right_shoulder', (0, 0, 0))[:2]
        elbow = key_points.get('right_elbow', (0, 0, 0))[:2]
        wrist = key_points.get('right_wrist', (0, 0, 0))[:2]
        
        elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Push-up rep counting
        if self.current_stage == "start" and elbow_angle < 100:
            self.current_stage = "down"
        elif self.current_stage == "down" and elbow_angle > 160:
            self.current_stage = "up"
            self.rep_count += 1
            feedback.append(f"🏋️ Rep {self.rep_count} completed!")
        elif self.current_stage == "up" and elbow_angle < 100:
            self.current_stage = "down"
            
        # Form checks
        if elbow_angle < 90:
            errors.append("Good depth! Push back up")
        elif elbow_angle > 170 and self.current_stage != "start":
            errors.append("Fully extend arms")
            
        return {
            'angles': {'elbow': elbow_angle},
            'rep_count': self.rep_count,
            'feedback': feedback,
            'errors': errors,
            'stage': self.current_stage
        }

    def analyze_form(self, key_points):
        if not key_points:
            return {'errors': ['No person detected'], 'rep_count': self.rep_count}
            
        if self.exercise_type == "bicep_curl":
            return self.analyze_bicep_curl(key_points)
        elif self.exercise_type == "squat":
            return self.analyze_squat(key_points)
        elif self.exercise_type == "push_up":
            return self.analyze_push_up(key_points)
        else:
            return {'errors': ['Exercise not supported'], 'rep_count': self.rep_count}

class FitnessTrainer:
    def __init__(self):
        self.pose_detector = PoseDetector()
        self.exercise_analyzer = None
        self.is_running = False
        self.camera = None
        self.current_exercise = "bicep_curl"

    def initialize_camera(self):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            # Try different camera indices
            for i in range(1, 3):
                self.camera = cv2.VideoCapture(i)
                if self.camera.isOpened():
                    break
        
        if not self.camera.isOpened():
            return False
            
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)
        return True

    def draw_workout_info(self, frame, analysis_result, exercise_type):
        h, w = frame.shape[:2]
        
        # Exercise title
        cv2.putText(frame, f"Exercise: {exercise_type.replace('_', ' ').title()}", 
                   (w - 300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Rep count with background
        rep_count = analysis_result.get('rep_count', 0)
        cv2.rectangle(frame, (w - 150, 50), (w - 10, 100), (0, 100, 0), -1)
        cv2.putText(frame, f"REPS: {rep_count}", 
                   (w - 140, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Stage
        stage = analysis_result.get('stage', 'start')
        cv2.putText(frame, f"Stage: {stage.upper()}", 
                   (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Angles
        angles = analysis_result.get('angles', {})
        y_offset = 60
        for joint, angle in angles.items():
            cv2.putText(frame, f"{joint}: {angle:.1f}°", 
                       (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 25
            
        # Errors
        errors = analysis_result.get('errors', [])
        if errors:
            cv2.putText(frame, "FORM FEEDBACK:", 
                       (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            y_offset += 25
            for error in errors[:3]:
                cv2.putText(frame, f"• {error}", 
                           (70, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                y_offset += 20
                
        return frame

    def show_exercise_menu(self, frame):
        h, w = frame.shape[:2]
        
        # Semi-transparent overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (w//4, h//4), (3*w//4, 3*h//4), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Title
        cv2.putText(frame, "SELECT EXERCISE", (w//2 - 100, h//4 + 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Exercise options
        exercises = [
            ("1 - Bicep Curls", "bicep_curl"),
            ("2 - Squats", "squat"), 
            ("3 - Push-ups", "push_up"),
            ("SPACE - Start Selected", ""),
            ("Q - Quit", "")
        ]
        
        y_offset = h//4 + 80
        for text, _ in exercises:
            cv2.putText(frame, text, (w//2 - 120, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            y_offset += 40
            
        return frame

    def run(self):
        if not self.initialize_camera():
            print("❌ Error: Could not access camera")
            print("💡 Make sure your camera is connected and not being used by another application")
            return
            
        print("✅ Camera initialized successfully")
        print("🎮 Controls:")
        print("   SPACE - Start/Stop exercise")
        print("   1,2,3 - Select exercise")
        print("   R - Reset rep counter") 
        print("   Q - Quit application")
        
        self.is_running = True
        in_menu = True
        self.current_exercise = "bicep_curl"
        
        while self.is_running:
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Failed to capture frame")
                break
                
            if in_menu:
                frame = self.show_exercise_menu(frame)
            else:
                # Process exercise
                landmarks, processed_frame = self.pose_detector.detect_pose(frame)
                
                if landmarks:
                    key_points = self.pose_detector.extract_key_points(landmarks)
                    analysis_result = self.exercise_analyzer.analyze_form(key_points)
                    processed_frame = self.draw_workout_info(processed_frame, analysis_result, self.current_exercise)
                    
                    # Print feedback to console
                    if analysis_result.get('feedback'):
                        for msg in analysis_result['feedback']:
                            print(f"🎉 {msg}")
                            
                    if analysis_result.get('errors'):
                        for error in analysis_result['errors']:
                            if "Good" not in error:  # Don't print positive feedback as errors
                                print(f"⚠️  {error}")
                else:
                    processed_frame = self.draw_workout_info(processed_frame, {}, self.current_exercise)
                    cv2.putText(processed_frame, "No person detected - Stand in frame", 
                               (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                
                frame = processed_frame
            
            # Display frame
            cv2.imshow('AI Fitness Trainer - Real-time Pose Detection', frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):  # Space bar
                if in_menu:
                    # Start exercise
                    self.exercise_analyzer = ExerciseAnalyzer(self.current_exercise)
                    in_menu = False
                    print(f"🎯 Starting {self.current_exercise} workout!")
                else:
                    # Return to menu
                    in_menu = True
                    print("📋 Returning to exercise menu")
            elif key in [ord('1'), ord('2'), ord('3')]:
                exercises = ["bicep_curl", "squat", "push_up"]
                exercise_index = key - ord('1')
                if exercise_index < len(exercises):
                    self.current_exercise = exercises[exercise_index]
                    print(f"📝 Selected: {self.current_exercise}")
            elif key == ord('r') and not in_menu:
                self.exercise_analyzer.rep_count = 0
                self.exercise_analyzer.current_stage = "start"
                print("🔄 Rep counter reset")
                
        self.cleanup()

    def cleanup(self):
        self.is_running = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        print("👋 Thank you for using AI Fitness Trainer!")

def main():
    print("=" * 60)
    print("🏋️‍♂️ AI FITNESS TRAINER - Real-time Pose Detection")
    print("=" * 60)
    print("📊 Features:")
    print("   • Real-time human pose detection")
    print("   • Exercise form analysis")
    print("   • Repetition counting")
    print("   • Form feedback and corrections")
    print("   • Multiple exercise support")
    print()
    
    trainer = FitnessTrainer()
    
    try:
        trainer.run()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        trainer.cleanup()

if __name__ == "__main__":
    main()