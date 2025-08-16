#!/usr/bin/env python3
"""
Conversation Context Manager
Handles conversation memory, context tracking, and follow-up understanding
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

class ConversationContext:
    def __init__(self, max_history: int = 50, context_timeout: int = 300):
        """
        Initialize conversation context manager
        
        Args:
            max_history: Maximum number of conversation turns to remember
            context_timeout: Context timeout in seconds (5 minutes default)
        """
        self.max_history = max_history
        self.context_timeout = context_timeout
        
        # Conversation history
        self.conversation_history: List[Dict[str, Any]] = []
        
        # Current context tracking
        self.current_topic = None
        self.current_entity = None
        self.last_command_type = None
        self.last_response_time = None
        
        # Context variables for follow-up questions
        self.context_vars = {}
        
        # Entity tracking (people, places, things mentioned)
        self.entities = {}
        
    def add_interaction(self, user_input: str, jarvis_response: str, command_type: str = None, entities: List[str] = None):
        """
        Add a new interaction to conversation history
        
        Args:
            user_input: What the user said
            jarvis_response: How JARVIS responded
            command_type: Type of command (weather, music, etc.)
            entities: Entities mentioned in the conversation
        """
        interaction = {
            'timestamp': datetime.now(),
            'user_input': user_input,
            'jarvis_response': jarvis_response,
            'command_type': command_type,
            'entities': entities or []
        }
        
        self.conversation_history.append(interaction)
        
        # Maintain history size
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        
        # Update current context
        self.last_command_type = command_type
        self.last_response_time = datetime.now()
        
        # Update entities
        if entities:
            for entity in entities:
                self.entities[entity] = datetime.now()
        
        # Extract and update context variables
        self._update_context_vars(user_input, command_type)
    
    def _update_context_vars(self, user_input: str, command_type: str):
        """Update context variables based on the interaction"""
        if command_type == 'weather':
            # Extract location if mentioned
            location_match = re.search(r'\b(?:in|for|at)\s+([A-Za-z\s]+)', user_input, re.IGNORECASE)
            if location_match:
                self.context_vars['last_location'] = location_match.group(1).strip()
            
        elif command_type == 'music':
            # Extract artist or song
            play_match = re.search(r'play\s+(.+)', user_input, re.IGNORECASE)
            if play_match:
                self.context_vars['last_music_query'] = play_match.group(1).strip()
        
        elif command_type == 'timer':
            # Extract timer duration
            timer_match = re.search(r'(\d+)\s*(minute|hour|second)', user_input, re.IGNORECASE)
            if timer_match:
                self.context_vars['last_timer_duration'] = f"{timer_match.group(1)} {timer_match.group(2)}"
    
    def get_context_for_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input and provide relevant context
        
        Args:
            user_input: Current user input
            
        Returns:
            Dict containing context information
        """
        context = {
            'is_follow_up': self._is_follow_up_question(user_input),
            'referenced_topic': self._get_referenced_topic(user_input),
            'implied_command': self._get_implied_command(user_input),
            'context_vars': self.context_vars.copy(),
            'recent_entities': self._get_recent_entities(),
            'conversation_flow': self._analyze_conversation_flow()
        }
        
        return context
    
    def _is_follow_up_question(self, user_input: str) -> bool:
        """Check if this is a follow-up question"""
        if not self.last_response_time:
            return False
        
        # Check if within context timeout
        if datetime.now() - self.last_response_time > timedelta(seconds=self.context_timeout):
            return False
        
        # Check for follow-up indicators
        follow_up_patterns = [
            r'\b(what about|how about|and)\b',
            r'\b(also|too|as well)\b',
            r'\b(tomorrow|yesterday|next|last)\b',
            r'\b(there|here|that|this)\b',
            r'\b(more|another|different)\b'
        ]
        
        for pattern in follow_up_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return True
        
        return False
    
    def _get_referenced_topic(self, user_input: str) -> Optional[str]:
        """Determine what topic is being referenced"""
        if not self.last_command_type:
            return None
        
        # Pronouns and references that might refer to previous topic
        reference_patterns = [
            r'\b(it|that|this|there|here)\b',
            r'\b(tomorrow|yesterday|next|last)\b',
            r'\b(more|another|different)\b'
        ]
        
        for pattern in reference_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return self.last_command_type
        
        return None
    
    def _get_implied_command(self, user_input: str) -> Optional[str]:
        """Determine implied command based on context"""
        if not self._is_follow_up_question(user_input):
            return None
        
        # Map follow-up patterns to likely commands
        if self.last_command_type == 'weather':
            if re.search(r'\b(tomorrow|next|later)\b', user_input, re.IGNORECASE):
                return 'weather_forecast'
            elif re.search(r'\b(there|that place)\b', user_input, re.IGNORECASE):
                return 'weather_location'
        
        elif self.last_command_type == 'music':
            if re.search(r'\b(more|another|different)\b', user_input, re.IGNORECASE):
                return 'music_similar'
            elif re.search(r'\b(pause|stop|next|previous)\b', user_input, re.IGNORECASE):
                return 'music_control'
        
        return self.last_command_type
    
    def _get_recent_entities(self) -> List[str]:
        """Get recently mentioned entities"""
        cutoff_time = datetime.now() - timedelta(seconds=self.context_timeout)
        recent_entities = []
        
        for entity, timestamp in self.entities.items():
            if timestamp > cutoff_time:
                recent_entities.append(entity)
        
        return recent_entities
    
    def _analyze_conversation_flow(self) -> Dict[str, Any]:
        """Analyze the flow of conversation"""
        if len(self.conversation_history) < 2:
            return {'pattern': 'initial', 'trend': 'none'}
        
        recent_commands = [h.get('command_type') for h in self.conversation_history[-5:]]
        
        # Detect patterns
        if len(set(recent_commands)) == 1 and recent_commands[0]:
            pattern = 'focused'  # User is focused on one type of command
        elif len(recent_commands) > 2 and recent_commands[-1] == recent_commands[-3]:
            pattern = 'alternating'  # User is alternating between command types
        else:
            pattern = 'varied'  # Mixed conversation
        
        return {
            'pattern': pattern,
            'recent_commands': recent_commands,
            'dominant_topic': max(set(recent_commands), key=recent_commands.count) if recent_commands else None
        }
    
    def resolve_follow_up(self, user_input: str) -> Dict[str, Any]:
        """
        Resolve follow-up questions by adding context
        
        Args:
            user_input: User's follow-up question
            
        Returns:
            Dict with resolved command and context
        """
        context = self.get_context_for_input(user_input)
        
        if not context['is_follow_up']:
            return {'resolved': False, 'original_input': user_input}
        
        resolved_input = user_input
        command_type = context['implied_command']
        
        # Resolve weather follow-ups
        if context['referenced_topic'] == 'weather':
            if 'tomorrow' in user_input.lower():
                resolved_input = f"weather forecast tomorrow"
                if 'last_location' in context['context_vars']:
                    resolved_input += f" in {context['context_vars']['last_location']}"
            elif 'there' in user_input.lower() and 'last_location' in context['context_vars']:
                resolved_input = f"weather in {context['context_vars']['last_location']}"
        
        # Resolve music follow-ups
        elif context['referenced_topic'] == 'music':
            if 'more' in user_input.lower() or 'another' in user_input.lower():
                if 'last_music_query' in context['context_vars']:
                    resolved_input = f"play similar to {context['context_vars']['last_music_query']}"
        
        return {
            'resolved': True,
            'original_input': user_input,
            'resolved_input': resolved_input,
            'command_type': command_type,
            'context': context
        }
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation state"""
        return {
            'total_interactions': len(self.conversation_history),
            'current_topic': self.last_command_type,
            'context_vars': self.context_vars,
            'recent_entities': self._get_recent_entities(),
            'conversation_flow': self._analyze_conversation_flow(),
            'last_interaction': self.conversation_history[-1] if self.conversation_history else None
        }
    
    def clear_context(self):
        """Clear conversation context (but keep history)"""
        self.current_topic = None
        self.current_entity = None
        self.last_command_type = None
        self.context_vars.clear()
    
    def save_context(self, filepath: str):
        """Save conversation context to file"""
        try:
            context_data = {
                'conversation_history': [
                    {
                        **interaction,
                        'timestamp': interaction['timestamp'].isoformat()
                    }
                    for interaction in self.conversation_history
                ],
                'context_vars': self.context_vars,
                'entities': {
                    entity: timestamp.isoformat()
                    for entity, timestamp in self.entities.items()
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving context: {e}")
    
    def load_context(self, filepath: str):
        """Load conversation context from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                context_data = json.load(f)
            
            # Restore conversation history
            self.conversation_history = []
            for interaction in context_data.get('conversation_history', []):
                interaction['timestamp'] = datetime.fromisoformat(interaction['timestamp'])
                self.conversation_history.append(interaction)
            
            # Restore context vars
            self.context_vars = context_data.get('context_vars', {})
            
            # Restore entities
            self.entities = {
                entity: datetime.fromisoformat(timestamp)
                for entity, timestamp in context_data.get('entities', {}).items()
            }
            
            # Update current state
            if self.conversation_history:
                last_interaction = self.conversation_history[-1]
                self.last_command_type = last_interaction.get('command_type')
                self.last_response_time = last_interaction['timestamp']
                
        except Exception as e:
            print(f"Error loading context: {e}")

