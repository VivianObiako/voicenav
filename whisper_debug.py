#!/usr/bin/env python3
"""
Whisper-powered speech recognition debug
Much more accurate than Google Speech API
"""

import whisper
import pyaudio
import wave
import tempfile
import os
import time

print("🎤 Whisper Speech Recognition Debug")
print("=" * 50)
print("Using OpenAI Whisper (offline, much more accurate)")
print("Press Ctrl+C to stop")
print()

# Load Whisper model (small model for speed)
print("🧠 Loading Whisper model...")
model = whisper.load_model("base")  # Good balance of speed/accuracy
print("✅ Whisper model loaded!")
print()

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper prefers 16kHz
RECORD_SECONDS = 3  # Record 3-second chunks

# Initialize PyAudio
audio = pyaudio.PyAudio()

print("🎤 LISTENING - Whisper will analyze 3-second chunks:")
print("-" * 50)

count = 0
try:
    while True:
        count += 1
        
        # Record audio chunk
        print(f"[{count:03d}] 🎙️ Recording 3 seconds...")
        
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            wf = wave.open(temp_file.name, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            # Process with Whisper
            print(f"[{count:03d}] 🧠 Processing with Whisper...")
            result = model.transcribe(temp_file.name)
            text = result["text"].strip().lower()
            
            # Clean up temp file
            os.unlink(temp_file.name)
        
        # Show results
        if text:
            print(f"[{count:03d}] 🎤 HEARD: '{text}'")
            
            # Check for wake word
            if 'hey voicenav' in text or 'hey voice nav' in text:
                print(f"[{count:03d}] ✅ WAKE WORD DETECTED!")
                print("     🔊 *BEEP* - This would trigger command mode!")
            
            # Check for other keywords
            if any(word in text for word in ['hello', 'computer', 'assistant']):
                print(f"[{count:03d}] 💬 Common greeting detected")
                
        else:
            print(f"[{count:03d}] 🔇 (silence or no speech)")
        
        print()

except KeyboardInterrupt:
    print("\n🛑 Stopping Whisper debug...")
    audio.terminate()
    print("✅ Whisper debug complete!")
    print(f"Total chunks processed: {count}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    audio.terminate()
