#!/usr/bin/env python3
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
