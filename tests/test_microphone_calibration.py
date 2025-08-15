#!/usr/bin/env python3
"""
Test script for microphone calibration functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.mic_calibration import MicrophoneCalibrator
from modules.mic_config import MicConfig
from modules.continuous_listener import ContinuousListener

def test_mic_config():
    """Test microphone configuration save/load"""
    print("Testing Microphone Configuration")
    print("=" * 40)
    
    config = MicConfig("test_mic_settings.json")
    
    # Test default settings
    print("1. Testing default settings:")
    settings = config.load_settings()
    print(f"   Default threshold: {settings['energy_threshold']}")
    print(f"   Calibrated: {settings['calibrated']}")
    
    # Test saving custom settings
    print("\n2. Testing save custom settings:")
    custom_settings = {
        'energy_threshold': 600,
        'environment_noise_level': 'MEDIUM_NOISE',
        'dynamic_energy_adjustment_damping': 0.12
    }
    
    success = config.save_settings(custom_settings)
    print(f"   Save successful: {success}")
    
    # Test loading saved settings
    print("\n3. Testing load saved settings:")
    loaded_settings = config.load_settings()
    print(f"   Loaded threshold: {loaded_settings['energy_threshold']}")
    print(f"   Environment: {loaded_settings['environment_noise_level']}")
    print(f"   Calibrated: {loaded_settings['calibrated']}")
    
    # Test calibration check
    print(f"\n4. Testing calibration check:")
    print(f"   Is calibrated: {config.is_calibrated()}")
    
    # Clean up
    if os.path.exists("test_mic_settings.json"):
        os.remove("test_mic_settings.json")
        print("   Test file cleaned up")
    
    print("✓ Configuration tests completed")

def test_continuous_listener_with_config():
    """Test continuous listener with configuration"""
    print("\nTesting Continuous Listener with Config")
    print("=" * 40)
    
    # Create a test config
    config = MicConfig("test_listener_config.json")
    test_settings = {
        'energy_threshold': 500,
        'environment_noise_level': 'LOW_NOISE',
        'dynamic_energy_adjustment_damping': 0.2
    }
    config.save_settings(test_settings)
    
    try:
        # Test listener initialization
        listener = ContinuousListener()
        listener.mic_config = config  # Use test config
        listener.mic_settings = config.load_settings()
        
        print("1. Testing listener initialization:")
        success = listener.initialize()
        print(f"   Initialization successful: {success}")
        
        if success:
            print(f"   Energy threshold: {listener.recognizer.energy_threshold}")
            print(f"   Dynamic adjustment: {listener.recognizer.dynamic_energy_threshold}")
            print(f"   Damping: {listener.recognizer.dynamic_energy_adjustment_damping}")
        
        listener.cleanup()
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # Clean up
    if os.path.exists("test_listener_config.json"):
        os.remove("test_listener_config.json")
        print("   Test config cleaned up")
    
    print("✓ Listener configuration tests completed")

def test_calibration_recommendations():
    """Test calibration recommendation system"""
    print("\nTesting Calibration Recommendations")
    print("=" * 40)
    
    config = MicConfig()
    
    # Test different scenarios
    scenarios = [
        {"noise": 200, "voice": 800, "desc": "Quiet environment, clear voice"},
        {"noise": 600, "voice": 1000, "desc": "Medium noise, good voice"},
        {"noise": 900, "voice": 1100, "desc": "Noisy environment, loud voice"},
        {"noise": 400, "voice": 350, "desc": "Voice too quiet for noise level"}
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['desc']}:")
        print(f"   Noise: {scenario['noise']}, Voice: {scenario['voice']}")
        
        recommendations = config.get_recommended_settings(scenario['noise'], scenario['voice'])
        
        print(f"   Recommended threshold: {recommendations['energy_threshold']}")
        print(f"   Environment type: {recommendations['environment_noise_level']}")
        print(f"   Damping factor: {recommendations['dynamic_energy_adjustment_damping']}")
    
    print("\n✓ Recommendation tests completed")

def main():
    """Run all microphone calibration tests"""
    print("JARVIS Microphone Calibration Tests")
    print("=" * 50)
    
    # Test configuration system
    test_mic_config()
    
    # Test continuous listener integration
    test_continuous_listener_with_config()
    
    # Test recommendation system
    test_calibration_recommendations()
    
    print(f"\n🎉 All microphone calibration tests completed!")
    
    # Ask if user wants to run actual calibration
    response = input("\nRun actual microphone calibration? (y/n): ").lower().strip()
    if response == 'y':
        print("\nRunning actual calibration...")
        calibrator = MicrophoneCalibrator()
        calibrator.full_calibration()

if __name__ == "__main__":
    main()