#!/usr/bin/env python3
"""
Test different wake words to find the easiest one for your voice
"""

import whisper
import pyaudio
import wave
import tempfile
import os

print("🎤 Wake Word Testing - Find Your Best Option")
print("=" * 60)
print("We'll test different wake words to find what works best")
print("for your voice and accent.")
print()

# Suggested wake words (easy to recognize)
wake_words = [
    "hey computer",      # Very common, easy to recognize
    "hello browser",     # Clear, browser-related
    "web control",       # Simple, relevant
    "browser help",      # Natural phrase
    "start browsing",    # Clear command
    "hey assistant",     # Common AI phrase
    "computer browser",  # Clear compound word
    "web assistant"      # Easy to say
]

print("🧠 Loading Whisper...")
model = whisper.load_model("base")
print("✅ Ready!")
print()

print("📝 SUGGESTED WAKE WORDS:")
for i, word in enumerate(wake_words, 1):
    print(f"   {i}. '{word}'")
print()

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
audio = pyaudio.PyAudio()

results = {}

try:
    for i, wake_word in enumerate(wake_words, 1):
        print(f"\n🧪 TEST {i}/8: '{wake_word}'")
        print("-" * 40)
        
        input(f"Press ENTER to start recording '{wake_word}'...")
        print(f"🎙️ RECORDING... Say: '{wake_word}' then press ENTER")
        
        # Record
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                          input=True, frames_per_buffer=CHUNK)
        frames = []
        
        # Simple recording with timeout
        import threading
        recording = True
        def stop():
            global recording
            input()
            recording = False
        
        stop_thread = threading.Thread(target=stop)
        stop_thread.daemon = True
        stop_thread.start()
        
        while recording:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except:
                break
        
        stream.stop_stream()
        stream.close()
        
        # Process
        if frames:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                wf = wave.open(temp_file.name, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                print("🧠 Processing...")
                result = model.transcribe(temp_file.name)
                text = result["text"].strip().lower()
                os.unlink(temp_file.name)
            
            print(f"✅ Whisper heard: '{text}'")
            
            # Check accuracy
            wake_word_clean = wake_word.lower()
            if wake_word_clean in text:
                print(f"🎉 PERFECT MATCH!")
                results[wake_word] = "PERFECT"
            elif any(word in text for word in wake_word_clean.split()):
                print(f"✅ PARTIAL MATCH (some words recognized)")
                results[wake_word] = "PARTIAL"
            else:
                print(f"❌ NO MATCH")
                results[wake_word] = "NO MATCH"
        else:
            print("❌ No audio recorded")
            results[wake_word] = "NO AUDIO"

except KeyboardInterrupt:
    print("\n🛑 Stopping early...")

finally:
    audio.terminate()

# Show final results
print("\n" + "=" * 60)
print("📊 WAKE WORD TEST RESULTS")
print("=" * 60)

perfect = []
partial = []
failed = []

for wake_word, result in results.items():
    if result == "PERFECT":
        perfect.append(wake_word)
        print(f"🎉 PERFECT: '{wake_word}'")
    elif result == "PARTIAL":
        partial.append(wake_word)
        print(f"✅ PARTIAL: '{wake_word}'")
    else:
        failed.append(wake_word)
        print(f"❌ FAILED:  '{wake_word}'")

print("\n🏆 RECOMMENDATIONS:")
if perfect:
    print(f"✅ BEST OPTIONS (perfect recognition):")
    for word in perfect:
        print(f"   • '{word}'")
elif partial:
    print(f"⚡ GOOD OPTIONS (partial recognition):")
    for word in partial:
        print(f"   • '{word}'")
else:
    print("🔄 Consider trying:")
    print("   • 'hey computer' (most common)")
    print("   • 'hello browser' (simple)")
    print("   • Speak louder and clearer")

print("\n💡 NEXT STEP:")
print("Choose your best wake word and I'll update VoiceNav to use it!")
