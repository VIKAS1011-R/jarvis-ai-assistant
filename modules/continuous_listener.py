#!/usr/bin/env python3
"""
Continuous Listening Module
Handles continuous speech recognition with wake word detection and NLP command extraction
"""

import speech_recognition as sr
import threading
import time
import re
from typing import Optional, Callable, Tuple
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from modules.mic_config import MicConfig

class ContinuousListener:
    def __init__(self, wake_words=None, timeout=10, phrase_timeout=2):
        """
        Initialize continuous listener with NLP processing
        
        Args:
            wake_words: List of wake words (default: ["jarvis"])
            timeout: Maximum time to wait for speech
            phrase_timeout: Time to wait after speech ends
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.timeout = timeout
        self.phrase_timeout = phrase_timeout
        self.is_listening = False
        self.callback = None
        
        # Wake words
        self.wake_words = wake_words or ["jarvis", "hey jarvis", "ok jarvis"]
        
        # Microphone configuration
        self.mic_config = MicConfig()
        self.mic_settings = self.mic_config.load_settings()
        
        # NLP setup
        self.setup_nlp()
        
        # Common articles and prepositions to filter out
        self.filter_words = {
            'articles': ['a', 'an', 'the'],
            'prepositions': ['in', 'on', 'at', 'by', 'for', 'with', 'to', 'from', 'of', 'about'],
            'conjunctions': ['and', 'or', 'but', 'so', 'yet'],
            'pronouns': ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'],
            'common_words': ['please', 'can', 'could', 'would', 'will', 'should', 'may', 'might']
        }
        
    def setup_nlp(self):
        """Setup NLTK components"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('punkt_tab', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            # Get English stopwords
            self.stop_words = set(stopwords.words('english'))
            print("✓ NLP components initialized")
            
        except Exception as e:
            print(f"✗ NLP setup failed: {e}")
            # Fallback stopwords
            self.stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 
                              'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 
                              'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 
                              'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
                              'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 
                              'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                              'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after', 
                              'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                              'further', 'then', 'once'}
    
    def initialize(self):
        """Initialize and calibrate microphone with saved settings"""
        try:
            print("Initializing microphone with optimized settings...")
            
            # Check if we have calibrated settings
            if self.mic_settings.get('calibrated', False):
                print(f"Using calibrated settings (Environment: {self.mic_settings.get('environment_noise_level', 'UNKNOWN')})")
                self._apply_saved_settings()
            else:
                print("No calibration found. Performing quick calibration...")
                print("Tip: Run 'python calibrate_microphone.py' for optimal settings")
                self._perform_quick_calibration()
            
            print("✓ Continuous listener ready with noise filtering")
            return True
        except Exception as e:
            print(f"✗ Continuous listener failed: {e}")
            return False
    
    def _apply_saved_settings(self):
        """Apply saved calibration settings"""
        with self.microphone as source:
            # Brief ambient check
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            current_ambient = self.recognizer.energy_threshold
            
            # Apply saved settings
            self.recognizer.energy_threshold = self.mic_settings['energy_threshold']
            self.recognizer.dynamic_energy_threshold = self.mic_settings['dynamic_energy_threshold']
            self.recognizer.dynamic_energy_adjustment_damping = self.mic_settings['dynamic_energy_adjustment_damping']
            self.recognizer.dynamic_energy_ratio = self.mic_settings['dynamic_energy_ratio']
            self.recognizer.pause_threshold = self.mic_settings['pause_threshold']
            self.recognizer.phrase_threshold = self.mic_settings['phrase_threshold']
            self.recognizer.non_speaking_duration = self.mic_settings['non_speaking_duration']
            
            # Adjust if current ambient is much higher than saved setting
            if current_ambient > self.recognizer.energy_threshold * 1.5:
                print(f"Current ambient noise ({current_ambient:.0f}) higher than saved setting")
                print(f"Adjusting threshold from {self.recognizer.energy_threshold} to {current_ambient * 1.2:.0f}")
                self.recognizer.energy_threshold = current_ambient * 1.2
            
            print(f"Applied settings - Threshold: {self.recognizer.energy_threshold:.0f}, Damping: {self.recognizer.dynamic_energy_adjustment_damping}")
    
    def _perform_quick_calibration(self):
        """Perform quick calibration if no saved settings exist"""
        with self.microphone as source:
            print("Please remain quiet for 2 seconds...")
            
            # Extended ambient noise calibration
            self.recognizer.adjust_for_ambient_noise(source, duration=2.0)
            
            # Get the ambient noise level
            ambient_level = self.recognizer.energy_threshold
            print(f"Ambient noise level: {ambient_level:.0f}")
            
            # Apply default optimized settings
            self.recognizer.energy_threshold = max(ambient_level * 1.5, 400)
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.dynamic_energy_adjustment_damping = 0.15
            self.recognizer.dynamic_energy_ratio = 1.5
            self.recognizer.pause_threshold = 0.8
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
            
            print(f"Quick calibration complete - Threshold: {self.recognizer.energy_threshold:.0f}")
    
    def extract_wake_word_and_command(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract wake word and command from text using NLP
        
        Args:
            text: Full recognized text
            
        Returns:
            Tuple of (wake_word_found, extracted_command)
        """
        text_lower = text.lower().strip()
        
        # Check for wake words
        wake_word_found = None
        wake_word_position = -1
        
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                wake_word_found = wake_word
                wake_word_position = text_lower.find(wake_word)
                break
        
        if not wake_word_found:
            return None, None
        
        # Extract command part (everything after wake word)
        command_start = wake_word_position + len(wake_word_found)
        command_text = text_lower[command_start:].strip()
        
        if not command_text:
            return wake_word_found, None
        
        # Clean and process the command
        cleaned_command = self.clean_command(command_text)
        
        return wake_word_found, cleaned_command
    
    def clean_command(self, command_text: str) -> str:
        """
        Clean command text using simple NLP techniques
        
        Args:
            command_text: Raw command text
            
        Returns:
            Cleaned command text
        """
        try:
            # Try advanced NLP cleaning
            tokens = word_tokenize(command_text)
            
            # Remove punctuation and convert to lowercase
            tokens = [token.lower() for token in tokens if token.isalnum()]
            
            # POS tagging to identify important words
            pos_tags = pos_tag(tokens)
            
            # Keep important words (nouns, verbs, adjectives, numbers)
            important_pos = {'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 
                           'JJ', 'JJR', 'JJS', 'CD', 'RB', 'RBR', 'RBS'}
            
            cleaned_tokens = []
            
            for token, pos in pos_tags:
                # Keep important POS tags
                if pos in important_pos:
                    cleaned_tokens.append(token)
                # Keep specific command words even if they're common
                elif token in ['open', 'close', 'play', 'stop', 'start', 'search', 'find', 'tell', 'show', 'get']:
                    cleaned_tokens.append(token)
                # Skip common filter words unless they're essential
                elif token not in self.stop_words and not self._is_filter_word(token):
                    cleaned_tokens.append(token)
            
            # If we filtered too much, fall back to basic cleaning
            if len(cleaned_tokens) < 1:
                cleaned_tokens = [token for token in tokens 
                                if token not in self.stop_words and not self._is_filter_word(token)]
            
            # Join and return
            cleaned_command = ' '.join(cleaned_tokens)
            
            # Handle special cases
            cleaned_command = self._handle_special_cases(cleaned_command)
            
            return cleaned_command
            
        except Exception as e:
            # Fallback to simple cleaning
            return self._simple_clean(command_text)
    
    def _is_filter_word(self, word: str) -> bool:
        """Check if word should be filtered out"""
        for category, words in self.filter_words.items():
            if word in words:
                return True
        return False
    
    def _handle_special_cases(self, command: str) -> str:
        """Handle special command cases"""
        # Time-related commands
        if 'time' in command:
            return 'time'
        
        # Weather commands
        if any(word in command for word in ['weather', 'temperature', 'forecast']):
            return 'weather'
        
        # Search commands
        if any(word in command for word in ['search', 'google', 'find']):
            # Extract search term
            search_terms = command.replace('search', '').replace('google', '').replace('find', '').strip()
            if search_terms:
                return f'search {search_terms}'
            return 'search'
        
        # Open commands
        if 'open' in command:
            app_name = command.replace('open', '').strip()
            if app_name:
                return f'open {app_name}'
            return 'open'
        
        return command
    
    def _simple_clean(self, text: str) -> str:
        """Simple fallback cleaning"""
        # Remove common articles and prepositions
        words = text.split()
        cleaned = [word for word in words if word not in ['the', 'a', 'an', 'please', 'can', 'you']]
        return ' '.join(cleaned)
    
    def listen_continuously(self):
        """
        Listen continuously for wake word + command combinations with noise filtering
        
        Returns:
            Tuple of (wake_word, command) or (None, None) if failed
        """
        try:
            # Only print listening message occasionally to reduce spam
            if hasattr(self, '_listen_count'):
                self._listen_count += 1
            else:
                self._listen_count = 1
            
            if self._listen_count % 10 == 1:  # Print every 10th attempt
                print("Listening continuously... (say wake word + command)")
            
            with self.microphone as source:
                # Apply additional noise reduction
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                
                # Listen for audio with improved settings
                audio = self.recognizer.listen(
                    source, 
                    timeout=self.timeout,
                    phrase_time_limit=6,  # Slightly shorter to avoid picking up too much noise
                    snowboy_configuration=None
                )
            
            # Check if audio has sufficient energy (not just noise)
            audio_data = audio.get_raw_data()
            if len(audio_data) < 1000:  # Too short, likely noise
                return None, None
            
            print("Processing speech...")
            
            # Use Google's speech recognition
            full_text = self.recognizer.recognize_google(audio)
            
            # Filter out very short or nonsensical results
            if len(full_text.strip()) < 3:
                print(f"Ignored short audio: '{full_text}'")
                return None, None
            
            print(f"Heard: '{full_text}'")
            
            # Extract wake word and command
            wake_word, command = self.extract_wake_word_and_command(full_text)
            
            if wake_word:
                print(f"Wake word detected: '{wake_word}'")
                if command:
                    print(f"Command extracted: '{command}'")
                    return wake_word, command
                else:
                    print("No command found after wake word")
                    return wake_word, None
            else:
                # Only print if the text was substantial
                if len(full_text.strip()) > 5:
                    print("No wake word detected")
                return None, None
                
        except sr.WaitTimeoutError:
            return None, None
        except sr.UnknownValueError:
            # Don't print this every time as it's common with ambient noise
            if hasattr(self, '_error_count'):
                self._error_count += 1
                if self._error_count % 20 == 1:  # Print every 20th error
                    print("Could not understand speech (ambient noise filtered)")
            else:
                self._error_count = 1
            return None, None
        except sr.RequestError as e:
            print(f"Speech service error: {e}")
            return None, None
        except Exception as e:
            print(f"Speech error: {e}")
            return None, None
    
    def set_callback(self, callback: Callable):
        """
        Set callback function for wake word + command detection
        
        Args:
            callback: Function to call with (wake_word, command) parameters
        """
        self.callback = callback
    
    def start_listening(self):
        """Start continuous listening loop"""
        self.is_listening = True
        print("Starting continuous listening...")
        
        try:
            while self.is_listening:
                wake_word, command = self.listen_continuously()
                
                if wake_word and self.callback:
                    self.callback(wake_word, command)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("Stopping continuous listening...")
        except Exception as e:
            print(f"Error in continuous listening: {e}")
        finally:
            self.stop_listening()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        print("Continuous listening stopped")
    
    def cleanup(self):
        """Clean up resources"""
        self.is_listening = False
        print("Continuous listener cleaned up")

# Test function
def test_nlp_extraction():
    """Test the NLP command extraction"""
    listener = ContinuousListener()
    
    test_phrases = [
        "Jarvis what time is it",
        "Hey Jarvis can you tell me the weather",
        "OK Jarvis please search for Python tutorials",
        "Jarvis open Google Chrome",
        "Hey Jarvis play some music",
        "Jarvis what's the current time please"
    ]
    
    print("Testing NLP command extraction:")
    print("=" * 50)
    
    for phrase in test_phrases:
        wake_word, command = listener.extract_wake_word_and_command(phrase)
        print(f"Input: '{phrase}'")
        print(f"Wake word: '{wake_word}'")
        print(f"Command: '{command}'")
        print("-" * 30)

if __name__ == "__main__":
    test_nlp_extraction()