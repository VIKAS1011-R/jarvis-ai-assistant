#!/usr/bin/env python3
"""
Edge TTS Module - High quality neural voices
Uses Microsoft Edge's TTS engine for better quality speech
"""

import subprocess
import tempfile
import os
import asyncio
import json
from typing import Optional

class EdgeTTS:
    def __init__(self, voice: str = "en-US-AriaNeural", rate: str = "+0%", volume: str = "+0%"):
        """
        Initialize Edge TTS
        
        Args:
            voice: Voice to use (e.g., "en-US-AriaNeural", "en-US-DavisNeural")
            rate: Speech rate (e.g., "+0%", "+20%", "-20%")
            volume: Volume (e.g., "+0%", "+20%", "-20%")
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.is_available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Check if edge-tts is available"""
        try:
            result = subprocess.run(["edge-tts", "--list-voices"], 
                                  capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def initialize(self) -> bool:
        """Initialize Edge TTS"""
        if not self.is_available:
            print("Edge TTS not available. Install with: pip install edge-tts")
            return False
        
        print("Edge TTS initialized")
        return True
    
    def speak(self, text: str, print_text: bool = True) -> bool:
        """
        Convert text to speech using Edge TTS
        
        Args:
            text: Text to speak
            print_text: Whether to print the text to console
            
        Returns:
            bool: True if successful, False otherwise
        """
        if print_text:
            print(f"Jarvis: {text}")
        
        if not self.is_available:
            return False
        
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Generate speech with edge-tts
            cmd = [
                "edge-tts",
                "--voice", self.voice,
                "--rate", self.rate,
                "--volume", self.volume,
                "--text", text,
                "--write-media", temp_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_path):
                # Play the audio file
                self._play_audio(temp_path)
                return True
            else:
                print(f"Edge TTS generation failed: {result.stderr.decode()}")
                return False
                
        except subprocess.TimeoutExpired:
            print("Edge TTS timeout")
            return False
        except Exception as e:
            print(f"Edge TTS Error: {e}")
            return False
        finally:
            # Clean up temporary file
            try:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.unlink(temp_path)
            except:
                pass
    
    def _play_audio(self, audio_path: str):
        """Play audio file using Windows media player"""
        try:
            # Try different audio players
            players = [
                ["powershell", "-c", f"(New-Object Media.SoundPlayer '{audio_path}').PlaySync()"],
                ["start", "/wait", audio_path],
                ["mplay32", "/play", "/close", audio_path]
            ]
            
            for player in players:
                try:
                    subprocess.run(player, check=True, timeout=30)
                    return
                except:
                    continue
            
            print("Could not play audio file")
            
        except Exception as e:
            print(f"Audio playback error: {e}")
    
    def list_voices(self):
        """List available Edge TTS voices"""
        if not self.is_available:
            return []
        
        try:
            result = subprocess.run(["edge-tts", "--list-voices"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("Available Edge TTS voices:")
                lines = result.stdout.strip().split('\n')
                voices = []
                for line in lines:
                    if 'Name:' in line:
                        voice_name = line.split('Name: ')[1].split(',')[0]
                        voices.append(voice_name)
                        print(f"  - {voice_name}")
                return voices
            else:
                print("Could not list Edge TTS voices")
                return []
                
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []
    
    def test_speech(self) -> bool:
        """Test Edge TTS functionality"""
        print("Testing Edge TTS...")
        
        test_phrases = [
            "Edge TTS test one",
            "Edge TTS test two", 
            "Edge TTS test three"
        ]
        
        for i, phrase in enumerate(test_phrases):
            print(f"Test {i+1}: {phrase}")
            success = self.speak(phrase)
            if not success:
                print(f"Test {i+1} failed")
                return False
        
        print("All Edge TTS tests passed!")
        return True
    
    def cleanup(self):
        """Clean up resources"""
        print("Edge TTS cleaned up")