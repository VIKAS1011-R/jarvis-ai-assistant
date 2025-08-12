#!/usr/bin/env python3
"""
J.A.R.V.I.S - Just A Rather Very Intelligent System
Modular voice assistant with hot word detection and text-to-speech
"""

# Fix distutils compatibility for Python 3.12+
try:
    import distutils
except ImportError:
    try:
        import setuptools
        print("Using setuptools for distutils compatibility")
    except ImportError:
        print("Error: distutils/setuptools not found. Run: python fix_distutils.py")
        exit(1)

import threading
from modules.config import config
from modules.hotword_detection import HotWordDetector
from modules.smart_tts import SmartTTS
from modules.jarvis_responses import JarvisResponses
from modules.simple_speech import SimpleSpeech
from modules.simple_commands import SimpleCommands

class JarvisAssistant:
    def __init__(self):
        """Initialize Jarvis with modular components"""
        print("Jarvis initializing...")
        
        # Validate configuration
        if not config.validate_setup():
            raise RuntimeError("Configuration validation failed")
        
        # Initialize modules
        self.tts = SmartTTS()
        self.hotword_detector = HotWordDetector(
            access_key=config.picovoice_access_key,
            keyword_path=config.wake_word_model_path
        )
        self.speech = SimpleSpeech()
        self.commands = SimpleCommands(self.tts)
        
        # Set up wake word callback
        self.hotword_detector.set_callback(self.on_wake_word_detected)
        
    def on_wake_word_detected(self):
        """Callback function when wake word is detected"""
        print("Wake word 'Jarvis' detected!")
        # Run greeting in separate thread to avoid blocking audio
        threading.Thread(target=self.greet_user, daemon=True).start()
        
    def greet_user(self):
        """Greet user and listen for command"""
        try:
            greeting = JarvisResponses.get_random_greeting()
            self.tts.speak(greeting)
            
            # Listen for command
            command = self.speech.listen_for_command()
            
            if command:
                result = self.commands.process_command(command)
                if result == "exit":
                    self.hotword_detector.stop_listening()
            else:
                # No command detected
                responses = ["Standing by.", "Ready for orders.", "At your service."]
                import random
                self.tts.speak(random.choice(responses))
            
        except Exception as e:
            print(f"Error in greet_user: {e}")
            print(f"Jarvis: {JarvisResponses.get_random_greeting()}")
        
    def start(self):
        """Start the Jarvis assistant"""
        try:
            # Initialize components
            print("Initializing TTS engine...")
            self.tts.initialize()
            
            print("Initializing hotword detector...")
            self.hotword_detector.initialize()
            
            print("Initializing speech recognition...")
            self.speech.initialize()
            
            # Startup greeting
            startup_message = JarvisResponses.get_random_startup()
            self.tts.speak(startup_message)
            
            # Start listening for wake word
            self.hotword_detector.start_listening()
            
        except KeyboardInterrupt:
            print("\nShutting down Jarvis...")
            shutdown_message = JarvisResponses.get_random_shutdown()
            self.tts.speak(shutdown_message)
        except Exception as e:
            print(f"Error starting Jarvis: {e}")
            error_message = JarvisResponses.get_random_error()
            self.tts.speak(error_message)
        finally:
            self.cleanup()
            
    def cleanup(self):
        """Clean up all resources"""
        if hasattr(self, 'hotword_detector'):
            self.hotword_detector.cleanup()
        if hasattr(self, 'tts'):
            self.tts.cleanup()
        if hasattr(self, 'speech'):
            self.speech.cleanup()
        print("Jarvis shutdown complete")

def main():
    """Main entry point"""
    try:
        jarvis = JarvisAssistant()
        jarvis.start()
    except Exception as e:
        print(f"Failed to start Jarvis: {e}")

if __name__ == "__main__":
    main()