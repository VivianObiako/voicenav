"""
VoiceNav Whisper Voice Listener Module
High-accuracy voice detection using OpenAI Whisper
"""

import whisper
import pyaudio
import wave
import tempfile
import os
import time
import threading
from datetime import datetime
import sys
import warnings

# Suppress Whisper FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU.*")

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("whisper_voice_listener")


class WhisperVoiceListener:
    """
    Whisper-powered voice listening system for VoiceNav
    
    Features:
    - High-accuracy offline speech recognition using OpenAI Whisper
    - Wake word detection ("hey maya") 
    - Command capture with configurable timeout
    - Audio feedback and text-to-speech
    - Error handling and robust microphone management
    """
    
    def __init__(self, wake_word="hey maya", command_timeout=5, model_size="base"):
        """
        Initialize the Whisper voice listener
        
        Args:
            wake_word (str): The wake word to listen for
            command_timeout (int): Seconds to wait for command after wake word
            model_size (str): Whisper model size (tiny, base, small, medium, large)
        """
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
        self.model_size = model_size
        self.is_listening = False
        self.whisper_model = None
        self.audio_interface = None
        self.tts_engine = None
        
        # Audio settings optimized for Whisper
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # Whisper's preferred sample rate
        
        # Initialize components
        self._setup_whisper()
        self._setup_audio()
        self._setup_tts()
        
        logger.info(f"WhisperVoiceListener initialized with wake word: '{wake_word}'")
    
    def _setup_whisper(self):
        """Setup Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            print(f"🧠 Loading Whisper {self.model_size} model...")
            self.whisper_model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
            print("✅ Whisper model ready!")
        except Exception as e:
            error_msg = f"Whisper setup failed: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _setup_audio(self):
        """Setup PyAudio interface"""
        try:
            self.audio_interface = pyaudio.PyAudio()
            logger.info("Audio interface initialized")
            
            # Test microphone access
            self._test_microphone_access()
            
        except Exception as e:
            error_msg = f"Audio setup failed: {e}"
            logger.error(error_msg)
            self._print_microphone_error()
            raise RuntimeError(error_msg)
    
    def _setup_tts(self):
        """Setup text-to-speech engine"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            # Set speaking rate (words per minute)
            self.tts_engine.setProperty('rate', 150)
            # Set volume (0.0 to 1.0)
            self.tts_engine.setProperty('volume', 0.8)
            logger.info("Text-to-speech engine initialized")
            
        except Exception as e:
            logger.error(f"TTS setup failed: {e}")
            self.tts_engine = None
    
    def _test_microphone_access(self):
        """Test microphone availability and permissions"""
        try:
            # Try to open microphone briefly
            stream = self.audio_interface.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            stream.close()
            logger.info("Microphone access confirmed")
            
        except Exception as e:
            logger.error(f"Microphone access failed: {e}")
            raise e
    
    def _print_microphone_error(self):
        """Print helpful error message for microphone issues"""
        print("\n" + "="*60)
        print("🎤 MICROPHONE ACCESS ERROR")
        print("="*60)
        print("VoiceNav with Whisper needs microphone access.")
        print("\n🔧 PERMISSION DIALOG SOLUTION:")
        print("If you see a dialog asking 'Terminal would like to access")
        print("the Microphone' → Click 'Allow'")
        print("\n🔧 MANUAL PERMISSION SETUP:")
        print("1. Open System Settings/Preferences")
        print("2. Go to Privacy & Security → Microphone")
        print("3. Add Terminal (and your IDE) to allowed apps")
        print("4. Restart your terminal/IDE")
        print("5. Try running the test again")
        print("\n🎯 NEXT STEP:")
        print("After granting permission, test with: python3 test_maya.py")
        print("="*60)
    
    def _play_beep(self):
        """Play system beep to indicate wake word detected"""
        try:
            # Play system beep (macOS)
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        except:
            # Fallback: print visual indicator
            print("🔊 *BEEP*")
    
    def _speak(self, text):
        """Use text-to-speech to say something"""
        try:
            # Use macOS built-in 'say' command with Samantha voice
            import subprocess
            logger.info(f"Maya speaking: {text}")
            subprocess.run(['say', '-v', 'Samantha', text], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"macOS say command failed: {e}")
            # Fallback to default voice
            try:
                subprocess.run(['say', text], check=True)
            except:
                print(f"🔊 Maya would say: {text}")
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"🔊 Maya would say: {text}")
    
    def _record_audio(self, duration=3, stop_event=None):
        """
        Record audio for specified duration or until stop event
        
        Args:
            duration (int): Maximum recording duration in seconds
            stop_event (threading.Event): Optional event to stop recording early
            
        Returns:
            str: Path to temporary audio file, or None if failed
        """
        try:
            # Open audio stream
            stream = self.audio_interface.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            frames = []
            start_time = time.time()
            
            # Record audio
            while True:
                # Check duration limit
                if time.time() - start_time >= duration:
                    break
                    
                # Check stop event
                if stop_event and stop_event.is_set():
                    break
                
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    frames.append(data)
                except Exception as e:
                    logger.warning(f"Audio read error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            
            # Save to temporary file
            if frames:
                temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                wf = wave.open(temp_file.name, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio_interface.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                temp_file.close()
                
                return temp_file.name
            
            return None
            
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return None
    
    def _transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_file_path (str): Path to audio file
            
        Returns:
            str: Transcribed text (lowercase)
        """
        try:
            result = self.whisper_model.transcribe(audio_file_path)
            text = result["text"].strip().lower()
            logger.debug(f"Whisper transcription: '{text}'")
            return text
            
        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            return ""
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(audio_file_path):
                    os.unlink(audio_file_path)
            except:
                pass
    
    def _listen_for_wake_word(self):
        """
        Listen for wake word using Whisper
        
        Returns:
            bool: True if wake word detected, False if stopped
        """
        logger.info(f"Listening for wake word: '{self.wake_word}'")
        
        while self.is_listening:
            try:
                # Record 3-second chunks for wake word detection
                print("👂 Listening for Maya...")
                audio_file = self._record_audio(duration=3)
                
                if audio_file:
                    print("🧠 Processing...")
                    text = self._transcribe_audio(audio_file)
                    
                    if text:
                        print(f"🎤 Heard: '{text}'")
                        
                        # Check for wake word (allow variations)
                        wake_variations = [
                            "hey maya", "hey maia", "a maya", "hey maria",
                            "maya", "maia", "maria"
                        ]
                        
                        if any(wake in text for wake in wake_variations):
                            logger.info(f"Wake word detected in: '{text}'")
                            print(f"✅ Maya detected!")
                            return True
                    else:
                        print("🔇 (silence)")
                else:
                    print("❌ Recording failed")
                    time.sleep(0.5)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Wake word listening error: {e}")
                time.sleep(1)
        
        return False
    
    def _listen_for_command(self):
        """
        Listen for command after wake word detection
        
        Returns:
            dict: Command object with timestamp, text, and confidence
        """
        logger.info(f"Listening for command (timeout: {self.command_timeout}s)")
        print(f"🎤 Say your command (you have {self.command_timeout} seconds)...")
        
        try:
            # Record command with timeout
            audio_file = self._record_audio(duration=self.command_timeout)
            
            if audio_file:
                print("🧠 Maya is processing your command...")
                text = self._transcribe_audio(audio_file)
                
                if text:
                    command = {
                        "timestamp": datetime.now().isoformat(),
                        "raw_text": text,
                        "confidence": 0.95  # Whisper is generally high confidence
                    }
                    
                    logger.info(f"Command captured: {command}")
                    return command
                else:
                    return {
                        "timestamp": datetime.now().isoformat(),
                        "raw_text": "No speech detected",
                        "confidence": 0.0
                    }
            else:
                return {
                    "timestamp": datetime.now().isoformat(),
                    "raw_text": "Recording failed",
                    "confidence": 0.0
                }
                
        except Exception as e:
            logger.error(f"Command listening error: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "raw_text": f"Error: {str(e)}",
                "confidence": 0.0
            }
    
    def start_listening(self):
        """Start the voice listening loop"""
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        self.is_listening = True
        logger.info("Voice listening started")
        print("🎤 Maya is listening...")
        print(f"Say: '{self.wake_word}' to activate")
    
    def stop_listening(self):
        """Stop the voice listening loop"""
        self.is_listening = False
        logger.info("Voice listening stopped")
        print("🎤 Maya stopped listening")
    
    def listen_once(self):
        """
        Listen for one wake word + command cycle
        
        Returns:
            dict or None: Command object if successful, None if no wake word
        """
        if not self.is_listening:
            self.start_listening()
        
        try:
            # Listen for wake word
            wake_word_detected = self._listen_for_wake_word()
            
            if wake_word_detected:
                # Play feedback beep
                self._play_beep()
                
                # Announce we're listening
                self._speak("I'm listening")
                print("🎤 Maya heard you! Say your command:")
                
                # Listen for command
                command = self._listen_for_command()
                return command
            
            return None
            
        except KeyboardInterrupt:
            logger.info("Listening interrupted by user")
            self.stop_listening()
            return None
        except Exception as e:
            logger.error(f"Listening error: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "raw_text": f"Error: {str(e)}",
                "confidence": 0.0
            }
    
    def continuous_listen(self, callback=None):
        """
        Continuous listening loop
        
        Args:
            callback (function): Optional function to call with each command
        """
        self.start_listening()
        
        try:
            while self.is_listening:
                command = self.listen_once()
                if command:
                    if callback:
                        callback(command)
                    else:
                        print(f"Maya understood: {command['raw_text']}")
                
                # Small delay to prevent CPU spinning
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Continuous listening stopped by user")
        finally:
            self.stop_listening()
    
    def test_microphone(self):
        """Test microphone setup and permissions"""
        print("🎤 Testing microphone access...")
        
        try:
            self._test_microphone_access()
            print("✅ Microphone test successful!")
            return True
                
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            self._print_microphone_error()
            return False
    
    def test_whisper_recognition(self):
        """Test Whisper speech recognition"""
        print("🧠 Testing Whisper recognition...")
        print("Say something clearly (3 seconds):")
        
        try:
            audio_file = self._record_audio(duration=3)
            if audio_file:
                text = self._transcribe_audio(audio_file)
                if text:
                    print(f"✅ Whisper recognition successful!")
                    print(f"Maya heard: '{text}'")
                    return True
                else:
                    print("❌ No speech detected")
                    return False
            else:
                print("❌ Recording failed")
                return False
                
        except Exception as e:
            print(f"❌ Whisper test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.audio_interface:
                self.audio_interface.terminate()
            logger.info("Resources cleaned up")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


def main():
    """Test the Whisper voice listener directly"""
    print("Maya (Whisper) Voice Listener Test")
    print("="*40)
    
    try:
        # Initialize Whisper voice listener
        listener = WhisperVoiceListener()
        
        # Test microphone
        if not listener.test_microphone():
            return
        
        # Test Whisper recognition
        if not listener.test_whisper_recognition():
            return
        
        print("\n🎤 Starting Maya wake word test...")
        print(f"Say: '{listener.wake_word}' followed by a command")
        print("Press Ctrl+C to stop")
        
        # Test one cycle
        command = listener.listen_once()
        if command:
            print(f"\n✅ Maya captured your command:")
            print(f"   Text: {command['raw_text']}")
            print(f"   Confidence: {command['confidence']}")
            print(f"   Timestamp: {command['timestamp']}")
        else:
            print("\n❌ Maya didn't detect the wake word")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Whisper voice listener test error: {e}")
    finally:
        try:
            listener.cleanup()
        except:
            pass


if __name__ == "__main__":
    main()
