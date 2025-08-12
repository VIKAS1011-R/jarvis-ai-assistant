#!/usr/bin/env python3
"""
J.A.R.V.I.S Response Module
Contains predefined responses and greeting messages
"""

from typing import List
import random

class JarvisResponses:
    """Collection of J.A.R.V.I.S responses and greetings"""
    
    # Wake word detection greetings
    GREETINGS = [
        "Good day, sir. How may I assist you?",
        "Jarvis at your service.",
        "Yes, sir? What can I do for you?",
        "I'm here and ready to help.",
        "At your command, sir.",
        "How can I be of assistance?",
        "Ready for your orders, sir.",
        "Jarvis online and operational.",
        "What do you need, sir?",
        "Standing by for instructions."
    ]
    
    # System startup messages
    STARTUP_MESSAGES = [
        "Jarvis online. Wake word detection activated.",
        "Systems initialized. Jarvis ready for service.",
        "All systems operational. Listening for wake word.",
        "Jarvis neural network online. Ready to assist."
    ]
    
    # System shutdown messages
    SHUTDOWN_MESSAGES = [
        "Jarvis going offline. Goodbye, sir.",
        "Systems shutting down. Until next time.",
        "Jarvis signing off.",
        "Powering down. Have a good day, sir."
    ]
    
    # Error messages
    ERROR_MESSAGES = [
        "I'm sorry, sir. I'm experiencing technical difficulties.",
        "There seems to be a system error. Please try again.",
        "My apologies, sir. Something went wrong.",
        "I'm having trouble processing that request."
    ]
    
    @classmethod
    def get_random_greeting(cls) -> str:
        """Get a random greeting message"""
        return random.choice(cls.GREETINGS)
    
    @classmethod
    def get_random_startup(cls) -> str:
        """Get a random startup message"""
        return random.choice(cls.STARTUP_MESSAGES)
    
    @classmethod
    def get_random_shutdown(cls) -> str:
        """Get a random shutdown message"""
        return random.choice(cls.SHUTDOWN_MESSAGES)
    
    @classmethod
    def get_random_error(cls) -> str:
        """Get a random error message"""
        return random.choice(cls.ERROR_MESSAGES)
    
    @classmethod
    def add_custom_greeting(cls, greeting: str):
        """Add a custom greeting to the collection"""
        if greeting not in cls.GREETINGS:
            cls.GREETINGS.append(greeting)
    
    @classmethod
    def add_custom_responses(cls, responses: List[str], category: str = "greetings"):
        """
        Add multiple custom responses to a category
        
        Args:
            responses: List of response strings
            category: Category to add to ("greetings", "startup", "shutdown", "error")
        """
        category_map = {
            "greetings": cls.GREETINGS,
            "startup": cls.STARTUP_MESSAGES,
            "shutdown": cls.SHUTDOWN_MESSAGES,
            "error": cls.ERROR_MESSAGES
        }
        
        if category in category_map:
            for response in responses:
                if response not in category_map[category]:
                    category_map[category].append(response)
        else:
            print(f"Unknown category: {category}")