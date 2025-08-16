#!/usr/bin/env python3
"""
YouTube Music Player Module
Direct YouTube integration for reliable music playback
"""

import webbrowser
import subprocess
import time
import requests
from typing import Optional
import re

class YouTubeMusicPlayer:
    def __init__(self):
        """Initialize YouTube Music Player"""
        self.base_url = "https://www.youtube.com"
        
    def play_song(self, query: str) -> str:
        """
        Play a song directly on YouTube
        
        Args:
            query: Song name, artist, or search query
            
        Returns:
            str: Status message
        """
        try:
            print(f"YouTube Music: Searching for '{query}'")
            
            # Method 1: Try to get direct video URL
            video_url = self._get_first_video_url(query)
            
            if video_url:
                print(f"Found direct video URL: {video_url}")
                webbrowser.open(video_url)
                return f"Playing '{query}' on YouTube."
            else:
                # Method 2: Fallback to search with auto-play attempt
                return self._search_and_autoplay(query)
                
        except Exception as e:
            print(f"YouTube play error: {e}")
            return f"I couldn't play '{query}' on YouTube."
    
    def _get_first_video_url(self, query: str) -> Optional[str]:
        """
        Get the URL of the first video result
        
        Args:
            query: Search query
            
        Returns:
            str: Video URL or None
        """
        try:
            # Search YouTube and try to extract first video URL
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            
            # Make request to get search results
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Look for video URLs in the response
                video_pattern = r'/watch\?v=([a-zA-Z0-9_-]{11})'
                matches = re.findall(video_pattern, response.text)
                
                if matches:
                    video_id = matches[0]  # Get first video
                    video_url = f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
                    return video_url
            
            return None
            
        except Exception as e:
            print(f"Error getting video URL: {e}")
            return None
    
    def _search_and_autoplay(self, query: str) -> str:
        """Search YouTube and attempt autoplay"""
        try:
            # Add terms that are more likely to find music
            music_query = f"{query} official audio music"
            search_url = f"https://www.youtube.com/results?search_query={music_query.replace(' ', '+')}"
            
            webbrowser.open(search_url)
            time.sleep(3)
            
            # Try to click first video
            self._click_first_video()
            
            return f"Playing '{query}' on YouTube."
            
        except Exception as e:
            print(f"Search and autoplay error: {e}")
            return f"Opened YouTube search for '{query}'."
    
    def _click_first_video(self):
        """Attempt to click the first video in YouTube search results"""
        try:
            import time
            
            # Multiple approaches to click first video
            click_attempts = [
                # Attempt 1: Tab to first video, then Enter
                "{TAB}{TAB}{TAB}{TAB}{ENTER}",
                
                # Attempt 2: Just Enter (might work if focus is on first result)
                "{ENTER}",
                
                # Attempt 3: Down arrow then Enter
                "{DOWN}{ENTER}",
                
                # Attempt 4: Tab more times (different page layouts)
                "{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{ENTER}",
            ]
            
            for i, keys in enumerate(click_attempts):
                try:
                    subprocess.run(['powershell', '-Command', 
                                  f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{keys}")'], 
                                  capture_output=True)
                    time.sleep(2)  # Wait between attempts
                except Exception as e:
                    print(f"Click attempt {i+1} failed: {e}")
                    
        except Exception as e:
            print(f"Click first video error: {e}")
    
    def play_youtube_music(self, query: str) -> str:
        """Play on YouTube Music specifically"""
        try:
            # YouTube Music has better auto-play
            music_query = f"{query} song"
            youtube_music_url = f"https://music.youtube.com/search?q={music_query.replace(' ', '+')}"
            
            webbrowser.open(youtube_music_url)
            time.sleep(3)
            
            # YouTube Music often auto-plays first result
            # But we can try to ensure it plays
            self._youtube_music_autoplay()
            
            return f"Playing '{query}' on YouTube Music."
            
        except Exception as e:
            print(f"YouTube Music error: {e}")
            return f"Opened YouTube Music search for '{query}'."
    
    def _youtube_music_autoplay(self):
        """Attempt autoplay on YouTube Music"""
        try:
            import time
            
            # YouTube Music specific automation
            autoplay_attempts = [
                " ",  # Space bar
                "{ENTER}",  # Enter key
                "{TAB}{ENTER}",  # Tab then Enter
                "{MEDIA_PLAY_PAUSE}",  # Media key
            ]
            
            for keys in autoplay_attempts:
                try:
                    subprocess.run(['powershell', '-Command', 
                                  f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{keys}")'], 
                                  capture_output=True)
                    time.sleep(1)
                except:
                    continue
                    
        except Exception as e:
            print(f"YouTube Music autoplay error: {e}")

# Test function
def test_youtube_music_player():
    """Test the YouTube music player"""
    print("Testing YouTube Music Player")
    print("=" * 30)
    
    player = YouTubeMusicPlayer()
    
    print("1. Testing direct video URL extraction:")
    video_url = player._get_first_video_url("test song")
    print(f"   Video URL found: {video_url is not None}")
    if video_url:
        print(f"   URL: {video_url}")
    
    print("\n2. Testing YouTube Music play:")
    result = player.play_youtube_music("test song")
    print(f"   Result: {result}")

if __name__ == "__main__":
    test_youtube_music_player()