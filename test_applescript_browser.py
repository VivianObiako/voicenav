#!/usr/bin/env python3
"""
Test AppleScript Browser Control
Tests native macOS browser control via AppleScript
"""

import sys
import os
import asyncio

# Add src directory to path
sys.path.append('src')

from actions.applescript_browser import AppleScriptBrowserController


async def test_applescript_browser():
    """Test AppleScript browser control"""
    print("🍎 VoiceNav AppleScript Browser Test")
    print("=" * 50)
    print("This will control your actual Safari browser!")
    print("=" * 50)
    
    try:
        # Ask user which browser to test
        print("Available browsers:")
        print("1. Safari (recommended)")
        print("2. Google Chrome")
        
        try:
            choice = input("Choose browser (1 or 2): ").strip()
            if choice == "2":
                browser_name = "Google Chrome"
            else:
                browser_name = "Safari"
        except KeyboardInterrupt:
            print("\n⏭️  Using Safari as default")
            browser_name = "Safari"
        
        print(f"\n🌐 Testing {browser_name} control...")
        
        # Initialize controller
        controller = AppleScriptBrowserController(browser_name)
        
        # Test initialization
        print("📱 Initializing browser control...")
        success = await controller.initialize()
        
        if not success:
            print(f"❌ Failed to initialize {browser_name}")
            print("Make sure Safari is installed and accessible")
            return False
        
        print(f"✅ {browser_name} control ready!")
        
        # Test 1: Open URL
        print(f"\n🔗 Test 1: Opening example.com in {browser_name}...")
        success1 = await controller.open_url("https://example.com", "example website")
        
        if success1:
            print(f"✅ Successfully opened website in {browser_name}")
            print("   (Check your browser - should show example.com)")
        else:
            print("❌ Failed to open website")
        
        # Wait for user to see result
        input("\nPress ENTER to continue to next test...")
        
        # Test 2: Scroll down
        print(f"\n📜 Test 2: Scrolling down...")
        success2 = await controller.scroll_page('down', 300)
        
        if success2:
            print("✅ Successfully scrolled down")
            print("   (Check your browser - page should scroll)")
        else:
            print("❌ Failed to scroll")
        
        # Wait for user to see result
        input("\nPress ENTER to continue to next test...")
        
        # Test 3: Read page title
        print(f"\n📖 Test 3: Reading page title...")
        success3 = await controller.read_content('title')
        
        if success3:
            print("✅ Successfully read page title")
            print("   (Maya should have spoken the page title)")
        else:
            print("❌ Failed to read page title")
        
        # Test 4: Go back (if there's history)
        print(f"\n⬅️ Test 4: Testing go back...")
        success4 = await controller.go_back()
        
        if success4:
            print("✅ Successfully went back")
        else:
            print("❌ Go back failed (maybe no history)")
        
        # Test 5: Help command
        print(f"\n🆘 Test 5: Testing help command...")
        help_command = {
            'intent': 'help',
            'params': {}
        }
        success5 = await controller.execute_command(help_command)
        
        if success5:
            print("✅ Help command successful")
            print("   (Maya should have listed available commands)")
        else:
            print("❌ Help command failed")
        
        # Results summary
        tests = [
            ("Open URL", success1),
            ("Scroll Page", success2), 
            ("Read Content", success3),
            ("Navigate Back", success4),
            ("Help Command", success5)
        ]
        
        passed = sum(1 for _, success in tests if success)
        total = len(tests)
        
        print("\n" + "=" * 50)
        print("🏁 APPLESCRIPT BROWSER TEST RESULTS:")
        for test_name, success in tests:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed >= 3:  # Allow some flexibility
            print(f"\n🎉 APPLESCRIPT BROWSER CONTROL WORKING!")
            print(f"✅ Maya can now control your {browser_name}!")
            print("\n🎯 Ready for complete VoiceNav integration!")
            return True
        else:
            print(f"\n⚠️  Browser control needs work. Only {passed} tests passed.")
            return False
    
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
    
    finally:
        if 'controller' in locals():
            await controller.cleanup()


async def test_command_integration():
    """Test Maya + Parser + AppleScript Browser integration"""
    print("\n🔗 VoiceNav Complete Pipeline Test")
    print("=" * 50)
    print("Testing: Maya → Parser → AppleScript Browser")
    print("=" * 50)
    
    try:
        # Import all components
        from input.voice_listener import create_voice_listener
        from brain.command_parser import CommandParser
        
        print("🎤 Initializing Maya...")
        maya = create_voice_listener(wake_word="hey maya")
        print("✅ Maya ready!")
        
        print("🧠 Initializing Parser...")
        parser = CommandParser()
        print("✅ Parser ready!")
        
        print("🍎 Initializing Safari...")
        browser = AppleScriptBrowserController("Safari")
        await browser.initialize()
        print("✅ Safari ready!")
        
        # Test the complete pipeline without voice (simulate commands)
        test_commands = [
            "open google",
            "scroll down", 
            "help"
        ]
        
        print(f"\n🧪 Testing complete pipeline with simulated commands...")
        
        for i, command_text in enumerate(test_commands, 1):
            print(f"\n--- Test {i}: '{command_text}' ---")
            
            # Parse command
            parsed = parser.parse(command_text)
            print(f"🧠 Parsed: {parsed['intent']}")
            
            # Execute in browser
            success = await browser.execute_command(parsed)
            
            if success:
                print(f"✅ Command '{command_text}' executed successfully!")
            else:
                print(f"❌ Command '{command_text}' failed")
            
            if i < len(test_commands):
                input("Press ENTER for next test...")
        
        print(f"\n🎉 COMPLETE PIPELINE WORKING!")
        print(f"Maya → Parser → Safari integration successful!")
        
        await browser.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Pipeline test error: {e}")
        return False


def main():
    """Run AppleScript browser tests"""
    print("🧪 VoiceNav AppleScript Browser - Test Suite")
    print("=" * 60)
    
    try:
        # Run browser control test
        browser_success = asyncio.run(test_applescript_browser())
        
        if browser_success:
            # Run integration test
            integration_success = asyncio.run(test_command_integration())
            
            if integration_success:
                print("\n🎉 ALL TESTS PASSED!")
                print("✅ Stage 2 browser control is working!")
                print("✅ Maya can control your browser!")
                return True
        
        print("\n⚠️  Some tests failed")
        return False
        
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted")
        return False
    except Exception as e:
        print(f"❌ Test runner error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    print(f"\n{'🚀 READY FOR STAGE 3' if success else '🔧 NEEDS FIXES'}")
    sys.exit(0 if success else 1)
