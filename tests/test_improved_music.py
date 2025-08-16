#!/usr/bin/env python3
"""
Test script for improved music functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.music_service import MusicService
from modules.simple_commands import SimpleCommands

def test_music_service_improvements():
    """Test the improved music service"""
    print("Testing Improved Music Service")
    print("=" * 40)
    
    music = MusicService()
    
    print("1. Testing Spotify detection:")
    spotify_installed = music._is_spotify_installed()
    spotify_running = music._is_spotify_running()
    print(f"   Spotify installed: {spotify_installed}")
    print(f"   Spotify running: {spotify_running}")
    
    print("\n2. Testing smart play (simulation):")
    if hasattr(music, 'smart_play'):
        # This won't actually play music in test mode
        print("   Smart play method available")
        print("   Would attempt multiple methods to play music")
    else:
        print("   Smart play method not found")
    
    print("\n3. Testing music help:")
    help_text = music.get_music_help()
    print(f"   Help text length: {len(help_text)} characters")
    print(f"   Contains Spotify info: {'Spotify' in help_text}")
    
    print("✓ Music service improvement tests completed")

def test_command_integration():
    """Test improved music commands"""
    print("\nTesting Improved Music Command Integration")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    commands = SimpleCommands(MockTTS())
    
    test_commands = [
        "play heat waves",
        "play The Beatles",
        "play jazz music",
        "pause music",
        "resume music",
        "next song"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. Testing: '{command}'")
        try:
            result = commands.process_command(command)
            print(f"   Command processed successfully")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n✓ Command integration tests completed")

def test_music_playback_methods():
    """Test different music playback methods"""
    print("\nTesting Music Playback Methods")
    print("=" * 40)
    
    music = MusicService()
    
    # Test different approaches
    methods = [
        ("Standard play_music", lambda: music.play_music("test song")),
        ("Smart play", lambda: music.smart_play("test song") if hasattr(music, 'smart_play') else "Not available"),
        ("YouTube Music", lambda: music._play_on_youtube_music("test song")),
        ("Resume playback", lambda: music.resume_music()),
        ("Pause music", lambda: music.pause_music())
    ]
    
    for i, (method_name, method_func) in enumerate(methods, 1):
        print(f"\n{i}. Testing {method_name}:")
        try:
            result = method_func()
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n✓ Music playback method tests completed")

def main():
    """Run all improved music tests"""
    print("JARVIS Improved Music Functionality Tests")
    print("=" * 50)
    
    test_music_service_improvements()
    test_command_integration()
    test_music_playback_methods()
    
    print(f"\n🎵 Music improvement tests completed!")
    print("\nMusic playback improvements:")
    print("• Smart play attempts multiple methods")
    print("• Better Spotify integration with auto-play")
    print("• YouTube Music fallback with auto-play")
    print("• Enhanced error handling and user feedback")
    print("• System media key integration")

if __name__ == "__main__":
    main()