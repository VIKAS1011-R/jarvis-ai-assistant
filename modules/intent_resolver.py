#!/usr/bin/env python3
"""
Intent Resolver
Combines NLU Engine with Conversation Context for intelligent command resolution
"""

from typing import Dict, List, Optional, Any, Tuple
try:
    from .conversation_context import ConversationContext
    from .nlu_engine import NLUEngine
except ImportError:
    from conversation_context import ConversationContext
    from nlu_engine import NLUEngine
import re

class IntentResolver:
    def __init__(self):
        """Initialize the Intent Resolver"""
        self.context = ConversationContext()
        self.nlu = NLUEngine()
        
        # Command mapping to actual functions
        self.command_mappings = {
            'weather': self._resolve_weather_command,
            'music': self._resolve_music_command,
            'timer': self._resolve_timer_command,
            'calculator': self._resolve_calculator_command,
            'time': self._resolve_time_command,
            'calendar': self._resolve_calendar_command,
            'system': self._resolve_system_command,
            'web': self._resolve_web_command,
            'email': self._resolve_email_command,
            'news': self._resolve_news_command,
            'wikipedia': self._resolve_wikipedia_command,
            'joke': self._resolve_joke_command,
            'greeting': self._resolve_greeting_command,
            'goodbye': self._resolve_goodbye_command,
            'help': self._resolve_help_command
        }
    
    def resolve_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Main method to resolve user intent with context awareness
        
        Args:
            user_input: User's natural language input
            
        Returns:
            Dict containing resolved command and metadata
        """
        # Get conversation context
        context = self.context.get_context_for_input(user_input)
        
        # Check if this is a follow-up question
        if context['is_follow_up']:
            follow_up_result = self.context.resolve_follow_up(user_input)
            if follow_up_result['resolved']:
                # Use the resolved input for NLU analysis
                user_input = follow_up_result['resolved_input']
                context['follow_up_resolved'] = True
        
        # Perform NLU analysis
        analysis = self.nlu.analyze_input(user_input, context)
        
        # Generate structured command
        command = self.nlu.generate_command(analysis)
        
        # Resolve command to actual function call
        resolved_command = self._resolve_to_function_call(command, analysis, context)
        
        # Prepare response
        response = {
            'original_input': user_input,
            'resolved_command': resolved_command,
            'analysis': analysis,
            'context': context,
            'confidence': analysis['confidence'],
            'needs_clarification': self._needs_clarification(analysis, context)
        }
        
        return response
    
    def _resolve_to_function_call(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve command to actual function call"""
        if not command.get('intent'):
            return {'function': None, 'error': 'No intent detected'}
        
        intent = command['intent']
        
        # Get resolver function
        resolver = self.command_mappings.get(intent)
        if not resolver:
            return {'function': None, 'error': f'No resolver for intent: {intent}'}
        
        # Resolve the command
        try:
            resolved = resolver(command, analysis, context)
            return resolved
        except Exception as e:
            return {'function': None, 'error': f'Error resolving {intent}: {str(e)}'}
    
    def _resolve_weather_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve weather commands"""
        function_call = {
            'function': 'weather',
            'method': 'get_weather',
            'parameters': {}
        }
        
        # Determine location
        location = None
        if 'location' in command.get('parameters', {}):
            location = command['parameters']['location']
        elif context.get('context_vars', {}).get('last_location'):
            location = context['context_vars']['last_location']
        
        if location:
            function_call['parameters']['location'] = location
        
        # Determine if forecast or current
        if command.get('type') == 'forecast':
            function_call['method'] = 'get_forecast'
        
        return function_call
    
    def _resolve_music_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve music commands"""
        action = command.get('action', 'play')
        
        function_call = {
            'function': 'music',
            'method': f'{action}_music',
            'parameters': {}
        }
        
        # Handle play command
        if action == 'play':
            query = None
            if 'query' in command.get('parameters', {}):
                query = command['parameters']['query']
            elif context.get('context_vars', {}).get('last_music_query'):
                query = context['context_vars']['last_music_query']
            
            if query:
                function_call['parameters']['query'] = query
            else:
                # Extract query from original input
                play_match = re.search(r'play\s+(.+)', analysis['original_input'], re.IGNORECASE)
                if play_match:
                    function_call['parameters']['query'] = play_match.group(1).strip()
        
        return function_call
    
    def _resolve_timer_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve timer commands"""
        action = command.get('action', 'set')
        
        function_call = {
            'function': 'timer',
            'method': f'{action}_timer',
            'parameters': {}
        }
        
        # Handle set timer
        if action == 'set':
            duration = None
            if 'duration' in command.get('parameters', {}):
                duration = command['parameters']['duration']
            else:
                # Extract duration from original input
                duration_match = re.search(r'(\d+)\s*(minute|hour|second)', analysis['original_input'], re.IGNORECASE)
                if duration_match:
                    duration = f"{duration_match.group(1)} {duration_match.group(2)}"
            
            if duration:
                function_call['parameters']['duration'] = duration
        
        return function_call
    
    def _resolve_calculator_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve calculator commands"""
        function_call = {
            'function': 'calculator',
            'method': 'calculate',
            'parameters': {}
        }
        
        # Extract mathematical expression
        math_match = re.search(r'(\d+\s*[\+\-\*\/]\s*\d+)', analysis['original_input'])
        if math_match:
            function_call['parameters']['expression'] = math_match.group(1)
        else:
            # Try to extract from words
            expression = self._extract_math_from_words(analysis['original_input'])
            if expression:
                function_call['parameters']['expression'] = expression
        
        return function_call
    
    def _extract_math_from_words(self, text: str) -> Optional[str]:
        """Extract mathematical expression from words"""
        # Simple word-to-number conversion
        word_to_num = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13',
            'fourteen': '14', 'fifteen': '15', 'sixteen': '16', 'seventeen': '17',
            'eighteen': '18', 'nineteen': '19', 'twenty': '20'
        }
        
        word_to_op = {
            'plus': '+', 'add': '+', 'added to': '+',
            'minus': '-', 'subtract': '-', 'take away': '-',
            'times': '*', 'multiply': '*', 'multiplied by': '*',
            'divide': '/', 'divided by': '/'
        }
        
        # This is a simplified implementation
        # In a real system, you'd want more sophisticated parsing
        text_lower = text.lower()
        
        # Look for patterns like "fifteen plus twenty seven"
        pattern = r'(\w+)\s+(plus|minus|times|divide|add|subtract|multiply)\s+(\w+)'
        match = re.search(pattern, text_lower)
        
        if match:
            num1_word, op_word, num2_word = match.groups()
            
            num1 = word_to_num.get(num1_word, num1_word)
            num2 = word_to_num.get(num2_word, num2_word)
            op = word_to_op.get(op_word, op_word)
            
            if num1.isdigit() and num2.isdigit() and op in ['+', '-', '*', '/']:
                return f"{num1} {op} {num2}"
        
        return None
    
    def _resolve_time_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve time commands"""
        return {
            'function': 'time',
            'method': 'get_current_time',
            'parameters': {}
        }
    
    def _resolve_calendar_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve calendar commands"""
        return {
            'function': 'calendar',
            'method': 'get_events',
            'parameters': {}
        }
    
    def _resolve_system_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve system commands"""
        return {
            'function': 'system',
            'method': 'get_system_info',
            'parameters': {}
        }
    
    def _resolve_web_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve web commands"""
        function_call = {
            'function': 'web',
            'method': 'search',
            'parameters': {}
        }
        
        # Extract search query
        if 'search_query' in analysis.get('entities', {}):
            function_call['parameters']['query'] = analysis['entities']['search_query'][0]['value']
        else:
            # Try to extract from input
            search_match = re.search(r'(?:search|google)\s+(?:for\s+)?(.+)', analysis['original_input'], re.IGNORECASE)
            if search_match:
                function_call['parameters']['query'] = search_match.group(1).strip()
        
        return function_call
    
    def _resolve_email_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve email commands"""
        return {
            'function': 'email',
            'method': 'check_email',
            'parameters': {}
        }
    
    def _resolve_news_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve news commands"""
        return {
            'function': 'news',
            'method': 'get_headlines',
            'parameters': {}
        }
    
    def _resolve_wikipedia_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve Wikipedia commands"""
        function_call = {
            'function': 'wikipedia',
            'method': 'search',
            'parameters': {}
        }
        
        # Extract search topic
        topic_patterns = [
            r'(?:tell me about|what is|information about)\s+(.+)',
            r'wikipedia\s+(.+)',
            r'wiki\s+(.+)'
        ]
        
        for pattern in topic_patterns:
            match = re.search(pattern, analysis['original_input'], re.IGNORECASE)
            if match:
                function_call['parameters']['topic'] = match.group(1).strip()
                break
        
        return function_call
    
    def _resolve_joke_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve joke commands"""
        return {
            'function': 'joke',
            'method': 'tell_joke',
            'parameters': {}
        }
    
    def _resolve_greeting_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve greeting commands"""
        return {
            'function': 'greeting',
            'method': 'respond_greeting',
            'parameters': {}
        }
    
    def _resolve_goodbye_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve goodbye commands"""
        return {
            'function': 'goodbye',
            'method': 'respond_goodbye',
            'parameters': {}
        }
    
    def _resolve_help_command(self, command: Dict[str, Any], analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve help commands"""
        return {
            'function': 'help',
            'method': 'show_help',
            'parameters': {}
        }
    
    def _needs_clarification(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Determine if the command needs clarification"""
        # Low confidence
        if analysis['confidence'] < 0.5:
            return True
        
        # Multiple intents with similar confidence
        if len(analysis['intents']) > 1:
            if analysis['intents'][0]['confidence'] - analysis['intents'][1]['confidence'] < 0.2:
                return True
        
        # Ambiguous and no context to resolve
        if analysis['ambiguity']['has_ambiguity'] and not context.get('referenced_topic'):
            return True
        
        return False
    
    def add_interaction_to_context(self, user_input: str, jarvis_response: str, command_type: str = None, entities: List[str] = None):
        """Add interaction to conversation context"""
        self.context.add_interaction(user_input, jarvis_response, command_type, entities)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return self.context.get_conversation_summary()
    
    def clear_context(self):
        """Clear conversation context"""
        self.context.clear_context()
    
    def save_context(self, filepath: str):
        """Save conversation context"""
        self.context.save_context(filepath)
    
    def load_context(self, filepath: str):
        """Load conversation context"""
        self.context.load_context(filepath)

# Test function
def test_intent_resolver():
    """Test the Intent Resolver"""
    print("Testing Intent Resolver")
    print("=" * 30)
    
    resolver = IntentResolver()
    
    # Test conversation flow
    test_conversation = [
        "What's the weather like in San Francisco?",
        "What about tomorrow?",  # Follow-up
        "Play some jazz music",
        "Play something different",  # Follow-up
        "Set a timer for 10 minutes",
        "Calculate 25 plus 17"
    ]
    
    for i, user_input in enumerate(test_conversation, 1):
        print(f"\n{i}. User: '{user_input}'")
        
        # Resolve intent
        result = resolver.resolve_intent(user_input)
        
        print(f"   Intent: {result['resolved_command'].get('function', 'Unknown')}")
        print(f"   Method: {result['resolved_command'].get('method', 'Unknown')}")
        print(f"   Parameters: {result['resolved_command'].get('parameters', {})}")
        print(f"   Confidence: {result['confidence']:.2f}")
        print(f"   Follow-up: {result['context'].get('is_follow_up', False)}")
        print(f"   Needs clarification: {result['needs_clarification']}")
        
        # Add to context for next iteration
        resolver.add_interaction_to_context(
            user_input,
            f"Processed {result['resolved_command'].get('function', 'unknown')} command",
            result['resolved_command'].get('function')
        )
    
    print(f"\n✓ Intent Resolver test completed!")
    
    # Show conversation summary
    summary = resolver.get_conversation_summary()
    print(f"\nConversation Summary:")
    print(f"   Total interactions: {summary['total_interactions']}")
    print(f"   Current topic: {summary['current_topic']}")
    print(f"   Context variables: {summary['context_vars']}")

if __name__ == "__main__":
    test_intent_resolver()