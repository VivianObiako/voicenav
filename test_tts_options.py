#!/usr/bin/env python3
"""
Test different TTS options for Maya's voice
"""

import os
import sys
import tempfile
import subprocess

print("🎤 Maya Voice Testing - AI Text-to-Speech Options")
print("=" * 60)
print("Testing different ways for Maya to speak back to you")
print()

# Test messages
test_messages = [
    "Hello! I'm Maya, your voice assistant.",
    "I'm listening for your command.",
    "Command received. Processing now.",
    "Ready for your next request."
]

def test_macos_say():
    """Test macOS built-in 'say' command"""
    print("🧪 Testing macOS built-in speech...")
    try:
        # Test basic say command
        result = subprocess.run(['say', '-v', '?'], capture_output=True, text=True)
        if result.returncode == 0:
            voices = result.stdout.split('\n')[:5]  # Show first 5 voices
            print("✅ macOS speech available. Sample voices:")
            for voice in voices:
                if voice.strip():
                    print(f"   {voice.strip()}")
            
            # Test speaking
            print("\n🎤 Testing Maya speaking...")
            subprocess.run(['say', '-v', 'Samantha', test_messages[0]])
            return True
        else:
            print("❌ macOS speech not available")
            return False
    except Exception as e:
        print(f"❌ macOS speech test failed: {e}")
        return False

def test_openai_tts():
    """Test OpenAI TTS (requires API key)"""
    print("\n🧪 Testing OpenAI TTS...")
    try:
        # Check if openai is installed
        import openai
        print("✅ OpenAI library available")
        
        # Note: This would require API key setup
        print("💡 OpenAI TTS available but requires:")
        print("   - OpenAI API key setup")
        print("   - Account with TTS credits")
        print("   - Internet connection")
        print("   - Cost per usage (~$0.015 per 1000 characters)")
        return False  # Don't test without API key
        
    except ImportError:
        print("❌ OpenAI library not installed")
        print("   Install with: pip install openai")
        return False

def test_edge_tts():
    """Test Microsoft Edge TTS (free)"""
    print("\n🧪 Testing Microsoft Edge TTS (free)...")
    try:
        # Check if edge-tts is available
        result = subprocess.run(['which', 'edge-tts'], capture_output=True)
        if result.returncode == 0:
            print("✅ Edge TTS available")
            
            # Test speaking
            print("🎤 Testing Edge TTS...")
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                temp_file = f.name
            
            # Generate speech
            cmd = ['edge-tts', '--voice', 'en-US-AriaNeural', '--text', test_messages[0], '--write-media', temp_file]
            result = subprocess.run(cmd, capture_output=True)
            
            if result.returncode == 0 and os.path.exists(temp_file):
                # Play the audio
                subprocess.run(['afplay', temp_file])
                os.unlink(temp_file)
                print("✅ Edge TTS working!")
                return True
            else:
                print("❌ Edge TTS generation failed")
                return False
        else:
            print("❌ Edge TTS not installed")
            print("   Install with: pip install edge-tts")
            return False
            
    except Exception as e:
        print(f"❌ Edge TTS test failed: {e}")
        return False

def test_system_speech():
    """Test various system speech options"""
    print("\n🧪 Testing system speech alternatives...")
    
    # Test different macOS voices
    voices_to_test = ['Samantha', 'Alex', 'Victoria', 'Allison', 'Ava']
    
    for voice in voices_to_test:
        try:
            print(f"   Testing voice: {voice}")
            result = subprocess.run(['say', '-v', voice, f"Hello, this is {voice}"], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ {voice} works")
            else:
                print(f"   ❌ {voice} failed")
        except Exception:
            print(f"   ❌ {voice} not available")

def recommend_best_option():
    """Recommend the best TTS option"""
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATION FOR MAYA'S VOICE")
    print("=" * 60)
    
    print("Based on testing, here are your options:")
    print()
    print("🥇 OPTION 1: macOS 'say' command (RECOMMENDED)")
    print("   ✅ Free and built-in")
    print("   ✅ Works offline") 
    print("   ✅ Natural-sounding voices")
    print("   ✅ Fast and reliable")
    print("   💡 Best voice for Maya: 'Samantha' or 'Ava'")
    print()
    print("🥈 OPTION 2: Microsoft Edge TTS (FREE AI)")
    print("   ✅ Free AI-powered voices")
    print("   ✅ Very natural sounding")
    print("   ❌ Requires internet")
    print("   ❌ Slightly slower")
    print("   💡 Install: pip install edge-tts")
    print()
    print("🥉 OPTION 3: OpenAI TTS (PREMIUM AI)")
    print("   ✅ Highest quality AI voices")
    print("   ❌ Costs money (~$0.015 per 1000 chars)")
    print("   ❌ Requires API key")
    print("   ❌ Requires internet")
    print()
    print("🎯 RECOMMENDATION: Use macOS 'say' with Samantha voice")
    print("   It's free, fast, offline, and sounds great!")

def main():
    """Run all TTS tests"""
    # Test macOS say
    macos_works = test_macos_say()
    
    # Test Edge TTS
    edge_works = test_edge_tts()
    
    # Test OpenAI TTS  
    openai_available = test_openai_tts()
    
    # Test system voices
    if macos_works:
        test_system_speech()
    
    # Give recommendation
    recommend_best_option()
    
    print("\n🔧 NEXT STEP:")
    print("I can update Maya to use the macOS 'say' command")
    print("for much better text-to-speech. Would you like me to do that?")

if __name__ == "__main__":
    main()
