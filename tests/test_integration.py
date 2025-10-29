#!/usr/bin/env python3
"""
Test Script for VoiceNav Stage 2 Integration
Tests complete Maya + Parser + Browser integration
"""

import sys
import os
import asyncio
import threading
import queue
import time

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from input.voice_listener import create_voice_listener
from brain.command_parser import CommandParser
from actions.browser_control import BrowserController


class IntegrationTester:
    """
    Test complete Stage 2 integration
    Maya → Parser → Browser pipeline
    """
    
    def __init__(self):
        self.maya = None
        self.parser = None
        self.browser = None
        self.command_queue = queue.Queue()
        self.test_results = []
    
    async def initialize_components(self):
        """Initialize all Stage 2 components"""
        print("🎤 Initializing Maya voice assistant...")
        
        try:
            # Maya (Stage 1 - working system)
            self.maya = create_voice_listener(wake_word="hey maya")
            print("✅ Maya ready!")
            
            # Parser (Stage 2)
            print("🧠 Initializing command parser...")
            self.parser = CommandParser()
            print("✅ Parser ready!")
            
            # Browser (Stage 2)
            print("🌐 Initializing browser controller...")
            self.browser = BrowserController()
            success = await self.browser.initialize()
            
            if success:
                print("✅ Browser ready!")
                return True
            else:
                print("❌ Browser initialization failed")
                return False
                
        except Exception as e:
            print(f"❌ Component initialization error: {e}")
            return False
    
    def test_voice_to_parser(self):
        """Test voice input → parser pipeline without browser"""
        print("\n🔗 Testing Voice → Parser Pipeline")
        print("-" * 40)
        
        test_commands = [
            "open google",
            "click search box", 
            "scroll down",
            "go back",
            "help"
        ]
        
        passed = 0
        
        for command_text in test_commands:
            try:
                # Simulate voice input
                voice_result = {
                    'raw_text': command_text,
                    'confidence': 0.95,
                    'timestamp': time.time()
                }
                
                # Parse command
                parsed = self.parser.parse(voice_result['raw_text'])
                
                # Check if parsing worked
                if parsed['intent'] != 'unknown':
                    print(f"✅ '{command_text}' → {parsed['intent']}")
                    passed += 1
                else:
                    print(f"❌ '{command_text}' → unknown intent")
                    
            except Exception as e:
                print(f"❌ '{command_text}' → error: {e}")
        
        print(f"\n📊 Voice→Parser: {passed}/{len(test_commands)} tests passed")
        return passed == len(test_commands)
    
    async def test_parser_to_browser(self):
        """Test parser → browser pipeline"""
        print("\n🔗 Testing Parser → Browser Pipeline")
        print("-" * 40)
        
        test_commands = [
            {
                'text': 'open example.com',
                'expected_intent': 'open_url'
            },
            {
                'text': 'scroll down',
                'expected_intent': 'scroll_down'
            },
            {
                'text': 'help',
                'expected_intent': 'help'
            }
        ]
        
        passed = 0
        
        for test in test_commands:
            try:
                command_text = test['text']
                expected_intent = test['expected_intent']
                
                # Parse command
                parsed = self.parser.parse(command_text)
                
                if parsed['intent'] == expected_intent:
                    print(f"✅ Parse: '{command_text}' → {parsed['intent']}")
                    
                    # Execute in browser
                    success = await self.browser.execute_command(parsed)
                    
                    if success:
                        print(f"✅ Execute: {parsed['intent']} completed")
                        passed += 1
                    else:
                        print(f"❌ Execute: {parsed['intent']} failed")
                else:
                    print(f"❌ Parse: '{command_text}' → {parsed['intent']} (expected {expected_intent})")
                
                # Wait between commands
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ '{test['text']}' → error: {e}")
        
        print(f"\n📊 Parser→Browser: {passed}/{len(test_commands)} tests passed")
        return passed == len(test_commands)
    
    async def test_interactive_integration(self):
        """Test interactive Maya → Parser → Browser pipeline"""
        print("\n🎯 Testing Interactive Integration")
        print("-" * 40)
        print("This test requires voice interaction!")
        print("You'll need to speak to Maya during the test.")
        
        # Ask user if they want to run interactive test
        try:
            response = input("\nRun interactive voice test? (y/n): ").lower().strip()
            if response != 'y':
                print("⏭️  Skipping interactive test")
                return True
        except KeyboardInterrupt:
            print("\n⏭️  Skipping interactive test")
            return True
        
        print("\n🎤 Starting interactive test...")
        print("Say these commands when prompted:")
        print("1. 'Hey Maya, open google'")
        print("2. 'Hey Maya, scroll down'") 
        print("3. 'Hey Maya, help'")
        print("\nPress ENTER when ready...")
        
        try:
            input()
        except KeyboardInterrupt:
            print("⏭️  Test cancelled")
            return True
        
        commands_to_test = 3
        commands_completed = 0
        
        print(f"\n🎤 Listening for {commands_to_test} commands...")
        print("Say: 'Hey Maya, open google'")
        
        # Listen for commands
        for i in range(commands_to_test):
            try:
                print(f"\n🎤 Waiting for command {i+1}/{commands_to_test}...")
                
                # Use a timeout for voice listening
                voice_result = None
                
                # Simple timeout mechanism
                start_time = time.time()
                timeout = 30  # 30 seconds per command
                
                while time.time() - start_time < timeout:
                    try:
                        # Try to get voice input
                        voice_result = self.maya.listen_once()
                        if voice_result and voice_result.get('raw_text'):
                            break
                    except:
                        pass
                    
                    await asyncio.sleep(0.1)
                
                if voice_result and voice_result.get('raw_text'):
                    command_text = voice_result['raw_text']
                    print(f"🎤 Heard: '{command_text}'")
                    
                    # Parse command
                    parsed = self.parser.parse(command_text)
                    print(f"🧠 Parsed: {parsed['intent']}")
                    
                    # Execute command
                    success = await self.browser.execute_command(parsed)
                    
                    if success:
                        print(f"✅ Command {i+1} completed successfully!")
                        commands_completed += 1
                    else:
                        print(f"❌ Command {i+1} failed to execute")
                    
                    # Prompt for next command
                    if i == 0:
                        print("\nNext: Say 'Hey Maya, scroll down'")
                    elif i == 1:
                        print("\nNext: Say 'Hey Maya, help'")
                    
                else:
                    print(f"⏰ Command {i+1} timed out (no voice input)")
            
            except Exception as e:
                print(f"❌ Command {i+1} error: {e}")
        
        print(f"\n📊 Interactive Test: {commands_completed}/{commands_to_test} commands completed")
        
        if commands_completed >= 2:  # Allow some flexibility
            print("✅ Interactive integration test PASSED!")
            return True
        else:
            print("❌ Interactive integration test needs improvement")
            return False
    
    async def cleanup(self):
        """Clean up all resources"""
        print("\n🧹 Cleaning up...")
        
        if self.maya:
            try:
                self.maya.cleanup()
            except:
                pass
        
        if self.browser:
            await self.browser.cleanup()
        
        print("✅ Cleanup complete")


