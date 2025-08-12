# Contributing to J.A.R.V.I.S AI Assistant

Thank you for your interest in contributing to J.A.R.V.I.S! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```
3. **Set up the development environment**:
   ```bash
   python fix_distutils.py
   pip install -r requirements.txt
   ```

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- Working microphone (for testing)
- Windows OS (primary target platform)

### Testing Your Changes
Before submitting changes, make sure to test:

```bash
# Test TTS engines
python test_all_tts.py

# Test the main application
python jarvis.py

# Test specific modules
python -m modules.smart_tts
```

## 📝 How to Contribute

### Reporting Bugs
1. **Check existing issues** first
2. **Create a new issue** with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (Python version, OS, etc.)
   - Error messages/logs

### Suggesting Features
1. **Open an issue** with the "enhancement" label
2. **Describe the feature** clearly:
   - What problem does it solve?
   - How should it work?
   - Any implementation ideas?

### Code Contributions

#### 1. Choose an Issue
- Look for issues labeled `good first issue` for beginners
- Comment on the issue to let others know you're working on it

#### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

#### 3. Make Your Changes
- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed

#### 4. Test Your Changes
- Ensure all existing functionality still works
- Test your new feature thoroughly
- Add tests if applicable

#### 5. Commit Your Changes
```bash
git add .
git commit -m "Add: brief description of changes"
```

Use conventional commit messages:
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for improvements
- `Remove:` for deletions

#### 6. Push and Create Pull Request
```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- Screenshots/demos if applicable

## 📋 Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Example:
```python
def process_voice_command(command: str) -> Optional[str]:
    """
    Process a voice command and execute the appropriate action.
    
    Args:
        command: The recognized voice command text
        
    Returns:
        str: Special command result, or None for normal commands
    """
    if not command:
        return None
    
    command = command.lower().strip()
    # Implementation here...
```

### Module Structure
- Keep modules focused on single responsibilities
- Use clear imports
- Add module-level docstrings

## 🎯 Areas for Contribution

### High Priority
- **Cross-platform support** (Linux, macOS)
- **Additional voice commands** (weather, news, etc.)
- **Improved error handling**
- **Performance optimizations**

### Medium Priority
- **GUI interface**
- **Configuration management**
- **Plugin system**
- **Voice training/customization**

### Documentation
- **Code documentation**
- **User guides**
- **Video tutorials**
- **API documentation**

## 🧪 Testing Guidelines

### Manual Testing
1. Test wake word detection
2. Test all voice commands
3. Test TTS engines
4. Test error scenarios

### Automated Testing
- Add unit tests for new functions
- Test edge cases
- Ensure backward compatibility

## 📚 Resources

### Useful Links
- [Picovoice Documentation](https://picovoice.ai/docs/)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
- [Edge TTS Documentation](https://pypi.org/project/edge-tts/)

### Project Structure
```
modules/
├── config.py              # Configuration management
├── hotword_detection.py   # Wake word detection
├── smart_tts.py          # TTS engine manager
├── simple_speech.py      # Speech recognition
├── simple_commands.py    # Command processing
└── jarvis_responses.py   # Response templates
```

## ❓ Questions?

- **Open an issue** for questions about the codebase
- **Check existing issues** for similar questions
- **Read the documentation** in `available_commands.txt`

## 🙏 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Contributors list

Thank you for helping make J.A.R.V.I.S better! 🚀