"""
Install web dependencies properly
"""
import subprocess
import sys
import os

def install_dependencies():
    print("📦 Installing web dependencies...")
    
    packages = [
        "streamlit",
        "opencv-python", 
        "mediapipe",
        "numpy",
        "pandas",
        "matplotlib",
        "pillow"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            print("Trying with --user flag...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
                print(f"✅ {package} installed with --user flag")
            except:
                print(f"💥 Could not install {package}")

def test_imports():
    print("\n🧪 Testing imports...")
    imports = [
        "streamlit",
        "cv2", 
        "mediapipe",
        "numpy",
        "pandas"
    ]
    
    for import_name in imports:
        try:
            if import_name == "cv2":
                __import__('cv2')
            else:
                __import__(import_name)
            print(f"✅ {import_name} imports successfully")
        except ImportError as e:
            print(f"❌ {import_name} import failed: {e}")

if __name__ == "__main__":
    install_dependencies()
    test_imports()
    print("\n🎉 Installation complete! Now run: python fix_web_launch.py")