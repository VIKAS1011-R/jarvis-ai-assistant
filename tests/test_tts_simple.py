#!/usr/bin/env python3
"""
Simple TTS test to diagnose text-to-speech issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_basic_pyttsx3():
    """Test basic pyttsx3 without our wrapper"""
    print("Testing basic pyttsx3...")
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        print("✓ pyttsx3 engine created")
        
        # Test basic speech
        print("Speaking: 'Hello, this is a TTS test'")
        engine.say("Hello, this is a TTS test")
        engine.runAndWait()
        print("✓ Basic TTS completed")
        
        # Test multiple calls
        for i in range(3):
            print(f"Speaking test {i+1}")
            engine.say(f"This is test number {i+1}")
            engine.runAndWait()
        
        engine.stop()
        print("✓ All TTS tests passed")
        return True
        
    except Exception as e:
        print(f"✗ TTS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_jarvis_tts():
    """Test our Jarvis TTS module"""
    print("\nTesting Jarvis TTS module...")
    
    try:
        from modules.tts import TextToSpeech
        
        tts = TextToSpeech()
        tts.initialize()
        print("✓ Jarvis TTS initialized")
        
        # Test multiple calls like in Jarvis
        test_phrases = [
            "Good day, sir. How may I assist you?",
            "Jarvis at your service.",
            "Yes, sir? What can I do for you?",
            "I'm here and ready to help."
        ]
        
        for i, phrase in enumerate(test_phrases):
            print(f"Test {i+1}: {phrase}")
            tts.speak(phrase)
            print(f"✓ Test {i+1} completed")
        
        tts.cleanup()
        print("✓ Jarvis TTS tests completed")
        return True
        
    except Exception as e:
        print(f"✗ Jarvis TTS failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run TTS diagnostic tests"""
    print("TTS Diagnostic - Text-Only Mode Fix")
    print("=" * 40)
    
    # Test basic pyttsx3
    basic_success = test_basic_pyttsx3()
    
    if basic_success:
        # Test Jarvis TTS
        jarvis_success = test_jarvis_tts()
        
        if jarvis_success:
            print("\n✓ All TTS tests passed! Jarvis should work correctly.")
        else:
            print("\n✗ Jarvis TTS module has issues. Check the error above.")
    else:
        print("\n✗ Basic TTS failed. Possible solutions:")
        print("1. Restart Windows audio service")
        print("2. Check audio drivers")
        print("3. Try: pip uninstall pyttsx3 && pip install pyttsx3")
        print("4. Restart your computer")

if __name__ == "__main__":
    main()