"""
Test the complete setup
"""
import os
import subprocess
import sys

def test_structure():
    print("📁 Testing project structure...")
    
    required_dirs = ['web', 'src', 'data', 'assets']
    required_files = ['web/fitness_website.html', 'web/web_server.py']
    
    all_good = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False
    
    return all_good

def test_imports():
    print("\n🐍 Testing Python imports...")
    
    imports_to_test = [
        'cv2',
        'numpy', 
        'mediapipe'
    ]
    
    all_good = True
    
    for import_name in imports_to_test:
        try:
            __import__(import_name)
            print(f"✅ {import_name} imports successfully")
        except ImportError as e:
            print(f"❌ {import_name} import failed: {e}")
            all_good = False
    
    return all_good

def main():
    print("🧪 AI Fitness Trainer - Setup Test")
    print("=" * 40)
    
    structure_ok = test_structure()
    imports_ok = test_imports()
    
    print("\n" + "=" * 40)
    if structure_ok and imports_ok:
        print("🎉 All tests passed! You're ready to go!")
        print("\n🚀 Next steps:")
        print("1. Run: python launch_web.py")
        print("2. Choose option 1 for HTML website")
        print("3. Your browser will open with the website")
    else:
        print("❌ Some tests failed.")
        print("\n🔧 Fix steps:")
        if not structure_ok:
            print("- Run: python create_structure.py")
        if not imports_ok:
            print("- Run: python install_web_dependencies.py")

if __name__ == "__main__":
    main()