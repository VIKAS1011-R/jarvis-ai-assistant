#!/usr/bin/env python3
"""
Smart TTS Manager
Tries multiple TTS engines in order of preference for maximum reliability
"""

from typing import Optional, List
import time

class SmartTTS:
    def __init__(self):
        """Initialize Smart TTS with multiple engine fallbacks"""
        self.engines = []
        self.active_engine = None
        self.engine_names = []
        
    def initialize(self) -> bool:
        """Initialize TTS engines in order of preference"""
        print("Initializing Smart TTS with multiple engines...")
        
        # Try Windows SAPI first (most reliable on Windows)
        try:
            from modules.windows_tts import WindowsTTS
            windows_tts = WindowsTTS(rate=1, volume=90)
            if windows_tts.initialize():
                self.engines.append(windows_tts)
                self.engine_names.append("Windows SAPI")
                print("✓ Windows SAPI TTS available")
        except Exception as e:
            print(f"✗ Windows SAPI TTS failed: {e}")
        
        # Try Edge TTS (high quality neural voices)
        try:
            from modules.edge_tts import EdgeTTS
            edge_tts = EdgeTTS(voice="en-US-DavisNeural")  # Male voice
            if edge_tts.initialize():
                self.engines.append(edge_tts)
                self.engine_names.append("Edge TTS")
                print("✓ Edge TTS available")
        except Exception as e:
            print(f"✗ Edge TTS failed: {e}")
        
        # Try Simple TTS as fallback
        try:
            from modules.simple_tts import SimpleTTS
            simple_tts = SimpleTTS(rate=180, volume=0.9)
            if simple_tts.initialize():
                self.engines.append(simple_tts)
                self.engine_names.append("Simple TTS")
                print("✓ Simple TTS available")
        except Exception as e:
            print(f"✗ Simple TTS failed: {e}")
        
        if self.engines:
            self.active_engine = self.engines[0]
            print(f"✓ Smart TTS initialized with {len(self.engines)} engines")
            print(f"✓ Primary engine: {self.engine_names[0]}")
            return True
        else:
            print("✗ No TTS engines available")
            return False
    
    def speak(self, text: str, print_text: bool = True) -> bool:
        """
        Speak text using the best available engine
        
        Args:
            text: Text to speak
            print_text: Whether to print the text to console
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.engines:
            if print_text:
                print(f"Jarvis (no TTS): {text}")
            return False
        
        # Try each engine until one works
        for i, engine in enumerate(self.engines):
            try:
                success = engine.speak(text, print_text=False)  # Prevent duplicate printing
                if success:
                    if print_text:
                        print(f"Jarvis ({self.engine_names[i]}): {text}")
                    
                    # Move successful engine to front for next time
                    if i > 0:
                        self.engines[0], self.engines[i] = self.engines[i], self.engines[0]
                        self.engine_names[0], self.engine_names[i] = self.engine_names[i], self.engine_names[0]
                        self.active_engine = self.engines[0]
                    
                    return True
                    
            except Exception as e:
                print(f"Engine {self.engine_names[i]} failed: {e}")
                continue
        
        # All engines failed
        if print_text:
            print(f"Jarvis (text-only): {text}")
        return False
    
    def test_all_engines(self) -> bool:
        """Test all available TTS engines"""
        print("Testing all TTS engines...")
        
        if not self.engines:
            print("No engines to test")
            return False
        
        all_passed = True
        
        for i, engine in enumerate(self.engines):
            print(f"\nTesting {self.engine_names[i]}...")
            try:
                success = engine.speak(f"Testing {self.engine_names[i]} engine", print_text=False)
                if success:
                    print(f"✓ {self.engine_names[i]} test passed")
                else:
                    print(f"✗ {self.engine_names[i]} test failed")
                    all_passed = False
            except Exception as e:
                print(f"✗ {self.engine_names[i]} test error: {e}")
                all_passed = False
            
            time.sleep(1)  # Small delay between tests
        
        return all_passed
    
    def get_engine_info(self) -> List[str]:
        """Get information about available engines"""
        return [f"{name} ({'Active' if i == 0 else 'Backup'})" 
                for i, name in enumerate(self.engine_names)]
    
    def switch_engine(self, engine_name: str) -> bool:
        """Switch to a specific engine"""
        try:
            index = self.engine_names.index(engine_name)
            # Move selected engine to front
            self.engines[0], self.engines[index] = self.engines[index], self.engines[0]
            self.engine_names[0], self.engine_names[index] = self.engine_names[index], self.engine_names[0]
            self.active_engine = self.engines[0]
            print(f"Switched to {engine_name}")
            return True
        except ValueError:
            print(f"Engine {engine_name} not found")
            return False
    
    def cleanup(self):
        """Clean up all engines"""
        for engine in self.engines:
            try:
                engine.cleanup()
            except:
                pass
        print("Smart TTS cleaned up")