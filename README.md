# J.A.R.V.I.S - Just A Rather Very Intelligent System

An advanced voice-activated AI assistant with natural language understanding, conversation memory, and secure real-world integrations. Built with Python and featuring enterprise-grade security.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![AI](https://img.shields.io/badge/AI-Advanced%20NLU-brightgreen.svg)
![Security](https://img.shields.io/badge/Security-Enterprise%20Grade-red.svg)

## 🧠 Advanced AI Features

- **🎤 Wake Word Detection**: Responds to "Jarvis" using Picovoice Porcupine
- **🧠 Natural Language Understanding**: Advanced NLU with conversation memory and context awareness
- **💬 Conversation Context**: Remembers previous interactions and handles follow-up questions
- **🎯 Intent Classification**: Understands 15+ command types with confidence scoring
- **🔍 Entity Extraction**: Identifies locations, times, numbers, and other entities automatically
- **❓ Smart Clarification**: Handles ambiguous commands intelligently

## 🔐 Secure Integrations

- **📧 Email Management**: Secure email access with encrypted credentials (Gmail, Outlook, Yahoo)
- **🎵 Music Control**: Spotify and YouTube Music integration with voice commands
- **🌤️ Weather Service**: Real-time weather and forecasts with location memory
- **📰 News & Information**: Wikipedia, news feeds, and web search capabilities
- **📅 Calendar & Tasks**: Event management and timer functionality
- **💻 System Monitoring**: CPU, memory, disk usage, and system control

## 📁 Project Structure

```
JARVIS/
├── 📁 docs/          # Documentation and guides
├── 📁 modules/       # Core JARVIS modules
├── 📁 scripts/       # Setup and utility scripts
├── 📁 tools/         # Diagnostic and testing tools
├── 📁 tests/         # Automated test suites
├── 📁 resources/     # Voice models and assets
├── 🤖 jarvis.py     # Main application
└── 📋 requirements.txt # Dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows operating system (Linux/Mac support planned)
- Working microphone and speakers
- Internet connection

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VIKAS1011-R/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   cd jarvis-ai-assistant
   ```

2. **Fix dependencies (if needed)**
   ```bash
   python fix_distutils.py
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Calibrate microphone (recommended)**
   ```bash
   python calibrate_microphone.py
   ```

5. **Test TTS engines**
   ```bash
   python tests/test_all_tts.py
   ```

5. **Run Jarvis**
   ```bash
   python jarvis.py
   ```

## 🎮 Usage

1. **Activate Jarvis**: Say "Jarvis"
2. **Wait for response**: "Good day, sir. How may I assist you?"
3. **Give command**: "What time is it?"
4. **Get response**: "The current time is 3:45 PM"

### Available Commands

See [available_commands.txt](available_commands.txt) for a complete list of voice commands.

**Quick Examples:**
- `"Jarvis"` → `"What time is it?"` → Gets current time
- `"Jarvis"` → `"Open Google"` → Opens Google in browser
- `"Jarvis"` → `"Sleep"` → Puts computer to sleep
- `"Jarvis"` → `"Help"` → Lists all commands

## 🏗️ Architecture

```
jarvis-ai-assistant/
├── jarvis.py                    # Main application
├── available_commands.txt       # Command manual
├── fix_distutils.py            # Dependency fixer
├── tests/                     # Test files
│   ├── test_all_tts.py       # TTS engine tester
│   ├── test_continuous_listening.py  # Continuous listening tests
│   └── run_tests.py          # Test runner
├── modules/
│   ├── config.py              # Configuration management
│   ├── hotword_detection.py   # Wake word detection
│   ├── smart_tts.py          # TTS engine manager
│   ├── windows_tts.py        # Windows SAPI TTS
│   ├── edge_tts.py           # Edge neural TTS
│   ├── simple_speech.py      # Speech recognition
│   ├── simple_commands.py    # Command processing
│   └── jarvis_responses.py   # Response templates
└── resources/
    └── Jarvis_en_windows_v3_0_0.ppn  # Wake word model
```

## 🔧 Configuration

The system uses environment variables stored in `.env`:

```env
pico_access_key="your_picovoice_access_key_here"
```

## 🎵 TTS Engines

Jarvis supports multiple TTS engines with automatic fallback:

1. **Windows SAPI** (Most reliable)
2. **Edge TTS** (Best quality - requires `pip install edge-tts`)
3. **Automatic fallback** if primary engine fails

## 🐛 Troubleshooting

### Common Issues

**"No module named 'distutils'"**
```bash
python fix_distutils.py
```

**Microphone too sensitive / picking up noise**
```bash
python calibrate_microphone.py
```

**TTS not working**
```bash
python tests/test_all_tts.py
```

**Wake word not detected**
- Check microphone permissions
- Ensure `.ppn` file exists in `resources/`
- Verify Picovoice access key in `.env`

**Speech recognition fails**
- Check internet connection
- Verify microphone is working
- Speak clearly and at normal volume

## 📋 Requirements

- `pvporcupine==3.0.2` - Wake word detection
- `python-dotenv>=1.0.0` - Environment configuration
- `edge-tts>=6.1.9` - High-quality TTS
- `SpeechRecognition>=3.10.0` - Voice command recognition
- `pyaudio>=0.2.11` - Audio processing
- `setuptools>=65.0.0` - Python 3.12+ compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Picovoice** for the excellent wake word detection engine
- **Microsoft** for Edge TTS neural voices
- **Marvel Studios** for the inspiration from Tony Stark's J.A.R.V.I.S
- **OpenAI** for development assistance

## 📞 Support

If you encounter any issues:

1. Check the [available_commands.txt](available_commands.txt) manual
2. Run `python tests/test_all_tts.py` to diagnose TTS issues
3. Run `python fix_distutils.py` for dependency issues
4. Open an issue on GitHub with error details

---

**"Sometimes you gotta run before you can walk."** - Tony Stark

Made with ❤️ for AI enthusiasts and Marvel fans!