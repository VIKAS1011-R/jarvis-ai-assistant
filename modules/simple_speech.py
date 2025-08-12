#!/usr/bin/env python3
"""
Simple Speech Recognition Module
Lightweight speech-to-text for voice commands
"""

import speech_recognition as sr
import threading
import time

class SimpleSpeech:
    def __init__(self, timeout=3, phrase_timeout=1):
        """
        Initialize simple speech recognizer
        
        Args:
            timeout: Maximum time to wait for speech
            phrase_timeout: Time to wait after speech ends
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.timeout = timeout
        self.phrase_timeout = phrase_timeout
        
    def initialize(self):
        """Initialize and calibrate microphone"""
        try:
            print("Calibrating microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("✓ Speech recognition ready")
            return True
        except Exception as e:
            print(f"✗ Speech recognition failed: {e}")
            return False
    
    def listen_for_command(self):
        """
        Listen for a voice command
        
        Returns:
            str: Recognized command text, or None if failed
        """
        try:
            print("Listening for command...")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.timeout, 
                    phrase_time_limit=self.phrase_timeout
                )
            
            print("Processing speech...")
            
            # Use Google's speech recognition
            command = self.recognizer.recognize_google(audio)
            print(f"Command: '{command}'")
            return command.lower().strip()
            
        except sr.WaitTimeoutError:
            print("No command detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand command")
            return None
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return None
        except Exception as e:
            print(f"Speech error: {e}")
            return None
    
    def cleanup(self):
        """Clean up resources"""
        print("Speech recognition cleaned up")