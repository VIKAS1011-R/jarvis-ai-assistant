#!/usr/bin/env python3
"""
Test script to verify actual music autoplay functionality
"""

import sys
import os
import time
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.music_service import MusicService

def test_spotify_autoplay():
    """Test if Spotify actually plays music automatically"""
    print("Testing Spotify Autoplay")
    print("=" * 30)
    
    music = MusicService()
    
    print("1. Checking Spotify status:")
    spotify_installed = music._is_spotify_installed()
    spotify_running = music._is_spotify_running()
    print(f"   Spotify installed: {spotify_installed}")
    print(f"   Spotify running: {spotify_running}")
    
    if spotify_installed:
        print("\n2. Testing current play method:")
        result = music.play_music("test song")
        print(f"   Result: {result}")
        
        print("\n3. The issue:")
        print("   - Spotify opens with search")
        print("   - But doesn't automatically play the first result")
        print("   - User still needs to click play manually")
        
        print("\n4. What we need:")
        print("   - Automatic selection of first search result")
        print("   - Automatic playback initiation")
        print("   - No manual user interaction required")
    else:
        print("   Spotify not installed - cannot test autoplay")

def test_alternative_approaches():
    """Test alternative approaches for music playback"""
    print("\nTesting Alternative Approaches")
    print("=" * 30)
    
    print("1. Web-based approach:")
    print("   - Open Spotify Web Player")
    print("   - Attempt to automate web interactions")
    
    print("\n2. System integration approach:")
    print("   - Use Windows media controls")
    print("   - Integrate with system audio")
    
    print("\n3. API approach:")
    print("   - Use Spotify Web API")
    print("   - Requires authentication setup")

if __name__ == "__main__":
    test_spotify_autoplay()
    test_alternative_approaches()