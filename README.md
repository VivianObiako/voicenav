# VoiceNav MVP - MacBook M3 Pro Edition

🎙️ **Voice-controlled browser automation for macOS**

A desktop Python application that runs in the background on your MacBook and controls your web browser using voice commands.

## 🎯 What is VoiceNav?

VoiceNav is a powerful productivity tool that lets you control your browser hands-free using natural voice commands. Perfect for accessibility, multitasking, or hands-free web navigation.

### Architecture

```
┌─────────────────────────────────────┐
│  VoiceNav Desktop App (Python)      │
│  - Listens to microphone            │
│  - Processes voice commands         │
│  - Controls browser via Playwright  │
└─────────────────────────────────────┘
           ↓ (controls)
┌─────────────────────────────────────┐
│  Chrome/Safari Browser              │
│  - Opens and navigates pages        │
│  - Clicks elements                  │
│  - Reads content aloud              │
└─────────────────────────────────────┘
```

### NOT...

❌ A browser extension (too limited)  
❌ A web app (needs system access)  
❌ A mobile app (different challenge)

### BUT...

✅ A macOS desktop application (Python-based)  
✅ Runs as a background service  
✅ Has a menu bar icon for status/controls  
✅ Controls your default browser programmatically

---

## 📋 MVP Features

### Core Features

- **Voice Command System**
  - Wake word: "Hey VoiceNav"
  - 8 essential commands
  - Voice confirmation feedback

- **Browser Control**
  - Open URLs
  - Click elements by description
  - Scroll navigation
  - Read page content aloud

- **Accessibility Features**
  - Text-to-speech feedback
  - Visual overlay showing active state
  - Clear error messages

- **User Interface**
  - Menu bar app (macOS status bar)
  - Simple settings window
  - Landing page (promotional website)

---

## 🚀 Quick Start

### Prerequisites

- **macOS** (Optimized for M3 Pro chip)
- **Python 3.11+**
- **Homebrew** (for installing portaudio)
- **Microphone** (built-in or external)

### Installation

#### 1. Install Homebrew Dependencies

For PyAudio to work on M3 Mac, you need portaudio:

```bash
brew install portaudio
```

#### 2. Clone or Download VoiceNav

```bash
# Navigate to your desired directory
cd ~/Projects
```

#### 3. Create Virtual Environment

```bash
cd voicenav
python3.11 -m venv venv
source venv/bin/activate
```

#### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If you encounter PyAudio issues:**

```bash
LDFLAGS="-L/opt/homebrew/lib" CFLAGS="-I/opt/homebrew/include" pip install pyaudio
```

#### 5. Test Your Environment

```bash
python3 tests/test_environment.py
```

You should see:
```
✓ Python Version Check: PASS
✓ System Info: PASS
✓ Project Structure: PASS
✓ Dependencies: PASS
✓ Microphone Access: PASS

Total: 5/5 checks passed
✓ All checks passed! VoiceNav environment is ready.
```

---

## 🔧 Configuration

### Grant Microphone Permissions

On macOS, you'll need to grant microphone access:

1. **System Preferences → Security & Privacy → Microphone**
2. Add Terminal (or your IDE) to the allowed apps
3. You may need to restart your application after granting permissions

### Environment Variables

Create a `.env` file in the project root (template provided in `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your preferences:

```env
LOG_LEVEL=INFO
WAKE_WORD=Hey VoiceNav
DEFAULT_BROWSER=chrome
DEBUG=false
```

### Configuration File

Edit `config.yaml` to customize:
- Wake word
- Voice settings
- Browser preferences
- Command definitions
- Logging level

---

## 📁 Project Structure

```
voicenav/
├── README.md                 # This file
├── requirements.txt         # Python dependencies
├── config.yaml             # Application configuration
├── .gitignore              # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── main.py             # Main application entry point
│   └── utils/
│       ├── __init__.py
│       └── logger.py       # Logging utility
└── tests/
    ├── __init__.py
    └── test_environment.py  # Environment validation tests
```

---

## 🧪 Testing

### Environment Test

Run the environment test to verify everything is set up correctly:

```bash
source venv/bin/activate
python3 tests/test_environment.py
```

### Run Main Application

Once tests pass:

```bash
cd src
python3 main.py
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| SpeechRecognition | 3.10.0 | Voice input processing |
| PyAudio | 0.2.14 | Microphone access |
| pyttsx3 | 2.90 | Text-to-speech output |
| Playwright | 1.40.0 | Browser control automation |
| rumps | 0.4.0 | macOS menu bar app |
| python-dotenv | 1.0.0 | Environment configuration |

---

## 🐛 Troubleshooting

### PyAudio Installation Issues

**Error: `error: command 'clang' failed with exit status 1`**

Solution:
```bash
LDFLAGS="-L/opt/homebrew/lib" CFLAGS="-I/opt/homebrew/include" pip install pyaudio
```

### Microphone Not Detected

1. Check System Preferences → Security & Privacy → Microphone
2. Ensure your application has microphone access
3. Test microphone with: `python3 -c "import pyaudio; p = pyaudio.PyAudio(); print(p.get_device_count())"`

### Import Errors

Make sure you're using the virtual environment:
```bash
source venv/bin/activate
which python3  # Should show path in venv/bin/
```

### macOS Permissions

Some features may require additional permissions:
- **Microphone**: System Preferences → Security & Privacy → Microphone
- **Accessibility**: System Preferences → Security & Privacy → Accessibility
- **Screen Recording** (future): System Preferences → Security & Privacy → Screen Recording

---

## 📚 Development Stages

### ✅ Stage 0: Project Setup & Environment (CURRENT)
- Project structure created
- All dependencies configured
- Environment tests implemented

### 📋 Stage 1: Voice Input System
- Microphone listening loop
- Wake word detection ("Hey VoiceNav")
- Command speech-to-text conversion
- Error handling and feedback

### 📋 Stage 2: Browser Control
- Playwright integration
- URL navigation
- Element clicking
- Scroll functionality
- Page content reading

### 📋 Stage 3: Menu Bar UI
- rumps-based status bar app
- Settings window
- Visual feedback

### 📋 Stage 4: Polish & Testing
- Comprehensive testing
- Performance optimization
- User experience refinement

---

## 📝 Next Steps

1. ✅ Verify environment: `python3 tests/test_environment.py`
2. ⏭️ Move to Stage 1: Voice Input System
3. 📖 See `DEVELOPMENT_STAGES.md` for detailed roadmap

---

## 📄 License

VoiceNav MVP - 2024

---

## 🤝 Contributing

This is an MVP project. Feedback and suggestions are welcome!

---

## ⚠️ Important Notes

- **M3 Compatibility**: This project is optimized for Apple Silicon (M3 Pro). Some dependencies may need compilation for ARM64.
- **Microphone Required**: A functioning microphone is essential for the application.
- **System Permissions**: Grant necessary permissions in macOS Security & Privacy settings.
- **Background Service**: When fully developed, this will run as a background service.

---

## 🆘 Support

For issues with installation:

1. Check the **Troubleshooting** section above
2. Run `python3 tests/test_environment.py` for detailed diagnostics
3. Verify all Homebrew dependencies: `brew list | grep portaudio`

---

**Happy Voice Navigation! 🎙️**
