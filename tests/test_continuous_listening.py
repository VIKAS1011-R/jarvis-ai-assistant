#!/usr/bin/env python3
"""
Test script for continuous listening and NLP command extraction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.continuous_listener import ContinuousListener

def test_command_extraction():
    """Test the NLP command extraction without audio"""
    print("Testing NLP Command Extraction")
    print("=" * 50)
    
    listener = ContinuousListener()
    
    test_phrases = [
        "Jarvis what time is it",
        "Hey Jarvis can you tell me the weather",
        "OK Jarvis please search for Python tutorials",
        "Jarvis open Google Chrome",
        "Hey Jarvis play some music",
        "Jarvis what's the current time please",
        "OK Jarvis search Google for machine learning",
        "Hey Jarvis open YouTube",
        "Jarvis exit the program",
        "Jarvis help me with commands",
        "OK Jarvis tell me a joke",
        "Hey Jarvis what's the weather like today"
    ]
    
    for phrase in test_phrases:
        wake_word, command = listener.extract_wake_word_and_command(phrase)
        print(f"Input: '{phrase}'")
        print(f"  Wake word: '{wake_word}'")
        print(f"  Command: '{command}'")
        print("-" * 40)

def test_audio_listening():
    """Test actual audio listening (requires microphone)"""
    print("\nTesting Audio Listening")
    print("=" * 50)
    print("Say something like: 'Jarvis what time is it'")
    print("Press Ctrl+C to stop")
    
    def on_command(wake_word, command):
        print(f"\n✓ Detected - Wake word: '{wake_word}', Command: '{command}'")
    
    listener = ContinuousListener()
    listener.set_callback(on_command)
    
    try:
        if listener.initialize():
            # Test a few iterations
            for i in range(3):
                print(f"\nListening attempt {i+1}/3...")
                wake_word, command = listener.listen_continuously()
                if wake_word:
                    print(f"✓ Wake word: '{wake_word}'")
                    if command:
                        print(f"✓ Command: '{command}'")
                    else:
                        print("✗ No command extracted")
                else:
                    print("✗ No wake word detected")
        else:
            print("Failed to initialize listener")
    except KeyboardInterrupt:
        print("\nStopped by user")
    finally:
        listener.cleanup()

if __name__ == "__main__":
    # Test NLP extraction first
    test_command_extraction()
    
    # Ask user if they want to test audio
    response = input("\nTest audio listening? (y/n): ").lower().strip()
    if response == 'y':
        test_audio_listening()
    else:
        print("Skipping audio test")