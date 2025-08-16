# JARVIS Project Structure

## 📁 **Directory Organization**

```
JARVIS/
├── 📁 docs/                    # Documentation
│   ├── ADVANCED_NLU_SYSTEM.md
│   ├── EMAIL_SYSTEM_SETUP.md
│   ├── MUSIC_IMPROVEMENTS.md
│   ├── CLEANUP_SUMMARY.md
│   └── outlook_setup_guide.md
│
├── 📁 modules/                 # Core JARVIS modules
│   ├── conversation_context.py
│   ├── nlu_engine.py
│   ├── intent_resolver.py
│   ├── enhanced_commands.py
│   ├── email_service.py
│   ├── music_service.py
│   ├── weather_service.py
│   └── ... (other services)
│
├── 📁 scripts/                 # Setup and utility scripts
│   ├── setup_email.py
│   ├── calibrate_microphone.py
│   ├── fix_distutils.py
│   └── setup_demo_email.py
│
├── 📁 tools/                   # Diagnostic and testing tools
│   ├── diagnose_email.py
│   ├── fix_outlook_setup.py
│   ├── manual_email_setup.py
│   └── test_outlook_connection.py
│
├── 📁 tests/                   # Test suites
│   ├── test_improved_music.py
│   ├── test_medium_priority_commands.py
│   └── test_music_autoplay.py
│
├── 📁 resources/               # Voice models and assets
│   ├── Jarvis_en_windows_v3_0_0.ppn
│   └── LICENSE.txt
│
├── 📁 examples/                # Example configurations
│
├── 📁 .kiro/                   # Kiro IDE configuration
│   └── email/                  # Email credentials (encrypted)
│
├── 🤖 jarvis.py               # Main JARVIS application
├── 📋 requirements.txt        # Python dependencies
├── 📄 README.md              # Project overview
├── 📄 CONTRIBUTING.md        # Contribution guidelines
├── 📄 LICENSE                # License information
├── 🚀 run_jarvis.bat         # Windows launcher
├── 🚀 run_jarvis.sh          # Linux/Mac launcher
└── ⚙️ setup.py               # Package setup
```

## 🎯 **Key Files**

### **Core Application:**
- `jarvis.py` - Main JARVIS voice assistant
- `modules/` - All core functionality modules
- `requirements.txt` - Python dependencies

### **Setup & Configuration:**
- `scripts/setup_email.py` - Email configuration wizard
- `scripts/calibrate_microphone.py` - Microphone setup
- `run_jarvis.bat/sh` - Quick launch scripts

### **Documentation:**
- `docs/ADVANCED_NLU_SYSTEM.md` - NLU capabilities overview
- `docs/EMAIL_SYSTEM_SETUP.md` - Email setup guide
- `docs/MUSIC_IMPROVEMENTS.md` - Music system details

### **Development Tools:**
- `tools/` - Diagnostic and troubleshooting utilities
- `tests/` - Automated test suites
- `examples/` - Configuration examples

## 🚀 **Quick Start**

1. **Install Dependencies:** `pip install -r requirements.txt`
2. **Setup Email:** `python scripts/setup_email.py`
3. **Run JARVIS:** `python jarvis.py` or `./run_jarvis.bat`

## 🔧 **Development**

- **Add New Features:** Create modules in `modules/`
- **Add Tests:** Create test files in `tests/`
- **Add Documentation:** Create docs in `docs/`
- **Add Tools:** Create utilities in `tools/`

This structure keeps the project organized, maintainable, and easy to navigate!