#!/usr/bin/env python3
"""
Windows TTS Module using SAPI (Speech API)
Much more reliable than pyttsx3 for Windows systems
"""

import subprocess
import tempfile
import os
import time
from typing import Optional

class WindowsTTS:
    def __init__(self, rate: int = 0, volume: int = 100):
        """
        Initialize Windows TTS using SAPI
        
        Args:
            rate: Speech rate (-10 to 10, 0 is normal)
            volume: Volume (0 to 100)
        """
        self.rate = max(-10, min(10, rate))
        self.volume = max(0, min(100, volume))
        self.voice = "Microsoft David Desktop"  # Default male voice
        self.is_available = self._check_availability()
        
    def _check_availability(self) -> bool:
        """Check if Windows SAPI is available"""
        try:
            # Test PowerShell TTS command
            test_cmd = [
                "powershell", "-Command",
                "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Dispose()"
            ]
            result = subprocess.run(test_cmd, capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def initialize(self) -> bool:
        """Initialize the TTS engine"""
        if not self.is_available:
            print("Windows SAPI TTS not available")
            return False
        
        print("Windows SAPI TTS initialized")
        return True
    
    def speak(self, text: str, print_text: bool = True) -> bool:
        """
        Convert text to speech using Windows SAPI
        
        Args:
            text: Text to speak
            print_text: Whether to print the text to console
            
        Returns:
            bool: True if successful, False otherwise
        """
        if print_text:
            print(f"Jarvis: {text}")
        
        if not self.is_available:
            print("TTS not available")
            return False
        
        try:
            # Escape quotes in text
            escaped_text = text.replace('"', '""')
            
            # PowerShell command for TTS
            ps_command = f'''
            Add-Type -AssemblyName System.Speech
            $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speak.Rate = {self.rate}
            $speak.Volume = {self.volume}
            $speak.Speak("{escaped_text}")
            $speak.Dispose()
            '''
            
            # Execute PowerShell command
            result = subprocess.run([
                "powershell", "-Command", ps_command
            ], capture_output=True, timeout=30)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("TTS timeout")
            return False
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def speak_async(self, text: str, print_text: bool = True) -> bool:
        """
        Speak text asynchronously (non-blocking)
        
        Args:
            text: Text to speak
            print_text: Whether to print the text to console
            
        Returns:
            bool: True if started successfully, False otherwise
        """
        if print_text:
            print(f"Jarvis: {text}")
        
        if not self.is_available:
            return False
        
        try:
            escaped_text = text.replace('"', '""')
            
            ps_command = f'''
            Add-Type -AssemblyName System.Speech
            $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speak.Rate = {self.rate}
            $speak.Volume = {self.volume}
            $speak.SpeakAsync("{escaped_text}")
            Start-Sleep -Seconds 0.1
            $speak.Dispose()
            '''
            
            # Start process without waiting
            subprocess.Popen([
                "powershell", "-Command", ps_command
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return True
            
        except Exception as e:
            print(f"Async TTS Error: {e}")
            return False
    
    def set_voice(self, voice_name: str):
        """Set the voice to use"""
        self.voice = voice_name
    
    def set_rate(self, rate: int):
        """Set speech rate (-10 to 10)"""
        self.rate = max(-10, min(10, rate))
    
    def set_volume(self, volume: int):
        """Set volume (0 to 100)"""
        self.volume = max(0, min(100, volume))
    
    def list_voices(self):
        """List available voices"""
        try:
            ps_command = '''
            Add-Type -AssemblyName System.Speech
            $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speak.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
            $speak.Dispose()
            '''
            
            result = subprocess.run([
                "powershell", "-Command", ps_command
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                voices = result.stdout.strip().split('\n')
                print("Available voices:")
                for voice in voices:
                    if voice.strip():
                        print(f"  - {voice.strip()}")
                return voices
            else:
                print("Could not list voices")
                return []
                
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []
    
    def test_speech(self) -> bool:
        """Test TTS functionality"""
        print("Testing Windows SAPI TTS...")
        
        test_phrases = [
            "Windows TTS test one",
            "Windows TTS test two",
            "Windows TTS test three"
        ]
        
        for i, phrase in enumerate(test_phrases):
            print(f"Test {i+1}: {phrase}")
            success = self.speak(phrase)
            if not success:
                print(f"Test {i+1} failed")
                return False
            time.sleep(0.5)
        
        print("All Windows TTS tests passed!")
        return True
    
    def cleanup(self):
        """Clean up resources (nothing to clean for Windows SAPI)"""
        print("Windows TTS cleaned up")