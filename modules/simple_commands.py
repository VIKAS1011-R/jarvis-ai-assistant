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
from modules.wikipedia_service import WikipediaService
from modules.news_service import NewsService
from modules.email_service import EmailService, SimpleEmailReader
from modules.calendar_service import CalendarService
from modules.music_service import MusicService, SystemMusicPlayer
from modules.wikipedia_service import WikipediaService
from modules.news_service import NewsService
from modules.email_service import EmailService
from modules.calendar_service import CalendarService
from modules.music_service import MusicService

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
        self.wikipedia_service = WikipediaService()
        self.news_service = NewsService()
        self.email_service = EmailService()
        self.email_reader = SimpleEmailReader()
        self.calendar_service = CalendarService()
        self.music_service = MusicService()
        self.system_player = SystemMusicPlayer()
        self.wikipedia_service = WikipediaService()
        self.news_service = NewsService()
        self.email_service = EmailService()
        self.calendar_service = CalendarService()
        self.music_service = MusicService()
        
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
        
        # Wikipedia commands
        if re.search(r'\b(wikipedia|search wikipedia|wiki)\b', command, re.IGNORECASE):
            self.search_wikipedia(command)
            return None
        
        # News commands
        if re.search(r'\b(news|latest news|headlines)\b', command, re.IGNORECASE):
            if re.search(r'\b(tech|technology)\b', command, re.IGNORECASE):
                self.get_tech_news()
            elif re.search(r'\b(science)\b', command, re.IGNORECASE):
                self.get_science_news()
            elif re.search(r'\bsearch\b', command, re.IGNORECASE):
                self.search_news(command)
            else:
                self.get_general_news()
            return None
        
        # Email commands
        if re.search(r'\b(email|emails|check email)\b', command, re.IGNORECASE):
            if re.search(r'\b(recent|latest|new)\b', command, re.IGNORECASE):
                self.get_recent_emails()
            elif re.search(r'\bread\b', command, re.IGNORECASE):
                self.read_email(command)
            else:
                self.get_email_summary()
            return None
        
        # Calendar commands
        if re.search(r'\b(calendar|schedule|appointment|meeting)\b', command, re.IGNORECASE):
            if re.search(r'\b(add|create|schedule)\b', command, re.IGNORECASE):
                self.add_calendar_event(command)
            elif re.search(r'\b(today|today\'s)\b', command, re.IGNORECASE):
                self.get_today_schedule()
            elif re.search(r'\b(upcoming|next|future)\b', command, re.IGNORECASE):
                self.get_upcoming_events()
            else:
                self.get_calendar_summary()
            return None
        
        # Music commands
        if re.search(r'\b(play|music|song|spotify)\b', command, re.IGNORECASE):
            if re.search(r'\b(pause|stop)\b', command, re.IGNORECASE):
                self.pause_music()
            elif re.search(r'\b(resume|continue)\b', command, re.IGNORECASE):
                self.resume_music()
            elif re.search(r'\b(next|skip)\b', command, re.IGNORECASE):
                self.next_track()
            elif re.search(r'\b(previous|back)\b', command, re.IGNORECASE):
                self.previous_track()
            elif re.search(r'\bvolume\b', command, re.IGNORECASE):
                self.set_music_volume(command)
            else:
                self.play_music(command)
            return None
        
        # Wikipedia commands
        if re.search(r'\b(wikipedia|search wikipedia|wiki)\b', command, re.IGNORECASE):
            self.search_wikipedia(command)
            return None
        
        # News commands
        if re.search(r'\b(news|headlines|latest news)\b', command, re.IGNORECASE):
            self.get_news(command)
            return None
        
        # Email commands
        if re.search(r'\b(email|send email|check email)\b', command, re.IGNORECASE):
            self.handle_email(command)
            return None
        
        # Calendar commands
        if re.search(r'\b(calendar|schedule|appointment|event)\b', command, re.IGNORECASE):
            self.handle_calendar(command)
            return None
        
        # Music commands
        if re.search(r'\b(play|music|song|spotify|pause|volume)\b', command, re.IGNORECASE):
            self.handle_music(command)
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
    
    # Wikipedia commands
    def search_wikipedia(self, command: str):
        """Search Wikipedia"""
        try:
            # Extract search query
            patterns = [
                r'(?:wikipedia|wiki|search wikipedia) (?:for |about )?(.+)',
                r'(?:search|look up) (.+) (?:on |in )?wikipedia'
            ]
            
            query = None
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    query = match.group(1).strip()
                    break
            
            if query:
                result = self.wikipedia_service.search_wikipedia(query)
                self.tts.speak(result)
            else:
                self.tts.speak("What would you like me to search for on Wikipedia?")
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            self.tts.speak("I couldn't search Wikipedia right now.")
    
    # News commands
    def get_general_news(self):
        """Get general news"""
        try:
            news = self.news_service.get_latest_news('general', 3)
            self.tts.speak(news)
        except Exception as e:
            print(f"Error getting news: {e}")
            self.tts.speak("I couldn't fetch the news right now.")
    
    def get_tech_news(self):
        """Get technology news"""
        try:
            news = self.news_service.get_latest_news('tech', 3)
            self.tts.speak(news)
        except Exception as e:
            print(f"Error getting tech news: {e}")
            self.tts.speak("I couldn't fetch technology news right now.")
    
    def get_science_news(self):
        """Get science news"""
        try:
            news = self.news_service.get_latest_news('science', 3)
            self.tts.speak(news)
        except Exception as e:
            print(f"Error getting science news: {e}")
            self.tts.speak("I couldn't fetch science news right now.")
    
    def search_news(self, command: str):
        """Search for specific news topics"""
        try:
            # Extract search query
            pattern = r'(?:search|find) (?:news )?(?:about |for )?(.+)'
            match = re.search(pattern, command, re.IGNORECASE)
            
            if match:
                topic = match.group(1).strip()
                result = self.news_service.search_news(topic)
                self.tts.speak(result)
            else:
                self.tts.speak("What news topic would you like me to search for?")
        except Exception as e:
            print(f"Error searching news: {e}")
            self.tts.speak("I couldn't search for news right now.")
    
    # Email commands
    def get_email_summary(self):
        """Get email summary"""
        try:
            # Check if email is configured
            if not self.email_service.is_configured():
                self.tts.speak("Email is not configured. Say 'setup email' to configure your email securely.")
                return
            
            summary = self.email_service.get_email_summary()
            self.tts.speak(summary)
        except Exception as e:
            print(f"Error getting email summary: {e}")
            self.tts.speak("I couldn't access your email right now.")
    
    def get_recent_emails(self):
        """Get recent emails"""
        try:
            # Check if email is configured
            if not self.email_service.is_configured():
                self.tts.speak("Email is not configured. Say 'setup email' to configure your email securely.")
                return
            
            summary = self.email_service.get_email_summary()
            self.tts.speak(summary)
        except Exception as e:
            print(f"Error getting recent emails: {e}")
            self.tts.speak("I couldn't get your recent emails.")
    
    def check_email(self):
        """Check for new emails"""
        try:
            # Check if email is configured
            if not self.email_service.is_configured():
                self.tts.speak("Email is not configured. Say 'setup email' to configure your email securely.")
                return
            
            result = self.email_service.check_new_emails()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error checking email: {e}")
            self.tts.speak("I couldn't check your email right now.")
    
    def setup_email_command(self):
        """Setup email configuration"""
        try:
            self.tts.speak("I'll help you set up email securely. Please check the console for setup instructions.")
            result = self.email_service.setup_email_interactive()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error setting up email: {e}")
            self.tts.speak("I couldn't set up email right now. Please try running the setup script manually.")
    
    def read_email(self, command: str):
        """Read specific email"""
        try:
            # Check if email is configured
            if not self.email_service.is_configured():
                self.tts.speak("Email is not configured. Say 'setup email' to configure your email securely.")
                return
            
            # For now, just get email summary
            summary = self.email_service.get_email_summary()
            self.tts.speak(summary)
        except Exception as e:
            print(f"Error reading email: {e}")
            self.tts.speak("I couldn't read that email.")
    
    # Calendar commands
    def add_calendar_event(self, command: str):
        """Add calendar event"""
        try:
            # This is a simplified parser - in practice you'd want more sophisticated NLP
            # Pattern: "add meeting tomorrow at 2 PM" or "schedule appointment next Monday at 10 AM"
            patterns = [
                r'(?:add|create|schedule) (.+?) (?:on |for )?(.+?) at (.+)',
                r'(?:add|create|schedule) (.+?) (.+?) at (.+)',
                r'(?:add|create|schedule) (.+?) (?:on |for )?(.+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 3:
                        title = match.group(1).strip()
                        date_str = match.group(2).strip()
                        time_str = match.group(3).strip()
                    else:
                        title = match.group(1).strip()
                        date_str = match.group(2).strip()
                        time_str = None
                    
                    result = self.calendar_service.add_event(title, date_str, time_str)
                    self.tts.speak(result)
                    return
            
            self.tts.speak("I couldn't understand the event details. Try 'add meeting tomorrow at 2 PM'.")
        except Exception as e:
            print(f"Error adding calendar event: {e}")
            self.tts.speak("I couldn't add that event to your calendar.")
    
    def get_today_schedule(self):
        """Get today's schedule"""
        try:
            schedule = self.calendar_service.get_today_events()
            self.tts.speak(schedule)
        except Exception as e:
            print(f"Error getting today's schedule: {e}")
            self.tts.speak("I couldn't get your schedule for today.")
    
    def get_upcoming_events(self):
        """Get upcoming events"""
        try:
            events = self.calendar_service.get_upcoming_events(7)
            self.tts.speak(events)
        except Exception as e:
            print(f"Error getting upcoming events: {e}")
            self.tts.speak("I couldn't get your upcoming events.")
    
    def get_calendar_summary(self):
        """Get calendar summary"""
        try:
            summary = self.calendar_service.get_calendar_summary()
            self.tts.speak(summary)
        except Exception as e:
            print(f"Error getting calendar summary: {e}")
            self.tts.speak("I couldn't get your calendar summary.")
    
    # Music commands
    def play_music(self, command: str):
        """Play music"""
        try:
            # Extract song/artist name
            patterns = [
                r'play (.+)',
                r'music (.+)',
                r'song (.+)'
            ]
            
            query = None
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    query = match.group(1).strip()
                    # Remove common words
                    query = re.sub(r'\b(music|song|by|from)\b', '', query, flags=re.IGNORECASE).strip()
                    break
            
            if query:
                # Use smart play for better results
                if hasattr(self.music_service, 'smart_play'):
                    result = self.music_service.smart_play(query)
                else:
                    result = self.music_service.play_music(query)
                self.tts.speak(result)
            else:
                # Just resume playback
                result = self.music_service.resume_music()
                self.tts.speak(result)
        except Exception as e:
            print(f"Error playing music: {e}")
            self.tts.speak("I couldn't play music right now.")
    
    def pause_music(self):
        """Pause music"""
        try:
            result = self.music_service.pause_music()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error pausing music: {e}")
            self.tts.speak("I couldn't pause the music.")
    
    def resume_music(self):
        """Resume music"""
        try:
            result = self.music_service.resume_music()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error resuming music: {e}")
            self.tts.speak("I couldn't resume the music.")
    
    def next_track(self):
        """Next track"""
        try:
            result = self.music_service.next_track()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error skipping track: {e}")
            self.tts.speak("I couldn't skip to the next track.")
    
    def previous_track(self):
        """Previous track"""
        try:
            result = self.music_service.previous_track()
            self.tts.speak(result)
        except Exception as e:
            print(f"Error going to previous track: {e}")
            self.tts.speak("I couldn't go to the previous track.")
    
    def set_music_volume(self, command: str):
        """Set music volume"""
        try:
            # Extract volume level
            volume_match = re.search(r'(\d+)', command)
            if volume_match:
                level = int(volume_match.group(1))
                result = self.music_service.set_volume(level)
                self.tts.speak(result)
            else:
                self.tts.speak("What volume level would you like? Say a number between 0 and 100.")
        except Exception as e:
            print(f"Error setting volume: {e}")
            self.tts.speak("I couldn't adjust the volume.")
    
    # Wikipedia commands
    def search_wikipedia(self, command: str):
        """Search Wikipedia"""
        try:
            # Extract search query
            patterns = [
                r'(?:wikipedia|search wikipedia|wiki) (?:for |about )?(.+)',
                r'(?:search|look up) (.+) (?:on |in )?wikipedia'
            ]
            
            query = None
            for pattern in patterns:
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    query = match.group(1).strip()
                    break
            
            if query:
                result = self.wikipedia_service.search_wikipedia(query)
                self.tts.speak(result)
            else:
                self.tts.speak("What would you like me to search for on Wikipedia?")
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            self.tts.speak("I couldn't search Wikipedia right now.")
    
    # News commands
    def get_news(self, command: str):
        """Get news headlines"""
        try:
            if re.search(r'\b(search|about|for)\b', command, re.IGNORECASE):
                # Extract topic
                topic_match = re.search(r'(?:news|headlines) (?:about|for|on) (.+)', command, re.IGNORECASE)
                if topic_match:
                    topic = topic_match.group(1).strip()
                    result = self.news_service.search_news(topic)
                else:
                    result = self.news_service.get_top_news()
            else:
                result = self.news_service.get_top_news()
            
            self.tts.speak(result)
        except Exception as e:
            print(f"Error getting news: {e}")
            self.tts.speak("I couldn't get the news right now.")
    
    # Email commands
    def handle_email(self, command: str):
        """Handle email commands"""
        try:
            if re.search(r'\b(setup|configure)\b', command, re.IGNORECASE):
                # Setup email
                self.setup_email_command()
            elif re.search(r'\b(check|new)\b', command, re.IGNORECASE):
                # Check for new emails
                self.check_email()
            elif re.search(r'\b(read|get|summary)\b', command, re.IGNORECASE):
                # Get email summary
                self.get_email_summary()
            elif re.search(r'\b(send|compose)\b', command, re.IGNORECASE):
                # Send email command
                self.tts.speak("Email sending is not implemented yet. I can help you check and read emails.")
            else:
                self.tts.speak("I can help with checking emails, reading emails, or setting up email. What would you like to do?")
        except Exception as e:
            print(f"Error handling email: {e}")
            self.tts.speak("I couldn't handle that email command.")
    
    # Calendar commands
    def handle_calendar(self, command: str):
        """Handle calendar commands"""
        try:
            if re.search(r'\b(add|create|schedule)\b', command, re.IGNORECASE):
                # Add event
                self.tts.speak("To add calendar events, please specify the event title and time. For example: 'schedule meeting tomorrow at 2 PM'")
            elif re.search(r'\b(today|today\'s)\b', command, re.IGNORECASE):
                # Today's events
                result = self.calendar_service.get_today_events()
                self.tts.speak(result)
            elif re.search(r'\b(upcoming|next|future)\b', command, re.IGNORECASE):
                # Upcoming events
                result = self.calendar_service.get_upcoming_events()
                self.tts.speak(result)
            elif re.search(r'\b(summary|status)\b', command, re.IGNORECASE):
                # Calendar summary
                result = self.calendar_service.get_calendar_summary()
                self.tts.speak(result)
            else:
                result = self.calendar_service.get_today_events()
                self.tts.speak(result)
        except Exception as e:
            print(f"Error handling calendar: {e}")
            self.tts.speak("I couldn't access your calendar right now.")
    
    # Music commands
    def handle_music(self, command: str):
        """Handle music commands"""
        try:
            if re.search(r'\b(play|start)\b', command, re.IGNORECASE):
                # Play music
                music_match = re.search(r'play (.+)', command, re.IGNORECASE)
                if music_match:
                    query = music_match.group(1).strip()
                    # Remove common words
                    query = re.sub(r'\b(music|song|by|from)\b', '', query, flags=re.IGNORECASE).strip()
                    result = self.music_service.play_music(query)
                else:
                    result = self.music_service.play_music()
                self.tts.speak(result)
            elif re.search(r'\b(pause|stop)\b', command, re.IGNORECASE):
                # Pause music
                result = self.music_service.pause_music()
                self.tts.speak(result)
            elif re.search(r'\b(next|skip)\b', command, re.IGNORECASE):
                # Next track
                result = self.music_service.next_track()
                self.tts.speak(result)
            elif re.search(r'\b(previous|back)\b', command, re.IGNORECASE):
                # Previous track
                result = self.music_service.previous_track()
                self.tts.speak(result)
            elif re.search(r'\bvolume\b', command, re.IGNORECASE):
                # Volume control
                volume_match = re.search(r'volume (?:to )?(\d+)', command, re.IGNORECASE)
                if volume_match:
                    volume = int(volume_match.group(1))
                    result = self.music_service.set_volume(volume)
                else:
                    result = self.music_service.get_volume()
                self.tts.speak(result)
            else:
                self.tts.speak("I can help with playing music, pausing, skipping tracks, or controlling volume. What would you like to do?")
        except Exception as e:
            print(f"Error handling music: {e}")
            self.tts.speak("I couldn't control music right now.")
    
    def show_help(self):
        """Show available commands"""
        help_text = """I can help you with these commands:
        
        Time & Date: What time is it? What date is it?
        
        Weather: What's the weather? Weather forecast, Weather in London
        
        Math: Calculate 15 plus 25, Convert 5 feet to meters, What's 12 times 8?
        
        System Info: System information, Disk space, Battery level, Running processes, Network info, Uptime
        
        Files: Create folder Documents, List files
        
        Timers: Start timer for 5 minutes, Stop timer, List timers, Remind me to check oven in 10 minutes
        
        Wikipedia: Search Wikipedia for Python, Wiki artificial intelligence
        
        News: Latest news, News headlines, News about technology
        
        Email: Check email, Send email, Email status
        
        Calendar: Today's events, Upcoming events, Calendar summary
        
        Music: Play music, Play The Beatles, Pause music, Next song, Volume 50
        
        Web: Open Google, Open YouTube, Open GitHub
        
        Apps: Open Notepad, Open Calculator, Open File Explorer
        
        Entertainment: Tell me a joke, Programming joke, Dad joke
        
        System: Sleep
        
        Control: Help, Goodbye"""
        
        self.tts.speak("Here are the commands I understand. I can help with time, weather, calculations, system information, timers, Wikipedia searches, news, email, calendar, music control, web browsing, applications, and entertainment.")
        print(help_text)
    
    def goodbye(self):
        """Say goodbye"""
        self.tts.speak("Goodbye, sir. Jarvis signing off.")