"""
VoiceNav Voice Listener Module
Handles wake word detection and command capture
Now powered by OpenAI Whisper for better accuracy
"""

import speech_recognition as sr
import pyttsx3
import time
import threading
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

# Try to import Whisper and Enhanced listeners, fallback to Google Speech
try:
    from input.whisper_voice_listener import WhisperVoiceListener
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    from input.enhanced_voice_listener import EnhancedVoiceListener
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False

# Initialize logger
logger = setup_logger("voice_listener")


class VoiceListener:
    """
    Voice listening system for VoiceNav
    
    Features:
    - Continuous microphone monitoring
    - Wake word detection ("hey voicenav")
    - Command capture (5 second window)
    - Audio feedback and text-to-speech
    - Error handling and timeouts
    """
    
    def __init__(self, wake_word="hey maya", command_timeout=5):
        """
        Initialize the voice listener
        
        Args:
            wake_word (str): The wake word to listen for
            command_timeout (int): Seconds to wait for command after wake word
        """
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        
        # Initialize components
        self._setup_microphone()
        self._setup_tts()
        self._configure_recognition()
        
        logger.info(f"VoiceListener initialized with wake word: '{wake_word}'")
    
    def _setup_microphone(self):
        """Setup and test microphone access"""
        try:
            self.microphone = sr.Microphone()
            logger.info("Microphone initialized successfully")
            
            # Test microphone access
            with self.microphone as source:
                logger.info("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone setup complete")
                
        except Exception as e:
            error_msg = f"Microphone setup failed: {e}"
            logger.error(error_msg)
            self._print_microphone_error()
            raise RuntimeError(error_msg)
    
    def _setup_tts(self):
        """Setup text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            # Set speaking rate (words per minute)
            self.tts_engine.setProperty('rate', 150)
            # Set volume (0.0 to 1.0)
            self.tts_engine.setProperty('volume', 0.8)
            logger.info("Text-to-speech engine initialized")
            
        except Exception as e:
            logger.error(f"TTS setup failed: {e}")
            self.tts_engine = None
    
    def _configure_recognition(self):
        """Configure speech recognition parameters"""
        # Adjust recognition sensitivity - LOWERED for better wake word detection
        self.recognizer.energy_threshold = 1000  # Lowered from 4000 for higher sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Reduced from 0.8 for faster response
        self.recognizer.phrase_threshold = 0.2  # Reduced from 0.3 for shorter phrases
        
        logger.info("Speech recognition configured with higher sensitivity")
    
    def _print_microphone_error(self):
        """Print helpful error message for microphone issues"""
        print("\n" + "="*60)
        print("🎤 MICROPHONE ACCESS ERROR")
        print("="*60)
        print("VoiceNav needs microphone access to work.")
        print("\n🔧 PERMISSION DIALOG SOLUTION:")
        print("If you see a dialog asking 'Terminal would like to access")
        print("the Microphone' → Click 'Allow'")
        print("\n🔧 MANUAL PERMISSION SETUP:")
        print("1. Open System Settings/Preferences")
        print("2. Go to Privacy & Security → Microphone")
        print("3. Add Terminal (and your IDE) to allowed apps")
        print("4. Restart your terminal/IDE")
        print("5. Try running the test again")
        print("\n🔧 EXTERNAL MICROPHONE:")
        print("- Make sure it's plugged in and working")
        print("- Check it appears in System Settings → Sound → Input")
        print("\n🎯 NEXT STEP:")
        print("After granting permission, run: python3 tests/test_voice.py")
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
    
    def _listen_for_wake_word(self):
        """
        Listen continuously for the wake word
        
        Returns:
            bool: True if wake word detected, False if stopped
        """
        logger.info(f"Listening for wake word: '{self.wake_word}'")
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                try:
                    # Convert speech to text
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"🎤 Heard: '{text}'")  # Debug output
                    logger.debug(f"Heard: '{text}'")
                    
                    # Check if wake word is in the text
                    if self.wake_word in text:
                        logger.info(f"Wake word detected in: '{text}'")
                        print(f"✅ Wake word '{self.wake_word}' detected!")
                        return True
                        
                except sr.UnknownValueError:
                    # Speech was unintelligible - this is normal, keep listening
                    pass
                except sr.RequestError as e:
                    logger.warning(f"Recognition service error: {e}")
                    time.sleep(0.5)  # Brief pause before retrying
                
            except sr.WaitTimeoutError:
                # No speech detected in timeout period - this is normal
                pass
            except Exception as e:
                logger.error(f"Wake word listening error: {e}")
                time.sleep(0.1)  # Prevent CPU spinning
        
        return False
    
    def _listen_for_command(self):
        """
        Listen for a command after wake word detection
        
        Returns:
            dict: Command object with timestamp, text, and confidence
        """
        logger.info(f"Listening for command (timeout: {self.command_timeout}s)")
        
        try:
            with self.microphone as source:
                # Listen for the command with timeout
                audio = self.recognizer.listen(source, timeout=self.command_timeout, phrase_time_limit=5)
            
            try:
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                confidence = 0.95  # Google API doesn't provide confidence, use default
                
                command = {
                    "timestamp": datetime.now().isoformat(),
                    "raw_text": text,
                    "confidence": confidence
                }
                
                logger.info(f"Command captured: {command}")
                return command
                
            except sr.UnknownValueError:
                logger.warning("No speech detected during command window")
                return {
                    "timestamp": datetime.now().isoformat(),
                    "raw_text": "No speech detected",
                    "confidence": 0.0
                }
            except sr.RequestError as e:
                logger.error(f"Recognition service error: {e}")
                return {
                    "timestamp": datetime.now().isoformat(),
                    "raw_text": "Network error - unknown command",
                    "confidence": 0.0
                }
                
        except sr.WaitTimeoutError:
            logger.warning("Command timeout - no speech detected")
            return {
                "timestamp": datetime.now().isoformat(),
                "raw_text": "Timeout - no command heard",
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
        print("🎤 VoiceNav is listening...")
        print(f"Say: '{self.wake_word}' to activate")
    
    def stop_listening(self):
        """Stop the voice listening loop"""
        self.is_listening = False
        logger.info("Voice listening stopped")
        print("🎤 VoiceNav stopped listening")
    
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
                self._speak("Listening...")
                print("🎤 Wake word detected! Say your command:")
                
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
                        print(f"Command: {command['raw_text']}")
                
                # Small delay to prevent CPU spinning
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Continuous listening stopped by user")
        finally:
            self.stop_listening()
    
    def test_microphone(self):
        """Test microphone setup and permissions"""
        print("🎤 Testing microphone...")
        
        try:
            with self.microphone as source:
                print("Adjusting for ambient noise... (2 seconds)")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("✅ Microphone test successful!")
                return True
                
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            self._print_microphone_error()
            return False
    
    def test_speech_recognition(self):
        """Test speech recognition with a simple phrase"""
        print("🎤 Testing speech recognition...")
        print("Say something (you have 5 seconds):")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            text = self.recognizer.recognize_google(audio)
            print(f"✅ Speech recognition test successful!")
            print(f"You said: '{text}'")
            return True
            
        except sr.WaitTimeoutError:
            print("❌ No speech detected during test")
            return False
        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
            return False
        except sr.RequestError as e:
            print(f"❌ Recognition service error: {e}")
            return False
        except Exception as e:
            print(f"❌ Speech recognition test failed: {e}")
            return False


def main():
    """Test the voice listener directly"""
    print("VoiceNav Voice Listener Test")
    print("="*40)
    
    try:
        # Initialize voice listener
        listener = VoiceListener()
        
        # Test microphone
        if not listener.test_microphone():
            return
        
        # Test speech recognition
        if not listener.test_speech_recognition():
            return
        
        print("\n🎤 Starting wake word test...")
        print(f"Say: '{listener.wake_word}' followed by a command")
        print("Press Ctrl+C to stop")
        
        # Test one cycle
        command = listener.listen_once()
        if command:
            print(f"\n✅ Command captured:")
            print(f"   Text: {command['raw_text']}")
            print(f"   Confidence: {command['confidence']}")
            print(f"   Timestamp: {command['timestamp']}")
        else:
            print("\n❌ No wake word detected")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Voice listener test error: {e}")


def create_voice_listener(wake_word="hey maya", command_timeout=5, prefer_whisper=True):
    """
    Factory function to create the best available voice listener
    
    Args:
        wake_word (str): The wake word to listen for
        command_timeout (int): Seconds to wait for command after wake word  
        prefer_whisper (bool): Use Whisper if available (recommended)
        
    Returns:
        WhisperVoiceListener or VoiceListener: Best available listener
    """
    # Use the working Whisper listener (revert to original working system)
    if prefer_whisper and WHISPER_AVAILABLE:
        try:
            logger.info("Creating Whisper voice listener (high accuracy - REVERTED)")
            return WhisperVoiceListener(wake_word=wake_word, command_timeout=command_timeout)
        except Exception as e:
            logger.warning(f"Whisper initialization failed: {e}, falling back to Google Speech")
    
    # Fallback to standard listener
    logger.info("Creating standard voice listener (Google Speech)")
    return VoiceListener(wake_word=wake_word, command_timeout=command_timeout)


def create_enhanced_voice_listener(wake_word="hey maya", command_timeout=5, confidence_threshold=0.8, noise_reduction=True):
    """
    Create specifically an Enhanced voice listener with Step 1 Extra features
    
    Args:
        wake_word (str): The wake word to listen for
        command_timeout (int): Seconds to wait for command after wake word
        confidence_threshold (float): Minimum confidence to act on commands (0.0-1.0)
        noise_reduction (bool): Enable noise cancellation
        
    Returns:
        EnhancedVoiceListener: Enhanced listener with all Step 1 Extra features
        
    Raises:
        RuntimeError: If enhanced listener dependencies not available
    """
    if not ENHANCED_AVAILABLE:
        raise RuntimeError("Enhanced voice listener not available. Install: pip install noisereduce colorama")
    
    logger.info("Creating Enhanced voice listener with Step 1 Extra features")
    return EnhancedVoiceListener(
        wake_word=wake_word,
        command_timeout=command_timeout,
        confidence_threshold=confidence_threshold,
        noise_reduction=noise_reduction
    )


if __name__ == "__main__":
    main()
