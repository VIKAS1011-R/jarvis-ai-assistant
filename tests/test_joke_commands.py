#!/usr/bin/env python3
"""
Test script for joke commands and joke service
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.joke_service import JokeService
from modules.simple_commands import SimpleCommands
from modules.smart_tts import SmartTTS

def test_joke_service():
    """Test the joke service directly"""
    print("Testing Joke Service")
    print("=" * 40)
    
    service = JokeService()
    
    print("1. Testing regular joke:")
    joke = service.get_joke()
    print(f"   {joke}")
    print(f"   Length: {len(joke)} characters")
    
    print("\n2. Testing programming joke:")
    prog_joke = service.get_programming_joke()
    print(f"   {prog_joke}")
    
    print("\n3. Testing dad joke:")
    dad_joke = service.get_dad_joke()
    print(f"   {dad_joke}")
    
    print("\n✓ Joke service tests completed")

def test_joke_commands():
    """Test joke commands through the command processor"""
    print("\nTesting Joke Commands")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"TTS: {text}")
    
    mock_tts = MockTTS()
    commands = SimpleCommands(mock_tts)
    
    test_commands = [
        "tell me a joke",
        "joke",
        "make me laugh",
        "tell me a programming joke",
        "tell me a dad joke",
        "programming joke",
        "dad joke"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. Testing command: '{command}'")
        result = commands.process_command(command)
        print(f"   Result: {result}")
    
    print("\n✓ Command tests completed")

def test_with_real_tts():
    """Test with real TTS (optional)"""
    print("\nTesting with Real TTS")
    print("=" * 40)
    
    try:
        tts = SmartTTS()
        if tts.initialize():
            commands = SimpleCommands(tts)
            
            print("Testing joke command with real TTS...")
            commands.process_command("tell me a joke")
            
            print("✓ Real TTS test completed")
            tts.cleanup()
        else:
            print("✗ Could not initialize TTS")
    except Exception as e:
        print(f"✗ TTS test failed: {e}")

def main():
    """Run all joke tests"""
    print("JARVIS Joke Command Tests")
    print("=" * 50)
    
    # Test joke service
    test_joke_service()
    
    # Test commands
    test_joke_commands()
    
    # Ask if user wants to test with real TTS
    response = input("\nTest with real TTS? (y/n): ").lower().strip()
    if response == 'y':
        test_with_real_tts()
    else:
        print("Skipping real TTS test")
    
    print("\n🎉 All joke tests completed!")

if __name__ == "__main__":
    main()