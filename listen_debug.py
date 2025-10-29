#!/usr/bin/env python3
"""
Simple script to log what speech recognition is hearing
"""

import speech_recognition as sr
import time

print("🎤 Speech Recognition Debug - What Am I Hearing?")
print("=" * 60)
print("This will show everything the system recognizes.")
print("Speak normally and see what appears.")
print("Press Ctrl+C to stop when you're done.")
print()

# Setup speech recognition with same settings as VoiceNav
recognizer = sr.Recognizer()
recognizer.energy_threshold = 1000  # Same as VoiceNav
recognizer.pause_threshold = 0.5
recognizer.phrase_threshold = 0.2

microphone = sr.Microphone()

# Adjust for ambient noise
print("🔧 Setting up microphone...")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
print(f"✅ Ready! Energy threshold: {recognizer.energy_threshold}")
print()

print("🎤 LISTENING - Start talking:")
print("-" * 40)

count = 0
try:
    while True:
        count += 1
        try:
            # Listen for audio
            with microphone as source:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
            
            # Try to recognize speech
            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"[{count:03d}] 🎤 HEARD: '{text}'")
                
                # Highlight wake word
                if 'hey voicenav' in text or 'hey voice nav' in text:
                    print(f"[{count:03d}] ✅ WAKE WORD DETECTED!")
                    
            except sr.UnknownValueError:
                print(f"[{count:03d}] 🔇 (unintelligible audio)")
            except sr.RequestError as e:
                print(f"[{count:03d}] ❌ Network error: {e}")
                
        except sr.WaitTimeoutError:
            print(f"[{count:03d}] ⏰ (silence)")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n")
    print("=" * 40)
    print("✅ Debug session complete!")
    print(f"Total audio attempts: {count}")
