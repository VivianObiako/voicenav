# Stage 1 Testing Guide - Voice Input System

## 🎯 Overview

This guide walks you through testing the Stage 1 Voice Input System for VoiceNav MVP. You'll verify that wake word detection and command capture work correctly on your M3 MacBook.

---

## 📋 Prerequisites Checklist

Before testing, ensure you have:

- [ ] **Python 3.11+** installed (`python3 --version`)
- [ ] **Virtual environment** activated (`source venv/bin/activate`)
- [ ] **Dependencies** installed (`pip install -r requirements.txt`)
- [ ] **Microphone permissions** granted (System Settings → Privacy & Security → Microphone)
- [ ] **Internet connection** (for Google Speech Recognition)
- [ ] **Quiet environment** (minimal background noise)

---

## 🚀 Quick Start Testing

### Option 1: Guided Testing (Recommended)

```bash
cd ~/Github/Personal/voicenav
source venv/bin/activate
python3 test_stage1.py
```

This script will:
1. Check your Python version
2. Verify virtual environment
3. Test dependencies
4. Guide through microphone setup
5. Run comprehensive voice tests

### Option 2: Direct Voice Testing

```bash
cd ~/Github/Personal/voicenav
source venv/bin/activate
python3 tests/test_voice.py
```

Choose from:
1. **Standard Test** - 3 automatic rounds
2. **Interactive Test** - Continuous listening
3. **Quick Microphone Test** - Basic setup verification

---

## 🧪 Test Scenarios

### Test 1: Standard 3-Round Test

**What it tests**: Wake word detection + command capture

**Process**:
1. Script says: "Say: Hey VoiceNav"
2. You say: "Hey VoiceNav" (clearly)
3. Listen for: System beep + "Listening..."
4. You say: Any command (e.g., "open google")
5. Repeat 3 times

**Expected Results**:
- ✅ Wake word detected: 3/3 times
- ✅ Commands captured correctly
- ✅ Response time: < 3 seconds
- ✅ Confidence score: > 0.9

### Test 2: Interactive Continuous Test

**What it tests**: Sustained listening performance

**Process**:
1. Say "Hey VoiceNav" when ready
2. Give various commands:
   - "open google"
   - "click search button" 
   - "scroll down"
   - "go back"
   - "refresh page"
3. Press Ctrl+C to stop

**Expected Results**:
- ✅ Responds to each wake word
- ✅ Captures commands accurately
- ✅ No crashes or hangs
- ✅ Memory usage stable

### Test 3: Error Handling Test

**What it tests**: Edge cases and error recovery

**Test Cases**:
1. **Silent wake word**: Say "Hey VoiceNav" very quietly
2. **No command**: Say wake word, then stay silent
3. **Background noise**: Test with music/TV on
4. **Wrong wake word**: Say "Hey Siri" or "Hey Google"
5. **Network test**: Disconnect internet briefly

**Expected Results**:
- ✅ Graceful timeout handling
- ✅ Clear error messages
- ✅ Recovery after errors
- ✅ No application crashes

---

## 🔧 Troubleshooting Common Issues

### Issue: "No module named pyaudio"

**Symptoms**: Import error when running tests

**Solution**:
```bash
brew install portaudio
pip install pyaudio

# If that fails on M3:
LDFLAGS="-L/opt/homebrew/lib" CFLAGS="-I/opt/homebrew/include" pip install pyaudio
```

### Issue: "Permission denied" for microphone

**Symptoms**: Microphone test fails, permission errors

**Solution**:
1. Open **System Settings** (or System Preferences)
2. Go to **Privacy & Security** → **Microphone**
3. Add **Terminal** to allowed apps
4. If using an IDE, add it too
5. Restart Terminal/IDE
6. Run test again

### Issue: Wake word not detected

**Symptoms**: Says "Hey VoiceNav" but no response

**Solutions**:
1. **Speak louder and clearer**
2. **Reduce background noise**
3. **Check microphone input level** (System Settings → Sound → Input)
4. **Try different phrasing**: "Hey Voice Nav" or "Hey VoiceNav"
5. **Move closer to microphone**

### Issue: Commands not captured

**Symptoms**: Wake word works, but commands fail

**Solutions**:
1. **Check internet connection** (Google Speech API requires internet)
2. **Speak during "Listening..." window** (5-second timeout)
3. **Speak clearly and at normal pace**
4. **Try shorter commands** ("open google" vs "please open google website")

### Issue: "Network error - unknown command"

**Symptoms**: All commands result in network errors

**Solutions**:
1. **Check internet connection**
2. **Test with**: `ping google.com`
3. **Firewall settings**: Ensure Python can access internet
4. **VPN issues**: Try disconnecting VPN temporarily

