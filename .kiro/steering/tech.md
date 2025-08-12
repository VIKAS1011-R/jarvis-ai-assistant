# Technology Stack

## Core Technologies
- **Picovoice Platform**: Voice AI technology stack
- **Porcupine**: Wake word detection engine
- **Platform**: Windows (win32)

## Dependencies
- Picovoice SDK (access key required)
- Porcupine wake word detection model

## Configuration
- Environment variables stored in `.env` file
- Picovoice access key: `pico_access_key`
- Wake word model: `Jarvis_en_windows_v3_0_0.ppn`

## Security Notes
- Access keys should be kept secure and not committed to version control
- The `.env` file contains sensitive API credentials

## Common Commands
Since this appears to be an early-stage project, specific build/test commands are not yet established. When implementing:
- Ensure proper environment variable loading
- Test wake word detection functionality
- Validate Picovoice API connectivity