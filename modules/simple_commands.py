#!/usr/bin/env python3
"""
Simple Command Processor
Handles basic voice commands without complexity
"""

import os
import subprocess
import datetime
import webbrowser
from typing import Optional

class SimpleCommands:
    def __init__(self, tts_engine):
        """
        Initialize command processor
        
        Args:
            tts_engine: Text-to-speech engine for responses
        """
        self.tts = tts_engine
        
    def process_command(self, command: str) -> Optional[str]:
        """
        Process a voice command
        
        Args:
            command: The recognized command text
            
        Returns:
            str: Special command result, or None for normal commands
        """
        if not command:
            return None
        
        command = command.lower().strip()
        
        # Time commands
        if "time" in command or "what time" in command:
            self.get_time()
            return None
            
        # Date commands
        if "date" in command or "what date" in command:
            self.get_date()
            return None
        
        # Web commands
        if "open google" in command or "google" in command:
            self.open_website("https://google.com", "Google")
            return None
            
        if "open youtube" in command or "youtube" in command:
            self.open_website("https://youtube.com", "YouTube")
            return None
            
        if "open github" in command or "github" in command:
            self.open_website("https://github.com", "GitHub")
            return None
        
        # Application commands
        if "notepad" in command:
            self.open_app("notepad", "Notepad")
            return None
            
        if "calculator" in command:
            self.open_app("calc", "Calculator")
            return None
            
        if "file explorer" in command or "explorer" in command:
            self.open_app("explorer", "File Explorer")
            return None
        
        # System commands
        if "sleep" in command:
            self.sleep_system()
            return None
        
        # Help command
        if "help" in command or "what can you do" in command:
            self.show_help()
            return None
        
        # Exit commands
        if "goodbye" in command or "exit" in command or "quit" in command:
            self.goodbye()
            return "exit"
        
        # Unknown command
        self.tts.speak(f"I don't understand '{command}'. Say 'help' for available commands.")
        return None
    
    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.tts.speak(f"The current time is {current_time}")
    
    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        self.tts.speak(f"Today is {current_date}")
    
    def open_website(self, url: str, name: str):
        """Open a website"""
        try:
            webbrowser.open(url)
            self.tts.speak(f"Opening {name}")
        except Exception:
            self.tts.speak(f"Unable to open {name}")
    
    def open_app(self, app_command: str, app_name: str):
        """Open an application"""
        try:
            subprocess.Popen([app_command])
            self.tts.speak(f"Opening {app_name}")
        except Exception:
            self.tts.speak(f"Unable to open {app_name}")
    
    def sleep_system(self):
        """Put system to sleep"""
        try:
            self.tts.speak("Putting system to sleep")
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        except Exception:
            self.tts.speak("Unable to put system to sleep")
    
    def show_help(self):
        """Show available commands"""
        help_text = """I can help you with these commands:
        Time: What time is it?
        Date: What date is it?
        Web: Open Google, Open YouTube, Open GitHub
        Apps: Open Notepad, Open Calculator, Open File Explorer
        System: Sleep
        Control: Help, Goodbye"""
        
        self.tts.speak("Here are the commands I understand")
        print(help_text)
    
    def goodbye(self):
        """Say goodbye"""
        self.tts.speak("Goodbye, sir. Jarvis signing off.")