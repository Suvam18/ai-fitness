"""
Simple web launcher for AI Fitness Trainer
"""
import os
import subprocess
import sys

def launch_website():
    """Launch the HTML website"""
    print("🌐 Launching AI Fitness Trainer Website...")
    print("📍 Starting web server...")
    
    # Check if web directory exists
    if not os.path.exists('web'):
        print("❌ Web directory not found!")
        return
    
    # Launch web server
    web_server_path = os.path.join('web', 'web_server.py')
    if os.path.exists(web_server_path):
        print("🚀 Starting professional website...")
        subprocess.run([sys.executable, web_server_path])
    else:
        print("❌ web_server.py not found!")

def launch_streamlit():
    """Launch Streamlit app"""
    print("🚀 Launching Streamlit App...")
    try:
        # Try direct streamlit command
        subprocess.run(['streamlit', 'run', 'web/professional_web_app.py'])
    except FileNotFoundError:
        print("❌ Streamlit command not found. Trying alternative...")
        try:
            # Try python -m streamlit
            subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'web/professional_web_app.py'])
        except:
            print("💥 Streamlit not available.")
            print("💡 Install with: pip install streamlit")

def main():
    print("=" * 50)
    print("🏋️ AI Fitness Trainer - Web Interface Launcher")
    print("=" * 50)
    
    print("Choose web interface:")
    print("1. 🌐 Professional HTML Website (Recommended)")
    print("2. 💻 Interactive Streamlit App")
    print("3. 🖥️  Desktop Application")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        launch_website()
    elif choice == "2":
        launch_streamlit()
    elif choice == "3":
        print("🚀 Launching Desktop Application...")
        subprocess.run([sys.executable, 'run_fitness_trainer.py'])
    else:
        print("Launching website by default...")
        launch_website()

if __name__ == "__main__":
    main()