# JARVIS Tests

This directory contains all test files for the JARVIS voice assistant.

## Test Files

### `test_all_tts.py`
Tests all available TTS (Text-to-Speech) engines to find the best one for your system.

**Usage:**
```bash
python tests/test_all_tts.py
```

**Tests:**
- Windows SAPI TTS
- Edge TTS (Neural)
- Simple TTS (pyttsx3)
- Smart TTS Manager

### `test_tts_simple.py`
Simple diagnostic test for TTS issues. Useful for troubleshooting basic TTS problems.

**Usage:**
```bash
python tests/test_tts_simple.py
```

### `test_continuous_listening.py`
Tests the continuous listening functionality and NLP command extraction.

**Usage:**
```bash
python tests/test_continuous_listening.py
```

**Features:**
- Tests NLP command extraction without audio
- Tests actual audio listening (requires microphone)
- Validates wake word detection and command parsing

### `test_joke_commands.py`
Tests the joke functionality and online API integration.

**Usage:**
```bash
python tests/test_joke_commands.py
```

**Features:**
- Tests joke service with multiple APIs
- Tests different joke types (regular, programming, dad jokes)
- Tests command processing with mock and real TTS

### `run_tests.py`
Test runner that executes all available tests.

**Usage:**
```bash
python tests/run_tests.py
```

## Running Tests

### Run All Tests
```bash
python tests/run_tests.py
```

### Run Individual Tests
```bash
# Test TTS engines
python tests/test_all_tts.py

# Test continuous listening
python tests/test_continuous_listening.py

# Test joke commands
python tests/test_joke_commands.py

# Test simple TTS
python tests/test_tts_simple.py
```

## Test Requirements

All tests use the same dependencies as the main JARVIS application. Make sure you have:

- Python 3.8+
- All requirements from `requirements.txt` installed
- Microphone access (for audio tests)
- Audio output (for TTS tests)

## Troubleshooting

If tests fail:

1. **TTS Tests Failing**: Check audio drivers and Windows audio service
2. **Audio Tests Failing**: Check microphone permissions and PyAudio installation
3. **Import Errors**: Make sure you're running from the project root directory

## Adding New Tests

When adding new test files:

1. Place them in the `tests/` directory
2. Add the path setup at the top:
   ```python
   import sys
   import os
   sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```
3. Update `run_tests.py` to include the new test
4. Update this README with test documentation