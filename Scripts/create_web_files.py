"""
Create all missing web files
"""
import os

def create_fitness_website():
    """Create the main HTML website file"""
    content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Fitness Trainer - Smart Workout Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #f093fb;
            --dark: #2d3748;
            --light: #f7fafc;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: var(--light);
            line-height: 1.6;
            min-height: 100vh;
        }

        /* Navigation */
        .navbar {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }

        .nav-links a {
            color: var(--light);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }

        .nav-links a:hover {
            color: var(--accent);
        }

        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            padding: 0 2rem;
            margin-top: 80px;
        }

        .hero-content {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, var(--accent), var(--light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s;
        }

        .feature-card:hover {
            transform: translateY(-10px);
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .cta-button {
            background: var(--accent);
            color: white;
            padding: 1rem 2rem;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            margin-top: 2rem;
            transition: transform 0.3s;
        }

        .cta-button:hover {
            transform: translateY(-2px);
        }

        /* Sections */
        .section {
            padding: 5rem 2rem;
        }

        .section-title {
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 3rem;
        }

        .features-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }

        .feature-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 2rem;
            border-radius: 15px;
            border-left: 4px solid var(--accent);
        }

        /* Stats */
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .stat-item {
            text-align: center;
            padding: 2rem;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            color: var(--accent);
        }

        /* Demo Section */
        .demo-section {
            background: var(--dark);
            padding: 5rem 2rem;
        }

        .demo-container {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3rem;
            align-items: center;
        }

        .demo-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
        }

        /* Footer */
        .footer {
            background: var(--dark);
            padding: 3rem 2rem;
            text-align: center;
        }

        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            .hero h1 {
                font-size: 2.5rem;
            }
            .demo-container {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="logo">
            <span>🏋️</span>
            AI Fitness Trainer
        </div>
        <ul class="nav-links">
            <li><a href="#home">Home</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#demo">Demo</a></li>
            <li><a href="#technology">Technology</a></li>
        </ul>
        <a href="#demo" class="cta-button">Try Now</a>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-content">
            <h1>Revolutionize Your Workouts with AI</h1>
            <p>Real-time pose detection and form analysis for perfect workouts every time</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <h3>AI-Powered Analysis</h3>
                    <p>Advanced computer vision analyzes your form in real-time</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Instant Feedback</h3>
                    <p>Get immediate corrections and improvements</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💰</div>
                    <h3>Completely Free</h3>
                    <p>No subscriptions, no hidden costs</p>
                </div>
            </div>

            <a href="#demo" class="cta-button">Start Your Free Workout</a>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="section">
        <h2 class="section-title">Powerful Features</h2>
        <div class="features-container">
            <div class="feature-item">
                <h3>🎯 Real-time Pose Detection</h3>
                <p>Advanced MediaPipe AI tracks 33 body points with 95%+ accuracy for precise form analysis.</p>
            </div>
            <div class="feature-item">
                <h3>📊 Smart Rep Counting</h3>
                <p>Automatically counts repetitions and tracks your workout progress with intelligent algorithms.</p>
            </div>
            <div class="feature-item">
                <h3>🔊 Audio & Visual Feedback</h3>
                <p>Get instant corrections through both on-screen visuals and audio cues for hands-free workouts.</p>
            </div>
            <div class="feature-item">
                <h3>💪 Multiple Exercise Support</h3>
                <p>Specialized analysis for bicep curls, squats, push-ups, shoulder press, lunges, and planks.</p>
            </div>
            <div class="feature-item">
                <h3>📈 Progress Tracking</h3>
                <p>Comprehensive workout history, calorie tracking, and performance analytics.</p>
            </div>
            <div class="feature-item">
                <h3>🌐 No Equipment Needed</h3>
                <p>Works with any standard webcam - no expensive wearables or sensors required.</p>
            </div>
        </div>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">6+</div>
                <div>Exercises</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">99%</div>
                <div>Accuracy</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">0₹</div>
                <div>Cost</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">33</div>
                <div>Body Points Tracked</div>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="demo-section">
        <h2 class="section-title">Live AI Demo</h2>
        <div class="demo-container">
            <div>
                <h3>Experience AI Fitness Training</h3>
                <p>See how our advanced computer vision technology provides real-time form correction and feedback.</p>
                
                <div class="demo-card">
                    <h4>🚀 Desktop Application</h4>
                    <p>Full-featured AI trainer with all exercises</p>
                    <a href="../run_fitness_trainer.py" class="cta-button" style="margin-top: 1rem;">
                        Download Desktop App
                    </a>
                </div>

                <div class="demo-card" style="margin-top: 2rem;">
                    <h4>🌐 Web Version</h4>
                    <p>Try the basic version in your browser</p>
                    <a href="../web/professional_web_app.py" class="cta-button" style="margin-top: 1rem; background: #48bb78;">
                        Launch Web App
                    </a>
                </div>
            </div>
            
            <div class="demo-card">
                <div style="background: #2d3748; height: 300px; display: flex; align-items: center; justify-content: center; border-radius: 10px;">
                    <div style="text-align: center;">
                        <div style="font-size: 4rem;">🎥</div>
                        <p>Live AI Pose Detection</p>
                        <p style="opacity: 0.7; margin-top: 1rem;">Real-time body tracking demo</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Technology Section -->
    <section id="technology" class="section">
        <h2 class="section-title">Advanced Technology Stack</h2>
        <div class="features-container">
            <div class="feature-item">
                <h3>🤖 MediaPipe Pose</h3>
                <p>Google's state-of-the-art pose estimation framework for accurate body tracking.</p>
            </div>
            <div class="feature-item">
                <h3>🐍 Python & OpenCV</h3>
                <p>Robust computer vision processing and real-time video analysis.</p>
            </div>
            <div class="feature-item">
                <h3>📊 NumPy & SciPy</h3>
                <p>Advanced mathematical computations for angle calculations and form analysis.</p>
            </div>
            <div class="feature-item">
                <h3>🎮 Streamlit UI</h3>
                <p>Modern web interface for accessible fitness tracking across devices.</p>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="logo" style="justify-content: center; margin-bottom: 1rem;">
            <span>🏋️</span>
            AI Fitness Trainer
        </div>
        <p>Revolutionizing fitness with artificial intelligence</p>
        <p style="margin-top: 2rem; opacity: 0.7;">Built with ❤️ for the fitness community</p>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Navbar background on scroll
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 100) {
                navbar.style.background = 'rgba(45, 55, 72, 0.95)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.1)';
            }
        });
    </script>
