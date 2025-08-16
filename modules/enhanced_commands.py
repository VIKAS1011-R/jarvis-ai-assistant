#!/usr/bin/env python3
"""
Enhanced Commands Module
Integrates advanced NLU with existing JARVIS functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .intent_resolver import IntentResolver
    from .simple_commands import SimpleCommands
except ImportError:
    from intent_resolver import IntentResolver
    from simple_commands import SimpleCommands

from typing import Dict, Any, Optional

class EnhancedCommands:
    def __init__(self, tts):
        """
        Initialize Enhanced Commands with NLU capabilities
        
        Args:
            tts: Text-to-speech engine
        """
        self.tts = tts
        self.intent_resolver = IntentResolver()
        self.simple_commands = SimpleCommands(tts)
        
        # Map resolved functions to actual methods
        self.function_mappings = {
            'weather': self._handle_weather,
            'music': self._handle_music,
            'timer': self._handle_timer,
            'calculator': self._handle_calculator,
            'time': self._handle_time,
            'calendar': self._handle_calendar,
            'system': self._handle_system,
            'web': self._handle_web,
            'email': self._handle_email,
            'news': self._handle_news,
            'wikipedia': self._handle_wikipedia,
            'joke': self._handle_joke,
            'greeting': self._handle_greeting,
            'goodbye': self._handle_goodbye,
            'help': self._handle_help
        }
    
    def process_command(self, user_input: str) -> Optional[str]:
        """
        Process user command with advanced NLU
        
        Args:
            user_input: User's natural language input
            
        Returns:
            Optional[str]: "exit" if user wants to quit, None otherwise
        """
        try:
            # Resolve intent with context awareness
            result = self.intent_resolver.resolve_intent(user_input)
            
            # Check if clarification is needed
            if result['needs_clarification']:
                self._handle_clarification_needed(result)
                return None
            
            # Get resolved command
            resolved_command = result['resolved_command']
            
            if not resolved_command.get('function'):
                self.tts.speak("I'm not sure what you want me to do. Can you try rephrasing that?")
                return None
            
            # Execute the command
            response = self._execute_command(resolved_command, result)
            
            # Add interaction to context for future reference
            self.intent_resolver.add_interaction_to_context(
                user_input,
                response or "Command executed",
                resolved_command.get('function'),
                self._extract_entities_for_context(result)
            )
            
            # Check for exit command
            if resolved_command.get('function') == 'goodbye':
                return "exit"
            
            return None
            
        except Exception as e:
            print(f"Error processing command: {e}")
            self.tts.speak("I encountered an error processing that command. Please try again.")
            return None
    
    def _execute_command(self, resolved_command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Execute the resolved command"""
        function_name = resolved_command.get('function')
        handler = self.function_mappings.get(function_name)
        
        if not handler:
            self.tts.speak(f"I don't know how to handle {function_name} commands yet.")
            return f"Unknown function: {function_name}"
        
        try:
            response = handler(resolved_command, result)
            return response
        except Exception as e:
            print(f"Error executing {function_name}: {e}")
            self.tts.speak(f"I had trouble with that {function_name} command.")
            return f"Error in {function_name}: {str(e)}"
    
    def _handle_clarification_needed(self, result: Dict[str, Any]):
        """Handle cases where clarification is needed"""
        analysis = result['analysis']
        
        if analysis['confidence'] < 0.3:
            self.tts.speak("I'm not sure what you're asking for. Could you be more specific?")
        elif len(analysis['intents']) > 1:
            # Multiple possible intents
            intent1 = analysis['intents'][0]['intent']
            intent2 = analysis['intents'][1]['intent']
            self.tts.speak(f"Did you want me to help with {intent1} or {intent2}?")
        elif analysis['ambiguity']['has_ambiguity']:
            self.tts.speak("I need more context. What specifically are you referring to?")
        else:
            self.tts.speak("Could you rephrase that? I want to make sure I understand correctly.")
    
    def _extract_entities_for_context(self, result: Dict[str, Any]) -> list:
        """Extract entities for context tracking"""
        entities = []
        for entity_type, entity_list in result['analysis']['entities'].items():
            for entity in entity_list:
                entities.append(entity['value'])
        return entities
    
    # Command handlers - delegate to existing SimpleCommands where possible
    
    def _handle_weather(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle weather commands"""
        method = command.get('method', 'get_weather')
        parameters = command.get('parameters', {})
        
        if method == 'get_weather':
            location = parameters.get('location', '')
            if location:
                response = self.simple_commands.get_weather(f"weather in {location}")
            else:
                response = self.simple_commands.get_weather("weather")
        elif method == 'get_forecast':
            location = parameters.get('location', '')
            if location:
                response = self.simple_commands.get_weather(f"weather forecast {location}")
            else:
                response = self.simple_commands.get_weather("weather forecast")
        else:
            response = self.simple_commands.get_weather("weather")
        
        return response or "Weather information retrieved"
    
    def _handle_music(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle music commands"""
        method = command.get('method', 'play_music')
        parameters = command.get('parameters', {})
        
        if method == 'play_music':
            query = parameters.get('query', '')
            if query:
                self.simple_commands.play_music(f"play {query}")
                return f"Playing {query}"
            else:
                self.simple_commands.play_music("play music")
                return "Playing music"
        elif method == 'pause_music':
            self.simple_commands.pause_music()
            return "Music paused"
        elif method == 'resume_music':
            self.simple_commands.resume_music()
            return "Music resumed"
        elif method == 'next_music':
            self.simple_commands.next_track()
            return "Skipping to next track"
        elif method == 'previous_music':
            self.simple_commands.previous_track()
            return "Going to previous track"
        else:
            self.simple_commands.play_music("play music")
            return "Music command executed"
    
    def _handle_timer(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle timer commands"""
        method = command.get('method', 'set_timer')
        parameters = command.get('parameters', {})
        
        if method == 'set_timer':
            duration = parameters.get('duration', '5 minutes')
            self.simple_commands.set_timer(f"set timer {duration}")
            return f"Timer set for {duration}"
        elif method == 'cancel_timer':
            self.simple_commands.cancel_timer()
            return "Timer cancelled"
        elif method == 'check_timer':
            self.simple_commands.check_timers()
            return "Checking timers"
        else:
            self.simple_commands.set_timer("set timer 5 minutes")
            return "Timer command executed"
    
    def _handle_calculator(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle calculator commands"""
        parameters = command.get('parameters', {})
        expression = parameters.get('expression', '')
        
        if expression:
            response = self.simple_commands.calculate(f"calculate {expression}")
            return response or f"Calculated {expression}"
        else:
            self.tts.speak("What would you like me to calculate?")
            return "Calculator ready"
    
    def _handle_time(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle time commands"""
        self.simple_commands.get_time()
        return "Current time provided"
    
    def _handle_calendar(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle calendar commands"""
        self.simple_commands.get_calendar_events()
        return "Calendar events retrieved"
    
    def _handle_system(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle system commands"""
        self.simple_commands.get_system_info()
        return "System information provided"
    
    def _handle_web(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle web commands"""
        parameters = command.get('parameters', {})
        query = parameters.get('query', '')
        
        if query:
            self.simple_commands.web_search(f"search {query}")
            return f"Searching for {query}"
        else:
            self.simple_commands.web_search("search")
            return "Web search executed"
    
    def _handle_email(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle email commands"""
        self.simple_commands.check_email()
        return "Email checked"
    
    def _handle_news(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle news commands"""
        self.simple_commands.get_news()
        return "News headlines retrieved"
    
    def _handle_wikipedia(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle Wikipedia commands"""
        parameters = command.get('parameters', {})
        topic = parameters.get('topic', '')
        
        if topic:
            self.simple_commands.search_wikipedia(f"wikipedia {topic}")
            return f"Wikipedia search for {topic}"
        else:
            self.tts.speak("What would you like me to look up on Wikipedia?")
            return "Wikipedia ready"
    
    def _handle_joke(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle joke commands"""
        self.simple_commands.tell_joke()
        return "Joke told"
    
    def _handle_greeting(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle greeting commands"""
        self.simple_commands.respond_to_greeting()
        return "Greeting responded"
    
    def _handle_goodbye(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle goodbye commands"""
        self.simple_commands.handle_exit()
        return "Goodbye"
    
    def _handle_help(self, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Handle help commands"""
        self.simple_commands.show_help()
        return "Help provided"
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return self.intent_resolver.get_conversation_summary()
    
    def clear_context(self):
        """Clear conversation context"""
        self.intent_resolver.clear_context()
    
    def save_context(self, filepath: str):
        """Save conversation context"""
        self.intent_resolver.save_context(filepath)
    
    def load_context(self, filepath: str):
        """Load conversation context"""
        self.intent_resolver.load_context(filepath)

# Test function
def test_enhanced_commands():
    """Test the Enhanced Commands system"""
    print("Testing Enhanced Commands System")
    print("=" * 40)
    
    # Mock TTS for testing
    class MockTTS:
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    enhanced_commands = EnhancedCommands(MockTTS())
    
    # Test conversation with context
    test_conversation = [
        "What's the weather like in Seattle?",
        "What about tomorrow?",  # Should understand this refers to weather
        "Play some classical music",
        "Play something more upbeat",  # Should understand this refers to music
        "Set a timer for 15 minutes",
        "Calculate 42 times 7"
    ]
    
    for i, user_input in enumerate(test_conversation, 1):
        print(f"\n{i}. User: '{user_input}'")
        
        try:
            result = enhanced_commands.process_command(user_input)
            print(f"   ✓ Command processed successfully")
            if result == "exit":
                print("   → Exit command detected")
                break
        except Exception as e:
            print(f"   ✗ Error: {e}")
    
    print(f"\n✓ Enhanced Commands test completed!")
    
    # Show conversation summary
    summary = enhanced_commands.get_conversation_summary()
    print(f"\nConversation Summary:")
    print(f"   Total interactions: {summary['total_interactions']}")
    print(f"   Current topic: {summary['current_topic']}")
    print(f"   Context variables: {summary['context_vars']}")

if __name__ == "__main__":
    test_enhanced_commands()