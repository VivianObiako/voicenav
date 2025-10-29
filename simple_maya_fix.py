#!/usr/bin/env python3
"""
Simple Maya Fix - Lower Confidence Threshold Test
"""

import sys
sys.path.append('src')

def test_lower_confidence():
    """Test Maya with lower confidence thresholds"""
    print("🔧 Testing Maya with Lower Confidence Thresholds")
    print("="*60)
    print("Based on your output showing 1-71% confidence, let's try lower thresholds...")
    print()
    
    try:
        from input.enhanced_voice_listener import EnhancedVoiceListener
        
        # Test with 30% threshold (much more permissive)
        print("🎯 Testing with 30% confidence threshold...")
        print("This should accept most of your speech attempts.")
        print()
        
        listener = EnhancedVoiceListener(
            confidence_threshold=0.3,  # Much lower than 0.8
            noise_reduction=True,
            wake_word="hey maya"
        )
        
        print("Say: 'Hey Maya test command'")
        print("(This should now work with your typical confidence levels)")
        print()
        
        result = listener.listen_once()
        
        if result:
            print("✅ SUCCESS with lower threshold!")
            print(f"   Text: '{result['raw_text']}'")
            print(f"   Confidence: {result['confidence']*100:.0f}%")
            print(f"   Meets 30% threshold: {result.get('meets_threshold', False)}")
            
            if result.get('meets_threshold', False):
                print("\n🎉 Maya is now working!")
                print("💡 Recommendation: Use 30% confidence threshold for your setup")
                print()
                print("To use this permanently:")
                print("listener = EnhancedVoiceListener(confidence_threshold=0.3)")
        else:
            print("❌ Still not working with 30% threshold")
            print("Let's try even lower...")
            
        listener.cleanup()
        
        # If 30% didn't work, try 10%
        if not result or not result.get('meets_threshold', False):
            print("\n🔧 Testing with 10% confidence threshold (very permissive)...")
            
            listener2 = EnhancedVoiceListener(
                confidence_threshold=0.1,  # Very low
                noise_reduction=True,
                wake_word="hey maya"
            )
            
            print("Say: 'Hey Maya anything'")
            result2 = listener2.listen_once()
            
            if result2 and result2.get('meets_threshold', False):
                print("✅ SUCCESS with 10% threshold!")
                print(f"   Text: '{result2['raw_text']}'")
                print(f"   Confidence: {result2['confidence']*100:.0f}%")
                print("\n💡 Recommendation: Use 10% confidence threshold")
            else:
                print("❌ Issue may be with microphone or Whisper setup")
                
            listener2.cleanup()
        
        print("\n" + "="*60)
        print("🎯 SOLUTION SUMMARY:")
        print("Your original 80% confidence threshold was too strict.")
        print("Most users need 30-50% for reliable operation.")
        print("You can adjust this based on your environment:")
        print()
        print("# For quieter environments:")
        print("listener = EnhancedVoiceListener(confidence_threshold=0.5)")
        print()
        print("# For noisier environments:")
        print("listener = EnhancedVoiceListener(confidence_threshold=0.3)")
        print()
        print("# For very noisy or accent-heavy environments:")
        print("listener = EnhancedVoiceListener(confidence_threshold=0.2)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're in the voicenav directory")
        print("2. Virtual environment is activated: source venv/bin/activate")
        print("3. Dependencies installed: pip install noisereduce colorama")


def create_practical_config():
    """Create a practical Maya configuration file"""
    print("\n📄 Creating Practical Maya Configuration")
    print("-" * 50)
    
    config_content = '''#!/usr/bin/env python3
"""
Practical Maya Configuration - Optimized for Real Use
Use this instead of the high-threshold defaults
"""

import sys
sys.path.append('src')
from input.enhanced_voice_listener import EnhancedVoiceListener

def create_practical_maya():
    """Create Maya with practical settings"""
    return EnhancedVoiceListener(
        wake_word="hey maya",
        confidence_threshold=0.3,  # Practical threshold (not 0.8)
        noise_reduction=True,
        command_timeout=5
    )

def quick_test():
    """Quick test with practical settings"""
    print("🎤 Maya with Practical Settings")
    print("="*40)
    
    maya = create_practical_maya()
    
    print("Say: 'Hey Maya test command'")
    print("(Using 30% confidence threshold)")
    
    result = maya.listen_once()
    
    if result:
        print(f"✅ Maya heard: '{result['raw_text']}' ({result['confidence']*100:.0f}%)")
        if result.get('meets_threshold', False):
            print("🎉 Command accepted!")
        else:
            print("⚠️  Command below threshold (but Maya heard it)")
    else:
        print("❌ No wake word detected")
    
    maya.cleanup()

if __name__ == "__main__":
    quick_test()
'''
    
    with open('practical_maya.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Created: practical_maya.py")
    print("🚀 Test it with: python3 practical_maya.py")


if __name__ == "__main__":
    print("🔧 Maya Quick Fix Tool")
    print("Based on your low confidence scores (1-71%), we need to lower the threshold.")
    print()
    
    test_lower_confidence()
    create_practical_config()
    
    print("\n🎯 Next Steps:")
    print("1. Test the practical configuration: python3 practical_maya.py")
    print("2. If that works, use 30% confidence in your applications")
    print("3. Adjust threshold based on your environment needs")
    print()
    print("Remember: 80% confidence is very strict - most users need 30-50%!")
