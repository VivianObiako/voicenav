#!/usr/bin/env python3
"""
Test Maya's new Samantha voice
"""

import sys
sys.path.append('src')

from input.voice_listener import create_voice_listener

print("🎤 Testing Maya's New Voice (Samantha)")
print("=" * 50)
print("Maya now uses macOS built-in speech with Samantha's voice!")
print()

try:
    # Test the voice directly first
    print("🧪 Testing Samantha voice directly...")
    import subprocess
    
    test_phrases = [
        "Hello! I'm Maya, your voice assistant.",
        "I'm listening for your command.",
        "Wake word detected! Please continue.",
        "Command received. Ready for browser control."
    ]
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"   {i}. Testing: '{phrase}'")
        try:
            subprocess.run(['say', '-v', 'Samantha', phrase], check=True)
            print(f"   ✅ Samantha voice working!")
        except Exception as e:
            print(f"   ❌ Voice test failed: {e}")
            break
        
        if i < len(test_phrases):
            input("      Press Enter for next test...")
    
    print("\n🎤 Now testing Maya with integrated voice...")
    print("This will test both wake word detection AND Maya speaking back")
    print()
    
    # Initialize Maya with new voice
    listener = create_voice_listener(wake_word="hey maya")
    
    print("🔧 Testing microphone...")
    if not listener.test_microphone():
        print("❌ Fix microphone first")
        exit(1)
    
    print("✅ Microphone working!")
    print("\n" + "=" * 50)
    print("🎤 MAYA VOICE TEST")
    print("=" * 50)
    print("1. Say 'Hey Maya' to activate")
    print("2. Maya will beep and say 'I'm listening' with Samantha's voice")
    print("3. Say any command (e.g., 'open Google')")
    print("4. Press Ctrl+C to stop")
    print()
    
    # Main test
    print("👂 Maya is listening...")
    command = listener.listen_once()
    
    if command:
        # Maya should have spoken "I'm listening" already
        print(f"\n✅ SUCCESS! Maya heard: '{command['raw_text']}'")
        
        # Test Maya's response
        print("\n🎤 Maya will now confirm what she heard...")
        if hasattr(listener, '_speak'):
            listener._speak(f"I heard you say: {command['raw_text']}")
        
        print("\n🎉 Maya's voice integration complete!")
    else:
        print("\n❌ Maya didn't detect the wake word")

except KeyboardInterrupt:
    print("\n👋 Voice test stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")

finally:
    try:
        if 'listener' in locals() and hasattr(listener, 'cleanup'):
            listener.cleanup()
    except:
        pass

print("\n🎯 Maya Voice Status:")
print("   Voice Engine: macOS Samantha")
print("   Quality: Natural human-like speech")
print("   Speed: Instant (offline)")
print("   Cost: Free")
print("   Maya is ready to talk back! 🗣️")
