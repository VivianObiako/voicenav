#!/usr/bin/env python3
"""
Simple test to see if speech recognition works AT ALL
Tests multiple approaches to find what works
"""

import speech_recognition as sr
import time

print("🎤 Simple Speech Recognition Test")
print("=" * 50)
print("Testing different approaches to find what works...")
print()

# Initialize
recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("🔧 Testing microphone setup...")
try:
    with microphone as source:
        print("Adjusting for ambient noise... (3 seconds)")
        recognizer.adjust_for_ambient_noise(source, duration=3)
    print(f"✅ Microphone OK. Energy threshold: {recognizer.energy_threshold}")
except Exception as e:
    print(f"❌ Microphone failed: {e}")
    exit(1)

print()
print("🧪 TEST 1: Single word recognition")
print("Say a SINGLE WORD clearly (like 'hello' or 'test')")
print("You have 5 seconds...")

try:
    with microphone as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
    
    print("Processing...")
    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ SUCCESS! Heard: '{text}'")
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")
        
except sr.WaitTimeoutError:
    print("❌ No speech detected")

print()
print("🧪 TEST 2: Wake word test")
print("Say 'Hey VoiceNav' clearly")
print("You have 5 seconds...")

try:
    with microphone as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
    
    print("Processing...")
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"✅ Heard: '{text}'")
        
        if 'hey' in text and ('voicenav' in text or 'voice nav' in text):
            print("🎉 WAKE WORD DETECTED!")
        else:
            print("❌ Wake word not detected")
            
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")
        
except sr.WaitTimeoutError:
    print("❌ No speech detected")

print()
print("🧪 TEST 3: Loud and clear test")
print("Speak LOUDLY and CLEARLY: 'COMPUTER'")
print("You have 5 seconds...")

try:
    with microphone as source:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=2)
    
    print("Processing...")
    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"✅ Heard: '{text}'")
        
        if 'computer' in text:
            print("🎉 LOUD SPEECH DETECTED!")
        else:
            print("ℹ️ Different word detected")
            
    except sr.UnknownValueError:
        print("❌ Could not understand audio")
    except sr.RequestError as e:
        print(f"❌ Google API error: {e}")
        
except sr.WaitTimeoutError:
    print("❌ No speech detected")

print()
print("📊 SUMMARY:")
print("If ANY test worked, speech recognition is functional.")
print("If ALL tests failed, we need to:")
print("1. Check internet connection")
print("2. Try different microphone settings")
print("3. Use a different recognition engine")