</body>
</html>'''
    
    with open('web/fitness_website.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: web/fitness_website.html")

def create_web_server():
    """Create the web server file"""
    content = '''"""
Simple web server for AI Fitness Trainer website
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os
import socket

def find_available_port(start_port=8000):
    """Find an available port starting from start_port"""
    port = start_port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1

def start_web_server():
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    
    port = find_available_port()
    
    print("🚀 Starting AI Fitness Trainer Website...")
    print(f"📍 Website running at: http://localhost:{port}")
    print("💡 Press Ctrl+C to stop the server")
    print("🌐 Your browser should open automatically...")
    
    # Open browser automatically
    webbrowser.open(f'http://localhost:{port}/fitness_website.html')
    
    try:
        server = HTTPServer(('', port), SimpleHTTPRequestHandler)
        print(f"✅ Server started successfully on port {port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_web_server()
'''
    
    with open('web/web_server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: web/web_server.py")

def create_professional_web_app():
    """Create the Streamlit web app"""
    content = '''"""
Professional Streamlit Web App for AI Fitness Trainer
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="AI Fitness Trainer Pro",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: rgba(102, 126, 234, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🏋️ AI Fitness Trainer Pro</h1>', unsafe_allow_html=True)
    
    # Navigation
    st.sidebar.title("🎯 Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose Mode",
        ["🏠 Dashboard", "💪 Live Trainer", "📊 Progress", "ℹ️ About"]
    )
    
    if app_mode == "🏠 Dashboard":
        show_dashboard()
    elif app_mode == "💪 Live Trainer":
        show_live_trainer()
    elif app_mode == "📊 Progress":
        show_progress()
    else:
        show_about()

def show_dashboard():
    st.subheader("🚀 Welcome to AI-Powered Fitness")
    st.markdown("""
    Transform your workouts with real-time AI form analysis and personalized feedback. 
    Our advanced computer vision technology ensures you perform every exercise with perfect form.
    """)
    
    # Features
    st.subheader("✨ Key Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Real-time Pose Detection</h4>
            <p>Advanced AI tracks 33 body points with 95%+ accuracy</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Smart Rep Counting</h4>
            <p>Automated repetition tracking with form analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🔊 Audio Feedback</h4>
            <p>Hands-free corrections during workouts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💪 6+ Exercises</h4>
            <p>Specialized analysis for different workout types</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>💰 Completely Free</h4>
            <p>No subscriptions, no hidden costs</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🌐 No Equipment</h4>
            <p>Works with any standard webcam</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats
    st.subheader("📈 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>6+</h3>
            <p>Exercises</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>99%</h3>
            <p>Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>0₹</h3>
            <p>Cost</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>33</h3>
            <p>Body Points</p>
        </div>
        """, unsafe_allow_html=True)

def show_live_trainer():
    st.header("💪 Live AI Fitness Trainer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📷 Live Camera Feed")
        st.info("Camera feed will appear here when started")
        
        col1a, col1b = st.columns(2)
        with col1a:
            if st.button("🎥 Start Camera", use_container_width=True):
                st.success("Camera started! (Demo mode)")
        with col1b:
            if st.button("⏹️ Stop Camera", use_container_width=True):
                st.info("Camera stopped")
    
    with col2:
        st.subheader("⚙️ Workout Settings")
        
        exercise = st.selectbox(
            "Select Exercise",
            ["Bicep Curls", "Squats", "Push-ups", "Shoulder Press", "Lunges", "Plank"]
        )
        
        target_reps = st.slider("Target Reps", 5, 20, 12)
        
        st.subheader("📊 Live Stats")
        st.metric("Current Reps", "0")
        st.metric("Calories Burned", "0.0")
        
        st.subheader("🎯 Form Feedback")
        st.info("Start your workout to see real-time feedback")

def show_progress():
    st.header("📊 Your Fitness Journey")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Workouts", "12")
    with col2:
        st.metric("Total Reps", "156")
    with col3:
        st.metric("Calories Burned", "89.5")
    with col4:
        st.metric("Current Streak", "5 days")
    
    st.subheader("📅 Recent Workouts")
    workouts = [
        {"date": "2024-01-20", "exercise": "Bicep Curls", "reps": 12, "calories": 6.0},
        {"date": "2024-01-19", "exercise": "Squats", "reps": 15, "calories": 15.0},
        {"date": "2024-01-18", "exercise": "Push-ups", "reps": 10, "calories": 8.0},
    ]
    
    for workout in workouts:
        st.write(f"**{workout['date']}** - {workout['exercise']} - {workout['reps']} reps - {workout['calories']} calories")

def show_about():
    st.header("ℹ️ About AI Fitness Trainer")
    st.markdown("""
    ## 🚀 Revolutionizing Fitness with AI
    
    **AI Fitness Trainer Pro** uses cutting-edge computer vision technology to provide 
    real-time form analysis and personalized workout feedback.
    
    ### 🛠️ Technology Stack
    - **MediaPipe Pose**: Google's advanced pose estimation
    - **OpenCV**: Real-time computer vision
    - **Python**: Backend AI algorithms
    - **Streamlit**: Modern web interface
    
    ### 💡 Why Choose Us?
    - ✅ Real-time form corrections
    - ✅ No equipment needed
    - ✅ Completely free
    - ✅ Privacy focused
    """)

if __name__ == "__main__":
    main()
'''
    
    with open('web/professional_web_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: web/professional_web_app.py")

def create_simple_web_app():
    """Create a simple Streamlit app"""
    content = '''"""
Simple Streamlit Web App for AI Fitness Trainer
"""
import streamlit as st

st.set_page_config(page_title="AI Fitness Trainer", page_icon="🏋️")

st.title("🏋️ AI Fitness Trainer")
st.markdown("Real-time pose detection and form analysis")

st.sidebar.title("Settings")
exercise = st.sidebar.selectbox("Choose Exercise", ["Bicep Curls", "Squats", "Push-ups"])

st.info("🚀 This is a simple web interface for the AI Fitness Trainer")
st.success("✅ For full features, use the desktop application")

if st.button("Launch Desktop App"):
    st.write("Please run: python run_fitness_trainer.py")
'''
    
    with open('web/simple_web.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Created: web/simple_web.py")

def main():
    print("📁 Creating all missing web files...")
    
    # Create the files
    create_fitness_website()
    create_web_server()
    create_professional_web_app()
    create_simple_web_app()
    
    print("\\n🎉 All web files created successfully!")
    print("\\n🚀 Next steps:")
    print("1. Run: python web/web_server.py")
    print("2. Your browser will open with the professional website")
    print("3. Or run: streamlit run web/professional_web_app.py")

if __name__ == "__main__":
    main()