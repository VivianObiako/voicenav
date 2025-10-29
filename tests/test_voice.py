"""
VoiceNav Voice System Test Script
Tests wake word detection and command capture functionality
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from input.voice_listener import create_voice_listener, WHISPER_AVAILABLE
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("test_voice")


def print_banner():
    """Print test banner"""
    print("\n" + "="*60)
    print("🎤 VOICENAV VOICE SYSTEM TEST")
    print("="*60)
    print("This test will:")
    print("1. Initialize the voice listener")
    print("2. Test wake word detection 3 times")
    print("3. Capture commands after each wake word")
    print("4. Display results")
    print("\nMake sure:")
    print("- Your microphone is working")
    print("- You've granted microphone permissions")
    print("- You're in a reasonably quiet environment")
    print("="*60)


def run_voice_test():
    """Run the voice system test"""
    print_banner()
    
    # Show recognition engine status
    if WHISPER_AVAILABLE:
        print("🚀 Maya powered by Whisper (high accuracy)")
    else:
        print("📡 Maya using standard recognition")
        print("   💡 For better accuracy: pip install openai-whisper")
    
    try:
        # Initialize voice listener with Maya
        print("\n🔧 Initializing Maya's voice system...")
        listener = create_voice_listener(wake_word="hey maya", command_timeout=5)
        print("✅ Maya initialized successfully")
        
        # Test microphone setup
        print("\n🎤 Testing microphone setup...")
        if not listener.test_microphone():
            print("❌ Microphone test failed. Please check your setup.")
            return False
        
        # Run 3 test cycles
        test_results = []
        
        for test_round in range(1, 4):
            print(f"\n" + "="*40)
            print(f"🎯 TEST ROUND {test_round}/3")
            print("="*40)
            
            print(f"\n🎤 Say: 'Hey Maya'")
            print("Listening for Maya...")
            
            # Listen for wake word and command
            start_time = time.time()
            command = listener.listen_once()
            end_time = time.time()
            
            if command:
                # Check if it's a real command (not timeout/error)
                if command['confidence'] > 0:
                    print(f"✅ Wake word detected! Command captured:")
                    print(f"   📝 You said: '{command['raw_text']}'")
                    print(f"   🎯 Confidence: {command['confidence']:.2f}")
                    print(f"   ⏰ Response time: {end_time - start_time:.1f}s")
                    
                    test_results.append({
                        'round': test_round,
                        'success': True,
                        'command': command['raw_text'],
                        'confidence': command['confidence'],
                        'response_time': end_time - start_time
                    })
                else:
                    print(f"⚠️ Wake word detected but command failed:")
                    print(f"   📝 Result: {command['raw_text']}")
                    print(f"   🎯 Confidence: {command['confidence']}")
                    
                    test_results.append({
                        'round': test_round,
                        'success': False,
                        'command': command['raw_text'],
                        'confidence': command['confidence'],
                        'response_time': end_time - start_time
                    })
            else:
                print("❌ No wake word detected in this round")
                test_results.append({
                    'round': test_round,
                    'success': False,
                    'command': 'No wake word detected',
                    'confidence': 0.0,
                    'response_time': end_time - start_time
                })
            
            # Brief pause between rounds
            if test_round < 3:
                print("\n⏳ Waiting 3 seconds before next test...")
                time.sleep(3)
        
        # Display final results
        print_test_results(test_results)
        
        return len([r for r in test_results if r['success']]) >= 2  # 2/3 success rate
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logger.error(f"Voice test error: {e}")
        return False


def print_test_results(results):
    """Print formatted test results"""
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    successful_tests = 0
    total_response_time = 0
    
    for result in results:
        round_num = result['round']
        success = result['success']
        command = result['command']
        confidence = result['confidence']
        response_time = result['response_time']
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"\nRound {round_num}: {status}")
        print(f"  Command: {command}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  Response Time: {response_time:.1f}s")
        
        if success:
            successful_tests += 1
            total_response_time += response_time
    
    # Overall statistics
    print("\n" + "-"*40)
    print("📈 OVERALL STATISTICS")
    print("-"*40)
    print(f"Success Rate: {successful_tests}/3 ({successful_tests/3*100:.0f}%)")
    
    if successful_tests > 0:
        avg_response_time = total_response_time / successful_tests
        print(f"Average Response Time: {avg_response_time:.1f}s")
    
    # Final verdict
    if successful_tests >= 2:
        print("\n🎉 TEST STATUS: PASSED")
        print("VoiceNav voice system is working correctly!")
    else:
        print("\n⚠️ TEST STATUS: FAILED")
        print("Voice system needs adjustment. Check:")
        print("- Microphone permissions")
        print("- Background noise levels")
        print("- Internet connection (for speech recognition)")
        print("- Speaking clearly and at normal volume")
    
    print("="*60)


def run_interactive_test():
    """Run an interactive test mode"""
    print("\n🎮 INTERACTIVE TEST MODE")
    print("="*30)
    print("This mode lets you test commands continuously.")
    print("Press Ctrl+C to exit.")
    
    try:
        listener = create_voice_listener(wake_word="hey maya")
        
        def command_callback(command):
            """Handle each command in interactive mode"""
            if command['confidence'] > 0:
                print(f"\n💬 Maya heard: '{command['raw_text']}'")
                print(f"🎯 Confidence: {command['confidence']:.2f}")
                print(f"⏰ Time: {command['timestamp']}")
            else:
                print(f"\n⚠️ {command['raw_text']}")
            
            print("\n🎤 Listening for 'Hey Maya'...")
        
        print("\n🎤 Starting interactive mode...")
        print("Say 'Hey Maya' followed by any command")
        
        listener.continuous_listen(callback=command_callback)
        
    except KeyboardInterrupt:
        print("\n\n👋 Interactive test ended")
    except Exception as e:
        print(f"\n❌ Interactive test error: {e}")


def main():
    """Main test function"""
    print("VoiceNav Voice System Test Suite")
    print("================================")
    print("\nChoose test mode:")
    print("1. Standard Test (3 rounds, automatic)")
    print("2. Interactive Test (continuous, manual stop)")
    print("3. Quick Microphone Test")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🏃 Running standard test...")
            success = run_voice_test()
            if success:
                print("\n🎉 All tests completed successfully!")
                print("VoiceNav is ready for Stage 2!")
            else:
                print("\n⚠️ Tests failed. Please check your setup.")
                print("See SETUP_GUIDE.md for troubleshooting.")
        
        elif choice == "2":
            run_interactive_test()
        
        elif choice == "3":
            print("\n🎤 Running quick microphone test...")
            listener = create_voice_listener(wake_word="hey maya")
            success = listener.test_microphone()
            if success:
                print("✅ Microphone is working correctly!")
            else:
                print("❌ Microphone setup needs attention.")
        
        else:
            print("Invalid choice. Exiting.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Test suite exited")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")


if __name__ == "__main__":
    main()
