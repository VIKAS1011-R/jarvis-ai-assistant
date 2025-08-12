#!/usr/bin/env python3
"""
Example script demonstrating individual module usage
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.config import config
from modules.tts import TextToSpeech
from modules.hotword_detection import HotWordDetector
from modules.jarvis_responses import JarvisResponses

def test_tts():
    """Test text-to-speech module"""
    print("Testing TTS module...")
    
    with TextToSpeech() as tts:
        # Test basic speech
        tts.speak("Testing text to speech functionality")
        
        # Test random responses
        tts.speak_random(JarvisResponses.GREETINGS)
        
        # List available voices
        tts.list_voices()

def test_config():
    """Test configuration module"""
    print("Testing configuration module...")
    
    try:
        print(f"Access key configured: {'Yes' if config.picovoice_access_key else 'No'}")
        print(f"Wake word model path: {config.wake_word_model_path}")
        print(f"Model exists: {os.path.exists(config.wake_word_model_path)}")
        
        # Validate setup
        config.validate_setup()
        
    except Exception as e:
        print(f"Configuration error: {e}")

def test_responses():
    """Test response module"""
    print("Testing responses module...")
    
    print(f"Random greeting: {JarvisResponses.get_random_greeting()}")
    print(f"Random startup: {JarvisResponses.get_random_startup()}")
    print(f"Random shutdown: {JarvisResponses.get_random_shutdown()}")
    
    # Add custom response
    JarvisResponses.add_custom_greeting("Hello there, how can I help you today?")
    print(f"After adding custom: {JarvisResponses.get_random_greeting()}")

def test_hotword_detection():
    """Test hot word detection (requires microphone)"""
    print("Testing hot word detection...")
    print("Say 'Jarvis' to test detection (Ctrl+C to stop)")
    
    def on_detection():
        print("Detection callback triggered!")
    
    try:
        with HotWordDetector(config.picovoice_access_key, config.wake_word_model_path) as detector:
            detector.set_callback(on_detection)
            detector.start_listening()
    except Exception as e:
        print(f"Hot word detection error: {e}")

def main():
    """Run module tests"""
    print("J.A.R.V.I.S Module Testing")
    print("=" * 30)
    
    # Test configuration first
    test_config()
    print()
    
    # Test responses
    test_responses()
    print()
    
    # Test TTS
    test_tts()
    print()
    
    # Ask user if they want to test hot word detection
    response = input("Test hot word detection? (y/n): ").lower().strip()
    if response == 'y':
        test_hotword_detection()

if __name__ == "__main__":
    main()