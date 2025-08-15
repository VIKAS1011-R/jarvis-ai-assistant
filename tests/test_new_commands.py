#!/usr/bin/env python3
"""
Test script for new high-priority commands
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.weather_service import WeatherService
from modules.calculator_service import CalculatorService
from modules.system_service import SystemService
from modules.timer_service import TimerService
from modules.simple_commands import SimpleCommands
import time

def test_weather_service():
    """Test weather service"""
    print("Testing Weather Service")
    print("=" * 40)
    
    weather = WeatherService()
    
    print("1. Current weather:")
    result = weather.get_weather()
    print(f"   {result}")
    
    print("\n2. Weather forecast:")
    forecast = weather.get_forecast("", 2)
    print(f"   {forecast}")
    
    print("✓ Weather service tests completed")

def test_calculator_service():
    """Test calculator service"""
    print("\nTesting Calculator Service")
    print("=" * 40)
    
    calc = CalculatorService()
    
    test_calculations = [
        "15 plus 25",
        "12 times 8",
        "100 divided by 4",
        "square root of 144",
        "2 to the power of 8"
    ]
    
    print("1. Calculations:")
    for i, expr in enumerate(test_calculations, 1):
        result = calc.calculate(expr)
        print(f"   {i}. {expr} = {result}")
    
    test_conversions = [
        (5, "feet", "meters"),
        (10, "kilograms", "pounds"),
        (32, "fahrenheit", "celsius"),
        (1, "mile", "kilometers")
    ]
    
    print("\n2. Unit conversions:")
    for i, (amount, from_unit, to_unit) in enumerate(test_conversions, 1):
        result = calc.convert_units(amount, from_unit, to_unit)
        print(f"   {i}. {result}")
    
    print("✓ Calculator service tests completed")

def test_system_service():
    """Test system service"""
    print("\nTesting System Service")
    print("=" * 40)
    
    system = SystemService()
    
    tests = [
        ("System info", system.get_system_info),
        ("Disk space", system.get_disk_space),
        ("Battery info", system.get_battery_info),
        ("Network info", system.get_network_info),
        ("Running processes", lambda: system.get_running_processes(3)),
        ("Uptime", system.get_uptime)
    ]
    
    for i, (name, func) in enumerate(tests, 1):
        try:
            result = func()
            print(f"   {i}. {name}: {result}")
        except Exception as e:
            print(f"   {i}. {name}: Error - {e}")
    
    print("✓ System service tests completed")

def test_timer_service():
    """Test timer service"""
    print("\nTesting Timer Service")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"TTS: {text}")
    
    timer = TimerService(MockTTS())
    
    print("1. Starting test timers:")
    result1 = timer.start_timer("3 seconds", "Test Timer 1")
    print(f"   {result1}")
    
    result2 = timer.start_timer("2 seconds", "Test Timer 2")
    print(f"   {result2}")
    
    print("\n2. Listing active timers:")
    time.sleep(1)
    active = timer.list_active_timers()
    print(f"   {active}")
    
    print("\n3. Setting reminder:")
    reminder = timer.set_reminder("Test reminder", "1 second")
    print(f"   {reminder}")
    
    print("\n4. Waiting for timers to complete...")
    time.sleep(4)
    
    final_list = timer.list_active_timers()
    print(f"   Final: {final_list}")
    
    print("✓ Timer service tests completed")

def test_command_integration():
    """Test command integration"""
    print("\nTesting Command Integration")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    commands = SimpleCommands(MockTTS())
    
    test_commands = [
        "what's the weather",
        "calculate 25 plus 17",
        "convert 10 feet to meters",
        "system information",
        "disk space",
        "start timer for 2 seconds",
        "tell me a joke"
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
    """Run all new command tests"""
    print("JARVIS New Commands Test Suite")
    print("=" * 50)
    
    # Test individual services
    test_weather_service()
    test_calculator_service()
    test_system_service()
    test_timer_service()
    
    # Test integration
    test_command_integration()
    
    print(f"\n🎉 All new command tests completed!")
    print("\nNew features available:")
    print("• Weather information and forecasts")
    print("• Mathematical calculations and unit conversions")
    print("• System information (CPU, memory, disk, battery, etc.)")
    print("• Timers and reminders")
    print("• File management basics")

if __name__ == "__main__":
    main()