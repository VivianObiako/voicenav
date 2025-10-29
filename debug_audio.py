#!/usr/bin/env python3
"""
VoiceNav Audio Debug Tool
Shows everything the system is hearing in real-time
"""

import speech_recognition as sr
import time
import sys
import os

# Add src to path
sys.path.append('src')
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("debug_audio")

def debug_audio_recognition():
    """Debug tool to see what speech recognition is picking up"""
    print("🎤 VoiceNav Audio Debug Tool")
    print("=" * 50)
    print("This tool will show EVERYTHING the system hears.")
    print("Press Ctrl+C to stop\n")
    
    # Initialize components
    recognizer = sr.Recognizer()
    
    # Apply the same sensitivity settings as voice_listener.py
    recognizer.energy_threshold = 1000  # Higher sensitivity
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.5    # Faster response
    recognizer.phrase_threshold = 0.2   # Shorter phrases
    
    print(f"🔧 Settings Applied:")
    print(f"   Energy threshold: {recognizer.energy_threshold}")
    print(f"   Pause threshold: {recognizer.pause_threshold}s")
    print(f"   Phrase threshold: {recognizer.phrase_threshold}s")
    print(f"   Dynamic energy: {recognizer.dynamic_energy_threshold}")
    print()
    
    try:
        microphone = sr.Microphone()
        
        # Setup microphone
        with microphone as source:
            print("🎤 Adjusting for ambient noise... (2 seconds)")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print(f"✅ Ambient noise adjusted. Energy threshold: {recognizer.energy_threshold}")
            print()
        
        print("🎤 LISTENING - Say anything and I'll show what I hear:")
        print("   (Try saying 'hey voicenav' and other phrases)")
        print("   (Press Ctrl+C to stop)")
        print("-" * 50)
        
        cycle = 0
        while True:
            cycle += 1
            try:
                with microphone as source:
                    print(f"[{cycle:03d}] 👂 Listening...")
                    # Listen for audio with timeout
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                print(f"[{cycle:03d}] 🔄 Processing audio...")
                
                # Try to recognize what was said
                try:
                    text = recognizer.recognize_google(audio).lower()
                    print(f"[{cycle:03d}] 🎤 HEARD: '{text}'")
                    
                    # Check for wake word
                    if 'hey voicenav' in text:
                        print(f"[{cycle:03d}] ✅ WAKE WORD DETECTED! '{text}'")
                        print("     🔊 *BEEP* - Wake word found!")
                        
                    # Check for other common phrases
                    if any(phrase in text for phrase in ['hello', 'test', 'computer']):
                        print(f"[{cycle:03d}] 💬 Common phrase detected")
                        
                except sr.UnknownValueError:
                    print(f"[{cycle:03d}] ❓ Audio detected but unintelligible")
                except sr.RequestError as e:
                    print(f"[{cycle:03d}] ❌ Network error: {e}")
                
            except sr.WaitTimeoutError:
                print(f"[{cycle:03d}] ⏰ No audio detected (timeout)")
            except Exception as e:
                print(f"[{cycle:03d}] ❌ Error: {e}")
                
            # Small delay to prevent spam
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping audio debug...")
        print("=" * 50)
        print("Audio debug session complete!")
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure microphone permissions are granted")
        print("2. Check that your microphone is working")
        print("3. Try running: python3 -c 'import pyaudio; print(\"PyAudio OK\")'")

def quick_mic_test():
    """Quick microphone availability test"""
    print("🎤 Quick Microphone Test")
    print("-" * 30)
    
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        
        print(f"✅ PyAudio working")
        print(f"📱 Audio devices found: {p.get_device_count()}")
        
        # List available microphones
        print("\n🎙️ Available input devices:")
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"   [{i}] {info['name']} - {info['maxInputChannels']} channels")
        
        p.terminate()
        print("✅ Microphone enumeration complete\n")
        
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("VoiceNav Audio Debug Tool")
    print("=" * 40)
    print("Choose option:")
    print("1. Real-time audio debug (shows everything)")
    print("2. Quick microphone test")
    print("3. Both")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        print()
        
        if choice in ['2', '3']:
            if not quick_mic_test():
                print("❌ Microphone test failed. Fix microphone issues first.")
                sys.exit(1)
        
        if choice in ['1', '3']:
            debug_audio_recognition()
        elif choice == '2':
            print("✅ Microphone test complete!")
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
