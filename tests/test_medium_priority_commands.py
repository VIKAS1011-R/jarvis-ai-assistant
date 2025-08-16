#!/usr/bin/env python3
"""
Test script for medium priority commands
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.wikipedia_service import WikipediaService
from modules.news_service import NewsService
from modules.email_service import EmailService, SimpleEmailReader
from modules.calendar_service import CalendarService
from modules.music_service import MusicService, SystemMusicPlayer
from modules.simple_commands import SimpleCommands

def test_wikipedia_service():
    """Test Wikipedia service"""
    print("Testing Wikipedia Service")
    print("=" * 40)
    
    wiki = WikipediaService()
    
    test_queries = [
        "Python programming language",
        "Artificial Intelligence",
        "Machine Learning"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Searching for: '{query}'")
        try:
            result = wiki.search_wikipedia(query, sentences=2)
            print(f"   Result: {result[:200]}...")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("✓ Wikipedia service tests completed")

def test_news_service():
    """Test news service"""
    print("\nTesting News Service")
    print("=" * 40)
    
    news = NewsService()
    
    print("1. General news:")
    try:
        general_news = news.get_latest_news('general', 2)
        print(f"   {general_news[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Tech news:")
    try:
        tech_news = news.get_latest_news('tech', 2)
        print(f"   {tech_news[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. News summary:")
    try:
        summary = news.get_news_summary()
        print(f"   {summary[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("✓ News service tests completed")

def test_email_service():
    """Test email service"""
    print("\nTesting Email Service")
    print("=" * 40)
    
    email_service = EmailService()
    email_reader = SimpleEmailReader()
    
    print("1. Email summary:")
    summary = email_service.get_email_summary()
    print(f"   {summary[:200]}...")
    
    print("\n2. Recent emails:")
    recent = email_reader.get_recent_emails(2)
    print(f"   {recent}")
    
    print("\n3. Read email preview:")
    preview = email_reader.read_email_preview(1)
    print(f"   {preview}")
    
    print("✓ Email service tests completed")

def test_calendar_service():
    """Test calendar service"""
    print("\nTesting Calendar Service")
    print("=" * 40)
    
    calendar = CalendarService("test_medium_calendar.json")
    
    print("1. Adding test events:")
    result1 = calendar.add_event("Team Meeting", "tomorrow", "2 PM")
    print(f"   {result1}")
    
    result2 = calendar.add_event("Doctor Appointment", "in 3 days", "10 AM")
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
    if os.path.exists("test_medium_calendar.json"):
        os.remove("test_medium_calendar.json")
    
    print("✓ Calendar service tests completed")

def test_music_service():
    """Test music service"""
    print("\nTesting Music Service")
    print("=" * 40)
    
    music = MusicService()
    player = SystemMusicPlayer()
    
    print("1. Music help:")
    help_text = music.get_music_help()
    print(f"   {help_text[:200]}...")
    
    print("\n2. System music controls:")
    print(f"   Play/Pause: {player.play_pause()}")
    print(f"   Volume Up: {player.volume_up()}")
    
    print("\n3. Music service controls:")
    print(f"   Play music: {music.play_music('test song')}")
    print(f"   Pause: {music.pause_music()}")
    
    print("✓ Music service tests completed")

def test_command_integration():
    """Test command integration"""
    print("\nTesting Medium Priority Command Integration")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"JARVIS: {text[:150]}...")
    
    commands = SimpleCommands(MockTTS())
    
    test_commands = [
        "search wikipedia for artificial intelligence",
        "latest news",
        "tech news",
        "check email",
        "calendar summary",
        "play music",
        "pause music"
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. Testing: '{command}'")
        try:
            result = commands.process_command(command)
            print(f"   Command result: {result}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n✓ Command integration tests completed")

def main():
    """Run all medium priority command tests"""
    print("JARVIS Medium Priority Commands Test Suite")
    print("=" * 50)
    
    # Test individual services
    test_wikipedia_service()
    test_news_service()
    test_email_service()
    test_calendar_service()
    test_music_service()
    
    # Test integration
    test_command_integration()
    
    print(f"\n🎉 All medium priority command tests completed!")
    print("\nNew medium priority features available:")
    print("• Wikipedia search and summaries")
    print("• News headlines from multiple sources")
    print("• Basic email functionality")
    print("• Calendar and event management")
    print("• Music control and playback")

if __name__ == "__main__":
    main()