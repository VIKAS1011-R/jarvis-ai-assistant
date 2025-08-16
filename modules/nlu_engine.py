#!/usr/bin/env python3
"""
Natural Language Understanding Engine
Advanced intent classification, entity extraction, and command understanding
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import spacy
from collections import defaultdict

class NLUEngine:
    def __init__(self):
        """Initialize the NLU Engine"""
        self.nlp = None
        self._load_spacy_model()
        
        # Intent patterns and classifications
        self.intent_patterns = self._load_intent_patterns()
        
        # Entity patterns
        self.entity_patterns = self._load_entity_patterns()
        
        # Command templates
        self.command_templates = self._load_command_templates()
        
    def _load_spacy_model(self):
        """Load spaCy model for NLP processing"""
        try:
            import spacy
            # Try to load English model
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("spaCy English model not found. Installing...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")
        except ImportError:
            print("spaCy not installed. Using basic NLU without advanced features.")
            self.nlp = None
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent classification patterns"""
        return {
            'weather': [
                r'\b(weather|temperature|forecast|rain|sunny|cloudy|storm)\b',
                r'\b(how.*(?:hot|cold|warm))\b',
                r'\b(will it rain|is it raining)\b'
            ],
            'music': [
                r'\b(play|music|song|artist|album|spotify|youtube)\b',
                r'\b(pause|resume|stop|next|previous|skip)\b',
                r'\b(volume|loud|quiet)\b'
            ],
            'time': [
                r'\b(time|clock|hour|minute|when)\b',
                r'\b(what time|current time)\b'
            ],
            'calendar': [
                r'\b(calendar|appointment|meeting|schedule|event)\b',
                r'\b(today|tomorrow|next week|this week)\b'
            ],
            'timer': [
                r'\b(timer|alarm|remind|countdown)\b',
                r'\b(set.*timer|start.*timer)\b'
            ],
            'calculator': [
                r'\b(calculate|math|plus|minus|times|divide)\b',
                r'\b(\d+\s*[\+\-\*\/]\s*\d+)\b'
            ],
            'system': [
                r'\b(system|computer|cpu|memory|disk|battery)\b',
                r'\b(shutdown|restart|sleep)\b'
            ],
            'web': [
                r'\b(search|google|open|website|browser)\b',
                r'\b(youtube|github|stackoverflow)\b'
            ],
            'email': [
                r'\b(email|mail|message|send)\b',
                r'\b(inbox|unread)\b'
            ],
            'news': [
                r'\b(news|headlines|breaking|latest)\b',
                r'\b(what.*happening|current events)\b'
            ],
            'wikipedia': [
                r'\b(wikipedia|wiki|tell me about|what is)\b',
                r'\b(information about|facts about)\b'
            ],
            'joke': [
                r'\b(joke|funny|humor|laugh)\b',
                r'\b(tell me.*joke|make me laugh)\b'
            ],
            'greeting': [
                r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b',
                r'\b(how are you|what\'s up)\b'
            ],
            'goodbye': [
                r'\b(bye|goodbye|see you|exit|quit|stop)\b',
                r'\b(shut down|turn off)\b'
            ],
            'help': [
                r'\b(help|assist|support|what can you do)\b',
                r'\b(commands|functions|capabilities)\b'
            ]
        }
    
    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """Load entity extraction patterns"""
        return {
            'location': [
                r'\b(?:in|at|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
                r'\b(New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose)\b'
            ],
            'time': [
                r'\b(\d{1,2}:\d{2}(?:\s*[AaPp][Mm])?)\b',
                r'\b(morning|afternoon|evening|night|noon|midnight)\b',
                r'\b(today|tomorrow|yesterday|next week|last week)\b'
            ],
            'duration': [
                r'\b(\d+)\s*(second|minute|hour|day|week|month|year)s?\b',
                r'\b(a|an|one)\s*(second|minute|hour|day|week|month|year)\b'
            ],
            'number': [
                r'\b(\d+(?:\.\d+)?)\b',
                r'\b(one|two|three|four|five|six|seven|eight|nine|ten)\b'
            ],
            'person': [
                r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b'  # First Last name pattern
            ],
            'music_query': [
                r'\bplay\s+(.+?)(?:\s+(?:on|by|from)|\s*$)',
                r'\b(?:song|track|music)\s+(.+?)(?:\s+by|\s*$)'
            ],
            'search_query': [
                r'\bsearch\s+(?:for\s+)?(.+?)(?:\s+on|\s*$)',
                r'\bgoogle\s+(.+?)(?:\s+for|\s*$)'
            ]
        }
    
    def _load_command_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load command templates for intent resolution"""
        return {
            'weather': {
                'base_command': 'weather',
                'parameters': ['location', 'time'],
                'default_location': 'current',
                'variations': {
                    'forecast': ['tomorrow', 'next', 'later', 'forecast'],
                    'current': ['now', 'current', 'today']
                }
            },
            'music': {
                'base_command': 'music',
                'parameters': ['action', 'query'],
                'actions': {
                    'play': ['play', 'start', 'begin'],
                    'pause': ['pause', 'stop', 'halt'],
                    'resume': ['resume', 'continue', 'unpause'],
                    'next': ['next', 'skip', 'forward'],
                    'previous': ['previous', 'back', 'last']
                }
            },
            'timer': {
                'base_command': 'timer',
                'parameters': ['duration', 'action'],
                'actions': {
                    'set': ['set', 'start', 'create'],
                    'cancel': ['cancel', 'stop', 'delete'],
                    'check': ['check', 'status', 'how long']
                }
            }
        }
    
    def analyze_input(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive analysis of user input
        
        Args:
            user_input: User's natural language input
            context: Conversation context from ConversationContext
            
        Returns:
            Dict containing analysis results
        """
        analysis = {
            'original_input': user_input,
            'processed_input': self._preprocess_input(user_input),
            'intents': self._classify_intents(user_input),
            'entities': self._extract_entities(user_input),
            'command_structure': self._parse_command_structure(user_input),
            'confidence': 0.0,
            'ambiguity': self._detect_ambiguity(user_input),
            'context_dependent': self._is_context_dependent(user_input, context)
        }
        
        # Calculate overall confidence
        analysis['confidence'] = self._calculate_confidence(analysis)
        
        # Resolve with context if available
        if context and analysis['context_dependent']:
            analysis = self._resolve_with_context(analysis, context)
        
        return analysis
    
    def _preprocess_input(self, user_input: str) -> str:
        """Preprocess user input for better analysis"""
        # Convert to lowercase
        processed = user_input.lower().strip()
        
        # Remove common filler words that don't affect meaning
        filler_words = ['um', 'uh', 'like', 'you know', 'well']
        for filler in filler_words:
            processed = re.sub(rf'\b{filler}\b', '', processed)
        
        # Normalize contractions
        contractions = {
            "what's": "what is",
            "how's": "how is",
            "where's": "where is",
            "when's": "when is",
            "who's": "who is",
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "didn't": "did not"
        }
        
        for contraction, expansion in contractions.items():
            processed = processed.replace(contraction, expansion)
        
        return processed.strip()
    
    def _classify_intents(self, user_input: str) -> List[Dict[str, Any]]:
        """Classify user intents with confidence scores"""
        intents = []
        processed_input = self._preprocess_input(user_input)
        
        for intent, patterns in self.intent_patterns.items():
            confidence = 0.0
            matched_patterns = []
            
            for pattern in patterns:
                matches = re.findall(pattern, processed_input, re.IGNORECASE)
                if matches:
                    confidence += 0.3  # Base confidence per pattern match
                    matched_patterns.append(pattern)
            
            # Boost confidence for multiple pattern matches
            if len(matched_patterns) > 1:
                confidence += 0.2
            
            # Boost confidence for exact keyword matches
            intent_keywords = self._get_intent_keywords(intent)
            for keyword in intent_keywords:
                if keyword in processed_input:
                    confidence += 0.1
            
            if confidence > 0:
                intents.append({
                    'intent': intent,
                    'confidence': min(confidence, 1.0),
                    'matched_patterns': matched_patterns
                })
        
        # Sort by confidence
        intents.sort(key=lambda x: x['confidence'], reverse=True)
        return intents
    
    def _get_intent_keywords(self, intent: str) -> List[str]:
        """Get key words associated with an intent"""
        keywords = {
            'weather': ['weather', 'temperature', 'rain', 'sunny', 'cloudy'],
            'music': ['play', 'music', 'song', 'pause', 'volume'],
            'time': ['time', 'clock', 'hour', 'minute'],
            'calendar': ['calendar', 'meeting', 'appointment', 'schedule'],
            'timer': ['timer', 'alarm', 'remind', 'countdown'],
            'calculator': ['calculate', 'math', 'plus', 'minus'],
            'system': ['system', 'computer', 'cpu', 'memory'],
            'web': ['search', 'google', 'open', 'website'],
            'email': ['email', 'mail', 'message', 'inbox'],
            'news': ['news', 'headlines', 'breaking'],
            'wikipedia': ['wikipedia', 'wiki', 'information'],
            'joke': ['joke', 'funny', 'humor', 'laugh'],
            'greeting': ['hello', 'hi', 'hey', 'morning'],
            'goodbye': ['bye', 'goodbye', 'exit', 'quit'],
            'help': ['help', 'assist', 'support', 'commands']
        }
        return keywords.get(intent, [])
    
    def _extract_entities(self, user_input: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract entities from user input"""
        entities = defaultdict(list)
        
        # Use regex patterns for entity extraction
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, user_input, re.IGNORECASE)
                for match in matches:
                    entity_value = match.group(1) if match.groups() else match.group(0)
                    entities[entity_type].append({
                        'value': entity_value.strip(),
                        'start': match.start(),
                        'end': match.end(),
                        'confidence': 0.8
                    })
        
        # Use spaCy for additional entity extraction if available
        if self.nlp:
            doc = self.nlp(user_input)
            for ent in doc.ents:
                spacy_type = self._map_spacy_entity_type(ent.label_)
                if spacy_type:
                    entities[spacy_type].append({
                        'value': ent.text,
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'confidence': 0.9,
                        'spacy_label': ent.label_
                    })
        
        return dict(entities)
    
    def _map_spacy_entity_type(self, spacy_label: str) -> Optional[str]:
        """Map spaCy entity labels to our entity types"""
        mapping = {
            'PERSON': 'person',
            'GPE': 'location',  # Geopolitical entity
            'LOC': 'location',
            'TIME': 'time',
            'DATE': 'time',
            'CARDINAL': 'number',
            'ORDINAL': 'number',
            'QUANTITY': 'number'
        }
        return mapping.get(spacy_label)
    
    def _parse_command_structure(self, user_input: str) -> Dict[str, Any]:
        """Parse the grammatical structure of the command"""
        structure = {
            'subject': None,
            'verb': None,
            'object': None,
            'modifiers': [],
            'question_type': self._identify_question_type(user_input)
        }
        
        if self.nlp:
            doc = self.nlp(user_input)
            
            # Extract grammatical components
            for token in doc:
                if token.dep_ == 'nsubj':  # Nominal subject
                    structure['subject'] = token.text
                elif token.pos_ == 'VERB' and not structure['verb']:
                    structure['verb'] = token.text
                elif token.dep_ == 'dobj':  # Direct object
                    structure['object'] = token.text
                elif token.dep_ in ['amod', 'advmod']:  # Modifiers
                    structure['modifiers'].append(token.text)
        
        return structure
    
    def _identify_question_type(self, user_input: str) -> Optional[str]:
        """Identify the type of question being asked"""
        question_patterns = {
            'what': r'\bwhat\b',
            'how': r'\bhow\b',
            'when': r'\bwhen\b',
            'where': r'\bwhere\b',
            'who': r'\bwho\b',
            'why': r'\bwhy\b',
            'which': r'\bwhich\b',
            'yes_no': r'\b(is|are|can|could|will|would|do|does|did)\b'
        }
        
        for q_type, pattern in question_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return q_type
        
        return None
    
    def _detect_ambiguity(self, user_input: str) -> Dict[str, Any]:
        """Detect potential ambiguities in the input"""
        ambiguity = {
            'has_ambiguity': False,
            'ambiguous_terms': [],
            'multiple_intents': False,
            'unclear_entities': []
        }
        
        # Check for ambiguous pronouns
        ambiguous_pronouns = ['it', 'that', 'this', 'there', 'here']
        for pronoun in ambiguous_pronouns:
            if re.search(rf'\b{pronoun}\b', user_input, re.IGNORECASE):
                ambiguity['ambiguous_terms'].append(pronoun)
                ambiguity['has_ambiguity'] = True
        
        # Check for multiple possible intents
        intents = self._classify_intents(user_input)
        if len(intents) > 1 and intents[0]['confidence'] - intents[1]['confidence'] < 0.3:
            ambiguity['multiple_intents'] = True
            ambiguity['has_ambiguity'] = True
        
        return ambiguity
    
    def _is_context_dependent(self, user_input: str, context: Dict[str, Any] = None) -> bool:
        """Check if the input depends on conversation context"""
        context_indicators = [
            r'\b(it|that|this|there|here)\b',
            r'\b(also|too|as well)\b',
            r'\b(more|another|different)\b',
            r'\b(tomorrow|yesterday|next|last)\b'
        ]
        
        for pattern in context_indicators:
            if re.search(pattern, user_input, re.IGNORECASE):
                return True
        
        return False
    
    def _calculate_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall confidence in the analysis"""
        confidence = 0.0
        
        # Intent confidence
        if analysis['intents']:
            confidence += analysis['intents'][0]['confidence'] * 0.4
        
        # Entity confidence
        entity_confidence = 0.0
        entity_count = 0
        for entity_type, entities in analysis['entities'].items():
            for entity in entities:
                entity_confidence += entity['confidence']
                entity_count += 1
        
        if entity_count > 0:
            confidence += (entity_confidence / entity_count) * 0.3
        
        # Structure confidence
        structure = analysis['command_structure']
        if structure['verb']:
            confidence += 0.2
        if structure['object']:
            confidence += 0.1
        
        # Penalize for ambiguity
        if analysis['ambiguity']['has_ambiguity']:
            confidence *= 0.8
        
        return min(confidence, 1.0)
    
    def _resolve_with_context(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve ambiguities using conversation context"""
        if not context:
            return analysis
        
        # Resolve pronoun references
        if analysis['ambiguity']['ambiguous_terms']:
            if context.get('referenced_topic'):
                analysis['resolved_intent'] = context['referenced_topic']
                analysis['confidence'] += 0.2
        
        # Add context variables to entities
        if context.get('context_vars'):
            for var_name, var_value in context['context_vars'].items():
                if var_name.startswith('last_'):
                    entity_type = var_name.replace('last_', '')
                    if entity_type not in analysis['entities']:
                        analysis['entities'][entity_type] = []
                    analysis['entities'][entity_type].append({
                        'value': var_value,
                        'confidence': 0.7,
                        'source': 'context'
                    })
        
        return analysis
    
    def generate_command(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured command from the analysis"""
        if not analysis['intents']:
            return {'command': None, 'error': 'No intent detected'}
        
        primary_intent = analysis['intents'][0]
        intent_name = primary_intent['intent']
        
        # Get command template
        template = self.command_templates.get(intent_name, {})
        
        command = {
            'intent': intent_name,
            'confidence': analysis['confidence'],
            'parameters': {},
            'raw_analysis': analysis
        }
        
        # Extract parameters based on template
        if template:
            for param in template.get('parameters', []):
                if param in analysis['entities']:
                    command['parameters'][param] = analysis['entities'][param][0]['value']
        
        # Handle specific intent logic
        if intent_name == 'music':
            command = self._generate_music_command(command, analysis)
        elif intent_name == 'weather':
            command = self._generate_weather_command(command, analysis)
        elif intent_name == 'timer':
            command = self._generate_timer_command(command, analysis)
        
        return command
    
    def _generate_music_command(self, command: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate music-specific command"""
        # Determine action
        user_input = analysis['original_input'].lower()
        
        if any(word in user_input for word in ['play', 'start']):
            command['action'] = 'play'
            # Extract music query
            if 'music_query' in analysis['entities']:
                command['parameters']['query'] = analysis['entities']['music_query'][0]['value']
        elif any(word in user_input for word in ['pause', 'stop']):
            command['action'] = 'pause'
        elif any(word in user_input for word in ['resume', 'continue']):
            command['action'] = 'resume'
        elif any(word in user_input for word in ['next', 'skip']):
            command['action'] = 'next'
        elif any(word in user_input for word in ['previous', 'back']):
            command['action'] = 'previous'
        
        return command
    
    def _generate_weather_command(self, command: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weather-specific command"""
        user_input = analysis['original_input'].lower()
        
        # Determine if it's current weather or forecast
        if any(word in user_input for word in ['tomorrow', 'forecast', 'next']):
            command['type'] = 'forecast'
        else:
            command['type'] = 'current'
        
        # Extract location
        if 'location' in analysis['entities']:
            command['parameters']['location'] = analysis['entities']['location'][0]['value']
        
        return command
    
    def _generate_timer_command(self, command: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate timer-specific command"""
        user_input = analysis['original_input'].lower()
        
        if any(word in user_input for word in ['set', 'start', 'create']):
            command['action'] = 'set'
            # Extract duration
            if 'duration' in analysis['entities']:
                command['parameters']['duration'] = analysis['entities']['duration'][0]['value']
        elif any(word in user_input for word in ['cancel', 'stop', 'delete']):
            command['action'] = 'cancel'
        elif any(word in user_input for word in ['check', 'status']):
            command['action'] = 'check'
        
        return command

# Test function
def test_nlu_engine():
    """Test the NLU Engine"""
    print("Testing NLU Engine")
    print("=" * 30)
    
    nlu = NLUEngine()
    
    test_inputs = [
        "What's the weather like in New York?",
        "Play some jazz music",
        "Set a timer for 5 minutes",
        "What about tomorrow?",  # Context-dependent
        "Play something different",  # Context-dependent
        "Calculate 15 plus 27"
    ]
    
    for i, test_input in enumerate(test_inputs, 1):
        print(f"\n{i}. Testing: '{test_input}'")
        analysis = nlu.analyze_input(test_input)
        
        print(f"   Primary intent: {analysis['intents'][0]['intent'] if analysis['intents'] else 'None'}")
        print(f"   Confidence: {analysis['confidence']:.2f}")
        print(f"   Entities: {list(analysis['entities'].keys())}")
        print(f"   Context dependent: {analysis['context_dependent']}")
        
        # Generate command
        command = nlu.generate_command(analysis)
        print(f"   Generated command: {command['intent']} - {command.get('action', 'N/A')}")
    
    print("\n✓ NLU Engine test completed!")

if __name__ == "__main__":
    test_nlu_engine()