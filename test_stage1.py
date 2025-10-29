#!/usr/bin/env python3
"""
VoiceNav Stage 1 Testing Guide
Complete testing workflow for voice input system
"""

import os
import sys
import subprocess
import importlib.util


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)


def print_step(step_num, title):
    """Print formatted step"""
    print(f"\n{step_num}. 🔧 {title}")
    print("-" * 40)


def check_python_version():
    """Check Python version"""
    print_step(1, "CHECKING PYTHON VERSION")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required")
        print("Run: brew install python@3.11")
        return False
    else:
        print("✅ Python version is compatible")
        return True


def check_virtual_environment():
    """Check if virtual environment is activated"""
    print_step(2, "CHECKING VIRTUAL ENVIRONMENT")
    
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        print(f"✅ Virtual environment active: {venv_path}")
        return True
    else:
        print("❌ Virtual environment not activated")
        print("Run: source venv/bin/activate")
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    print_step(3, "CHECKING DEPENDENCIES")
    
    dependencies = [
        'speech_recognition',
        'pyaudio', 
        'pyttsx3',
        'playwright',
        'rumps',
        'dotenv',
        'whisper',
        'torch',
        'numpy'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            spec = importlib.util.find_spec(dep)
            if spec is None:
                missing.append(dep)
                print(f"❌ {dep} not installed")
            else:
                print(f"✅ {dep} installed")
        except ImportError:
            missing.append(dep)
            print(f"❌ {dep} not installed")
    
    if missing:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies installed")
        return True


def check_microphone_permissions():
    """Guide user through microphone permission check"""
    print_step(4, "CHECKING MICROPHONE PERMISSIONS")
    
    print("To test microphone permissions:")
    print("1. We'll run a quick microphone test")
    print("2. If it fails, you'll need to grant permissions")
    print("\nMicrophone Permission Setup:")
    print("• macOS: System Settings → Privacy & Security → Microphone")
    print("• Add Terminal and your IDE to allowed apps")
    print("• Restart Terminal/IDE after granting permissions")
    
    response = input("\nRun microphone test? (y/n): ").lower().strip()
    return response == 'y'


def run_environment_test():
    """Run the environment test script"""
    print_step(5, "RUNNING ENVIRONMENT TEST")
    
    try:
        result = subprocess.run([
            sys.executable, 'tests/test_environment.py'
        ], capture_output=True, text=True, timeout=30)
        
        print("Environment test output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Environment test passed")
            return True
        else:
            print("❌ Environment test failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Environment test timed out")
        return False
    except Exception as e:
        print(f"❌ Environment test error: {e}")
        return False


def run_voice_test():
    """Run the voice system test"""
    print_step(6, "RUNNING VOICE SYSTEM TEST")
    
    print("This will test:")
    print("• Microphone access")
    print("• Wake word detection ('Hey Maya')")
    print("• Command capture")
    print("• Audio feedback with Samantha voice")
    print("• Whisper AI recognition (if available)")
    
    print("\nDuring the test:")
    print("1. Listen for 'Say: Hey Maya'")
    print("2. Speak clearly: 'Hey Maya'")
    print("3. Wait for beep and Maya saying 'I'm listening'")
    print("4. Say a command like 'open google'")
    print("5. Repeat 3 times")
    
    response = input("\nStart voice test? (y/n): ").lower().strip()
    if response != 'y':
        return False
    
    try:
        # Run the voice test
        result = subprocess.run([
            sys.executable, 'tests/test_voice.py'
        ], timeout=300)  # 5 minute timeout
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Voice test timed out")
        return False
    except KeyboardInterrupt:
        print("\n⚠️ Voice test interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Voice test error: {e}")
        return False


def print_troubleshooting():
    """Print troubleshooting guide"""
    print_header("TROUBLESHOOTING GUIDE")
    
    print("🔧 COMMON ISSUES & FIXES")
    print("\n1. 'No module named pyaudio'")
    print("   Fix: brew install portaudio")
    print("        pip install pyaudio")
    
    print("\n2. 'Permission denied' for microphone")
    print("   Fix: System Settings → Privacy & Security → Microphone")
    print("        Add Terminal to allowed apps")
    
    print("\n3. 'ModuleNotFoundError' for speech_recognition")
    print("   Fix: pip install -r requirements.txt")
    
    print("\n4. PyAudio won't compile on M3 Mac")
    print("   Fix: LDFLAGS='-L/opt/homebrew/lib' CFLAGS='-I/opt/homebrew/include' pip install pyaudio")
    
    print("\n5. Wake word not detected")
    print("   Fix: Speak clearly and loudly")
    print("        Reduce background noise")
    print("        Check microphone input level")
    
    print("\n6. 'Network error' during speech recognition")
    print("   Fix: Check internet connection")
    print("        Google Speech API requires internet")
    
    print("\n📖 MORE HELP")
    print("• Read: SETUP_GUIDE.md")
    print("• Read: README.md troubleshooting section")
    print("• Check: DEVLOG.md for known issues")


def print_success_message():
    """Print success message"""
    print_header("🎉 STAGE 1 COMPLETE!")
    
    print("✅ All tests passed successfully!")
    print("\nWhat's working:")
    print("• Voice listening system")
    print("• Wake word detection")
    print("• Command capture")
    print("• Audio feedback")
    print("• Error handling")
    
    print("\n🚀 READY FOR STAGE 2")
    print("Next: Browser control integration")
    print("\nDon't forget to:")
    print("1. Update DEVLOG.md with your test results")
    print("2. Commit changes to git")
    print("3. Review Stage 2 requirements")


def main():
    """Main testing workflow"""
    print_header("VOICENAV STAGE 1 TESTING GUIDE")
    
    print("This script will guide you through testing Stage 1:")
    print("• Environment verification")
    print("• Dependency checks")
    print("• Microphone setup")
    print("• Voice system testing")
    
    print("\nMake sure you're in the project directory:")
    print("$ cd ~/Github/Personal/voicenav")
    print("$ source venv/bin/activate")
    
    response = input("\nReady to begin? (y/n): ").lower().strip()
    if response != 'y':
        print("Test cancelled. Run this script when ready.")
        return
    
    # Run all checks
    checks = [
        check_python_version(),
        check_virtual_environment(), 
        check_dependencies(),
        check_microphone_permissions(),
    ]
    
    # Only run environment test if basic checks pass
    if all(checks):
        checks.append(run_environment_test())
    
    # Only run voice test if all checks pass
    if all(checks):
        checks.append(run_voice_test())
    
    # Print results
    print_header("TEST RESULTS")
    
    if all(checks):
        print_success_message()
    else:
        print("❌ Some tests failed")
        print("\nFailed checks:")
        check_names = [
            "Python Version",
            "Virtual Environment", 
            "Dependencies",
            "Microphone Permissions",
            "Environment Test",
            "Voice Test"
        ]
        
        for i, passed in enumerate(checks):
            if not passed and i < len(check_names):
                print(f"  • {check_names[i]}")
        
        print_troubleshooting()
    
    print("\n" + "="*60)
    print("Testing complete. See DEVLOG.md for next steps.")
    print("="*60)


if __name__ == "__main__":
    main()
