#!/usr/bin/env python3
"""
Quick test for 'Hey Maya' wake word
"""

import sys
sys.path.append('src')

from input.voice_listener import create_voice_listener, WHISPER_AVAILABLE

print("🎤 Testing VoiceNav with 'Hey Maya'")
print("=" * 40)
print("This will test the updated VoiceNav system")
print("with your chosen wake word: 'Hey Maya'")

# Show which recognition engine is being used
if WHISPER_AVAILABLE:
    print("🚀 Using Whisper AI recognition (high accuracy)")
else:
    print("📡 Using Google Speech recognition (install whisper for better accuracy)")
print()

try:
    # Initialize with Maya using the factory function
    listener = create_voice_listener(wake_word="hey maya")
    
    print("🔧 Testing microphone...")
    if not listener.test_microphone():
        print("❌ Fix microphone issues first")
        exit(1)
    
    print("\n✅ Microphone working!")
    print("🎤 Now testing wake word detection...")
    print(f"Say: '{listener.wake_word}' followed by a command")
    print("Press Ctrl+C to stop")
    print()
    print("👂 Listening for 'Hey Maya'...")
    
    # Test one complete cycle
    command = listener.listen_once()
    
    if command:
        print(f"\n🎉 SUCCESS! Maya heard you:")
        print(f"   Wake word: ✅ Detected")
        print(f"   Command: '{command['raw_text']}'")
        print(f"   Confidence: {command['confidence']}")
        print(f"   Time: {command['timestamp']}")
        print("\n✅ VoiceNav is working with Maya!")
    else:
        print("\n❌ Wake word not detected")
        print("💡 Tips:")
        print("   - Say 'Hey Maya' clearly")
        print("   - Speak at normal volume")
        print("   - Make sure you're close to microphone")

except KeyboardInterrupt:
    print("\n👋 Test stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("🔧 Check that all dependencies are installed")

print("\n🎯 Next step: If this works, VoiceNav is ready!")
print("Maya will be your voice assistant for browser control.")
