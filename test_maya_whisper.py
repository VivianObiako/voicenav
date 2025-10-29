#!/usr/bin/env python3
"""
Maya + Whisper Integration Test
High-accuracy voice recognition with "Hey Maya"
"""

import sys
sys.path.append('src')

from input.voice_listener import create_voice_listener, WHISPER_AVAILABLE

print("🎤 Maya + Whisper Integration Test")
print("=" * 50)
print("Testing VoiceNav with high-accuracy Whisper recognition")
print("and your chosen wake word: 'Hey Maya'")
print()

# Check Whisper availability
if WHISPER_AVAILABLE:
    print("✅ Whisper is available - using high-accuracy mode")
else:
    print("⚠️  Whisper not available - using standard recognition")
    print("   To get Whisper: pip install openai-whisper")

print()

try:
    # Create the best available voice listener
    print("🧠 Initializing Maya's voice system...")
    listener = create_voice_listener(wake_word="hey maya", prefer_whisper=True)
    
    # Check what type we got
    if hasattr(listener, 'whisper_model'):
        print("🚀 Maya is powered by Whisper (high accuracy)")
        recognition_type = "Whisper"
    else:
        print("📡 Maya is using standard recognition")
        recognition_type = "Google Speech"
    
    print(f"🎯 Wake word: '{listener.wake_word}'")
    print()
    
    # Test microphone
    print("🔧 Testing microphone access...")
    if not listener.test_microphone():
        print("❌ Fix microphone issues first")
        exit(1)
    
    print("✅ Microphone working!")
    
    # Test recognition if it's Whisper
    if hasattr(listener, 'test_whisper_recognition'):
        print("\n🧠 Testing Whisper recognition...")
        if not listener.test_whisper_recognition():
            print("❌ Whisper recognition test failed")
            exit(1)
        print("✅ Whisper is working perfectly!")
    
    print("\n" + "=" * 50)
    print("🎤 MAYA WAKE WORD TEST")
    print("=" * 50)
    print("Maya is listening for her wake word.")
    print(f"📢 Say: 'Hey Maya' followed by a command")
    print("💡 Example: 'Hey Maya, open Google'")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    # Main test
    print("👂 Maya is listening...")
    command = listener.listen_once()
    
    if command:
        print("\n" + "🎉" * 20)
        print("SUCCESS! Maya heard and understood you!")
        print("🎉" * 20)
        print(f"   👂 Recognition: {recognition_type}")
        print(f"   💬 Command: '{command['raw_text']}'")
        print(f"   📊 Confidence: {command['confidence']}")
        print(f"   ⏰ Time: {command['timestamp']}")
        print("\n✅ Maya + Whisper integration is working!")
        print("🚀 Ready for Stage 2: Browser Control")
    else:
        print("\n❌ Maya didn't detect the wake word")
        print("💡 Troubleshooting tips:")
        print("   - Make sure to say 'Hey Maya' clearly")
        print("   - Speak at normal volume")
        print("   - Wait for Maya to process between phrases")
        if not WHISPER_AVAILABLE:
            print("   - Consider installing Whisper for better accuracy")

except KeyboardInterrupt:
    print("\n👋 Test stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("🔧 Make sure all dependencies are installed:")
    print("   pip install -r requirements.txt")

finally:
    try:
        if hasattr(listener, 'cleanup'):
            listener.cleanup()
    except:
        pass

print(f"\n🎯 Maya Voice System Status:")
print(f"   Recognition Engine: {recognition_type if 'recognition_type' in locals() else 'Unknown'}")
print(f"   Wake Word: Hey Maya")
print(f"   Whisper Available: {'Yes' if WHISPER_AVAILABLE else 'No'}")
print(f"   Ready for Browser Control: {'Yes' if 'command' in locals() and command else 'Needs testing'}")
