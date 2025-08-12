#!/usr/bin/env python3
"""
Configuration Module
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration
        
        Args:
            env_file: Path to environment file
        """
        self.env_file = env_file
        self._load_environment()
    
    def _load_environment(self):
        """Load environment variables from .env file"""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            print(f"Environment loaded from {self.env_file}")
        else:
            print(f"Warning: {self.env_file} not found")
    
    @property
    def picovoice_access_key(self) -> str:
        """Get Picovoice access key from environment"""
        key = os.getenv('pico_access_key')
        if not key:
            raise ValueError("Picovoice access key not found. Check your .env file.")
        return key
    
    @property
    def wake_word_model_path(self) -> str:
        """Get path to wake word model"""
        return os.path.join('resources', 'Jarvis_en_windows_v3_0_0.ppn')
    
    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable with optional default
        
        Args:
            key: Environment variable key
            default: Default value if key not found
            
        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)
    
    def validate_setup(self) -> bool:
        """
        Validate that all required configuration is present
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Check access key
            if not self.picovoice_access_key:
                print("✗ Picovoice access key not configured")
                return False
            
            # Check wake word model
            if not os.path.exists(self.wake_word_model_path):
                print(f"✗ Wake word model not found: {self.wake_word_model_path}")
                return False
            
            print("✓ Configuration validation passed")
            return True
            
        except Exception as e:
            print(f"✗ Configuration validation failed: {e}")
            return False

# Default configuration instance
config = Config()