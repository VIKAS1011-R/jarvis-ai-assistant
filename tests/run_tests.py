#!/usr/bin/env python3
"""
Test runner for JARVIS - runs all available tests
"""

import sys
import os
import subprocess

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test(test_name, test_file):
    """Run a specific test"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {test_name}")
    print(f"{'='*60}")
    
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    
    try:
        result = subprocess.run([sys.executable, test_path], 
                              capture_output=False, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_name}: {e}")
        return False

def main():
    """Run all tests"""
    print("JARVIS Test Suite")
    print("="*60)
    
    tests = [
        ("TTS Engine Tests", "test_all_tts.py"),
        ("Simple TTS Test", "test_tts_simple.py"),
        ("Continuous Listening Test", "test_continuous_listening.py"),
        ("Joke Commands Test", "test_joke_commands.py")
    ]
    
    results = {}
    
    for test_name, test_file in tests:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(test_path):
            results[test_name] = run_test(test_name, test_file)
        else:
            print(f"Test file not found: {test_path}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)