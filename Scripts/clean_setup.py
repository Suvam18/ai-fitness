import os
import shutil

def create_clean_structure():
    """Create a clean project structure"""
    
    # Remove problematic __init__ files
    init_files = [
        "config/__init__.py",
        "src/__init__.py", 
        "utils/__init__.py",
        "tests/__init__.py"
    ]
    
    for file in init_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed {file}")
    
    print("✅ Cleaned project structure")
    print("🎯 Now try running: python fixed_main.py")

if __name__ == "__main__":
    create_clean_structure()