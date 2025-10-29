#!/usr/bin/env python3
"""
Test Original Maya System - Reverted to Working Version
This uses the original Whisper + Maya system that was working before Step 1 Extra
"""

import sys
sys.path.append('src')

def main():
    print("🔄 Testing REVERTED Maya System")
    print("="*50)
    print("Using the original working Whisper + Maya system")
    print("(Not the enhanced system with confidence thresholds)")
    print()
    
    try:
        # Import the factory function (should now default to Whisper)
        from input.voice_listener import create_voice_listener
        
        print("🧠 Creating Maya using original working system...")
        
        # This should create WhisperVoiceListener (not Enhanced)
        maya = create_voice_listener(
            wake_word="hey maya",
            prefer_whisper=True  # Use the working Whisper system
        )
        
        print(f"✅ Created: {type(maya).__name__}")
        print("   (Should be WhisperVoiceListener)")
        print()
        
        # Test the original system
        print("🎤 Testing Maya with original Whisper system...")
        print("Say: 'Hey Maya test command'")
        print("(This should work like before)")
        print()
        
        result = maya.listen_once()
        
        if result:
            print("✅ SUCCESS! Original Maya system is working!")
            print(f"   Text: {result['raw_text']}")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Type: {type(maya).__name__}")
        else:
            print("❌ No wake word detected")
            print("   Try speaking 'Hey Maya' clearly")
        
        maya.cleanup()
        
        print("\n" + "="*50)
        print("🎯 REVERT SUMMARY:")
        print("✅ Removed enhanced confidence threshold system")
        print("✅ Restored original working Whisper + Maya")
        print("✅ Suppressed FP16 warnings") 
        print("✅ Factory function now defaults to Whisper")
        print()
        print("Maya should now work as it did before the Step 1 Extra changes!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the voicenav directory with venv activated")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
