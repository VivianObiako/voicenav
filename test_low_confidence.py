#!/usr/bin/env python3
"""
Test Maya with Lower Confidence Threshold
Quick fix for recognition issues
"""

import sys
sys.path.append('src')

def main():
    print("🔧 Maya Low Confidence Test")
    print("="*40)
    print("Testing Maya with 30% confidence threshold instead of 80%")
    print()
    
    try:
        from input.enhanced_voice_listener import EnhancedVoiceListener
        
        # Create Maya with much lower confidence threshold
        maya = EnhancedVoiceListener(
            wake_word="hey maya",
            confidence_threshold=0.3,  # 30% instead of 80%
            noise_reduction=True
        )
        
        print("🎤 Say: 'Hey Maya test this'")
        print("(Now using 30% confidence threshold - should work better)")
        print()
        
        result = maya.listen_once()
        
        if result:
            confidence_pct = result['confidence'] * 100
            meets_threshold = result.get('meets_threshold', False)
            
            print(f"📝 Maya heard: '{result['raw_text']}'")
            print(f"📊 Confidence: {confidence_pct:.0f}%")
            print(f"✅ Accepted: {meets_threshold}")
            
            if meets_threshold:
                print("\n🎉 SUCCESS! Maya is working with 30% threshold!")
                print("💡 Use this threshold for better performance:")
                print("   EnhancedVoiceListener(confidence_threshold=0.3)")
            else:
                print(f"\n⚠️  Still below 30% threshold")
                print("   Try speaking louder or closer to microphone")
        else:
            print("❌ No wake word detected")
            print("   Make sure to say 'Hey Maya' clearly")
        
        maya.cleanup()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Make sure you:")
        print("1. cd ~/Github/Personal/voicenav")
        print("2. source venv/bin/activate")
        print("3. pip install openai-whisper noisereduce colorama")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