# Test function
def test_conversation_context():
    """Test the conversation context system"""
    print("Testing Conversation Context System")
    print("=" * 40)
    
    context = ConversationContext()
    
    # Simulate a conversation
    print("1. Initial weather query:")
    context.add_interaction(
        "what's the weather in New York?",
        "It's sunny and 75°F in New York",
        "weather",
        ["New York"]
    )
    
    print("2. Follow-up question:")
    follow_up = context.resolve_follow_up("what about tomorrow?")
    print(f"   Original: 'what about tomorrow?'")
    print(f"   Resolved: '{follow_up.get('resolved_input', 'Not resolved')}'")
    print(f"   Is follow-up: {follow_up.get('resolved', False)}")
    
    print("\n3. Music conversation:")
    context.add_interaction(
        "play some jazz music",
        "Playing jazz music on Spotify",
        "music",
        ["jazz"]
    )
    
    follow_up2 = context.resolve_follow_up("play something different")
    print(f"   Original: 'play something different'")
    print(f"   Resolved: '{follow_up2.get('resolved_input', 'Not resolved')}'")
    
    print("\n4. Conversation summary:")
    summary = context.get_conversation_summary()
    print(f"   Total interactions: {summary['total_interactions']}")
    print(f"   Current topic: {summary['current_topic']}")
    print(f"   Context vars: {summary['context_vars']}")
    
    print("\n✓ Conversation context system test completed!")

if __name__ == "__main__":
    test_conversation_context()