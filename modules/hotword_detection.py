#!/usr/bin/env python3
"""
Hot Word Detection Module
Handles Picovoice Porcupine wake word detection
"""

import os
import struct
import pyaudio
import pvporcupine
from typing import Callable, Optional

class HotWordDetector:
    def __init__(self, access_key: str, keyword_path: str):
        """
        Initialize hot word detector
        
        Args:
            access_key: Picovoice access key
            keyword_path: Path to the .ppn wake word model file
        """
        self.access_key = access_key
        self.keyword_path = keyword_path
        self.porcupine = None
        self.audio_stream = None
        self.pa = None
        self.is_listening = False
        self.callback = None
        
    def initialize(self):
        """Initialize Porcupine and audio stream"""
        try:
            # Verify keyword file exists
            if not os.path.exists(self.keyword_path):
                raise FileNotFoundError(f"Wake word model not found: {self.keyword_path}")
            
            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=self.access_key,
                keyword_paths=[self.keyword_path]
            )
            
            # Initialize PyAudio
            self.pa = pyaudio.PyAudio()
            self.audio_stream = self.pa.open(
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            
            print(f"Hot word detector initialized")
            print(f"Sample rate: {self.porcupine.sample_rate}")
            print(f"Frame length: {self.porcupine.frame_length}")
            
        except Exception as e:
            print(f"Error initializing hot word detector: {e}")
            self.cleanup()
            raise
    
    def set_callback(self, callback: Callable):
        """
        Set callback function to be called when wake word is detected
        
        Args:
            callback: Function to call when wake word is detected
        """
        self.callback = callback
    
    def start_listening(self):
        """Start listening for wake word"""
        if not self.porcupine or not self.audio_stream:
            raise RuntimeError("Detector not initialized. Call initialize() first.")
        
        self.is_listening = True
        print("Listening for wake word...")
        
        try:
            while self.is_listening:
                # Read audio frame
                pcm = self.audio_stream.read(self.porcupine.frame_length)
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                
                # Process audio frame
                keyword_index = self.porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print("Wake word detected!")
                    if self.callback:
                        self.callback()
                        
        except KeyboardInterrupt:
            print("Stopping wake word detection...")
        except Exception as e:
            print(f"Error during wake word detection: {e}")
        finally:
            self.stop_listening()
    
    def stop_listening(self):
        """Stop listening for wake word"""
        self.is_listening = False
        print("Wake word detection stopped")
    
    def cleanup(self):
        """Clean up resources"""
        self.is_listening = False
        
        if self.audio_stream:
            self.audio_stream.close()
            self.audio_stream = None
            
        if self.pa:
            self.pa.terminate()
            self.pa = None
            
        if self.porcupine:
            self.porcupine.delete()
            self.porcupine = None
            
        print("Hot word detector resources cleaned up")
    
    def __enter__(self):
        """Context manager entry"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()