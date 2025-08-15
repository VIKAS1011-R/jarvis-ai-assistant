#!/usr/bin/env python3
"""
Joke Service Module
Fetches jokes from various online APIs and provides fallback jokes
"""

import requests
import random
import json
from typing import Optional, Dict, Any

class JokeService:
    def __init__(self, timeout: int = 5):
        """
        Initialize joke service
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        
        # Fallback jokes in case APIs are down
        self.fallback_jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "I invented a new word: Plagiarism!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "I'm reading a book about anti-gravity. It's impossible to put down!",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
            "Why do we tell actors to 'break a leg?' Because every play has a cast!",
            "Helvetica and Times New Roman walk into a bar. The bartender says, 'Get out! We don't serve your type here.'",
            "I used to hate facial hair, but then it grew on me.",
            "Why don't programmers like nature? It has too many bugs!",
            "I would tell you a UDP joke, but you might not get it.",
            "There are only 10 types of people in the world: those who understand binary and those who don't.",
            "Why do Java developers wear glasses? Because they can't C#!",
            "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'"
        ]
        
        # API configurations
        self.apis = [
            {
                'name': 'JokeAPI',
                'url': 'https://v2.jokeapi.dev/joke/Programming,Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single',
                'parser': self._parse_jokeapi
            },
            {
                'name': 'Official Joke API',
                'url': 'https://official-joke-api.appspot.com/random_joke',
                'parser': self._parse_official_joke_api
            },
            {
                'name': 'icanhazdadjoke',
                'url': 'https://icanhazdadjoke.com/',
                'headers': {'Accept': 'application/json'},
                'parser': self._parse_icanhazdadjoke
            }
        ]
    
    def get_joke(self) -> str:
        """
        Get a joke from online APIs with fallback to local jokes
        
        Returns:
            str: A joke text
        """
        # Try each API
        for api in self.apis:
            try:
                joke = self._fetch_from_api(api)
                if joke:
                    print(f"Joke fetched from {api['name']}")
                    return joke
            except Exception as e:
                print(f"Failed to fetch from {api['name']}: {e}")
                continue
        
        # Fallback to local jokes
        print("Using fallback joke")
        return random.choice(self.fallback_jokes)
    
    def _fetch_from_api(self, api_config: Dict[str, Any]) -> Optional[str]:
        """
        Fetch joke from a specific API
        
        Args:
            api_config: API configuration dictionary
            
        Returns:
            str: Joke text or None if failed
        """
        headers = api_config.get('headers', {})
        
        response = requests.get(
            api_config['url'],
            headers=headers,
            timeout=self.timeout
        )
        
        if response.status_code == 200:
            return api_config['parser'](response.json())
        
        return None
    
    def _parse_jokeapi(self, data: Dict[str, Any]) -> Optional[str]:
        """Parse JokeAPI response"""
        if data.get('type') == 'single':
            return data.get('joke')
        elif data.get('type') == 'twopart':
            setup = data.get('setup', '')
            delivery = data.get('delivery', '')
            return f"{setup} {delivery}"
        return None
    
    def _parse_official_joke_api(self, data: Dict[str, Any]) -> Optional[str]:
        """Parse Official Joke API response"""
        setup = data.get('setup', '')
        punchline = data.get('punchline', '')
        if setup and punchline:
            return f"{setup} {punchline}"
        return None
    
    def _parse_icanhazdadjoke(self, data: Dict[str, Any]) -> Optional[str]:
        """Parse icanhazdadjoke API response"""
        return data.get('joke')
    
    def get_programming_joke(self) -> str:
        """
        Get a programming-specific joke
        
        Returns:
            str: A programming joke
        """
        programming_jokes = [
            joke for joke in self.fallback_jokes 
            if any(word in joke.lower() for word in ['programmer', 'programming', 'code', 'bug', 'java', 'python', 'sql', 'binary', 'udp'])
        ]
        
        # Try to get a programming joke from JokeAPI
        try:
            response = requests.get(
                'https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit',
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                joke = self._parse_jokeapi(data)
                if joke:
                    return joke
        except Exception:
            pass
        
        # Fallback to local programming jokes
        return random.choice(programming_jokes) if programming_jokes else random.choice(self.fallback_jokes)
    
    def get_dad_joke(self) -> str:
        """
        Get a dad joke specifically
        
        Returns:
            str: A dad joke
        """
        try:
            response = requests.get(
                'https://icanhazdadjoke.com/',
                headers={'Accept': 'application/json'},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                joke = self._parse_icanhazdadjoke(data)
                if joke:
                    return joke
        except Exception:
            pass
        
        # Fallback to random joke
        return random.choice(self.fallback_jokes)

# Test function
def test_joke_service():
    """Test the joke service"""
    print("Testing Joke Service")
    print("=" * 30)
    
    service = JokeService()
    
    print("1. Regular joke:")
    print(f"   {service.get_joke()}")
    
    print("\n2. Programming joke:")
    print(f"   {service.get_programming_joke()}")
    
    print("\n3. Dad joke:")
    print(f"   {service.get_dad_joke()}")

if __name__ == "__main__":
    test_joke_service()