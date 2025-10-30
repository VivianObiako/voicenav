#!/usr/bin/env python3
"""
Test the fixed VoiceNav system with audio issue fixes
"""

import sys
import os
import asyncio
import time

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.input.voice_listener import create_voice_listener
from src.brain.command_parser import CommandParser
from src.actions.applescript_browser import AppleScriptBrowserController


async def test_individual_components():
    """Test each component individually"""
    print("🧪 Testing Individual Components")
    print("=" * 50)
    
    # Test 1: Command Parser
    print("\n1️⃣ Testing Command Parser...")
    parser = CommandParser()
    
    test_commands = [
        "open google",
        "scroll down", 
        "go back",
        "help"
    ]
    
    for cmd in test_commands:
        result = parser.parse(cmd)
        print(f"   '{cmd}' → {result['intent']} (confidence: {result['confidence']})")
    
    # Test 2: Browser Controller
    print("\n2️⃣ Testing Browser Controller...")
    browser = AppleScriptBrowserController("Safari")
    
    try:
        success = await browser.initialize()
        if success:
            print("   ✅ Browser initialized successfully")
            
            # Test opening a page
            print("   🔗 Testing page opening...")
            await browser.open_url("https://example.com", "example")
            
            print("   ⏳ Waiting 3 seconds...")
            await asyncio.sleep(3)
            
            print("   ✅ Browser test completed")
        else:
            print("   ❌ Browser initialization failed")
    except Exception as e:
        print(f"   ❌ Browser test failed: {e}")
    finally:
        await browser.cleanup()
    
    # Test 3: Voice Listener (Basic setup only)
    print("\n3️⃣ Testing Voice Listener Setup...")
    try:
        maya = create_voice_listener(wake_word="hey maya")
        if maya.test_microphone():
            print("   ✅ Voice listener setup successful")
        else:
            print("   ❌ Voice listener setup failed")
    except Exception as e:
        print(f"   ❌ Voice listener test failed: {e}")
    
    print("\n✅ Component testing completed!")


async def test_simple_integration():
    """Test integration without full voice loop"""
    print("\n🔗 Testing Simple Integration")
    print("=" * 50)
    
    try:
        # Initialize components
        print("🎤 Initializing Maya...")
        maya = create_voice_listener(wake_word="hey maya")
        
        print("🧠 Initializing parser...")
        parser = CommandParser()
        
        print("🌐 Initializing browser...")
        browser = AppleScriptBrowserController("Safari")
        await browser.initialize()
        
        print("\n✅ All components ready!")
        print("\n📝 Testing command pipeline:")
        
        # Test command pipeline manually
        test_command = "open google"
        print(f"   Input: '{test_command}'")
        
        # Parse command
        parsed = parser.parse(test_command)
        print(f"   Parsed: {parsed['intent']} → {parsed['params']}")
        
        # Execute command
        success = await browser.execute_command(parsed)
        print(f"   Executed: {'✅ Success' if success else '❌ Failed'}")
        
        print("\n✅ Integration test completed!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
    finally:
        try:
            await browser.cleanup()
        except:
            pass


async def test_one_voice_cycle():
    """Test one complete voice cycle with fixes"""
    print("\n🎙️ Testing One Complete Voice Cycle")
    print("=" * 50)
    print("This will test the full voice → parse → browser pipeline")
    print("With the new fixes for audio feedback loops and language detection")
    
    try:
        # Initialize everything
        maya = create_voice_listener(wake_word="hey maya")
        parser = CommandParser()
        browser = AppleScriptBrowserController("Safari")
        await browser.initialize()
        
        print("\n🎤 Ready for voice test!")
        print("Say: 'Hey Maya' followed by 'open google'")
        print("The system should now properly handle audio pauses and English-only recognition")
        print("\nPress Enter when ready to start, or Ctrl+C to skip...")
        
        try:
            input()  # Wait for user
        except KeyboardInterrupt:
            print("\n⏭️ Skipping voice test")
            return
        
        print("\n👂 Listening for Maya wake word...")
        
        # Listen for one command
        result = maya.listen_once()
        
        if result and result.get('raw_text'):
            command_text = result['raw_text']
            print(f"\n🎤 Maya heard: '{command_text}'")
            
            # Parse and execute
            parsed = parser.parse(command_text)
            print(f"🧠 Parsed as: {parsed['intent']}")
            
            success = await browser.execute_command(parsed)
            print(f"🌐 Execution: {'✅ Success' if success else '❌ Failed'}")
            
            print("\n✅ Voice cycle completed successfully!")
            print("Check if the feedback loop issue is resolved!")
            
        else:
            print("\n❌ No wake word detected or command captured")
    
    except Exception as e:
        print(f"❌ Voice test failed: {e}")
    finally:
        try:
            await browser.cleanup()
            maya.cleanup()
        except:
            pass


async def main():
    """Main test function"""
    print("🔧 VoiceNav Fixed System Test")
    print("=" * 60)
    print("Testing the fixes for:")
    print("• Audio feedback loop (Maya's voice triggering new wake words)")
    print("• Korean language detection ('open google' → '아픔거구')")
    print("• Improved wake word filtering")
    print("• Proper audio pauses after Maya speaks")
    print("=" * 60)
    
    try:
        # Test 1: Individual components
        await test_individual_components()
        
        # Test 2: Simple integration
        await test_simple_integration()
        
        # Test 3: One complete voice cycle
        await test_one_voice_cycle()
        
        print("\n🎉 All tests completed!")
        print("\nThe main fixes implemented:")
        print("✅ Force English language in Whisper transcription")
        print("✅ Add 2.5s pause after Maya says 'I'm listening'")
        print("✅ Add 1.5s pause after Maya speaks feedback")
        print("✅ Filter out Maya's own voice responses")
        print("✅ Stricter wake word detection (length < 30 chars)")
        print("✅ Better skip phrases detection")
        
        print("\n🚀 Try running the full system now:")
        print("   python3 src/main.py")
        
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
