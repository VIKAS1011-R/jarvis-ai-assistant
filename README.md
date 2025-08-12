# J.A.R.V.I.S - Just A Rather Very Intelligent System

A voice-activated AI assistant built with Python, featuring wake word detection and natural speech responses. Inspired by Tony Stark's AI assistant from the Marvel universe.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Features

- **🎤 Wake Word Detection**: Responds to "Jarvis" using Picovoice Porcupine
- **🗣️ Natural Speech**: High-quality text-to-speech with multiple engine support
- **🌐 Web Control**: Open websites with voice commands
- **💻 System Control**: Launch applications and control system functions
- **⏰ Time & Date**: Get current time and date information
- **🔧 Smart Fallbacks**: Multiple TTS engines for maximum reliability

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows operating system
- Working microphone
- Internet connection (for speech recognition)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jarvis-ai-assistant.git
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

4. **Test TTS engines**
   ```bash
   python test_all_tts.py
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
├── test_all_tts.py            # TTS engine tester
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

**TTS not working**
```bash
python test_all_tts.py
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
2. Run `python test_all_tts.py` to diagnose TTS issues
3. Run `python fix_distutils.py` for dependency issues
4. Open an issue on GitHub with error details

---

**"Sometimes you gotta run before you can walk."** - Tony Stark

Made with ❤️ for AI enthusiasts and Marvel fans!