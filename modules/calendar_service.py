#!/usr/bin/env python3
"""
Calendar Service Module
Basic calendar functionality and event management
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

class CalendarService:
    def __init__(self, calendar_file: str = "jarvis_calendar.json"):
        """
        Initialize calendar service
        
        Args:
            calendar_file: File to store calendar events
        """
        self.calendar_file = calendar_file
        self.events = self._load_events()
    
    def _load_events(self) -> List[Dict]:
        """Load events from file"""
        try:
            if os.path.exists(self.calendar_file):
                with open(self.calendar_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading calendar: {e}")
        
        return []
    
    def _save_events(self) -> bool:
        """Save events to file"""
        try:
            with open(self.calendar_file, 'w') as f:
                json.dump(self.events, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving calendar: {e}")
            return False
    
    def add_event(self, title: str, date_str: str, time_str: str = None, 
                  duration: str = "1 hour") -> str:
        """
        Add an event to the calendar
        
        Args:
            title: Event title
            date_str: Date string (e.g., "tomorrow", "January 15", "next Monday")
            time_str: Time string (e.g., "2 PM", "14:30")
            duration: Event duration
            
        Returns:
            str: Confirmation message
        """
        try:
            # Parse date
            event_date = self._parse_date(date_str)
            if not event_date:
                return f"I couldn't understand the date '{date_str}'. Try 'tomorrow', 'next Monday', or 'January 15'."
            
            # Parse time
            event_time = self._parse_time(time_str) if time_str else "09:00"
            
            # Create event
            event = {
                'id': len(self.events) + 1,
                'title': title,
                'date': event_date.strftime('%Y-%m-%d'),
                'time': event_time,
                'duration': duration,
                'created': datetime.now().isoformat()
            }
            
            self.events.append(event)
            
            if self._save_events():
                formatted_date = event_date.strftime('%A, %B %d')
                return f"Added '{title}' to your calendar for {formatted_date} at {event_time}."
            else:
                return "Event created but couldn't save to calendar file."
                
        except Exception as e:
            print(f"Add event error: {e}")
            return f"I couldn't add the event '{title}' to your calendar."
    
    def get_today_events(self) -> str:
        """Get today's events"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_events = [e for e in self.events if e['date'] == today]
        
        if not today_events:
            return "You have no events scheduled for today."
        
        # Sort by time
        today_events.sort(key=lambda x: x['time'])
        
        result = f"You have {len(today_events)} event{'s' if len(today_events) != 1 else ''} today: "
        
        for i, event in enumerate(today_events, 1):
            time_12h = self._convert_to_12h(event['time'])
            result += f"{i}. {event['title']} at {time_12h}. "
        
        return result
    
    def get_upcoming_events(self, days: int = 7) -> str:
        """Get upcoming events"""
        today = datetime.now()
        future_date = today + timedelta(days=days)
        
        upcoming = []
        for event in self.events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            if today.date() <= event_date.date() <= future_date.date():
                upcoming.append(event)
        
        if not upcoming:
            return f"You have no events scheduled for the next {days} days."
        
        # Sort by date and time
        upcoming.sort(key=lambda x: (x['date'], x['time']))
        
        result = f"You have {len(upcoming)} upcoming event{'s' if len(upcoming) != 1 else ''}: "
        
        for i, event in enumerate(upcoming, 1):
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            formatted_date = event_date.strftime('%A, %B %d')
            time_12h = self._convert_to_12h(event['time'])
            
            if event_date.date() == today.date():
                date_desc = "today"
            elif event_date.date() == (today + timedelta(days=1)).date():
                date_desc = "tomorrow"
            else:
                date_desc = formatted_date
            
            result += f"{i}. {event['title']} on {date_desc} at {time_12h}. "
        
        return result
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse natural language date"""
        date_str = date_str.lower().strip()
        today = datetime.now()
        
        # Handle relative dates
        if date_str in ['today']:
            return today
        elif date_str in ['tomorrow']:
            return today + timedelta(days=1)
        elif date_str in ['next week']:
            return today + timedelta(days=7)
        elif 'next monday' in date_str:
            days_ahead = 0 - today.weekday()  # Monday is 0
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif 'next tuesday' in date_str:
            days_ahead = 1 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif 'next wednesday' in date_str:
            days_ahead = 2 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif 'next thursday' in date_str:
            days_ahead = 3 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        elif 'next friday' in date_str:
            days_ahead = 4 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        
        # Handle "in X days"
        days_match = re.search(r'in (\d+) days?', date_str)
        if days_match:
            days = int(days_match.group(1))
            return today + timedelta(days=days)
        
        # For now, return None for complex dates
        # In a full implementation, you'd add more sophisticated date parsing
        return None
    
    def _parse_time(self, time_str: str) -> str:
        """Parse time string to 24-hour format"""
        if not time_str:
            return "09:00"
        
        time_str = time_str.lower().strip()
        
        # Handle common formats
        if 'pm' in time_str or 'am' in time_str:
            # Extract hour and convert
            hour_match = re.search(r'(\d+)', time_str)
            if hour_match:
                hour = int(hour_match.group(1))
                if 'pm' in time_str and hour != 12:
                    hour += 12
                elif 'am' in time_str and hour == 12:
                    hour = 0
                return f"{hour:02d}:00"
        
        # Handle 24-hour format
        if ':' in time_str:
            return time_str
        
        # Default
        return "09:00"
    
    def _convert_to_12h(self, time_24h: str) -> str:
        """Convert 24-hour time to 12-hour format"""
        try:
            hour, minute = map(int, time_24h.split(':'))
            if hour == 0:
                return f"12:{minute:02d} AM"
            elif hour < 12:
                return f"{hour}:{minute:02d} AM"
            elif hour == 12:
                return f"12:{minute:02d} PM"
            else:
                return f"{hour-12}:{minute:02d} PM"
        except:
            return time_24h
    
    def delete_event(self, event_id: int) -> str:
        """Delete an event"""
        try:
            for i, event in enumerate(self.events):
                if event['id'] == event_id:
                    deleted_event = self.events.pop(i)
                    if self._save_events():
                        return f"Deleted event '{deleted_event['title']}'."
                    else:
                        return "Event deleted but couldn't save changes."
            
            return f"Event {event_id} not found."
            
        except Exception as e:
            print(f"Delete event error: {e}")
            return "I couldn't delete that event."
    
    def get_calendar_summary(self) -> str:
        """Get overall calendar summary"""
        total_events = len(self.events)
        
        if total_events == 0:
            return "Your calendar is empty. You can add events by saying 'add meeting tomorrow at 2 PM'."
        
        today_count = len([e for e in self.events if e['date'] == datetime.now().strftime('%Y-%m-%d')])
        
        return f"You have {total_events} total events in your calendar, with {today_count} scheduled for today."

# Test function
def test_calendar_service():
    """Test the calendar service"""
    print("Testing Calendar Service")
    print("=" * 30)
    
    calendar = CalendarService("test_calendar.json")
    
    print("1. Adding events:")
    result1 = calendar.add_event("Team Meeting", "tomorrow", "2 PM")
    print(f"   {result1}")
    
    result2 = calendar.add_event("Doctor Appointment", "next Friday", "10 AM")
    print(f"   {result2}")
    
    print("\n2. Today's events:")
    today = calendar.get_today_events()
    print(f"   {today}")
    
    print("\n3. Upcoming events:")
    upcoming = calendar.get_upcoming_events(7)
    print(f"   {upcoming}")
    
    print("\n4. Calendar summary:")
    summary = calendar.get_calendar_summary()
    print(f"   {summary}")
    
    # Clean up test file
    if os.path.exists("test_calendar.json"):
        os.remove("test_calendar.json")

if __name__ == "__main__":
    test_calendar_service()