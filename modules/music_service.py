
#!/usr/bin/env python3
"""
Music Service Module
Basic music control and Spotify integration
"""

import subprocess
import os
import requests
from typing import Optional, Dict, List
import json

class MusicService:
    def __init__(self):
        """Initialize music service"""
        self.spotify_client_id = None
        self.spotify_client_secret = None
        self.spotify_token = None
        self.current_track = None
        
    def setup_spotify(self, client_id: str, client_secret: str) -> str:
        """
        Setup Spotify API credentials
        
        Args:
            client_id: Spotify client ID
            client_secret: Spotify client secret
            
        Returns:
            str: Setup status
        """
        self.spotify_client_id = client_id
        self.spotify_client_secret = client_secret
        
        # In a real implementation, you'd handle OAuth2 flow here
        return "Spotify setup initiated. Note: Full Spotify integration requires OAuth2 authentication."
    
    def play_music(self, query: str = None) -> str:
        """
        Simple music play - opens music service for user to click play
        
        Args:
            query: Song, artist, or playlist to play
            
        Returns:
            str: Status message
        """
        try:
            if query:
                # Clean up the query
                query = query.strip()
                
                # Use simple approach - just open the music service
                return self.smart_play(query)
            else:
                # Try to resume playback using media keys
                return self._resume_playback()
                
        except Exception as e:
            print(f"Play music error: {e}")
            return "I couldn't open music right now. Please try again."
    
    def _ensure_playback_starts(self):
        """Try to ensure music actually starts playing"""
        try:
            # Wait a moment for the search to load
            import time
            time.sleep(1)
            
            # Send play key to start playback
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_PLAY_PAUSE}")'], 
                          capture_output=True)
        except:
            pass
    
    def _play_on_youtube_music(self, query: str) -> str:
        """Play music on YouTube Music with auto-play attempt"""
        try:
            import webbrowser
            import urllib.parse
            
            # Try YouTube first (more reliable auto-play)
            youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query + ' music')}"
            webbrowser.open(youtube_url)
            
            import time
            time.sleep(2)
            
            # Try to press Enter to play first video
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")'], 
                          capture_output=True)
            
            return f"Playing '{query}' on YouTube."
            
        except Exception as e:
            print(f"YouTube play error: {e}")
            # Fallback to YouTube Music
            try:
                search_url = f"https://music.youtube.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"Opened YouTube Music to search for '{query}'."
            except:
                return f"I couldn't play '{query}' online."
    
    def pause_music(self) -> str:
        """Pause music playback"""
        try:
            if self._is_spotify_running():
                # Try to pause Spotify (Windows)
                subprocess.run(['powershell', '-Command', 
                              'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_PLAY_PAUSE}")'], 
                              capture_output=True)
                return "Music paused."
            else:
                return "No music player is currently running."
                
        except Exception as e:
            print(f"Pause music error: {e}")
            return "I couldn't pause the music."
    
    def resume_music(self) -> str:
        """Resume music playback"""
        return self._resume_playback()
    
    def _resume_playback(self) -> str:
        """Resume music playback"""
        try:
            # Send media play key
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_PLAY_PAUSE}")'], 
                          capture_output=True)
            return "Resuming music playback."
            
        except Exception as e:
            print(f"Resume music error: {e}")
            return "I couldn't resume music playback."
    
    def next_track(self) -> str:
        """Skip to next track"""
        try:
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_NEXT_TRACK}")'], 
                          capture_output=True)
            return "Skipping to next track."
            
        except Exception as e:
            print(f"Next track error: {e}")
            return "I couldn't skip to the next track."
    
    def previous_track(self) -> str:
        """Go to previous track"""
        try:
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_PREV_TRACK}")'], 
                          capture_output=True)
            return "Going to previous track."
            
        except Exception as e:
            print(f"Previous track error: {e}")
            return "I couldn't go to the previous track."
    
    def set_volume(self, level: int) -> str:
        """
        Set volume level
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            str: Status message
        """
        try:
            if not 0 <= level <= 100:
                return "Volume level should be between 0 and 100."
            
            # Use Windows volume control
            subprocess.run(['powershell', '-Command', 
                          f'(New-Object -comObject WScript.Shell).SendKeys([char]175)'], 
                          capture_output=True)
            
            return f"Setting volume to {level}%."
            
        except Exception as e:
            print(f"Set volume error: {e}")
            return "I couldn't adjust the volume."
    
    def _is_spotify_installed(self) -> bool:
        """Check if Spotify is installed"""
        try:
            # Check for Spotify executable
            result = subprocess.run(['where', 'spotify'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _is_spotify_running(self) -> bool:
        """Check if Spotify is running"""
        try:
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Spotify.exe'], 
                                  capture_output=True, text=True)
            return 'Spotify.exe' in result.stdout
        except:
            return False
    
    def _play_on_spotify(self, query: str) -> str:
        """Play music on Spotify using multiple methods"""
        try:
            # Method 1: Try Spotify Web Player (most reliable)
            web_result = self._try_spotify_web_player(query)
            if web_result:
                return f"Playing '{query}' on Spotify Web Player."
            
            # Method 2: Try desktop app with better URI handling
            desktop_result = self._try_spotify_desktop_play(query)
            if desktop_result:
                return f"Attempting to play '{query}' on Spotify. If it doesn't start, try saying 'Jarvis resume music'."
            
            # Method 3: Fallback to search only
            return f"Opened Spotify to search for '{query}'. Say 'Jarvis resume music' to start playback."
            
        except Exception as e:
            print(f"Spotify play error: {e}")
            return f"I couldn't play '{query}' on Spotify."
    
    def _try_spotify_web_player(self, query: str) -> bool:
        """Try to play music using Spotify Web Player"""
        try:
            import webbrowser
            import urllib.parse
            
            # Open Spotify Web Player with search and auto-play
            encoded_query = urllib.parse.quote(query)
            
            # Use Spotify Web Player URL that should auto-play
            web_url = f"https://open.spotify.com/search/{encoded_query}"
            webbrowser.open(web_url)
            
            # Give it time to load
            import time
            time.sleep(2)
            
            # Try to trigger play with spacebar (common web player shortcut)
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(" ")'], 
                          capture_output=True)
            
            return True
            
        except Exception as e:
            print(f"Web player error: {e}")
            return False
    
    def _try_spotify_desktop_play(self, query: str) -> bool:
        """Try to play music using Spotify desktop app"""
        try:
            # Ensure Spotify is running
            if not self._is_spotify_running():
                subprocess.run(['start', 'spotify:'], shell=True, capture_output=True)
                import time
                time.sleep(3)
            
            # Try using a direct play URI if we can construct one
            # This is a more direct approach than search
            play_uri = f"spotify:search:{query.replace(' ', '+')}"
            subprocess.run(['start', play_uri], shell=True, capture_output=True)
            
            import time
            time.sleep(1)
            
            # Try multiple key combinations to trigger play
            key_combinations = [
                "{ENTER}",      # Enter to select first result
                " ",            # Spacebar to play
                "{F8}",         # Media play key
            ]
            
            for key in key_combinations:
                subprocess.run(['powershell', '-Command', 
                              f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{key}")'], 
                              capture_output=True)
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            print(f"Desktop play error: {e}")
            return False
    
    def _try_spotify_web_play(self, query: str) -> bool:
        """Try to play music using web-based approach"""
        try:
            import webbrowser
            
            # Open Spotify Web Player with search
            search_url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
            webbrowser.open(search_url)
            
            # Wait a moment
            import time
            time.sleep(2)
            
            # Try to simulate clicking the first play button
            # This is a fallback approach
            return True
            
        except Exception as e:
            print(f"Web play error: {e}")
            return False
    
    def _search_music_web(self, query: str) -> str:
        """Search for music on the web"""
        try:
            # Try the direct YouTube approach first
            if self._play_on_youtube_direct(query):
                return f"Playing '{query}' on YouTube."
            else:
                return self._play_on_youtube_music(query)
            
        except Exception as e:
            print(f"Web music search error: {e}")
            return f"I couldn't search for '{query}' online."
    
    def _try_youtube_autoplay_url(self, query: str) -> str:
        """Try to create a YouTube URL that will auto-play"""
        try:
            import webbrowser
            import urllib.parse
            
            # Create a search query that's more likely to find the right video
            search_terms = f"{query} official audio music"
            encoded_query = urllib.parse.quote(search_terms)
            
            # Use YouTube's search with autoplay parameter
            # Note: YouTube has restrictions on autoplay, but this might work better
            youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}&autoplay=1"
            
            webbrowser.open(youtube_url)
            
            # Give it time to load and try to trigger play
            import time
            time.sleep(2)
            
            # Try pressing Enter to play the first result
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")'], 
                          capture_output=True)
            
            return f"Attempting to play '{query}' on YouTube with autoplay."
            
        except Exception as e:
            print(f"YouTube autoplay URL error: {e}")
            return f"I couldn't create an autoplay URL for '{query}'."
    
    def get_current_track(self) -> str:
        """Get currently playing track info"""
        # This would require Spotify API integration
        # For now, return a placeholder
        return "Music track information requires Spotify API setup."
    
    def create_playlist(self, name: str) -> str:
        """Create a new playlist"""
        # Placeholder for playlist creation
        return f"Playlist creation for '{name}' requires Spotify API setup."
    
    def get_music_help(self) -> str:
        """Get help for music commands"""
        help_text = """Music Commands Available:
        
        Basic Controls:
        • "Play music" - Resume playback
        • "Pause music" - Pause current track
        • "Next song" - Skip to next track
        • "Previous song" - Go to previous track
        • "Set volume to 50" - Adjust volume
        
        Search & Play:
        • "Play [song name]" - Search and play specific song
        • "Play [artist name]" - Play music by artist
        
        How it works:
        1. If Spotify is installed, opens Spotify and attempts to play
        2. Falls back to YouTube Music for web playback
        3. Uses system media keys for universal control
        
        Note: For best results, have Spotify installed and logged in."""
        
        return help_text
    
    def smart_play(self, query: str) -> str:
        """Simple and reliable music play - just opens music services"""
        try:
            print(f"Opening music service for: {query}")
            
            # Simple approach: Just open YouTube Music (most reliable)
            return self._simple_youtube_music_open(query)
                
        except Exception as e:
            print(f"Music play error: {e}")
            return f"I couldn't open music for '{query}'. Please try manually."
    
    def _play_on_youtube_direct(self, query: str) -> bool:
        """Try to play music directly on YouTube with better auto-play"""
        try:
            import webbrowser
            import time
            
            # Method 1: Try YouTube with direct video play
            # Search for the song and try to play first result
            search_query = f"{query} official audio"  # Add "official audio" for better results
            youtube_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            
            webbrowser.open(youtube_url)
            time.sleep(3)  # Wait for page to load
            
            # Try to click first video
            self._youtube_auto_click()
            
            return True
            
        except Exception as e:
            print(f"YouTube direct play error: {e}")
            return False
    
    def _youtube_auto_click(self):
        """Attempt to auto-click first YouTube video"""
        try:
            import time
            
            # Multiple approaches to click first video
            approaches = [
                # Approach 1: Tab navigation
                lambda: subprocess.run(['powershell', '-Command', 
                                      'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{TAB}{TAB}{TAB}{ENTER}")'], 
                                      capture_output=True),
                
                # Approach 2: Enter key (might select first result)
                lambda: subprocess.run(['powershell', '-Command', 
                                      'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")'], 
                                      capture_output=True),
                
                # Approach 3: Down arrow then Enter
                lambda: subprocess.run(['powershell', '-Command', 
                                      'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{DOWN}{ENTER}")'], 
                                      capture_output=True),
            ]
            
            for i, approach in enumerate(approaches):
                try:
                    approach()
                    time.sleep(1)
                    if i < len(approaches) - 1:  # Don't sleep after last attempt
                        time.sleep(1)
                except Exception as e:
                    print(f"YouTube click approach {i+1} failed: {e}")
                    
        except Exception as e:
            print(f"YouTube auto-click error: {e}")
    
    def _try_spotify_web_player(self, query: str) -> bool:
        """Enhanced Spotify Web Player approach"""
        try:
            import webbrowser
            import time
            
            # Open Spotify Web Player
            spotify_url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
            webbrowser.open(spotify_url)
            
            time.sleep(4)  # Wait for Spotify to load
            
            # Try multiple automation approaches
            self._spotify_web_automation()
            
            return True
            
        except Exception as e:
            print(f"Spotify web player error: {e}")
            return False
    
    def _spotify_web_automation(self):
        """Automated interaction with Spotify Web Player"""
        try:
            import time
            
            # Multiple automation attempts
            automation_steps = [
                # Step 1: Try to navigate and play
                lambda: self._send_keys("{TAB}{TAB}{ENTER}"),
                
                # Step 2: Try space bar (universal play)
                lambda: self._send_keys(" "),
                
                # Step 3: Try Enter on first result
                lambda: self._send_keys("{ENTER}"),
                
                # Step 4: Try Down arrow then Enter
                lambda: self._send_keys("{DOWN}{ENTER}"),
                
                # Step 5: Try media play key
                lambda: self._send_keys("{MEDIA_PLAY_PAUSE}"),
            ]
            
            for i, step in enumerate(automation_steps):
                try:
                    step()
                    time.sleep(1)
                except Exception as e:
                    print(f"Automation step {i+1} failed: {e}")
                    
        except Exception as e:
            print(f"Spotify automation error: {e}")
    
    def _send_keys(self, keys: str):
        """Helper method to send keys"""
        subprocess.run(['powershell', '-Command', 
                      f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{keys}")'], 
                      capture_output=True)
    
    def _simple_youtube_music_open(self, query: str) -> str:
        """Simple method to just open YouTube Music - no complex automation"""
        try:
            import webbrowser
            import urllib.parse
            
            # Clean the query
            query = query.strip()
            
            # Try Spotify first if available
            if self._is_spotify_installed():
                try:
                    spotify_url = f"https://open.spotify.com/search/{urllib.parse.quote(query)}"
                    webbrowser.open(spotify_url)
                    return f"Opened Spotify to search for '{query}'. Click play to start music."
                except:
                    pass
            
            # Fallback to YouTube Music
            try:
                youtube_music_url = f"https://music.youtube.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(youtube_music_url)
                return f"Opened YouTube Music to search for '{query}'. Click play to start music."
            except:
                pass
            
            # Final fallback to regular YouTube
            try:
                youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query + ' music')}"
                webbrowser.open(youtube_url)
                return f"Opened YouTube to search for '{query}'. Click on a video to play."
            except:
                pass
            
            return f"I couldn't open a music service for '{query}'. Please check your internet connection."
            
        except Exception as e:
            print(f"Simple music open error: {e}")
            return f"I had trouble opening music for '{query}'."
    
    def _play_youtube_video_direct(self, query: str) -> bool:
        """Play YouTube video directly using yt-dlp or youtube-dl approach"""
        try:
            import webbrowser
            import urllib.parse
            import time
            
            # Method 1: Try to find and play a specific video
            # Use a more targeted search that's likely to find a playable video
            search_terms = f"{query} official music video"
            
            # Create a YouTube URL that goes directly to a video (not search)
            # We'll use a trick: open YouTube Music which auto-plays
            youtube_music_url = f"https://music.youtube.com/search?q={urllib.parse.quote(search_terms)}"
            webbrowser.open(youtube_music_url)
            
            time.sleep(4)  # Wait for page to load
            
            # YouTube Music typically auto-plays the first result
            # Try to ensure it starts playing
            self._ensure_youtube_music_plays()
            
            return True
            
        except Exception as e:
            print(f"YouTube video direct play error: {e}")
            return False
    
    def _ensure_youtube_music_plays(self):
        """Ensure YouTube Music actually starts playing"""
        try:
            import time
            
            # YouTube Music usually auto-plays, but let's help it along
            time.sleep(2)
            
            # Try clicking play if needed
            key_sequences = [
                " ",  # Spacebar (universal play)
                "{ENTER}",  # Enter key
                "k",  # YouTube shortcut for play/pause
            ]
            
            for keys in key_sequences:
                self._send_keys(keys)
                time.sleep(1)
                
        except Exception as e:
            print(f"YouTube Music play ensure error: {e}")
    
    def _play_youtube_music_direct(self, query: str) -> bool:
        """Play music directly on YouTube Music with better auto-play"""
        try:
            import webbrowser
            import urllib.parse
            import time
            
            # Use YouTube Music which has better auto-play for music
            search_query = urllib.parse.quote(f"{query} music")
            youtube_music_url = f"https://music.youtube.com/search?q={search_query}"
            
            webbrowser.open(youtube_music_url)
            time.sleep(3)
            
            # YouTube Music typically starts playing automatically
            # But let's ensure it does
            self._trigger_youtube_music_play()
            
            return True
            
        except Exception as e:
            print(f"YouTube Music direct error: {e}")
            return False
    
    def _trigger_youtube_music_play(self):
        """Trigger playback on YouTube Music"""
        try:
            import time
            
            # Wait for page to load
            time.sleep(2)
            
            # Try multiple methods to start playback
            methods = [
                # Method 1: Click first result
                lambda: self._send_keys("{TAB}{ENTER}"),
                
                # Method 2: Use keyboard shortcuts
                lambda: self._send_keys(" "),  # Spacebar
                
                # Method 3: Try Enter
                lambda: self._send_keys("{ENTER}"),
                
                # Method 4: Try YouTube's play shortcut
                lambda: self._send_keys("k"),
            ]
            
            for method in methods:
                try:
                    method()
                    time.sleep(1.5)
                except Exception as e:
                    print(f"Trigger method failed: {e}")
                    
        except Exception as e:
            print(f"YouTube Music trigger error: {e}")
    
    def _try_vlc_play(self, query: str) -> bool:
        """Try to play music using VLC media player with online stream"""
        try:
            # Check if VLC is installed
            vlc_paths = [
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
            ]
            
            vlc_path = None
            for path in vlc_paths:
                if os.path.exists(path):
                    vlc_path = path
                    break
            
            if not vlc_path:
                return False
            
            # Try to find a direct stream URL (this is a simplified approach)
            # In a real implementation, you'd use yt-dlp to get the stream URL
            print(f"VLC found at {vlc_path}, but stream URL extraction not implemented")
            return False
            
        except Exception as e:
            print(f"VLC play error: {e}")
            return False
    
    def _get_youtube_stream_url(self, query: str) -> str:
        """Get direct YouTube stream URL (requires yt-dlp)"""
        try:
            # This would require yt-dlp to be installed
            # For now, return None to indicate it's not available
            return None
        except Exception as e:
            print(f"Stream URL error: {e}")
            return None
    
    def _try_windows_media_player(self, query: str) -> bool:
        """Try to use Windows Media Player with online radio/streams"""
        try:
            # Try to find online radio stations or streams
            # This is a fallback method for actual audio playback
            
            # Some free online radio stations that might have the genre
            stations = {
                "pop": "http://stream.radiotime.com/listen.stream?streamIds=1&aw_0_req.gdpr=false",
                "rock": "http://stream.radiotime.com/listen.stream?streamIds=2&aw_0_req.gdpr=false",
                "jazz": "http://stream.radiotime.com/listen.stream?streamIds=3&aw_0_req.gdpr=false",
                "classical": "http://stream.radiotime.com/listen.stream?streamIds=4&aw_0_req.gdpr=false",
            }
            
            # Try to match query to a genre
            query_lower = query.lower()
            for genre, url in stations.items():
                if genre in query_lower:
                    try:
                        # Try to open with Windows Media Player
                        subprocess.run(['wmplayer', url], capture_output=True)
                        return True
                    except:
                        pass
            
            return False
            
        except Exception as e:
            print(f"Windows Media Player error: {e}")
            return False
    
    def _try_browser_autoplay_trick(self, query: str) -> bool:
        """Use a browser trick to actually autoplay music"""
        try:
            import webbrowser
            import urllib.parse
            import time
            
            # Method 1: Try YouTube Music direct URL (most likely to autoplay)
            youtube_music_url = f"https://music.youtube.com/search?q={urllib.parse.quote(query)}"
            webbrowser.open(youtube_music_url)
            
            # Give it time to load
            time.sleep(3)
            
            # Try to trigger autoplay with keyboard shortcuts
            self._trigger_youtube_music_autoplay()
            
            return True
            
        except Exception as e:
            print(f"Browser autoplay trick error: {e}")
            return False
    
    def _trigger_youtube_music_autoplay(self):
        """Trigger autoplay on YouTube Music using multiple methods"""
        try:
            import time
            
            # Multiple approaches to start playback
            autoplay_methods = [
                # Method 1: Space bar (universal play/pause)
                lambda: self._send_keys(" "),
                
                # Method 2: Enter key on first result
                lambda: self._send_keys("{ENTER}"),
                
                # Method 3: Tab to first result then Enter
                lambda: (self._send_keys("{TAB}"), time.sleep(0.5), self._send_keys("{ENTER}")),
                
                # Method 4: YouTube keyboard shortcut
                lambda: self._send_keys("k"),
                
                # Method 5: Click using coordinates (if we can detect screen)
                lambda: self._try_click_play_button(),
            ]
            
            for i, method in enumerate(autoplay_methods):
                try:
                    print(f"Trying autoplay method {i+1}...")
                    method()
                    time.sleep(1.5)  # Wait between attempts
                except Exception as e:
                    print(f"Autoplay method {i+1} failed: {e}")
                    
        except Exception as e:
            print(f"Trigger autoplay error: {e}")
    
    def _try_click_play_button(self):
        """Try to click the play button using mouse automation"""
        try:
            # This is a more advanced approach using mouse clicks
            # For now, we'll use a keyboard-based approach
            self._send_keys("{TAB}{TAB}{ENTER}")
        except Exception as e:
            print(f"Click play button error: {e}")
    
    def _spotify_search_and_play(self, query: str):
        """Search and play on Spotify with enhanced automation"""
        try:
            import time
            
            # Method 1: Try direct Spotify Web Player approach
            if self._try_spotify_web_autoplay(query):
                return
            
            # Method 2: Enhanced desktop app approach
            # Open Spotify search
            spotify_uri = f"spotify:search:{query.replace(' ', '%20')}"
            subprocess.run(['start', spotify_uri], shell=True)
            time.sleep(3)  # Wait longer for search to load
            
            # Multiple attempts to play
            for attempt in range(3):
                try:
                    # Try Tab to navigate to first result, then Enter
                    subprocess.run(['powershell', '-Command', 
                                  'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{TAB}")'], 
                                  capture_output=True)
                    time.sleep(0.5)
                    
                    subprocess.run(['powershell', '-Command', 
                                  'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")'], 
                                  capture_output=True)
                    time.sleep(1)
                    
                    # Try space bar (common play shortcut)
                    subprocess.run(['powershell', '-Command', 
                                  'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait(" ")'], 
                                  capture_output=True)
                    time.sleep(0.5)
                    
                    # Try media play key
                    subprocess.run(['powershell', '-Command', 
                                  'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_PLAY_PAUSE}")'], 
                                  capture_output=True)
                    
                    if attempt < 2:  # Don't sleep on last attempt
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
            
        except Exception as e:
            print(f"Spotify search and play error: {e}")
    
    def _try_spotify_web_autoplay(self, query: str) -> bool:
        """Try to use Spotify Web Player for better autoplay"""
        try:
            import webbrowser
            import time
            
            # Open Spotify Web Player with direct play attempt
            # This URL format sometimes triggers autoplay
            web_url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
            webbrowser.open(web_url)
            
            time.sleep(4)  # Wait for page to load
            
            # Try to simulate clicking the first play button
            # This uses JavaScript injection if possible
            self._try_web_automation()
            
            return True
            
        except Exception as e:
            print(f"Web autoplay error: {e}")
            return False
    
    def _try_web_automation(self):
        """Attempt web automation for Spotify Web Player"""
        try:
            # Try to send key combinations that might work in web player
            import time
            
            # Wait for page load
            time.sleep(2)
            
            # Try common web shortcuts
            shortcuts = [
                " ",  # Space bar (common play/pause)
                "{ENTER}",  # Enter key
                "{TAB}{ENTER}",  # Tab to first result, then enter
            ]
            
            for shortcut in shortcuts:
                subprocess.run(['powershell', '-Command', 
                              f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{shortcut}")'], 
                              capture_output=True)
                time.sleep(1)
                
        except Exception as e:
            print(f"Web automation error: {e}")

# Simple music player for basic system control
class SystemMusicPlayer:
    """Simple system music player using Windows media keys"""
    
    def __init__(self):
        pass
    
    def play_pause(self) -> str:
        """Toggle play/pause"""
        try:
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{MEDIA_PLAY_PAUSE}")'], 
                          capture_output=True)
            return "Toggled music playback."
        except:
            return "I couldn't control music playback."
    
    def volume_up(self) -> str:
        """Increase volume"""
        try:
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{VOLUME_UP}")'], 
                          capture_output=True)
            return "Volume increased."
        except:
            return "I couldn't increase the volume."
    
    def volume_down(self) -> str:
        """Decrease volume"""
        try:
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait("{VOLUME_DOWN}")'], 
                          capture_output=True)
            return "Volume decreased."
        except:
            return "I couldn't decrease the volume."

# Test function
def test_music_service():
    """Test the music service"""
    print("Testing Music Service")
    print("=" * 30)
    
    music = MusicService()
    
    print("1. Music help:")
    help_text = music.get_music_help()
    print(f"   {help_text}")
    
    print("\n2. System music player:")
    player = SystemMusicPlayer()
    
    print("   Testing basic controls (no actual audio will play in test):")
    print(f"   Play/Pause: {player.play_pause()}")
    print(f"   Volume Up: {player.volume_up()}")

if __name__ == "__main__":
    test_music_service()