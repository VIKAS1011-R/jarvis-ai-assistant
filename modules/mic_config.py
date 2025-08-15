#!/usr/bin/env python3
"""
Microphone Configuration Module
Saves and loads microphone calibration settings
"""

import json
import os
from typing import Dict, Optional

class MicConfig:
    def __init__(self, config_file: str = "mic_settings.json"):
        """
        Initialize microphone configuration
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.default_settings = {
            'energy_threshold': 400,
            'dynamic_energy_threshold': True,
            'dynamic_energy_adjustment_damping': 0.15,
            'dynamic_energy_ratio': 1.5,
            'pause_threshold': 0.8,
            'phrase_threshold': 0.3,
            'non_speaking_duration': 0.5,
            'calibrated': False,
            'environment_noise_level': 'UNKNOWN'
        }
    
    def save_settings(self, settings: Dict) -> bool:
        """
        Save microphone settings to file
        
        Args:
            settings: Dictionary of microphone settings
            
        Returns:
            bool: True if saved successfully
        """
        try:
            # Merge with defaults
            final_settings = self.default_settings.copy()
            final_settings.update(settings)
            final_settings['calibrated'] = True
            
            with open(self.config_file, 'w') as f:
                json.dump(final_settings, f, indent=2)
            
            print(f"✓ Microphone settings saved to {self.config_file}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to save settings: {e}")
            return False
    
    def load_settings(self) -> Dict:
        """
        Load microphone settings from file
        
        Returns:
            Dict: Microphone settings
        """
        if not os.path.exists(self.config_file):
            print(f"No calibration file found. Using default settings.")
            return self.default_settings.copy()
        
        try:
            with open(self.config_file, 'r') as f:
                settings = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            final_settings = self.default_settings.copy()
            final_settings.update(settings)
            
            if settings.get('calibrated', False):
                print(f"✓ Loaded calibrated microphone settings")
                print(f"  Energy threshold: {final_settings['energy_threshold']}")
                print(f"  Environment: {final_settings['environment_noise_level']}")
            else:
                print(f"✓ Loaded default microphone settings")
            
            return final_settings
            
        except Exception as e:
            print(f"✗ Failed to load settings: {e}")
            print(f"Using default settings.")
            return self.default_settings.copy()
    
    def is_calibrated(self) -> bool:
        """
        Check if microphone has been calibrated
        
        Returns:
            bool: True if calibrated
        """
        settings = self.load_settings()
        return settings.get('calibrated', False)
    
    def get_recommended_settings(self, noise_level: float, voice_level: float) -> Dict:
        """
        Generate recommended settings based on calibration data
        
        Args:
            noise_level: Average ambient noise level
            voice_level: Average voice level
            
        Returns:
            Dict: Recommended settings
        """
        # Calculate optimal threshold
        if voice_level > noise_level:
            optimal_threshold = noise_level + (voice_level - noise_level) * 0.3
        else:
            optimal_threshold = max(noise_level * 1.5, 400)
        
        # Determine environment type
        if noise_level > 800:
            env_type = "HIGH_NOISE"
            damping = 0.1  # More aggressive adjustment in noisy environments
            ratio = 2.0
        elif noise_level > 400:
            env_type = "MEDIUM_NOISE"
            damping = 0.15
            ratio = 1.5
        else:
            env_type = "LOW_NOISE"
            damping = 0.2  # Less aggressive in quiet environments
            ratio = 1.3
        
        return {
            'energy_threshold': int(optimal_threshold),
            'dynamic_energy_threshold': True,
            'dynamic_energy_adjustment_damping': damping,
            'dynamic_energy_ratio': ratio,
            'pause_threshold': 0.8,
            'phrase_threshold': 0.3,
            'non_speaking_duration': 0.5,
            'environment_noise_level': env_type,
            'calibrated': True
        }
    
    def reset_to_defaults(self) -> bool:
        """
        Reset settings to defaults
        
        Returns:
            bool: True if reset successfully
        """
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            print("✓ Microphone settings reset to defaults")
            return True
        except Exception as e:
            print(f"✗ Failed to reset settings: {e}")
            return False

# Test function
def test_config():
    """Test the configuration system"""
    config = MicConfig("test_mic_settings.json")
    
    # Test saving
    test_settings = {
        'energy_threshold': 500,
        'environment_noise_level': 'MEDIUM_NOISE'
    }
    
    print("Testing save...")
    config.save_settings(test_settings)
    
    print("Testing load...")
    loaded = config.load_settings()
    print(f"Loaded settings: {loaded}")
    
    print("Testing calibration check...")
    print(f"Is calibrated: {config.is_calibrated()}")
    
    # Clean up
    if os.path.exists("test_mic_settings.json"):
        os.remove("test_mic_settings.json")

if __name__ == "__main__":
    test_config()