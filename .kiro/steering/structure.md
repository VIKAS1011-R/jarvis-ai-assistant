# Project Structure

## Root Directory
```
├── .env                    # Environment configuration (API keys)
├── resources/              # Voice models and licensing
│   ├── Jarvis_en_windows_v3_0_0.ppn  # Porcupine wake word model
│   └── LICENSE.txt         # Picovoice license terms
└── .kiro/                  # Kiro IDE configuration
    └── steering/           # AI assistant guidance documents
```

## Directory Conventions

### `/resources/`
- Contains voice recognition models and assets
- Stores licensing information
- Wake word models follow naming pattern: `{keyword}_{language}_{platform}_v{version}.ppn`

### Root Level
- `.env`: Environment variables and API configuration
- Keep sensitive credentials in environment files, not in source code

## File Naming Conventions
- Wake word models: Use descriptive names with language and platform identifiers
- Environment files: Standard `.env` format
- Follow Picovoice naming conventions for model files

## Security Considerations
- Never commit `.env` files with real API keys
- Use placeholder values in example configurations
- Reference Picovoice terms of use for licensing compliance