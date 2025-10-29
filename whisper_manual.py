#!/usr/bin/env python3
"""
Manual Whisper test - you control when to record
"""

import whisper
import pyaudio
import wave
import tempfile
import os

print("🎤 Manual Whisper Test")
print("=" * 40)
print("YOU control when to record!")
print("Press ENTER to start recording, ENTER again to stop")
print("Type 'quit' to exit")
print()

# Load Whisper model
print("🧠 Loading Whisper model...")
model = whisper.load_model("base")
print("✅ Whisper ready!")
print()

# Audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Initialize PyAudio
audio = pyaudio.PyAudio()

count = 0
try:
    while True:
        count += 1
        
        # Wait for user
        user_input = input(f"\n[{count:03d}] Press ENTER to start recording (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
            
        print(f"[{count:03d}] 🎙️ RECORDING... Press ENTER to stop")
        
        # Start recording
        stream = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
        
        frames = []
        
        # Record until user presses enter
        import threading
        import sys
        
        recording = True
        
        def stop_recording():
            global recording
            input()  # Wait for Enter
            recording = False
        
        # Start the stop thread
        stop_thread = threading.Thread(target=stop_recording)
        stop_thread.daemon = True
        stop_thread.start()
        
        # Record audio
        while recording:
            try:
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            except:
                break
        
        stream.stop_stream()
        stream.close()
        
        print(f"[{count:03d}] ⏹️ Recording stopped. Processing...")
        
        if frames:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                wf = wave.open(temp_file.name, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                # Process with Whisper
                print(f"[{count:03d}] 🧠 Whisper analyzing...")
                result = model.transcribe(temp_file.name)
                text = result["text"].strip().lower()
                
                # Clean up temp file
                os.unlink(temp_file.name)
            
            # Show results
            if text:
                print(f"[{count:03d}] 🎤 HEARD: '{text}'")
                
                # Check for wake word (multiple variations)
                wake_words = ['hey voicenav', 'hey voice nav', 'a voicenav', 'hey voice now']
                if any(wake in text for wake in wake_words):
                    print(f"[{count:03d}] ✅ WAKE WORD DETECTED!")
                    print("     🔊 *BEEP* - This would activate VoiceNav!")
                
                # Check for other keywords
                if any(word in text for word in ['hello', 'computer', 'assistant', 'system']):
                    print(f"[{count:03d}] 💬 Common activation word detected")
                    
            else:
                print(f"[{count:03d}] 🔇 No speech detected")
        else:
            print(f"[{count:03d}] ❌ No audio recorded")

except KeyboardInterrupt:
    print("\n🛑 Stopping...")

finally:
    audio.terminate()
    print("✅ Manual test complete!")
    print(f"Total recordings: {count-1}")
    print("\n💡 Tips for next recording:")
    print("- Speak clearly and at normal volume")
    print("- Try: 'Hey VoiceNav'")
    print("- Try: 'Hello computer'")
    print("- Try: 'Wake up system'")
