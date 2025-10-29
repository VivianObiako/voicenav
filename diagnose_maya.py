#!/usr/bin/env python3
"""
Maya Voice System Diagnosis Tool
Helps identify and fix recognition issues
"""

import sys
sys.path.append('src')

def diagnose_maya_issues():
    """Diagnose and fix Maya voice recognition issues"""
    print("🔍 Maya Voice System Diagnosis")
    print("="*50)
    
    # Check dependencies
    print("\n1. 📦 Checking Dependencies...")
    try:
        import whisper
        print("   ✅ Whisper available")
    except ImportError:
        print("   ❌ Whisper missing - run: pip install openai-whisper")
        return
    
    try:
        import noisereduce
        print("   ✅ Noise reduction available")
    except ImportError:
        print("   ⚠️  Noise reduction missing - run: pip install noisereduce")
    
    try:
        import colorama
        print("   ✅ Visual feedback available")
    except ImportError:
        print("   ⚠️  Visual feedback missing - run: pip install colorama")
    
    # Test different confidence thresholds
    print("\n2. 🎯 Testing Confidence Thresholds...")
    from input.enhanced_voice_listener import EnhancedVoiceListener
    
    thresholds = [0.3, 0.5, 0.8]  # Test low, medium, high
    
    for threshold in thresholds:
        print(f"\n   Testing {threshold*100:.0f}% confidence threshold:")
        print(f"   Say 'Hey Maya test' clearly...")
        
        try:
            listener = EnhancedVoiceListener(
                confidence_threshold=threshold,
                noise_reduction=False  # Disable to see raw performance
            )
            
            # Just record and test recognition without wake word filtering
            print("   🎤 Recording (3 seconds)...")
            audio_data, success = listener._record_audio(duration=3, show_progress=False)
            
            if success:
                text, confidence = listener._transcribe_audio(audio_data)
                meets_threshold = confidence >= threshold
                status = "✅ PASS" if meets_threshold else "❌ FAIL"
                
                print(f"   {status} Got: '{text}' (confidence: {confidence*100:.0f}%)")
                
                if "maya" in text.lower():
                    print(f"   🎉 Maya detected in speech!")
                
                if confidence >= 0.8:
                    print(f"   🏆 Excellent! This confidence level works well.")
                    listener.cleanup()
                    return True
                    
            listener.cleanup()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Environment testing
    print("\n3. 🌍 Environment Testing...")
    print("   Let's test different speaking conditions:")
    
    conditions = [
        ("Very close to microphone (6 inches)", "Speak very close to your microphone"),
        ("Normal distance (12 inches)", "Speak at normal distance"),
        ("Loud and clear", "Speak LOUDLY and CLEARLY"),
        ("Slower speech", "Speak very SLOWLY: Hey... Maya... test...")
    ]
    
    best_confidence = 0
    best_condition = None
    
    for condition_name, instruction in conditions:
        print(f"\n   📍 {condition_name}")
        print(f"      {instruction}")
        input("      Press ENTER when ready...")
        
        try:
            listener = EnhancedVoiceListener(confidence_threshold=0.1)  # Very low threshold
            
            audio_data, success = listener._record_audio(duration=3, show_progress=False)
            if success:
                text, confidence = listener._transcribe_audio(audio_data)
                print(f"      Result: '{text}' (confidence: {confidence*100:.0f}%)")
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_condition = condition_name
                    
            listener.cleanup()
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    # Recommendations
    print(f"\n4. 💡 Recommendations:")
    if best_confidence > 0.7:
        print(f"   ✅ Best condition: {best_condition} ({best_confidence*100:.0f}% confidence)")
        print(f"   🎯 Use confidence threshold: 70-80%")
    elif best_confidence > 0.5:
        print(f"   ⚠️  Best condition: {best_condition} ({best_confidence*100:.0f}% confidence)")
        print(f"   🎯 Use confidence threshold: 50%")
        print(f"   💡 Try:")
        print(f"      - Speak closer to microphone")
        print(f"      - Speak louder and clearer")
        print(f"      - Reduce background noise")
    else:
        print(f"   ❌ Low confidence across all conditions (best: {best_confidence*100:.0f}%)")
        print(f"   🔧 Troubleshooting needed:")
        print(f"      - Check microphone is working in System Settings")
        print(f"      - Try external microphone")
        print(f"      - Check background noise levels")
        print(f"      - Verify microphone permissions")
    
    # Quick fix suggestion
    print(f"\n5. 🚀 Quick Fix for Testing:")
    if best_confidence < 0.8:
        suggested_threshold = max(0.3, best_confidence * 0.8)  # 80% of best performance
        print(f"   Try lowering confidence threshold to {suggested_threshold*100:.0f}%:")
        print(f"   ")
        print(f"   from src.input.enhanced_voice_listener import EnhancedVoiceListener")
        print(f"   listener = EnhancedVoiceListener(confidence_threshold={suggested_threshold:.1f})")
        print(f"   listener.listen_once()")


