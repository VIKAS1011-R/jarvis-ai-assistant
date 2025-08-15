#!/usr/bin/env python3
"""
Simple Command Processor
Handles basic voice commands without complexity
"""

import os
import subprocess
import datetime
import webbrowser
import re
from typing import Optional
from modules.joke_service import JokeService
from modules.weather_service import WeatherService
from modules.calculator_service import CalculatorService
from modules.system_service import SystemService
from modules.timer_service import TimerService

class SimpleCommands:
    def __init__(self, tts_engine):
        """
        Initialize command processor
        
        Args:
            tts_engine: Text-to-speech engine for responses
        """
        self.tts = tts_engine
        self.joke_service = JokeService()
        self.weather_service = WeatherService()
        self.calculator_service = CalculatorService()
        self.system_service = SystemService()
        self.timer_service = TimerService(tts_engine)
        
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
        
        # Timer and reminder commands (check before time commands)
        if re.search(r'\btimer\b', command, re.IGNORECASE):
            if re.search(r'\b(start|set)\b', command, re.IGNORECASE):
                self.start_timer(command)
            elif re.search(r'\b(stop|cancel)\b', command, re.IGNORECASE):
                self.stop_timer(command)
            elif re.search(r'\b(list|show)\b', command, re.IGNORECASE):
                self.list_timers()
            return None
        
        if re.search(r'\b(remind me|reminder)\b', command, re.IGNORECASE):
            self.set_reminder(command)
            return None
        
        # Time commands (use word boundaries to avoid false matches)
        if re.search(r'\b(time|what time)\b', command, re.IGNORECASE):
            self.get_time()
            return None
            
        # Date commands
        if re.search(r'\b(date|what date)\b', command, re.IGNORECASE):
            self.get_date()
            return None
        
        # Web commands
        if re.search(r'\b(open google|google)\b', command, re.IGNORECASE):
            self.open_website("https://google.com", "Google")
            return None
            
        if re.search(r'\b(open youtube|youtube)\b', command, re.IGNORECASE):
            self.open_website("https://youtube.com", "YouTube")
            return None
            
        if re.search(r'\b(open github|github)\b', command, re.IGNORECASE):
            self.open_website("https://github.com", "GitHub")
            return None
        
        # Application commands
        if re.search(r'\bnotepad\b', command, re.IGNORECASE):
            self.open_app("notepad", "Notepad")
            return None
            
        if re.search(r'\bcalculator\b', command, re.IGNORECASE):
            self.open_app("calc", "Calculator")
            return None
            
        if re.search(r'\b(file explorer|explorer)\b', command, re.IGNORECASE):
            self.open_app("explorer", "File Explorer")
            return None
        
        # System commands
        if re.search(r'\bsleep\b', command, re.IGNORECASE):
            self.sleep_system()
            return None
        
        # Weather commands
        if re.search(r'\bweather\b', command, re.IGNORECASE):
            if re.search(r'\bforecast\b', command, re.IGNORECASE):
                self.get_weather_forecast(command)
            else:
                self.get_weather(command)
            return None
        
        # Unit conversion commands (check before calculator to avoid conflicts)
        if re.search(r'\bconvert\b', command, re.IGNORECASE) and (re.search(r'\bto\b', command, re.IGNORECASE) or re.search(r'\binto\b', command, re.IGNORECASE)):
            self.convert_units(command)
            return None
        
        # Calculator commands
        if re.search(r'\b(calculate|math|plus|minus|times|divide|multiply|add|subtract)\b', command, re.IGNORECASE):
            self.calculate(command)
            return None
        
        # System information commands
        if re.search(r'\b(system info|system information)\b', command, re.IGNORECASE):
            self.get_system_info()
            return None
        
        if re.search(r'\b(disk space|storage)\b', command, re.IGNORECASE):
            self.get_disk_space()
            return None
        
        if re.search(r'\b(battery|battery level)\b', command, re.IGNORECASE):
            self.get_battery_info()
            return None
        
        if re.search(r'\b(running processes|task manager)\b', command, re.IGNORECASE):
            self.get_running_processes()
            return None
        
        if re.search(r'\b(network|ip address)\b', command, re.IGNORECASE):
            self.get_network_info()
            return None
        
        if re.search(r'\buptime\b', command, re.IGNORECASE):
            self.get_uptime()
            return None
        
        # File management commands
        if re.search(r'\b(create folder|make folder|new folder)\b', command, re.IGNORECASE):
            self.create_folder(command)
            return None
        
        if re.search(r'\b(list files|show files)\b', command, re.IGNORECASE):
            self.list_files(command)
            return None
        

        
        # Joke commands
        if re.search(r'\b(joke|tell me a joke|make me laugh)\b', command, re.IGNORECASE):
            if re.search(r'\b(programming|coding|developer)\b', command, re.IGNORECASE):
                self.tell_programming_joke()
            elif re.search(r'\b(dad|dad joke)\b', command, re.IGNORECASE):
                self.tell_dad_joke()
            else:
                self.tell_joke()
            return None
        
        # Help command
        if re.search(r'\b(help|what can you do)\b', command, re.IGNORECASE):
            self.show_help()
            return None
        
        # Exit commands
        if re.search(r'\b(goodbye|exit|quit)\b', command, re.IGNORECASE):
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
    
    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = self.joke_service.get_joke()
            self.tts.speak(joke)
        except Exception as e:
            print(f"Error getting joke: {e}")
            self.tts.speak("Sorry, I couldn't fetch a joke right now. My humor module seems to be offline!")
    
    def tell_programming_joke(self):
        """Tell a programming joke"""
        try:
            joke = self.joke_service.get_programming_joke()
            self.tts.speak(joke)
        except Exception as e:
            print(f"Error getting programming joke: {e}")
            self.tts.speak("Sorry, my programming humor database is experiencing a null pointer exception!")
    
    def tell_dad_joke(self):
        """Tell a dad joke"""
        try:
            joke = self.joke_service.get_dad_joke()
            self.tts.speak(joke)
        except Exception as e:
            print(f"Error getting dad joke: {e}")
            self.tts.speak("Sorry, my dad joke collection is currently unavailable. That's not very a-peel-ing!")
    
    # Weather commands
    def get_weather(self, command: str):
        """Get current weather"""
        try:
            # Extract location if specified
            location = self._extract_location(command)
            weather = self.weather_service.get_weather(location)
            self.tts.speak(weather)
        except Exception as e:
            print(f"Error getting weather: {e}")
            self.tts.speak("I'm unable to get the weather information right now.")
    
    def get_weather_forecast(self, command: str):
        """Get weather forecast"""
        try:
            location = self._extract_location(command)
            forecast = self.weather_service.get_forecast(location)
            self.tts.speak(forecast)
        except Exception as e:
            print(f"Error getting forecast: {e}")
            self.tts.speak("I'm unable to get the weather forecast right now.")
    
    def _extract_location(self, command: str) -> Optional[str]:
        """Extract location from weather command"""
        # Look for patterns like "weather in London" or "weather for New York"
        patterns = [
            r'weather (?:in|for|at) (.+)',
            r'(?:in|for|at) (.+) weather'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    # Calculator commands
    def calculate(self, command: str):
        """Perform calculation"""
        try:
            # Remove "calculate" from the command
            expression = re.sub(r'\b(calculate|math|what is|what\'s)\b', '', command, flags=re.IGNORECASE).strip()
            result = self.calculator_service.calculate(expression)
            self.tts.speak(result)
        except Exception as e:
            print(f"Error calculating: {e}")
            self.tts.speak("I couldn't perform that calculation.")
    
    def convert_units(self, command: str):
        """Convert units"""
        try:
            # Parse conversion command
            # Pattern: "convert X Y to Z" or "X Y to Z"
            pattern = r'(?:convert\s+)?(\d+(?:\.\d+)?)\s+(\w+(?:\s+\w+)?)\s+(?:to|into)\s+(\w+(?:\s+\w+)?)'
            match = re.search(pattern, command, re.IGNORECASE)
            
            if match:
                amount = float(match.group(1))
                from_unit = match.group(2).strip()
                to_unit = match.group(3).strip()
                
                result = self.calculator_service.convert_units(amount, from_unit, to_unit)
                self.tts.speak(result)
            else:
                self.tts.speak("I couldn't understand that conversion. Try something like 'convert 5 feet to meters'.")
        except Exception as e:
            print(f"Error converting units: {e}")
            self.tts.speak("I couldn't perform that conversion.")
    
    # System information commands
    def get_system_info(self):
        """Get system information"""
        try:
            info = self.system_service.get_system_info()
            self.tts.speak(info)
        except Exception as e:
            print(f"Error getting system info: {e}")
            self.tts.speak("I couldn't retrieve system information.")
    
    def get_disk_space(self):
        """Get disk space information"""
        try:
            info = self.system_service.get_disk_space()
            self.tts.speak(info)
        except Exception as e:
            print(f"Error getting disk space: {e}")
            self.tts.speak("I couldn't retrieve disk space information.")
    
    def get_battery_info(self):
        """Get battery information"""
        try:
            info = self.system_service.get_battery_info()
            self.tts.speak(info)
        except Exception as e:
            print(f"Error getting battery info: {e}")
            self.tts.speak("I couldn't retrieve battery information.")
    
    def get_running_processes(self):
        """Get running processes"""
        try:
            info = self.system_service.get_running_processes()
            self.tts.speak(info)
        except Exception as e:
            print(f"Error getting processes: {e}")
            self.tts.speak("I couldn't retrieve process information.")
    
    def get_network_info(self):
        """Get network information"""
        try:
            info = self.system_service.get_network_info()
            self.tts.speak(info)
        except Exception as e:
            print(f"Error getting network info: {e}")
            self.tts.speak("I couldn't retrieve network information.")
    
    def get_uptime(self):
        """Get system uptime"""
        try:
            info = self.system_service.get_uptime()
            self.tts.speak(info)
        except Exception as e:
            print(f"Error getting uptime: {e}")
            self.tts.speak("I couldn't retrieve uptime information.")
    
    # File management commands
    def create_folder(self, command: str):
        """Create a new folder"""
        try:
            # Extract folder name
            patterns = [
                r'(?:create|make|new) folder (?:called |named )?(.+)',
                r'(?:create|make|new) (?:a )?folder (.+)'
            ]
            
            folder_name = None
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    folder_name = match.group(1).strip()
                    break
            
            if folder_name:
                result = self.system_service.create_folder(folder_name)
                self.tts.speak(result)
            else:
                self.tts.speak("I couldn't understand the folder name. Try 'create folder called Documents'.")
        except Exception as e:
            print(f"Error creating folder: {e}")
            self.tts.speak("I couldn't create that folder.")
    
    def list_files(self, command: str):
        """List files in directory"""
        try:
            # For now, list desktop files
            result = self.system_service.list_files()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error listing files: {e}")
            self.tts.speak("I couldn't list the files.")
    
    # Timer and reminder commands
    def start_timer(self, command: str):
        """Start a timer"""
        try:
            # Extract duration and optional label
            # Pattern: "start timer for 5 minutes" or "set timer 10 seconds cooking"
            duration_pattern = r'(?:start|set) timer (?:for )?(.+?)(?:\s+(?:called|named|for)\s+(.+))?$'
            match = re.search(duration_pattern, command, re.IGNORECASE)
            
            if match:
                duration = match.group(1).strip()
                label = match.group(2).strip() if match.group(2) else None
                
                result = self.timer_service.start_timer(duration, label)
                self.tts.speak(result)
            else:
                self.tts.speak("I couldn't understand the timer duration. Try 'start timer for 5 minutes'.")
        except Exception as e:
            print(f"Error starting timer: {e}")
            self.tts.speak("I couldn't start that timer.")
    
    def stop_timer(self, command: str):
        """Stop a timer"""
        try:
            result = self.timer_service.stop_timer()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error stopping timer: {e}")
            self.tts.speak("I couldn't stop the timer.")
    
    def list_timers(self):
        """List active timers"""
        try:
            result = self.timer_service.list_active_timers()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error listing timers: {e}")
            self.tts.speak("I couldn't list the timers.")
    
    def set_reminder(self, command: str):
        """Set a reminder"""
        try:
            # Pattern: "remind me to X in Y" or "remind me in Y to X"
            patterns = [
                r'remind me (?:to )?(.+?) in (.+)',
                r'remind me in (.+?) (?:to )?(.+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    if "to" in pattern:
                        reminder_text = match.group(1).strip()
                        when = match.group(2).strip()
                    else:
                        when = match.group(1).strip()
                        reminder_text = match.group(2).strip()
                    
                    result = self.timer_service.set_reminder(reminder_text, when)
                    self.tts.speak(result)
                    return
            
            self.tts.speak("I couldn't understand that reminder. Try 'remind me to check the oven in 10 minutes'.")
        except Exception as e:
            print(f"Error setting reminder: {e}")
            self.tts.speak("I couldn't set that reminder.")
    
    def show_help(self):
        """Show available commands"""
        help_text = """I can help you with these commands:
        
        Time & Date: What time is it? What date is it?
        
        Weather: What's the weather? Weather forecast, Weather in London
        
        Math: Calculate 15 plus 25, Convert 5 feet to meters, What's 12 times 8?
        
        System Info: System information, Disk space, Battery level, Running processes, Network info, Uptime
        
        Files: Create folder Documents, List files
        
        Timers: Start timer for 5 minutes, Stop timer, List timers, Remind me to check oven in 10 minutes
        
        Web: Open Google, Open YouTube, Open GitHub
        
        Apps: Open Notepad, Open Calculator, Open File Explorer
        
        Entertainment: Tell me a joke, Programming joke, Dad joke
        
        System: Sleep
        
        Control: Help, Goodbye"""
        
        self.tts.speak("Here are the commands I understand. I can help with time, weather, calculations, system information, timers, web browsing, applications, and entertainment.")
        print(help_text)
    
    def goodbye(self):
        """Say goodbye"""
        self.tts.speak("Goodbye, sir. Jarvis signing off.")