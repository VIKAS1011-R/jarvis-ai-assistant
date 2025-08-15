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
from modules.continuous_listener import ContinuousListener
from modules.smart_tts import SmartTTS
from modules.jarvis_responses import JarvisResponses
from modules.simple_commands import SimpleCommands

class JarvisAssistant:
    def __init__(self):
        """Initialize Jarvis with continuous listening"""
        print("Jarvis initializing with continuous listening...")
        
        # Validate configuration
        if not config.validate_setup():
            raise RuntimeError("Configuration validation failed")
        
        # Initialize modules
        self.tts = SmartTTS()
        self.listener = ContinuousListener(
            wake_words=["jarvis", "hey jarvis", "ok jarvis"],
            timeout=15,  # Longer timeout for natural speech
            phrase_timeout=3
        )
        self.commands = SimpleCommands(self.tts)
        
        # Set up continuous listening callback
        self.listener.set_callback(self.on_wake_word_and_command)
        
    def on_wake_word_and_command(self, wake_word: str, command: str):
        """Callback function when wake word and command are detected"""
        print(f"Wake word '{wake_word}' detected!")
        
        if command:
            print(f"Processing command: '{command}'")
            # Process command directly without additional greeting
            threading.Thread(target=self.process_command_directly, args=(command,), daemon=True).start()
        else:
            # No command found, give a brief acknowledgment
            print("No command detected after wake word")
            threading.Thread(target=self.acknowledge_wake_word, daemon=True).start()
    
    def process_command_directly(self, command: str):
        """Process command directly without greeting"""
        try:
            result = self.commands.process_command(command)
            if result == "exit":
                self.listener.stop_listening()
        except Exception as e:
            print(f"Error processing command: {e}")
            self.tts.speak("I encountered an error processing that command.")
    
    def acknowledge_wake_word(self):
        """Brief acknowledgment when wake word is detected without command"""
        try:
            responses = ["Yes?", "How can I help?", "I'm listening.", "What can I do for you?"]
            import random
            self.tts.speak(random.choice(responses))
        except Exception as e:
            print(f"Error in acknowledgment: {e}")
        
    def start(self):
        """Start the Jarvis assistant with continuous listening"""
        try:
            # Initialize components
            print("Initializing TTS engine...")
            self.tts.initialize()
            
            print("Initializing continuous listener...")
            self.listener.initialize()
            
            # Startup greeting
            startup_message = JarvisResponses.get_random_startup()
            self.tts.speak(startup_message)
            
            print("\n" + "="*60)
            print("JARVIS CONTINUOUS LISTENING MODE")
            print("="*60)
            print("Say: 'Jarvis [command]' in one sentence")
            print("Examples:")
            print("  • 'Jarvis what time is it'")
            print("  • 'Hey Jarvis search for Python tutorials'")
            print("  • 'OK Jarvis open Google'")
            print("  • 'Jarvis exit' to quit")
            print("="*60)
            
            # Start continuous listening
            self.listener.start_listening()
            
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
        if hasattr(self, 'listener'):
            self.listener.cleanup()
        if hasattr(self, 'tts'):
            self.tts.cleanup()
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