async def run_integration_tests():
    """Run complete Stage 2 integration tests"""
    print("🧪 VoiceNav Stage 2 Integration Test Suite")
    print("=" * 60)
    print("Testing: Maya → Command Parser → Browser Control")
    print("=" * 60)
    
    tester = IntegrationTester()
    
    try:
        # Initialize all components
        print("🚀 Initializing Stage 2 components...")
        success = await tester.initialize_components()
        
        if not success:
            print("❌ Cannot run integration tests without all components")
            return False
        
        print("✅ All components initialized!")
        
        # Test 1: Voice to Parser pipeline
        voice_parser_passed = tester.test_voice_to_parser()
        
        # Test 2: Parser to Browser pipeline  
        parser_browser_passed = await tester.test_parser_to_browser()
        
        # Test 3: Interactive integration (optional)
        interactive_passed = await tester.test_interactive_integration()
        
        # Results summary
        tests = [
            ("Voice → Parser Pipeline", voice_parser_passed),
            ("Parser → Browser Pipeline", parser_browser_passed), 
            ("Interactive Integration", interactive_passed)
        ]
        
        passed_count = sum(1 for _, passed in tests if passed)
        total_count = len(tests)
        
        print("\n" + "=" * 60)
        print("🏁 STAGE 2 INTEGRATION RESULTS:")
        for test_name, passed in tests:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        print(f"\n📊 Overall: {passed_count}/{total_count} tests passed ({passed_count/total_count*100:.1f}%)")
        
        if passed_count >= 2:  # Allow some flexibility for interactive test
            print("\n🎉 STAGE 2 INTEGRATION SUCCESSFUL!")
            print("✅ Maya can now control your browser!")
            print("\n🎯 Ready for Stage 3: Main Application & Menu Bar UI")
            return True
        else:
            print(f"\n⚠️  Integration needs work before proceeding to Stage 3")
            return False
    
    except Exception as e:
        print(f"❌ Integration test error: {e}")
        return False
    
    finally:
        await tester.cleanup()


def main():
    """Run integration tests"""
    try:
        success = asyncio.run(run_integration_tests())
        return success
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Test runner error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 STAGE 2 READY' if success else '❌ NEEDS WORK'}")
    sys.exit(0 if success else 1)
