"""
Enhanced Maya Voice System Test Script
Tests all Step 1 Extra features including confidence threshold,
noise cancellation, custom wake words, visual feedback, and undo functionality
"""

import sys
import os
import time

# Add src directory to path
sys.path.append('src')

def test_enhanced_maya():
    """Test all enhanced Maya features"""
    print("🔥 Enhanced Maya Voice System Test")
    print("="*50)
    print()
    
    try:
        # Import the enhanced voice listener
        from input.enhanced_voice_listener import EnhancedVoiceListener
        
        print("✅ Enhanced Maya module loaded successfully!")
        print()
        
        # Create enhanced listener with custom settings
        print("🔧 Initializing Enhanced Maya...")
        listener = EnhancedVoiceListener(
            wake_word="hey maya",
            confidence_threshold=0.8,  # 80% confidence required
            noise_reduction=True,      # Enable noise cancellation
            command_timeout=5
        )
        print()
        
        # Feature Test Menu
        while True:
            print("\n" + "="*50)
            print("🎯 Enhanced Maya Feature Tests")
            print("="*50)
            print("1. 🎤 Basic microphone and Whisper test")
            print("2. 🧠 Confidence threshold demonstration")
            print("3. 🎓 Train custom wake word")
            print("4. 📋 List custom wake words")
            print("5. 🔊 Full voice interaction test")
            print("6. ↩️  Test undo functionality")
            print("7. 📊 View system statistics")
            print("8. 🧪 Test all features automatically")
            print("9. ❌ Exit")
            print()
            
            choice = input("Choose a test (1-9): ").strip()
            
            if choice == "1":
                test_basic_features(listener)
            elif choice == "2":
                test_confidence_threshold(listener)
            elif choice == "3":
                test_custom_wake_word(listener)
            elif choice == "4":
                list_custom_wake_words(listener)
            elif choice == "5":
                test_full_interaction(listener)
            elif choice == "6":
                test_undo_functionality(listener)
            elif choice == "7":
                show_statistics(listener)
            elif choice == "8":
                test_all_features(listener)
            elif choice == "9":
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
        
        print("\n🎉 Enhanced Maya testing complete!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Install required dependencies:")
        print("pip install noisereduce colorama")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            listener.cleanup()
        except:
            pass
    
    return True


def test_basic_features(listener):
    """Test basic microphone and Whisper functionality"""
    print("\n🎤 Testing Basic Features")
    print("-" * 30)
    
    # Test microphone
    print("1. Testing microphone access...")
    if listener.test_microphone():
        print("   ✅ Microphone working!")
    else:
        print("   ❌ Microphone failed!")
        return
    
    # Test Whisper recognition
    print("\n2. Testing Whisper recognition...")
    if listener.test_whisper_recognition():
        print("   ✅ Whisper recognition working!")
    else:
        print("   ❌ Whisper recognition failed!")
        return
    
    print("\n✅ Basic features test complete!")


def test_confidence_threshold(listener):
    """Demonstrate confidence threshold filtering"""
    print("\n🧠 Confidence Threshold Test")
    print("-" * 30)
    print(f"Current threshold: {listener.confidence_threshold*100:.0f}%")
    print()
    
    print("This test demonstrates how Maya filters out low-confidence speech:")
    print("1. First, speak CLEARLY and LOUDLY")
    print("2. Then, speak quietly or mumble")
    print("3. Compare the confidence scores")
    print()
    
    # Test 1: Clear speech
    input("Press ENTER for Test 1 - Speak CLEARLY and LOUDLY...")
    print("🎤 Speak clearly now (3 seconds):")
    audio_data, success = listener._record_audio(duration=3)
    if success:
        text, confidence = listener._transcribe_audio(audio_data)
        meets_threshold = confidence >= listener.confidence_threshold
        status = "✅ ACCEPTED" if meets_threshold else "❌ REJECTED"
        print(f"   Result: '{text}'")
        print(f"   Confidence: {confidence*100:.1f}% - {status}")
    
    print()
    
    # Test 2: Unclear speech
    input("Press ENTER for Test 2 - Speak quietly or mumble...")
    print("🎤 Speak quietly/mumble now (3 seconds):")
    audio_data, success = listener._record_audio(duration=3)
    if success:
        text, confidence = listener._transcribe_audio(audio_data)
        meets_threshold = confidence >= listener.confidence_threshold
        status = "✅ ACCEPTED" if meets_threshold else "❌ REJECTED"
        print(f"   Result: '{text}'")
        print(f"   Confidence: {confidence*100:.1f}% - {status}")
    
    print(f"\n💡 Only commands above {listener.confidence_threshold*100:.0f}% confidence are processed!")
    print("   This prevents false triggers from unclear speech.")


def test_custom_wake_word(listener):
    """Test custom wake word training"""
    print("\n🎓 Custom Wake Word Training")
    print("-" * 30)
    
    name = input("Enter a name for your custom wake word (e.g., 'Hey Computer'): ").strip()
    if not name:
        print("❌ No name provided.")
        return
    
    print(f"\nTraining wake word: '{name}'")
    print("You'll record 5 samples. Speak consistently each time.")
    
    success = listener.train_custom_wake_word(name, num_samples=5)
    
    if success:
        print(f"\n✅ Custom wake word '{name}' trained successfully!")
        print("It will now be recognized alongside 'Hey Maya'")
    else:
        print(f"\n❌ Training failed for '{name}'")


