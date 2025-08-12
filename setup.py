#!/usr/bin/env python3
"""
Setup script for J.A.R.V.I.S
Creates virtual environment and installs required dependencies
"""

import subprocess
import sys
import os
import venv
import platform

VENV_NAME = "jarvis_env"
VENV_PATH = os.path.join(os.getcwd(), VENV_NAME)

def create_virtual_environment():
    """Create a virtual environment for the project"""
    print(f"Creating virtual environment: {VENV_NAME}")
    
    if os.path.exists(VENV_PATH):
        print(f"✓ Virtual environment '{VENV_NAME}' already exists")
        return True
    
    try:
        venv.create(VENV_PATH, with_pip=True)
        print(f"✓ Virtual environment '{VENV_NAME}' created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating virtual environment: {e}")
        return False

def get_venv_python():
    """Get the path to Python executable in virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(VENV_PATH, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_PATH, "bin", "python")

def get_venv_pip():
    """Get the path to pip executable in virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(VENV_PATH, "Scripts", "pip.exe")
    else:
        return os.path.join(VENV_PATH, "bin", "pip")

def upgrade_pip():
    """Upgrade pip in virtual environment"""
    print("Upgrading pip in virtual environment...")
    try:
        venv_python = get_venv_python()
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
        print("✓ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error upgrading pip: {e}")
        return False

def install_requirements():
    """Install required Python packages in virtual environment"""
    print("Installing required packages in virtual environment...")
    
    venv_python = get_venv_python()
    
    # Install setuptools first to fix distutils issue
    try:
        print("Installing setuptools for distutils compatibility...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "setuptools>=65.0.0"])
        print("✓ setuptools installed")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Could not install setuptools: {e}")
    
    # Install other requirements
    try:
        venv_pip = get_venv_pip()
        subprocess.check_call([venv_pip, "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        print("Trying alternative installation method...")
        try:
            subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Packages installed with alternative method")
        except subprocess.CalledProcessError as e2:
            print(f"✗ Alternative installation also failed: {e2}")
            return False
    return True

def get_activation_command():
    """Get the command to activate virtual environment"""
    if platform.system() == "Windows":
        return f"{VENV_NAME}\\Scripts\\activate"
    else:
        return f"source {VENV_NAME}/bin/activate"

def check_environment():
    """Check if environment is properly configured"""
    print("Checking environment configuration...")
    
    # Check .env file
    if not os.path.exists('.env'):
        print("✗ .env file not found")
        return False
    
    # Check wake word model
    model_path = os.path.join('resources', 'Jarvis_en_windows_v3_0_0.ppn')
    if not os.path.exists(model_path):
        print(f"✗ Wake word model not found: {model_path}")
        return False
    
    print("✓ Environment configuration looks good")
    return True

def test_imports():
    """Test if all required modules can be imported in virtual environment"""
    print("Testing module imports in virtual environment...")
    
    modules = ['pvporcupine', 'pyttsx3', 'pyaudio', 'dotenv']
    venv_python = get_venv_python()
    
    for module in modules:
        try:
            result = subprocess.run([venv_python, "-c", f"import {module}"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {module}")
            else:
                print(f"✗ {module}: Import failed")
                return False
        except Exception as e:
            print(f"✗ {module}: {e}")
            return False
    
    return True

def print_usage_instructions():
    """Print instructions for using the virtual environment"""
    activation_cmd = get_activation_command()
    
    print("\n" + "=" * 50)
    print("USAGE INSTRUCTIONS")
    print("=" * 50)
    print("\n1. Activate the virtual environment:")
    if platform.system() == "Windows":
        print(f"   {activation_cmd}")
    else:
        print(f"   {activation_cmd}")
    
    print("\n2. Run J.A.R.V.I.S:")
    print("   python jarvis.py")
    
    print("\n3. To deactivate virtual environment when done:")
    print("   deactivate")
    
    print("\nAlternatively, run directly with:")
    venv_python = get_venv_python()
    print(f"   {venv_python} jarvis.py")

def main():
    """Main setup function"""
    print("J.A.R.V.I.S Setup with Virtual Environment")
    print("=" * 45)
    
    success = True
    
    # Create virtual environment
    if not create_virtual_environment():
        success = False
    
    # Upgrade pip in virtual environment
    if success and not upgrade_pip():
        print("Warning: Could not upgrade pip, continuing anyway...")
    
    # Install requirements in virtual environment
    if success and not install_requirements():
        success = False
    
    # Check environment configuration
    if success and not check_environment():
        success = False
    
    # Test imports in virtual environment
    if success and not test_imports():
        success = False
    
    print("\nSetup Summary:")
    print("=" * 20)
    
    if success:
        print("✓ Setup completed successfully!")
        print(f"✓ Virtual environment '{VENV_NAME}' is ready")
        print_usage_instructions()
    else:
        print("✗ Setup encountered errors. Please fix the issues above.")
        
    return success

if __name__ == "__main__":
    main()