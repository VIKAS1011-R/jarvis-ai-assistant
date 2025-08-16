#!/usr/bin/env python3
"""
Fix distutils compatibility issue for Python 3.12+
"""

import sys
import subprocess

def fix_distutils():
    """Fix distutils compatibility"""
    print("Fixing distutils compatibility...")
    
    try:
        # Try to import distutils
        import distutils
        print("✓ distutils is available")
        return True
    except ImportError:
        print("✗ distutils not found, installing setuptools...")
        
        try:
            # Install setuptools which provides distutils compatibility
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "setuptools>=65.0.0"])
            print("✓ setuptools installed")
            
            # Try importing again
            import distutils
            print("✓ distutils now available")
            return True
            
        except Exception as e:
            print(f"✗ Failed to fix distutils: {e}")
            return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing Jarvis dependencies...")
    
    try:
        # Install core dependencies first
        core_deps = [
            "python-dotenv>=1.0.0",
            "setuptools>=65.0.0"
        ]
        
        for dep in core_deps:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        
        # Install Picovoice
        print("Installing Picovoice...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pvporcupine==3.0.2"])
        
        # Install Edge TTS
        print("Installing Edge TTS...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts>=6.1.9"])
        
        # Install Speech Recognition
        print("Installing Speech Recognition...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "SpeechRecognition>=3.10.0"])
        
        print("✓ All dependencies installed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    modules = [
        ("os", "Built-in"),
        ("dotenv", "python-dotenv"),
        ("pvporcupine", "Picovoice"),
        ("speech_recognition", "SpeechRecognition")
    ]
    
    all_good = True
    
    for module, description in modules:
        try:
            __import__(module)
            print(f"✓ {module} ({description})")
        except ImportError as e:
            print(f"✗ {module} ({description}): {e}")
            all_good = False
    
    return all_good

def main():
    """Main setup function"""
    print("Jarvis Dependency Fixer")
    print("=" * 30)
    
    # Fix distutils first
    if not fix_distutils():
        print("\n❌ Could not fix distutils compatibility")
        print("Try running: pip install --upgrade setuptools")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies")
        return False
    
    # Test imports
    if not test_imports():
        print("\n❌ Some imports failed")
        return False
    
    print("\n✅ All dependencies installed and working!")
    print("\nYou can now run: python jarvis.py")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)