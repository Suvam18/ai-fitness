import subprocess
import sys
import os

def install_requirements():
    """Install project dependencies with error handling"""
    
    # List of packages to install
    packages = [
        "opencv-python",
        "mediapipe", 
        "numpy",
        "pandas",
        "pygame",
        "streamlit",
        "matplotlib",
        "python-dotenv",
        "pillow"
    ]
    
    print("Installing AI Fitness Trainer dependencies...")
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            print("Trying with --user flag...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
                print(f"✓ {package} installed successfully with --user flag")
            except:
                print(f"✗ Could not install {package}. Please install manually.")
    
    print("\nDependency installation completed!")

if __name__ == "__main__":
    install_requirements()