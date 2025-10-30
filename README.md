# VoiceNav

Voice-controlled browser automation for macOS using Maya AI assistant.

## 🎤 What is VoiceNav?

VoiceNav is a voice-controlled browser automation system that lets you navigate the web using natural language commands. Powered by Maya, your AI assistant, VoiceNav uses offline speech recognition and native macOS browser control for a seamless, privacy-focused experience.

## ✨ Features

### 🗣️ Natural Voice Control
- **Wake Word Activation**: "Hey Maya" to start commands
- **Offline Recognition**: OpenAI Whisper for high-accuracy speech processing
- **Natural Language**: "open google", "scroll down", "go back"
- **Maya Voice Feedback**: Samantha voice confirms all actions

### 🌐 Universal Browser Support
- **Auto-Detection**: Automatically uses your default browser
- **Multi-Browser**: Safari, Chrome, Arc, Edge supported
- **Native Control**: AppleScript integration for reliable automation
- **No Extensions**: Works with your existing browser setup

### 🎯 Core Commands
- **Website Navigation**: "open [website]" with 40+ shortcuts
- **Page Control**: scroll up/down, go back/forward, refresh
- **Content Reading**: "read page title", "read content"
- **System Help**: "help" for available commands

## 🚀 Quick Start

### Prerequisites
- macOS (for AppleScript browser control)
- Python 3.8+ 
- Microphone access permissions

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/VivianObiako/voicenav.git
   cd voicenav
   ```

2. **Setup Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Grant Permissions**
   - Microphone access (System Preferences → Privacy → Microphone)
   - For Safari scrolling: Enable "Allow JavaScript from Apple Events" in Safari → Develop menu

4. **Run VoiceNav**
   ```bash
   python3 src/main.py
   ```

5. **Start Voice Control**
   - Say: "Hey Maya, open google"
   - Maya responds: "Opened google" and opens Google in your browser

## 🎯 Example Commands

```
"Hey Maya, open youtube"     → Opens YouTube
"Hey Maya, scroll down"      → Scrolls page down  
"Hey Maya, go back"          → Goes back in browser history
"Hey Maya, refresh"          → Refreshes current page
"Hey Maya, read title"       → Reads page title aloud
"Hey Maya, help"             → Lists available commands
```

## 🏗️ Development Status

- ✅ **Stage 0**: Environment Setup (Complete)
- ✅ **Stage 1**: Maya Voice Assistant (Complete)  
- ✅ **Stage 2**: Command Parser + Browser Control (Complete)
- 🚧 **Stage 3**: Menu Bar UI (In Progress)
- 📋 **Stage 4**: Enhanced Browser Control (Planned)

See [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for detailed roadmap.

## 🔧 Troubleshooting

### Microphone Issues
```bash
# Test microphone access
python3 -c "from src.input.voice_listener import create_voice_listener; maya = create_voice_listener(); maya.test_microphone()"
```

### Safari Scrolling Issues
1. Safari → Preferences → Advanced → Show Develop menu
2. Develop → Allow JavaScript from Apple Events

### Browser Detection Issues
```bash
# Test browser detection
python3 test_default_browser.py
```

## 🏛️ Architecture

- **Voice Input**: Whisper offline speech recognition
- **Command Processing**: Natural language parser with intent classification
- **Browser Control**: Native AppleScript automation
- **Voice Output**: macOS Samantha voice synthesis
- **Multi-Threading**: Responsive voice processing with async browser control

## 🤝 Contributing

VoiceNav is in active development. See [DEVLOG.md](DEVLOG.md) for recent changes and [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for upcoming features.

## 📄 License

MIT License - See LICENSE file for details.
