#!/usr/bin/env python3
"""
Test script for command parsing accuracy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.simple_commands import SimpleCommands

def test_command_parsing():
    """Test command parsing with potentially conflicting words"""
    print("Testing Command Parsing Accuracy")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def __init__(self):
            self.last_spoken = ""
        
        def speak(self, text):
            self.last_spoken = text
            print(f"JARVIS: {text}")
    
    mock_tts = MockTTS()
    commands = SimpleCommands(mock_tts)
    
    # Test cases that previously caused conflicts
    test_cases = [
        {
            'command': 'convert 3 feet to centimeters',
            'expected_type': 'conversion',
            'should_not_contain': 'time'
        },
        {
            'command': 'convert 10 meters to centimeters', 
            'expected_type': 'conversion',
            'should_not_contain': 'time'
        },
        {
            'command': 'what time is it',
            'expected_type': 'time',
            'should_contain': 'time'
        },
        {
            'command': 'timer for 5 minutes',
            'expected_type': 'timer',
            'should_not_contain': 'current time'
        },
        {
            'command': 'start timer for 30 seconds',
            'expected_type': 'timer',
            'should_contain': 'Timer'
        },
        {
            'command': 'calculate 25 times 4',
            'expected_type': 'calculation',
            'should_contain': 'answer'
        },
        {
            'command': 'what is the weather',
            'expected_type': 'weather',
            'should_not_contain': 'time'
        },
        {
            'command': 'system information',
            'expected_type': 'system',
            'should_contain': 'System'
        }
    ]
    
    print("Testing potentially conflicting commands:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        command = test_case['command']
        expected_type = test_case['expected_type']
        
        print(f"\n{i}. Testing: '{command}'")
        print(f"   Expected: {expected_type}")
        
        # Clear previous response
        mock_tts.last_spoken = ""
        
        # Process command
        result = commands.process_command(command)
        response = mock_tts.last_spoken.lower()
        
        # Check expectations
        success = True
        
        if 'should_contain' in test_case:
            expected_word = test_case['should_contain'].lower()
            if expected_word not in response:
                print(f"   ❌ FAIL: Response should contain '{expected_word}'")
                success = False
        
        if 'should_not_contain' in test_case:
            forbidden_word = test_case['should_not_contain'].lower()
            if forbidden_word in response:
                print(f"   ❌ FAIL: Response should NOT contain '{forbidden_word}'")
                success = False
            else:
                print(f"   ✅ PASS: Response correctly does NOT contain '{forbidden_word}'")
        
        if success:
            print(f"   ✅ PASS: Correctly identified as {expected_type}")
        
        print(f"   Response: {mock_tts.last_spoken}")
    
    print(f"\n" + "=" * 40)
    print("Command parsing test completed!")

def test_word_boundary_patterns():
    """Test specific word boundary cases"""
    print(f"\nTesting Word Boundary Patterns")
    print("=" * 40)
    
    import re
    
    test_patterns = [
        {
            'text': 'convert 3 feet to centimeters',
            'pattern': r'\btime\b',
            'should_match': False,
            'description': 'centimeters should not match "time"'
        },
        {
            'text': 'what time is it',
            'pattern': r'\btime\b',
            'should_match': True,
            'description': 'should match "time" in time query'
        },
        {
            'text': 'start timer for 5 minutes',
            'pattern': r'\btimer\b',
            'should_match': True,
            'description': 'should match "timer" in timer command'
        },
        {
            'text': 'convert meters to centimeters',
            'pattern': r'\btime\b',
            'should_match': False,
            'description': 'meters should not match "time"'
        }
    ]
    
    for i, test in enumerate(test_patterns, 1):
        text = test['text']
        pattern = test['pattern']
        should_match = test['should_match']
        description = test['description']
        
        match = re.search(pattern, text, re.IGNORECASE)
        actual_match = match is not None
        
        print(f"{i}. {description}")
        print(f"   Text: '{text}'")
        print(f"   Pattern: {pattern}")
        print(f"   Expected: {'Match' if should_match else 'No match'}")
        print(f"   Actual: {'Match' if actual_match else 'No match'}")
        
        if actual_match == should_match:
            print(f"   ✅ PASS")
        else:
            print(f"   ❌ FAIL")
        print()

if __name__ == "__main__":
    test_command_parsing()
    test_word_boundary_patterns()