def test_microphone_levels():
    """Test microphone input levels"""
    print("\n🎤 Microphone Level Test")
    print("-" * 30)
    
    try:
        import pyaudio
        import numpy as np
        
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("Speak normally for 5 seconds...")
        print("Watch the volume levels:")
        
        max_level = 0
        for i in range(50):  # 5 seconds worth
            data = stream.read(1024, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            level = np.abs(audio_data).mean()
            max_level = max(max_level, level)
            
            # Visual level indicator
            bar_length = min(50, int(level / 100))
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"\r   {bar} {level:4.0f}", end="", flush=True)
        
        stream.close()
        audio.terminate()
        
        print(f"\n\n📊 Results:")
        if max_level > 1000:
            print(f"   ✅ Good microphone levels (max: {max_level:.0f})")
        elif max_level > 300:
            print(f"   ⚠️  Low microphone levels (max: {max_level:.0f})")
            print(f"      Try speaking louder or closer to microphone")
        else:
            print(f"   ❌ Very low microphone levels (max: {max_level:.0f})")
            print(f"      Check microphone is working and not muted")
            
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")


def create_optimized_listener():
    """Create an optimized listener based on your environment"""
    print("\n🔧 Creating Optimized Maya Listener")
    print("-" * 40)
    
    # Test quick recognition
    print("Quick test - say 'Maya test' when ready:")
    input("Press ENTER...")
    
    try:
        from input.enhanced_voice_listener import EnhancedVoiceListener
        
        # Test with very permissive settings
        test_listener = EnhancedVoiceListener(confidence_threshold=0.1)
        audio_data, success = test_listener._record_audio(duration=3, show_progress=True)
        
        if success:
            text, confidence = test_listener._transcribe_audio(audio_data)
            print(f"Got: '{text}' (confidence: {confidence*100:.0f}%)")
            
            # Determine optimal settings
            if confidence >= 0.8:
                optimal_threshold = 0.8
                print("🏆 Excellent recognition! Using high confidence threshold.")
            elif confidence >= 0.6:
                optimal_threshold = 0.6
                print("✅ Good recognition! Using medium confidence threshold.")
            elif confidence >= 0.4:
                optimal_threshold = 0.4
                print("⚠️  Moderate recognition. Using low confidence threshold.")
            else:
                optimal_threshold = 0.3
                print("🔧 Low recognition. Using very low confidence threshold.")
            
            test_listener.cleanup()
            
            # Create optimized listener
            print(f"\n🎯 Creating optimized listener (threshold: {optimal_threshold*100:.0f}%)...")
            
            optimized = EnhancedVoiceListener(
                confidence_threshold=optimal_threshold,
                noise_reduction=True,
                wake_word="hey maya"
            )
            
            print("🎤 Test the optimized listener - say 'Hey Maya test command':")
            result = optimized.listen_once()
            
            if result:
                print(f"\n✅ Success! Maya recognized:")
                print(f"   Text: {result['raw_text']}")
                print(f"   Confidence: {result['confidence']*100:.0f}%")
                print(f"   Meets threshold: {result.get('meets_threshold', False)}")
            else:
                print("\n❌ Still not working. Try manual troubleshooting.")
            
            optimized.cleanup()
            
        else:
            print("❌ Recording failed. Check microphone setup.")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Maya Voice System Diagnosis & Fix Tool")
    print("="*50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. 🔍 Full diagnosis")
        print("2. 🎤 Test microphone levels")
        print("3. 🔧 Create optimized listener")
        print("4. ❌ Exit")
        
        choice = input("\nChoose (1-4): ").strip()
        
        if choice == "1":
            diagnose_maya_issues()
        elif choice == "2":
            test_microphone_levels()
        elif choice == "3":
            create_optimized_listener()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please select 1-4.")
    
    print("\n👋 Diagnosis complete!")
