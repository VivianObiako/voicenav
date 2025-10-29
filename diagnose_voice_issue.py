#!/usr/bin/env python3
"""
Voice Test Diagnostic Script
Identifies the exact cause of voice test failures
"""

import sys
import os
import subprocess
import traceback


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*50)
    print(f"🔍 {title}")
    print("="*50)


def test_basic_imports():
    """Test if basic Python imports work"""
    print_header("TESTING BASIC IMPORTS")
    
    imports = [
        ('sys', 'Python system'),
        ('os', 'Operating system'),
        ('subprocess', 'Process management'),
        ('time', 'Time functions'),
        ('datetime', 'Date/time'),
    ]
    
    for module, description in imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except Exception as e:
            print(f"❌ {module} - {description}: {e}")
            return False
    
    return True


def test_voice_dependencies():
    """Test voice-related dependencies"""
    print_header("TESTING VOICE DEPENDENCIES")
    
    dependencies = [
        ('speech_recognition', 'Speech Recognition'),
        ('pyaudio', 'PyAudio (microphone)'),
        ('pyttsx3', 'Text-to-Speech'),
        ('playwright', 'Browser automation'),
        ('rumps', 'macOS menu bar'),
        ('dotenv', 'Environment variables'),
    ]
    
    all_ok = True
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - {description}: Not installed")
            print(f"   Fix: pip install {module}")
            all_ok = False
        except Exception as e:
            print(f"⚠️ {module} - {description}: {e}")
    
    return all_ok


def test_microphone_basic():
    """Test basic microphone access"""
    print_header("TESTING MICROPHONE ACCESS")
    
    try:
        import pyaudio
        print("✅ PyAudio imported successfully")
        
        # Test PyAudio initialization
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        print(f"✅ Audio devices detected: {device_count}")
        
        # List audio devices
        print("\n📱 Available Audio Devices:")
        for i in range(device_count):
            try:
                device_info = p.get_device_info_by_index(i)
                name = device_info['name']
                channels = device_info['maxInputChannels']
                if channels > 0:
                    print(f"  {i}: {name} (Input channels: {channels})")
            except:
                pass
        
        p.terminate()
        print("✅ PyAudio cleanup successful")
        return True
        
    except ImportError:
        print("❌ PyAudio not installed")
        print("   Fix: brew install portaudio && pip install pyaudio")
        return False
    except Exception as e:
        print(f"❌ Microphone access failed: {e}")
        print("   Possible fixes:")
        print("   - Grant microphone permissions in System Settings")
        print("   - Check if another app is using microphone")
        print("   - Try unplugging/replugging external microphones")
        return False


def test_speech_recognition():
    """Test speech recognition setup"""
    print_header("TESTING SPEECH RECOGNITION")
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported")
        
        # Test recognizer initialization
        recognizer = sr.Recognizer()
        print("✅ Recognizer created")
        
        # Test microphone access through speech_recognition
        try:
            microphone = sr.Microphone()
            print("✅ Microphone object created")
            
            # Test microphone access
            with microphone as source:
                print("🎤 Adjusting for ambient noise... (2 seconds)")
                recognizer.adjust_for_ambient_noise(source, duration=2)
                print("✅ Ambient noise adjustment successful")
            
            return True
            
        except Exception as e:
            print(f"❌ Microphone setup failed: {e}")
            print("   Check microphone permissions!")
            return False
            
    except ImportError:
        print("❌ SpeechRecognition not installed")
        print("   Fix: pip install SpeechRecognition")
        return False
    except Exception as e:
        print(f"❌ Speech recognition setup failed: {e}")
        return False


def test_network_connectivity():
    """Test network for Google Speech API"""
    print_header("TESTING NETWORK CONNECTIVITY")
    
    try:
        import urllib.request
        import socket
        
        # Test internet connectivity
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Internet connectivity OK")
        
        # Test Google connectivity
        try:
            response = urllib.request.urlopen("https://www.google.com", timeout=5)
            print("✅ Google.com accessible")
        except:
            print("⚠️ Google.com not accessible (may affect speech recognition)")
        
        return True
        
    except Exception as e:
        print(f"❌ Network connectivity failed: {e}")
        print("   Speech recognition requires internet connection")
        return False


