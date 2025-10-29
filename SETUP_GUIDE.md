# VoiceNav Setup Guide - macOS M3 Pro

## ⚠️ Python Version Issue

Your current Python version is **3.9.6**, but VoiceNav requires **Python 3.11+**.

You'll need to install a newer version of Python first.

---

## Step 1: Install Homebrew (if not installed)

Homebrew is the easiest way to install Python and system dependencies on macOS.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, Homebrew should be available. If you're on Apple Silicon (M3), you might need to add it to your PATH:

```bash
# For Apple Silicon (M3)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify installation:
```bash
brew --version
```

---

## Step 2: Install Python 3.11+ via Homebrew

```bash
brew install python@3.11
```

Or install the latest version:
```bash
brew install python
```

---

## Step 3: Verify Python Installation

```bash
python3.11 --version
# or if you installed the latest
python3 --version
```

Should show: `Python 3.11.x` or higher

---

## Step 4: Install portaudio (Required for PyAudio)

```bash
brew install portaudio
```

---

## Step 5: Create Virtual Environment

From the `voicenav` directory:

```bash
cd ~/voicenav

# Create venv with Python 3.11
python3.11 -m venv venv

# Or if you installed the latest Python:
python3 -m venv venv

# Activate it
source venv/bin/activate
```

---

## Step 6: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If PyAudio fails to install:**

```bash
LDFLAGS="-L/opt/homebrew/lib" CFLAGS="-I/opt/homebrew/include" pip install pyaudio
```

---

## Step 7: Grant Microphone Permissions

1. Open **System Preferences/Settings**
2. Go to **Security & Privacy → Microphone** (or **Privacy & Security** on newer macOS)
3. Add **Terminal** (and your IDE if applicable) to the allowed apps list
4. May need to restart applications for changes to take effect

---

## Step 8: Run Environment Test

```bash
python3 tests/test_environment.py
```

You should see all 5 checks pass:
- ✓ Python Version Check: PASS
- ✓ System Info: PASS
- ✓ Project Structure: PASS
- ✓ Dependencies: PASS
- ✓ Microphone Access: PASS

---

## ✅ Success!

Once all tests pass, you're ready to move forward with Stage 1!

```bash
cd src
python3 main.py
```

---

## Troubleshooting

### PyAudio Still Failing?

Try installing with specific compiler flags:

```bash
pip uninstall pyaudio -y
LDFLAGS="-L/opt/homebrew/lib" CFLAGS="-I/opt/homebrew/include" ARCHFLAGS=-Qunused-arguments CFLAGS=-Qunused-arguments pip install pyaudio
```

### Microphone Not Detected?

```bash
# Test with Python directly
python3 -c "import pyaudio; p = pyaudio.PyAudio(); print(f'Audio devices: {p.get_device_count()}')"
```

### Virtual Environment Not Activating?

```bash
# Check the correct path
which python3
# Should show something like: /Users/vivianobiako/voicenav/venv/bin/python3

# If not, try:
source venv/bin/activate
which python3  # Verify it's now in venv
```

### Permission Denied When Installing?

Don't use `sudo pip` — use a virtual environment instead:

```bash
# Wrong:
sudo pip install -r requirements.txt

# Correct:
source venv/bin/activate
pip install -r requirements.txt
```

---

## Next Steps

Once the environment test passes:

1. ✅ Read the main `README.md`
2. ⏭️ Move to **Stage 1: Voice Input System**
3. 🎙️ Begin implementing microphone listening

---

## Need Help?

Check the `README.md` **Troubleshooting** section for more detailed diagnostics.

Good luck! 🚀
