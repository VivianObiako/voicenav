#!/usr/bin/env python3
"""
Test assistant names that work well with different accents
Focus on phonetically simple names
"""

import whisper
import pyaudio
import wave
import tempfile
import os

print("🎤 Assistant Name Testing - Accent-Friendly Options")
print("=" * 65)
print("Testing simple, phonetically clear assistant names")
print("that work well across different accents and languages.")
print()

# Assistant names optimized for accent tolerance
assistant_names = [
    # Simple vowel-consonant patterns
    "hey alex",        # Short, clear consonants
    "hey maya",        # Simple vowels, no difficult sounds
    "hey nova",        # Clear 'o' and 'a' sounds
    "hey luna",        # Soft sounds, easy to pronounce
    "hey aria",        # Open vowels, flows well
    
    # Single syllable options
    "hey max",         # Very short, hard consonants
    "hey kai",         # Simple, international sound
    "hey lee",         # Minimal, clear
    
    # Technology-inspired but simple
    "hey neo",         # Simple, modern
    "hey pixel",       # Tech-related, clear sounds
    "hey echo",        # Audio-related, simple
    "hey sage",        # Wisdom-related, soft sounds
    
    # Nature-inspired (often work across cultures)
    "hey river",       # Flowing, natural
    "hey sky",         # Simple, universal
    "hey ocean",       # Open vowels, peaceful
]

print("🧠 Loading Whisper...")
model = whisper.load_model("base")
print("✅ Ready!")
print()

print("📝 ASSISTANT NAME OPTIONS:")
for i, name in enumerate(assistant_names, 1):
    print(f"   {i:2d}. '{name}'")
print()

print("💡 These names are chosen for:")
print("   • Simple phonetics (easy consonants/vowels)")
print("   • Short length (easier to recognize)")
print("   • Common sounds across languages")
print("   • No complex letter combinations")
print()

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
audio = pyaudio.PyAudio()

results = {}

try:
    for i, name in enumerate(assistant_names, 1):
        print(f"\n🧪 TEST {i}/{len(assistant_names)}: '{name}'")
        print("-" * 50)
        
        input(f"Press ENTER to test '{name}'...")
        print(f"🎙️ RECORDING... Say: '{name}' clearly, then press ENTER")
        
        # Record
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                          input=True, frames_per_buffer=CHUNK)
        frames = []
        
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
                
                print("🧠 Whisper processing...")
                result = model.transcribe(temp_file.name)
                text = result["text"].strip().lower()
                os.unlink(temp_file.name)
            
            print(f"✅ Whisper heard: '{text}'")
            
            # Check accuracy
            name_clean = name.lower()
            name_words = name_clean.split()
            
            if name_clean in text:
                print(f"🎉 PERFECT MATCH!")
                results[name] = "PERFECT"
            elif all(word in text for word in name_words):
                print(f"✅ ALL WORDS RECOGNIZED!")
                results[name] = "ALL_WORDS"
            elif any(word in text for word in name_words):
                print(f"⚡ PARTIAL RECOGNITION")
                results[name] = "PARTIAL"
            else:
                print(f"❌ NOT RECOGNIZED")
                results[name] = "FAILED"
        else:
            print("❌ No audio recorded")
            results[name] = "NO_AUDIO"
        
        # Quick feedback
        if name in results and results[name] in ["PERFECT", "ALL_WORDS"]:
            print(f"   👍 '{name}' works well with your voice!")

except KeyboardInterrupt:
    print("\n🛑 Stopping test...")

finally:
    audio.terminate()

# Analyze results
print("\n" + "=" * 65)
print("📊 ASSISTANT NAME TEST RESULTS")
print("=" * 65)

perfect = []
good = []
partial = []
failed = []

for name, result in results.items():
    if result == "PERFECT":
        perfect.append(name)
        print(f"🎉 PERFECT:     '{name}' - Exact match!")
    elif result == "ALL_WORDS":
        good.append(name)
        print(f"✅ EXCELLENT:   '{name}' - All words recognized!")
    elif result == "PARTIAL":
        partial.append(name)
        print(f"⚡ PARTIAL:     '{name}' - Some recognition")
    else:
        failed.append(name)
        print(f"❌ FAILED:      '{name}' - Not recognized")

print("\n🏆 RECOMMENDATIONS:")

if perfect:
    print(f"🥇 TOP CHOICE (perfect recognition):")
    for name in perfect[:3]:  # Show top 3
        print(f"   • '{name}' - Use this one!")
        
if good:
    print(f"\n🥈 EXCELLENT OPTIONS (all words recognized):")
    for name in good[:3]:  # Show top 3
        print(f"   • '{name}' - Very reliable")

if perfect or good:
    best_name = perfect[0] if perfect else good[0]
    print(f"\n🎯 RECOMMENDED CHOICE: '{best_name}'")
    print(f"   This name works best with your voice!")
    print(f"   I can update VoiceNav to use '{best_name}' as the wake word.")
else:
    print(f"\n🔄 If none worked well, try:")
    print(f"   • Speaking louder and clearer")
    print(f"   • Testing 'hey alex' and 'hey max' (simplest)")
    print(f"   • Using a custom name you suggest")

print(f"\n💡 NEXT STEP:")
print(f"Tell me which name you prefer, and I'll update VoiceNav!")
print(f"Your assistant will respond to: '[chosen name]'")
