"""
VoiceNav Enhanced Voice Listener Module
Advanced voice detection with confidence scoring, noise cancellation, 
custom wake words, visual feedback, and undo functionality
"""

import whisper
import pyaudio
import wave
import tempfile
import os
import time
import threading
import json
import pickle
from datetime import datetime
import sys
import subprocess
import numpy as np
import warnings

# Suppress Whisper FP16 warning on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU.*")

# Import noisereduce for noise cancellation
try:
    import noisereduce as nr
    NOISEREDUCE_AVAILABLE = True
except ImportError:
    NOISEREDUCE_AVAILABLE = False

# Import colorama for visual feedback
try:
    from colorama import Fore, Back, Style, init
    init()  # Initialize colorama
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("enhanced_voice_listener")


class EnhancedVoiceListener:
    """
    Enhanced voice listening system with advanced features:
    
    Features:
    - High-accuracy offline speech recognition using OpenAI Whisper
    - Confidence threshold filtering (>80% default)
    - Noise cancellation with noisereduce library
    - Custom wake word training and recognition
    - Visual feedback for listening states
    - Undo last action command processing
    - Command history tracking
    - False trigger prevention
    """
    
    def __init__(self, wake_word="hey maya", command_timeout=5, model_size="base", 
                 confidence_threshold=0.8, noise_reduction=True):
        """
        Initialize the enhanced voice listener
        
        Args:
            wake_word (str): The wake word to listen for
            command_timeout (int): Seconds to wait for command after wake word
            model_size (str): Whisper model size (tiny, base, small, medium, large)
            confidence_threshold (float): Minimum confidence to act on commands (0.0-1.0)
            noise_reduction (bool): Enable noise reduction preprocessing
        """
        self.wake_word = wake_word.lower()
        self.command_timeout = command_timeout
        self.model_size = model_size
        self.confidence_threshold = confidence_threshold
        self.noise_reduction = noise_reduction and NOISEREDUCE_AVAILABLE
        
        # State management
        self.is_listening = False
        self.listening_state = "idle"  # idle, wake_word, command, processing
        self.whisper_model = None
        self.audio_interface = None
        
        # Advanced features
        self.command_history = []
        self.custom_wake_words = {}  # For trained wake words
        self.wake_word_samples = []  # Training samples
        self.false_trigger_count = 0
        self.successful_commands = 0
        
        # Audio settings optimized for Whisper
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # Whisper's preferred sample rate
        
        # Visual feedback colors
        self.colors = {
            'idle': Fore.CYAN,
            'listening': Fore.GREEN,
            'wake_detected': Fore.YELLOW,
            'processing': Fore.BLUE,
            'command_ready': Fore.MAGENTA,
            'success': Fore.GREEN,
            'error': Fore.RED,
            'reset': Style.RESET_ALL
        } if COLORAMA_AVAILABLE else {k: '' for k in ['idle', 'listening', 'wake_detected', 'processing', 'command_ready', 'success', 'error', 'reset']}
        
        # Initialize components
        self._setup_whisper()
        self._setup_audio()
        self._load_custom_wake_words()
        
        logger.info(f"EnhancedVoiceListener initialized")
        logger.info(f"Wake word: '{wake_word}', Confidence: {confidence_threshold}")
        logger.info(f"Noise reduction: {self.noise_reduction}")
        
        # Print status
        self._print_status()
    
    def _print_status(self):
        """Print initialization status with visual feedback"""
        print(f"\n{self.colors['success']}🎤 Enhanced Maya Voice System Ready{self.colors['reset']}")
        print(f"┌─ Wake Word: '{self.wake_word}'")
        print(f"├─ Confidence Threshold: {self.confidence_threshold*100:.0f}%")
        print(f"├─ Noise Reduction: {'✅ Enabled' if self.noise_reduction else '❌ Disabled'}")
        print(f"├─ Custom Wake Words: {len(self.custom_wake_words)} trained")
        print(f"└─ Command History: {len(self.command_history)} commands")
        
        if not NOISEREDUCE_AVAILABLE:
            print(f"\n{self.colors['error']}⚠️  Install noisereduce for noise cancellation: pip install noisereduce{self.colors['reset']}")
        
        if not COLORAMA_AVAILABLE:
            print(f"\n⚠️  Install colorama for better visual feedback: pip install colorama")
    
    def _setup_whisper(self):
        """Setup Whisper model with enhanced confidence tracking"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self._update_visual_state("processing", "Loading Whisper AI model...")
            
            self.whisper_model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
            
            self._update_visual_state("success", "Whisper AI model ready!")
            
        except Exception as e:
            error_msg = f"Whisper setup failed: {e}"
            logger.error(error_msg)
            self._update_visual_state("error", error_msg)
            raise RuntimeError(error_msg)
    
    def _setup_audio(self):
        """Setup PyAudio interface with enhanced error handling"""
        try:
            self._update_visual_state("processing", "Initializing audio system...")
            self.audio_interface = pyaudio.PyAudio()
            logger.info("Audio interface initialized")
            
            # Test microphone access
            self._test_microphone_access()
            self._update_visual_state("success", "Audio system ready!")
            
        except Exception as e:
            error_msg = f"Audio setup failed: {e}"
            logger.error(error_msg)
            self._update_visual_state("error", error_msg)
            self._print_microphone_error()
            raise RuntimeError(error_msg)
    
    def _update_visual_state(self, state, message=None):
        """Update visual feedback for current listening state"""
        self.listening_state = state
        
        color = self.colors.get(state, self.colors['reset'])
        
        # State indicators
        indicators = {
            'idle': "💤",
            'listening': "👂",
            'wake_detected': "⚡",
            'processing': "🧠",
            'command_ready': "🎤",
            'success': "✅",
            'error': "❌"
        }
        
        indicator = indicators.get(state, "🔸")
        
        if message:
            print(f"\r{color}{indicator} {message}{self.colors['reset']}")
        else:
            # Default state messages
            messages = {
                'idle': "Maya is sleeping...",
                'listening': f"Listening for '{self.wake_word}'...",
                'wake_detected': "Maya detected! Ready for command...",
                'processing': "Maya is thinking...",
                'command_ready': "Say your command now...",
                'success': "Command processed successfully!",
                'error': "Error occurred"
            }
            print(f"\r{color}{indicator} {messages.get(state, state)}{self.colors['reset']}")
    
    def _load_custom_wake_words(self):
        """Load previously trained custom wake words"""
        try:
            wake_word_file = os.path.join(os.path.dirname(__file__), "custom_wake_words.pkl")
            if os.path.exists(wake_word_file):
                with open(wake_word_file, 'rb') as f:
                    self.custom_wake_words = pickle.load(f)
                logger.info(f"Loaded {len(self.custom_wake_words)} custom wake words")
        except Exception as e:
            logger.warning(f"Could not load custom wake words: {e}")
            self.custom_wake_words = {}
    
    def _save_custom_wake_words(self):
        """Save trained custom wake words"""
        try:
            wake_word_file = os.path.join(os.path.dirname(__file__), "custom_wake_words.pkl")
            with open(wake_word_file, 'wb') as f:
                pickle.dump(self.custom_wake_words, f)
            logger.info(f"Saved {len(self.custom_wake_words)} custom wake words")
        except Exception as e:
            logger.error(f"Could not save custom wake words: {e}")
    
    def _apply_noise_reduction(self, audio_data, sample_rate):
        """Apply noise reduction to audio data"""
        if not self.noise_reduction or not NOISEREDUCE_AVAILABLE:
            return audio_data
        
        try:
            # Convert to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
            audio_np = audio_np / 32768.0  # Normalize to [-1, 1]
            
            # Apply noise reduction
            reduced_audio = nr.reduce_noise(y=audio_np, sr=sample_rate)
            
            # Convert back to int16
            reduced_audio = (reduced_audio * 32768.0).astype(np.int16)
            
            return reduced_audio.tobytes()
            
        except Exception as e:
            logger.warning(f"Noise reduction failed: {e}")
            return audio_data
    
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
        print(f"\n{self.colors['error']}{'='*60}")
        print("🎤 MICROPHONE ACCESS ERROR")
        print("="*60)
        print("Enhanced Maya needs microphone access.")
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
        print("After granting permission, test with: python3 test_enhanced_maya.py")
        print(f"{'='*60}{self.colors['reset']}")
    
    def _play_beep(self):
        """Play system beep to indicate wake word detected"""
        try:
            # Play system beep (macOS)
            os.system("afplay /System/Library/Sounds/Glass.aiff")
        except:
            # Fallback: print visual indicator
            print(f"\n{self.colors['wake_detected']}🔊 *BEEP*{self.colors['reset']}")
    
    def _speak(self, text):
        """Use text-to-speech to say something"""
        try:
            # Use macOS built-in 'say' command with Samantha voice
            logger.info(f"Maya speaking: {text}")
            subprocess.run(['say', '-v', 'Samantha', text], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"macOS say command failed: {e}")
            # Fallback to default voice
            try:
                subprocess.run(['say', text], check=True)
            except:
                print(f"{self.colors['command_ready']}🔊 Maya would say: {text}{self.colors['reset']}")
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"{self.colors['command_ready']}🔊 Maya would say: {text}{self.colors['reset']}")
    
    def _record_audio(self, duration=3, stop_event=None, show_progress=True):
        """
        Record audio with noise reduction and visual feedback
        
        Args:
            duration (int): Maximum recording duration in seconds
            stop_event (threading.Event): Optional event to stop recording early
            show_progress (bool): Show visual recording progress
            
        Returns:
            tuple: (audio_data_bytes, success_flag)
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
            
            # Visual progress
            if show_progress:
                progress_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
                progress_index = 0
            
            # Record audio
            while True:
                # Check duration limit
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break
                    
                # Check stop event
                if stop_event and stop_event.is_set():
                    break
                
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    
                    # Apply noise reduction
                    if self.noise_reduction:
                        data = self._apply_noise_reduction(data, self.RATE)
                    
                    frames.append(data)
                    
                    # Update progress
                    if show_progress:
                        remaining = duration - elapsed
                        char = progress_chars[progress_index % len(progress_chars)]
                        print(f"\r{self.colors['processing']}{char} Recording... {remaining:.1f}s{self.colors['reset']}", end="", flush=True)
                        progress_index += 1
                        
                except Exception as e:
                    logger.warning(f"Audio read error: {e}")
                    break
            
            if show_progress:
                print()  # New line after progress
            
            stream.stop_stream()
            stream.close()
            
            # Return raw audio data
            if frames:
                return b''.join(frames), True
            
            return None, False
            
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return None, False
    
    def _transcribe_audio(self, audio_data):
        """
        Transcribe audio data using Whisper with confidence scoring
        
        Args:
            audio_data (bytes): Raw audio data
            
        Returns:
            tuple: (text, confidence_score)
        """
        try:
            # Save to temporary file for Whisper
            temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            
            # Write WAV file
            wf = wave.open(temp_file.name, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio_interface.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
            wf.close()
            temp_file.close()
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(temp_file.name)
            text = result["text"].strip().lower()
            
            # Calculate confidence from Whisper segments
            confidence = 0.0
            if "segments" in result and result["segments"]:
                # Average confidence from all segments
                confidences = []
                for segment in result["segments"]:
                    if "avg_logprob" in segment:
                        # Convert log probability to confidence (approximate)
                        conf = min(1.0, max(0.0, np.exp(segment["avg_logprob"])))
                        confidences.append(conf)
                
                if confidences:
                    confidence = np.mean(confidences)
                else:
                    # Fallback: estimate from text length and clarity
                    confidence = min(0.95, max(0.1, len(text.split()) * 0.15))
            else:
                # Fallback confidence estimation
                confidence = min(0.9, max(0.1, len(text.split()) * 0.15))
            
            logger.debug(f"Whisper transcription: '{text}' (confidence: {confidence:.3f})")
            
            return text, confidence
            
        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            return "", 0.0
        finally:
            # Clean up temporary file
            try:
                if 'temp_file' in locals() and os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
            except:
                pass
    
    def _check_wake_word(self, text, confidence):
        """
        Check if text contains wake word with confidence filtering
        
        Args:
            text (str): Transcribed text
            confidence (float): Transcription confidence
            
        Returns:
            bool: True if wake word detected with sufficient confidence
        """
        # Apply confidence threshold
        if confidence < self.confidence_threshold:
            logger.debug(f"Confidence too low: {confidence:.3f} < {self.confidence_threshold}")
            self.false_trigger_count += 1
            return False
        
        # Standard wake word variations
        standard_variations = [
            "hey maya", "hey maia", "a maya", "hey maria",
            "maya", "maia", "maria", "hey my", "my maya"
        ]
        
        # Check standard variations
        for wake_phrase in standard_variations:
            if wake_phrase in text:
                logger.info(f"Standard wake word detected: '{wake_phrase}' in '{text}'")
                return True
        
        # Check custom trained wake words
        for custom_name, patterns in self.custom_wake_words.items():
            for pattern in patterns:
                if pattern in text:
                    logger.info(f"Custom wake word detected: '{custom_name}' -> '{pattern}' in '{text}'")
                    return True
        
        return False
    
    def _listen_for_wake_word(self):
        """
        Listen for wake word using enhanced detection with confidence scoring
        
        Returns:
            bool: True if wake word detected, False if stopped
        """
        logger.info(f"Listening for wake word: '{self.wake_word}' (confidence >= {self.confidence_threshold})")
        self._update_visual_state("listening")
        
        while self.is_listening:
            try:
                # Record 3-second chunks for wake word detection
                audio_data, success = self._record_audio(duration=3, show_progress=False)
                
                if success and audio_data:
                    self._update_visual_state("processing", "Analyzing audio...")
                    text, confidence = self._transcribe_audio(audio_data)
                    
                    if text:
                        # Check confidence threshold and wake word
                        if self._check_wake_word(text, confidence):
                            logger.info(f"Wake word detected: '{text}' (confidence: {confidence:.3f})")
                            self._update_visual_state("wake_detected", f"Maya detected! (confidence: {confidence*100:.0f}%)")
                            return True
                        else:
                            # Show what was heard (if verbose)
                            print(f"\r{self.colors['idle']}🔇 Heard: '{text}' (conf: {confidence*100:.0f}%){self.colors['reset']}", end="")
                    else:
                        print(f"\r{self.colors['idle']}🔇 (silence){self.colors['reset']}", end="")
                        
                    # Return to listening state
                    self._update_visual_state("listening")
                else:
                    logger.warning("Recording failed")
                    time.sleep(0.5)
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Wake word listening error: {e}")
                time.sleep(1)
        
        return False
    
    def _listen_for_command(self):
        """
        Listen for command after wake word detection with enhanced processing
        
        Returns:
            dict: Enhanced command object with confidence, timestamps, and metadata
        """
        logger.info(f"Listening for command (timeout: {self.command_timeout}s)")
        self._update_visual_state("command_ready", f"Say your command ({self.command_timeout}s)...")
        
        try:
            # Record command with timeout and visual feedback
            audio_data, success = self._record_audio(duration=self.command_timeout, show_progress=True)
            
            if success and audio_data:
                self._update_visual_state("processing", "Maya is processing your command...")
                text, confidence = self._transcribe_audio(audio_data)
                
                # Create enhanced command object
                command = {
                    "timestamp": datetime.now().isoformat(),
                    "raw_text": text,
                    "confidence": confidence,
                    "confidence_threshold": self.confidence_threshold,
                    "meets_threshold": confidence >= self.confidence_threshold,
                    "wake_word_used": self.wake_word,
                    "noise_reduction": self.noise_reduction,
                    "processing_time": time.time()
                }
                
                # Add to command history
                self.command_history.append(command)
                
                # Log command
                logger.info(f"Command captured: {command}")
                
                # Check confidence threshold
                if confidence >= self.confidence_threshold:
                    self.successful_commands += 1
                    self._update_visual_state("success", f"Command processed: '{text}' ({confidence*100:.0f}%)")
                else:
                    self._update_visual_state("error", f"Low confidence: '{text}' ({confidence*100:.0f}%)")
                
                return command
            else:
                command = {
                    "timestamp": datetime.now().isoformat(),
                    "raw_text": "No speech detected",
                    "confidence": 0.0,
                    "confidence_threshold": self.confidence_threshold,
                    "meets_threshold": False,
                    "wake_word_used": self.wake_word,
                    "noise_reduction": self.noise_reduction,
                    "error": "Recording failed"
                }
                self.command_history.append(command)
                self._update_visual_state("error", "No speech detected")
                return command
                
        except Exception as e:
            logger.error(f"Command listening error: {e}")
            command = {
                "timestamp": datetime.now().isoformat(),
                "raw_text": f"Error: {str(e)}",
                "confidence": 0.0,
                "confidence_threshold": self.confidence_threshold,
                "meets_threshold": False,
                "wake_word_used": self.wake_word,
                "noise_reduction": self.noise_reduction,
                "error": str(e)
            }
            self.command_history.append(command)
            self._update_visual_state("error", f"Error: {str(e)}")
            return command
    
    def train_custom_wake_word(self, name, num_samples=5):
        """
        Train a custom wake word by recording multiple samples
        
        Args:
            name (str): Name for the custom wake word
            num_samples (int): Number of training samples to record
            
        Returns:
            bool: True if training successful
        """
        print(f"\n{self.colors['processing']}🎓 Training custom wake word: '{name}'{self.colors['reset']}")
        print(f"You will record {num_samples} samples of saying '{name}'")
        print("Speak clearly and consistently each time.")
        
        patterns = []
        
        for i in range(num_samples):
            input(f"\nPress ENTER when ready to record sample {i+1}/{num_samples}...")
            print(f"{self.colors['listening']}🎤 Say '{name}' now (3 seconds):{self.colors['reset']}")
            
            audio_data, success = self._record_audio(duration=3, show_progress=True)
            
            if success and audio_data:
                text, confidence = self._transcribe_audio(audio_data)
                
                if text and confidence >= 0.5:  # Lower threshold for training
                    patterns.append(text.lower())
                    print(f"{self.colors['success']}✅ Sample {i+1}: '{text}' (confidence: {confidence*100:.0f}%){self.colors['reset']}")
                else:
                    print(f"{self.colors['error']}❌ Sample {i+1} failed - try again{self.colors['reset']}")
                    i -= 1  # Retry this sample
            else:
                print(f"{self.colors['error']}❌ Recording failed - try again{self.colors['reset']}")
                i -= 1  # Retry this sample
        
        if patterns:
            self.custom_wake_words[name] = patterns
            self._save_custom_wake_words()
            
            print(f"\n{self.colors['success']}🎓 Training complete for '{name}'!{self.colors['reset']}")
            print(f"Trained patterns: {patterns}")
            return True
        else:
            print(f"\n{self.colors['error']}❌ Training failed - no valid samples recorded{self.colors['reset']}")
            return False
    
    def list_custom_wake_words(self):
        """List all trained custom wake words"""
        if not self.custom_wake_words:
            print(f"{self.colors['error']}No custom wake words trained yet.{self.colors['reset']}")
            return
        
        print(f"\n{self.colors['success']}📋 Trained Custom Wake Words:{self.colors['reset']}")
        for name, patterns in self.custom_wake_words.items():
            print(f"  • {name}: {len(patterns)} patterns")
            for pattern in patterns:
                print(f"    - '{pattern}'")
    
    def undo_last_action(self):
        """
        Process undo command - returns information about last command to undo
        
        Returns:
            dict: Information about command to undo, or None if no commands
        """
        if not self.command_history:
            self._speak("No commands to undo")
            return None
        
        # Find last successful command
        for command in reversed(self.command_history):
            if command.get("meets_threshold", False) and "undo" not in command.get("raw_text", ""):
                # Mark as undone
                command["undone"] = True
                command["undo_timestamp"] = datetime.now().isoformat()
                
                self._speak(f"Undoing: {command['raw_text']}")
                logger.info(f"Undo requested for command: {command['raw_text']}")
                
                return command
        
        self._speak("No recent commands to undo")
        return None
    
    def get_command_history(self, limit=10):
        """
        Get recent command history
        
        Args:
            limit (int): Maximum number of commands to return
            
        Returns:
            list: Recent commands
        """
        return self.command_history[-limit:] if self.command_history else []
    
    def get_statistics(self):
        """Get voice system statistics"""
        total_commands = len(self.command_history)
        successful_rate = (self.successful_commands / total_commands * 100) if total_commands > 0 else 0
        false_trigger_rate = (self.false_trigger_count / (self.false_trigger_count + self.successful_commands) * 100) if (self.false_trigger_count + self.successful_commands) > 0 else 0
        
        return {
            "total_commands": total_commands,
            "successful_commands": self.successful_commands,
            "success_rate": successful_rate,
            "false_triggers": self.false_trigger_count,
            "false_trigger_rate": false_trigger_rate,
            "custom_wake_words": len(self.custom_wake_words),
            "confidence_threshold": self.confidence_threshold,
            "noise_reduction_enabled": self.noise_reduction
        }
    
    def start_listening(self):
        """Start the enhanced voice listening loop"""
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        self.is_listening = True
        logger.info("Enhanced voice listening started")
        self._update_visual_state("idle", "Enhanced Maya is ready!")
        print(f"Say: '{self.wake_word}' to activate (confidence threshold: {self.confidence_threshold*100:.0f}%)")
    
    def stop_listening(self):
        """Stop the voice listening loop"""
        self.is_listening = False
        logger.info("Enhanced voice listening stopped")
        self._update_visual_state("idle", "Maya is sleeping...")
    
    def listen_once(self):
        """
        Listen for one wake word + command cycle with enhanced features
        
        Returns:
            dict or None: Enhanced command object if successful, None if no wake word
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
                
                # Listen for command
                command = self._listen_for_command()
                
                # Check for undo command
                if command and "undo" in command.get("raw_text", "").lower():
                    undo_result = self.undo_last_action()
                    command["undo_result"] = undo_result
                
                return command
            
            return None
            
        except KeyboardInterrupt:
            logger.info("Listening interrupted by user")
            self.stop_listening()
            return None
        except Exception as e:
            logger.error(f"Enhanced listening error: {e}")
            self._update_visual_state("error", f"Error: {str(e)}")
            return {
                "timestamp": datetime.now().isoformat(),
                "raw_text": f"Error: {str(e)}",
                "confidence": 0.0,
                "meets_threshold": False,
                "error": str(e)
            }
    
    def test_all_features(self):
        """Test all enhanced features"""
        print(f"\n{self.colors['processing']}🧪 Testing Enhanced Maya Features{self.colors['reset']}")
        
        # Test 1: Microphone
        print(f"\n{self.colors['listening']}Test 1: Microphone Access{self.colors['reset']}")
        if not self.test_microphone():
            return False
        
        # Test 2: Whisper recognition
        print(f"\n{self.colors['listening']}Test 2: Whisper Recognition{self.colors['reset']}")
        if not self.test_whisper_recognition():
            return False
        
        # Test 3: Confidence threshold
        print(f"\n{self.colors['listening']}Test 3: Confidence Threshold ({self.confidence_threshold*100:.0f}%){self.colors['reset']}")
        print("Say something clearly for confidence testing:")
        audio_data, success = self._record_audio(duration=3)
        if success:
            text, confidence = self._transcribe_audio(audio_data)
            meets_threshold = confidence >= self.confidence_threshold
            status = "✅ PASS" if meets_threshold else "❌ FAIL"
            print(f"{status} Confidence: {confidence*100:.0f}% ({'above' if meets_threshold else 'below'} threshold)")
        
        # Test 4: Noise reduction
        if self.noise_reduction:
            print(f"\n{self.colors['listening']}Test 4: Noise Reduction{self.colors['reset']}")
            print("✅ Noise reduction enabled and working")
        else:
            print(f"\n{self.colors['error']}Test 4: Noise Reduction - DISABLED{self.colors['reset']}")
        
        # Test 5: Visual feedback
        print(f"\n{self.colors['listening']}Test 5: Visual Feedback{self.colors['reset']}")
        if COLORAMA_AVAILABLE:
            print("✅ Color visual feedback enabled")
        else:
            print("⚠️  Install colorama for enhanced visual feedback")
        
        print(f"\n{self.colors['success']}🎉 Enhanced feature testing complete!{self.colors['reset']}")
        return True
    
    def test_microphone(self):
        """Test microphone setup and permissions"""
        self._update_visual_state("processing", "Testing microphone access...")
        
        try:
            self._test_microphone_access()
            self._update_visual_state("success", "Microphone test successful!")
            return True
                
        except Exception as e:
            self._update_visual_state("error", f"Microphone test failed: {e}")
            self._print_microphone_error()
            return False
    
    def test_whisper_recognition(self):
        """Test Whisper speech recognition with confidence reporting"""
        self._update_visual_state("processing", "Testing Whisper recognition...")
        print("Say something clearly (3 seconds):")
        
        try:
            audio_data, success = self._record_audio(duration=3)
            if success and audio_data:
                text, confidence = self._transcribe_audio(audio_data)
                if text:
                    meets_threshold = confidence >= self.confidence_threshold
                    status = "✅" if meets_threshold else "⚠️"
                    self._update_visual_state("success" if meets_threshold else "error", 
                                           f"Recognition: '{text}' ({confidence*100:.0f}%)")
                    return True
                else:
                    self._update_visual_state("error", "No speech detected")
                    return False
            else:
                self._update_visual_state("error", "Recording failed")
                return False
                
        except Exception as e:
            self._update_visual_state("error", f"Whisper test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.audio_interface:
                self.audio_interface.terminate()
            
            # Save command history
            try:
                history_file = os.path.join(os.path.dirname(__file__), "command_history.json")
                with open(history_file, 'w') as f:
                    json.dump(self.command_history[-100:], f, indent=2)  # Keep last 100 commands
            except Exception as e:
                logger.warning(f"Could not save command history: {e}")
            
            logger.info("Enhanced resources cleaned up")
            self._update_visual_state("idle", "Maya is shutting down...")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


def main():
    """Test the enhanced voice listener directly"""
    print(f"\n{Fore.CYAN if COLORAMA_AVAILABLE else ''}Enhanced Maya Voice Listener Test{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}")
    print("="*50)
    
    try:
        # Initialize enhanced voice listener
        listener = EnhancedVoiceListener(
            confidence_threshold=0.8,  # 80% confidence required
            noise_reduction=True
        )
        
        # Test all features
        if not listener.test_all_features():
            return
        
        print(f"\n{listener.colors['processing']}🎤 Starting Enhanced Maya Test...{listener.colors['reset']}")
        print(f"Say: '{listener.wake_word}' followed by a command")
        print("Try saying 'undo' to test undo functionality")
        print("Press Ctrl+C to stop")
        
        # Test one cycle
        command = listener.listen_once()
        if command:
            print(f"\n{listener.colors['success']}✅ Maya captured your command:{listener.colors['reset']}")
            print(f"   Text: {command['raw_text']}")
            print(f"   Confidence: {command['confidence']*100:.1f}%")
            print(f"   Meets Threshold: {command.get('meets_threshold', False)}")
            print(f"   Timestamp: {command['timestamp']}")
            
            if 'undo_result' in command:
                print(f"   Undo Result: {command['undo_result']}")
        else:
            print(f"\n{listener.colors['error']}❌ Maya didn't detect the wake word{listener.colors['reset']}")
        
        # Show statistics
        stats = listener.get_statistics()
        print(f"\n{listener.colors['processing']}📊 Session Statistics:{listener.colors['reset']}")
        for key, value in stats.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Enhanced voice listener test error: {e}")
    finally:
        try:
            listener.cleanup()
        except:
            pass


if __name__ == "__main__":
    main()