def list_custom_wake_words(listener):
    """List all trained custom wake words"""
    print("\n📋 Custom Wake Words")
    print("-" * 30)
    listener.list_custom_wake_words()


def test_full_interaction(listener):
    """Test full voice interaction with enhanced features"""
    print("\n🔊 Full Voice Interaction Test")
    print("-" * 30)
    print("This tests the complete voice interaction cycle with all enhancements:")
    print("• Visual feedback")
    print("• Confidence filtering")
    print("• Noise reduction")
    print("• Wake word detection")
    print("• Command processing")
    print()
    
    print(f"Say: '{listener.wake_word}' followed by any command")
    print("Watch for colorized visual feedback!")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        command = listener.listen_once()
        
        if command:
            print("\n🎉 Command captured!")
            print(f"   Text: {command['raw_text']}")
            print(f"   Confidence: {command['confidence']*100:.1f}%")
            print(f"   Meets Threshold: {command.get('meets_threshold', False)}")
            print(f"   Noise Reduction: {command.get('noise_reduction', False)}")
        else:
            print("\n❌ No wake word detected")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test stopped by user")


def test_undo_functionality(listener):
    """Test undo functionality"""
    print("\n↩️  Undo Functionality Test")
    print("-" * 30)
    
    # Check command history
    history = listener.get_command_history(5)
    if not history:
        print("No command history yet. Let's create some commands first!")
        print()
        
        # Create some test commands
        for i in range(2):
            print(f"Command {i+1}: Say '{listener.wake_word}' followed by any command")
            command = listener.listen_once()
            if command and command.get('meets_threshold', False):
                print(f"   ✅ Command recorded: '{command['raw_text']}'")
            else:
                print("   ❌ Command not recorded (low confidence or no speech)")
            print()
    
    # Show recent commands
    history = listener.get_command_history(5)
    if history:
        print("Recent commands:")
        for i, cmd in enumerate(reversed(history), 1):
            status = "✅" if cmd.get('meets_threshold', False) else "❌"
            undone = " (UNDONE)" if cmd.get('undone', False) else ""
            print(f"   {i}. {status} '{cmd['raw_text']}' ({cmd['confidence']*100:.0f}%){undone}")
    
    print()
    print("Now test undo functionality:")
    print(f"Say: '{listener.wake_word}' followed by 'undo last command'")
    
    try:
        command = listener.listen_once()
        
        if command and 'undo' in command.get('raw_text', '').lower():
            if 'undo_result' in command:
                undone_cmd = command['undo_result']
                if undone_cmd:
                    print(f"\n✅ Undid command: '{undone_cmd['raw_text']}'")
                else:
                    print("\n❌ No commands to undo")
            else:
                print("\n❌ Undo not processed")
        else:
            print("\n❌ Undo command not detected")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test stopped by user")


def show_statistics(listener):
    """Show system statistics"""
    print("\n📊 System Statistics")
    print("-" * 30)
    
    stats = listener.get_statistics()
    
    print(f"Commands processed: {stats['total_commands']}")
    print(f"Successful commands: {stats['successful_commands']}")
    print(f"Success rate: {stats['success_rate']:.1f}%")
    print(f"False triggers: {stats['false_triggers']}")
    print(f"False trigger rate: {stats['false_trigger_rate']:.1f}%")
    print(f"Custom wake words: {stats['custom_wake_words']}")
    print(f"Confidence threshold: {stats['confidence_threshold']*100:.0f}%")
    print(f"Noise reduction: {'Enabled' if stats['noise_reduction_enabled'] else 'Disabled'}")
    
    # Show recent commands
    history = listener.get_command_history(5)
    if history:
        print("\nRecent commands:")
        for cmd in reversed(history):
            status = "✅" if cmd.get('meets_threshold', False) else "❌"
            undone = " (UNDONE)" if cmd.get('undone', False) else ""
            print(f"   {status} '{cmd['raw_text']}' ({cmd['confidence']*100:.0f}%){undone}")


def test_all_features(listener):
    """Run all feature tests automatically"""
    print("\n🧪 Automated Feature Testing")
    print("-" * 30)
    
    print("Running comprehensive feature tests...")
    success = listener.test_all_features()
    
    if success:
        print("\n✅ All feature tests passed!")
    else:
        print("\n❌ Some tests failed. Check the output above.")
    
    return success


def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking Enhanced Maya Dependencies...")
    
    required_packages = [
        ("noisereduce", "Noise cancellation"),
        ("colorama", "Visual feedback"),
        ("whisper", "OpenAI Whisper"),
        ("pyaudio", "Audio input"),
        ("numpy", "Audio processing")
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description} (MISSING)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✅ All dependencies satisfied!")
    return True


if __name__ == "__main__":
    print("🔥 Enhanced Maya Voice System")
    print("Step 1 Extra Features Test Suite")
    print("="*50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        sys.exit(1)
    
    print()
    
    # Run the main test
    try:
        success = test_enhanced_maya()
        if success:
            print("\n🎉 Enhanced Maya testing completed successfully!")
        else:
            print("\n❌ Enhanced Maya testing failed.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
