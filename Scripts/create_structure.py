"""
Create the complete project structure
"""
import os
import shutil

def create_project_structure():
    print("🏗️ Creating AI Fitness Trainer project structure...")
    
    # Create directories
    directories = [
        'web',
        'data/workouts',
        'data/user_sessions', 
        'data/models',
        'src/utils',
        'tests',
        'config',
        'assets/images',
        'assets/sounds',
        'assets/sample_videos'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Create empty __init__.py files
    init_files = [
        'src/__init__.py',
        'src/utils/__init__.py', 
        'tests/__init__.py',
        'config/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            pass
        print(f"✅ Created: {init_file}")
    
    print("🎉 Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()