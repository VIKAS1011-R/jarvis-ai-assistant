#!/usr/bin/env python3
"""
Timer and Reminder Service
Handles timers, alarms, and reminders
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re

class TimerService:
    def __init__(self, tts_engine=None):
        """
        Initialize timer service
        
        Args:
            tts_engine: Text-to-speech engine for notifications
        """
        self.tts = tts_engine
        self.active_timers = {}
        self.timer_counter = 0
        self.reminders = []
    
    def start_timer(self, duration_text: str, label: str = None) -> str:
        """
        Start a timer
        
        Args:
            duration_text: Duration in natural language (e.g., "5 minutes", "1 hour 30 minutes")
            label: Optional label for the timer
            
        Returns:
            str: Confirmation message
        """
        try:
            duration_seconds = self._parse_duration(duration_text)
            
            if duration_seconds <= 0:
                return "I couldn't understand that duration. Try something like '5 minutes' or '1 hour'."
            
            self.timer_counter += 1
            timer_id = self.timer_counter
            
            if not label:
                label = f"Timer {timer_id}"
            
            # Store timer info
            end_time = datetime.now() + timedelta(seconds=duration_seconds)
            self.active_timers[timer_id] = {
                'label': label,
                'duration': duration_seconds,
                'end_time': end_time,
                'thread': None
            }
            
            # Start timer thread
            timer_thread = threading.Thread(
                target=self._run_timer,
                args=(timer_id, duration_seconds, label),
                daemon=True
            )
            timer_thread.start()
            self.active_timers[timer_id]['thread'] = timer_thread
            
            duration_str = self._format_duration(duration_seconds)
            return f"Timer '{label}' started for {duration_str}"
            
        except Exception as e:
            print(f"Timer error: {e}")
            return "I couldn't start that timer. Please try again."
    
    def _parse_duration(self, duration_text: str) -> int:
        """Parse duration text into seconds"""
        duration_text = duration_text.lower().strip()
        
        # Remove common words
        duration_text = re.sub(r'\b(for|in|after|and)\b', '', duration_text)
        
        total_seconds = 0
        
        # Parse hours
        hours_match = re.search(r'(\d+)\s*(?:hour|hr|h)s?', duration_text)
        if hours_match:
            total_seconds += int(hours_match.group(1)) * 3600
        
        # Parse minutes
        minutes_match = re.search(r'(\d+)\s*(?:minute|min|m)s?', duration_text)
        if minutes_match:
            total_seconds += int(minutes_match.group(1)) * 60
        
        # Parse seconds
        seconds_match = re.search(r'(\d+)\s*(?:second|sec|s)s?', duration_text)
        if seconds_match:
            total_seconds += int(seconds_match.group(1))
        
        # If no specific units found, try to parse as just numbers
        if total_seconds == 0:
            # Look for just numbers (assume minutes)
            number_match = re.search(r'(\d+)', duration_text)
            if number_match:
                # If the text contains "second", treat as seconds, otherwise minutes
                if 'second' in duration_text:
                    total_seconds = int(number_match.group(1))
                else:
                    total_seconds = int(number_match.group(1)) * 60
        
        return total_seconds
    
    def _format_duration(self, seconds: int) -> str:
        """Format seconds into readable duration"""
        if seconds < 60:
            return f"{seconds} second{'s' if seconds != 1 else ''}"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes} minute{'s' if minutes != 1 else ''}"
            else:
                return f"{minutes} minute{'s' if minutes != 1 else ''} and {remaining_seconds} second{'s' if remaining_seconds != 1 else ''}"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes == 0:
                return f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours != 1 else ''} and {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
    
    def _run_timer(self, timer_id: int, duration: int, label: str):
        """Run a timer in a separate thread"""
        try:
            time.sleep(duration)
            
            # Timer finished
            if timer_id in self.active_timers:
                del self.active_timers[timer_id]
                
                message = f"Timer '{label}' has finished!"
                print(f"🔔 {message}")
                
                if self.tts:
                    self.tts.speak(message)
                    
        except Exception as e:
            print(f"Timer thread error: {e}")
    
    def list_active_timers(self) -> str:
        """List all active timers"""
        if not self.active_timers:
            return "No active timers."
        
        result = f"Active timers ({len(self.active_timers)}): "
        timer_info = []
        
        for timer_id, timer_data in self.active_timers.items():
            label = timer_data['label']
            end_time = timer_data['end_time']
            remaining = end_time - datetime.now()
            
            if remaining.total_seconds() > 0:
                remaining_str = self._format_duration(int(remaining.total_seconds()))
                timer_info.append(f"'{label}' ({remaining_str} remaining)")
            else:
                timer_info.append(f"'{label}' (finishing now)")
        
        result += ", ".join(timer_info)
        return result
    
    def stop_timer(self, label: str = None) -> str:
        """Stop a timer by label or stop all timers"""
        if not self.active_timers:
            return "No active timers to stop."
        
        if label is None:
            # Stop all timers
            count = len(self.active_timers)
            self.active_timers.clear()
            return f"Stopped {count} timer{'s' if count != 1 else ''}."
        
        # Find timer by label
        timer_to_stop = None
        for timer_id, timer_data in self.active_timers.items():
            if timer_data['label'].lower() == label.lower():
                timer_to_stop = timer_id
                break
        
        if timer_to_stop:
            del self.active_timers[timer_to_stop]
            return f"Stopped timer '{label}'."
        else:
            return f"No timer found with label '{label}'."
    
    def set_reminder(self, reminder_text: str, when: str) -> str:
        """
        Set a reminder (basic implementation)
        
        Args:
            reminder_text: What to remind about
            when: When to remind (e.g., "in 30 minutes")
            
        Returns:
            str: Confirmation message
        """
        try:
            duration_seconds = self._parse_duration(when)
            
            if duration_seconds <= 0:
                return "I couldn't understand when you want to be reminded. Try 'in 30 minutes' or 'in 2 hours'."
            
            # Use timer system for reminders
            label = f"Reminder: {reminder_text}"
            return self.start_timer(when, label)
            
        except Exception as e:
            print(f"Reminder error: {e}")
            return "I couldn't set that reminder. Please try again."
    
    def get_current_time(self) -> str:
        """Get current time (helper function)"""
        now = datetime.now()
        return now.strftime("%I:%M %p on %A, %B %d, %Y")

# Test function
def test_timer_service():
    """Test the timer service"""
    print("Testing Timer Service")
    print("=" * 30)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"TTS: {text}")
    
    timer_service = TimerService(MockTTS())
    
    print("1. Starting timers:")
    print(f"   {timer_service.start_timer('5 seconds', 'Test Timer')}")
    print(f"   {timer_service.start_timer('3 seconds')}")
    
    print("\n2. Listing active timers:")
    time.sleep(1)
    print(f"   {timer_service.list_active_timers()}")
    
    print("\n3. Setting reminder:")
    print(f"   {timer_service.set_reminder('Check the oven', '2 seconds')}")
    
    print("\n4. Waiting for timers to finish...")
    time.sleep(6)
    
    print("\n5. Final timer list:")
    print(f"   {timer_service.list_active_timers()}")

if __name__ == "__main__":
    test_timer_service()