def test_voicenav_imports():
    """Test VoiceNav-specific imports"""
    print_header("TESTING VOICENAV IMPORTS")
    
    try:
        # Add src to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        sys.path.insert(0, src_dir)
        
        print(f"📁 Source directory: {src_dir}")
        
        # Test logger import
        try:
            from utils.logger import setup_logger
            print("✅ Logger utility imported")
        except Exception as e:
            print(f"❌ Logger import failed: {e}")
            return False
        
        # Test VoiceListener import
        try:
            from input.voice_listener import VoiceListener
            print("✅ VoiceListener imported")
        except Exception as e:
            print(f"❌ VoiceListener import failed: {e}")
            print(f"   Error details: {traceback.format_exc()}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ VoiceNav imports failed: {e}")
        return False


def test_voicenav_initialization():
    """Test VoiceNav initialization"""
    print_header("TESTING VOICENAV INITIALIZATION")
    
    try:
        # Import VoiceListener
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        sys.path.insert(0, src_dir)
        
        from input.voice_listener import VoiceListener
        
        # Try to create VoiceListener instance
        print("🎤 Creating VoiceListener instance...")
        listener = VoiceListener()
        print("✅ VoiceListener created successfully")
        
        # Test microphone test method
        print("🎤 Testing microphone functionality...")
        result = listener.test_microphone()
        
        if result:
            print("✅ Microphone test passed")
            return True
        else:
            print("❌ Microphone test failed")
            return False
            
    except Exception as e:
        print(f"❌ VoiceNav initialization failed: {e}")
        print(f"   Error details: {traceback.format_exc()}")
        return False


def run_quick_speech_test():
    """Run a quick speech recognition test"""
    print_header("QUICK SPEECH TEST")
    
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Say something (you have 5 seconds):")
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
        
        print("🔄 Processing speech...")
        text = r.recognize_google(audio)
        print(f"✅ You said: '{text}'")
        return True
        
    except sr.WaitTimeoutError:
        print("⚠️ No speech detected in 5 seconds")
        print("   Try speaking louder or closer to microphone")
        return False
    except sr.UnknownValueError:
        print("⚠️ Could not understand the audio")
        print("   Try speaking more clearly")
        return False
    except sr.RequestError as e:
        print(f"❌ Google Speech API error: {e}")
        print("   Check internet connection")
        return False
    except Exception as e:
        print(f"❌ Speech test failed: {e}")
        return False


def print_summary(results):
    """Print diagnostic summary"""
    print_header("DIAGNOSTIC SUMMARY")
    
    tests = [
        ("Basic Imports", results[0]),
        ("Voice Dependencies", results[1]),
        ("Microphone Access", results[2]),
        ("Speech Recognition", results[3]),
        ("Network Connectivity", results[4]),
        ("VoiceNav Imports", results[5]),
        ("VoiceNav Initialization", results[6]),
    ]
    
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} passed")
    print()
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print()
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("Your voice system should be working correctly.")
        print("Try running: python3 tests/test_voice.py")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("Follow the specific fix instructions above.")
        
        # Suggest next steps based on failures
        if not results[1]:  # Dependencies
            print("\n🔧 IMMEDIATE FIX: Install missing dependencies")
            print("   Run: pip install -r requirements.txt")
        elif not results[2]:  # Microphone
            print("\n🔧 IMMEDIATE FIX: Grant microphone permissions")
            print("   Go to: System Settings → Privacy & Security → Microphone")
        elif not results[4]:  # Network
            print("\n🔧 IMMEDIATE FIX: Check internet connection")
            print("   Test: ping google.com")


def main():
    """Run comprehensive voice system diagnosis"""
    print("🏥 VoiceNav Voice System Diagnostic")
    print("=" * 50)
    print("This will identify why the voice test failed.")
    
    # Run all diagnostic tests
    results = [
        test_basic_imports(),
        test_voice_dependencies(),
        test_microphone_basic(),
        test_speech_recognition(),
        test_network_connectivity(),
        test_voicenav_imports(),
        test_voicenav_initialization(),
    ]
    
    # Print summary
    print_summary(results)
    
    # Optional speech test if everything else passes
    if all(results):
        print("\n🎤 Would you like to run a quick speech test? (y/n): ", end="")
        try:
            choice = input().strip().lower()
            if choice == 'y':
                speech_result = run_quick_speech_test()
                if speech_result:
                    print("\n🎉 COMPLETE SUCCESS!")
                    print("Your voice system is fully functional!")
                else:
                    print("\n⚠️ Speech test had issues, but core system works")
        except KeyboardInterrupt:
            print("\n👋 Diagnostic complete")


if __name__ == "__main__":
    main()