### Issue: High CPU usage

**Symptoms**: Fan spinning, computer getting warm

**Solutions**:
1. **This is normal** during voice processing
2. **Close other audio apps** (Zoom, Spotify, etc.)
3. **Check Activity Monitor** for Python processes
4. **Restart test** if CPU usage stays high after stopping

---

## 📊 Success Criteria

### Stage 1 Passes If:

- [ ] **Environment test**: All 5 checks pass
- [ ] **Microphone test**: Can detect and process audio
- [ ] **Wake word detection**: 2/3 or better success rate
- [ ] **Command capture**: Commands transcribed correctly
- [ ] **Audio feedback**: Hear beep and "Listening..."
- [ ] **Error handling**: No crashes on errors
- [ ] **Response time**: < 5 seconds per cycle

### What Good Results Look Like:

```
📊 TEST RESULTS SUMMARY
════════════════════════════

Round 1: ✅ PASS
  Command: open google
  Confidence: 0.95
  Response Time: 2.1s

Round 2: ✅ PASS
  Command: click search
  Confidence: 0.95
  Response Time: 1.8s

Round 3: ✅ PASS
  Command: go back
  Confidence: 0.95
  Response Time: 2.3s

────────────────────────────
📈 OVERALL STATISTICS
────────────────────────────
Success Rate: 3/3 (100%)
Average Response Time: 2.1s

🎉 TEST STATUS: PASSED
VoiceNav voice system is working correctly!
```

---

## 🎛️ Advanced Testing

### Performance Testing

```bash
# Test memory usage
python3 -c "
import psutil, time
from tests.test_voice import VoiceListener
listener = VoiceListener()
process = psutil.Process()
print(f'Memory before: {process.memory_info().rss / 1024 / 1024:.1f} MB')
listener.start_listening()
time.sleep(10)  # Let it run
print(f'Memory after: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

### Audio Quality Testing

```bash
# Test with different microphones
python3 -c "
import speech_recognition as sr
r = sr.Recognizer()
for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{i}: {mic}')
"
```

### Configuration Testing

```bash
# Test different wake words
python3 -c "
from src.input.voice_listener import VoiceListener
listener = VoiceListener(wake_word='computer')
listener.listen_once()
"
```

---

## 📝 Test Documentation

### After Testing, Record in DEVLOG.md:

```markdown
#### Stage 1: Voice System Testing
**Date**: [Today's date]
**Time**: [Current time]
**Status**: ✅ Complete

**What**: 
Completed comprehensive testing of Stage 1 voice input system including
wake word detection, command capture, and error handling.

**Test Results**:
- Standard Test: [X]/3 passes
- Interactive Test: [Success/Issues]
- Error Handling: [Pass/Fail]
- Performance: [Memory usage, response times]

**Issues Encountered**: 
[Any problems and how they were resolved]

**System Info**:
- Python Version: [Version]
- macOS Version: [Version]
- Microphone: [Built-in/External]
- Environment: [Quiet/Noisy]

**Next Steps**: 
1. Begin Stage 2: Browser Control integration
2. Update project statistics
3. Commit changes to git

**Status**: ✅ Complete
```

---

## 🚀 Next Steps After Testing

### If Tests Pass:

1. **Update DEVLOG.md** with test results
2. **Commit changes** to git:
   ```bash
   git add .
   git commit -m "Stage 1: Voice input system complete - tests pass"
   ```
3. **Update project statistics** in DEVLOG.md
4. **Read Stage 2 requirements** in project documentation
5. **Begin browser control integration**

### If Tests Fail:

1. **Review troubleshooting** section above
2. **Check SETUP_GUIDE.md** for environment issues
3. **Verify all prerequisites** are met
4. **Test individual components**:
   - Microphone: `python3 -c "from src.input.voice_listener import VoiceListener; VoiceListener().test_microphone()"`
   - Speech recognition: Basic test in test_voice.py
   - Dependencies: `python3 tests/test_environment.py`
5. **Document issues** in DEVLOG.md
6. **Retry testing** after fixes

---

## 📞 Support

If you encounter issues not covered here:

1. **Check DEVLOG.md** for known issues and solutions
2. **Review README.md** troubleshooting section
3. **Check project documentation** for setup guidance
4. **Verify your system meets** all requirements (M3 Mac, Python 3.11+)

Remember: Document everything in DEVLOG.md!

---

**Created**: 2024-10-29  
**Stage**: 1 (Voice Input System)  
**Status**: Ready for testing  
**Next**: Stage 2 (Browser Control)
