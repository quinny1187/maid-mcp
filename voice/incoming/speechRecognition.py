"""
Speech Recognition Module
Handles converting user's voice to text
"""

import speech_recognition as sr
import numpy as np
import logging
from typing import Optional, Callable
import queue
import threading

logger = logging.getLogger(__name__)

class SpeechRecognizer:
    """Handles speech-to-text conversion"""
    
    def __init__(self, 
                 energy_threshold: int = 2000,
                 dynamic_energy: bool = True,
                 pause_threshold: float = 0.8,
                 phrase_threshold: float = 0.3,
                 non_speaking_duration: float = 0.5):
        """
        Initialize speech recognizer
        
        Args:
            energy_threshold: Minimum audio energy to consider for recording
            dynamic_energy: Whether to adjust energy threshold dynamically
            pause_threshold: Seconds of silence before considering speech complete
            phrase_threshold: Minimum seconds of speaking audio before recording
            non_speaking_duration: Seconds of non-speaking audio to keep on both sides
        """
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Configure recognizer
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = dynamic_energy
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.phrase_threshold = phrase_threshold
        self.recognizer.non_speaking_duration = non_speaking_duration
        
        # Audio queue for processing
        self.audio_queue = queue.Queue()
        self.recognition_thread = None
        self.is_running = False
        
    def initialize(self) -> bool:
        """Initialize microphone"""
        try:
            self.microphone = sr.Microphone()
            
            # Store the configured threshold
            configured_threshold = self.recognizer.energy_threshold
            
            # Adjust for ambient noise
            with self.microphone as source:
                logger.info("Adjusting for ambient noise... Please be quiet.")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info(f"Ambient adjustment suggested: {self.recognizer.energy_threshold}")
                
                # If dynamic energy is disabled, restore configured threshold
                if not self.recognizer.dynamic_energy_threshold:
                    self.recognizer.energy_threshold = configured_threshold
                    logger.info(f"Restored configured threshold: {self.recognizer.energy_threshold}")
                else:
                    logger.info(f"Using dynamic threshold: {self.recognizer.energy_threshold}")
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            return False
    
    def recognize_speech(self, audio: sr.AudioData, language: str = "en-US") -> Optional[str]:
        """
        Convert audio to text using multiple recognition engines
        
        Args:
            audio: Audio data to recognize
            language: Language code (default: en-US)
            
        Returns:
            Recognized text or None if failed
        """
        text = None
        
        # Try Google Speech Recognition first (free, no API key)
        try:
            text = self.recognizer.recognize_google(audio, language=language)
            logger.info(f"Google Speech Recognition: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Google Speech Recognition error: {e}")
        
        # Skip Sphinx fallback if Google couldn't understand
        # (Sphinx is less accurate and tends to hallucinate words)
        if False:  # Disabled for now
            # Fallback to Windows Speech Recognition (offline)
            if not text:
                try:
                    # Try Windows Speech Recognition as fallback
                    import platform
                    if platform.system() == "Windows":
                        # Note: This requires pywin32 and Windows Speech Recognition to be set up
                        text = self.recognizer.recognize_sphinx(audio)
                        logger.info(f"Sphinx Speech Recognition: {text}")
                        return text
                except Exception as e:
                    logger.warning(f"Sphinx Speech Recognition failed: {e}")
        
        return None
    
    def listen_once(self, timeout: Optional[float] = None) -> Optional[str]:
        """
        Listen for a single phrase and return the text
        
        Args:
            timeout: Maximum time to wait for speech (None = wait forever)
            
        Returns:
            Recognized text or None if failed/timeout
        """
        try:
            with self.microphone as source:
                logger.info("Listening for speech...")
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout)
                
                # Convert to text
                text = self.recognize_speech(audio)
                return text
                
        except sr.WaitTimeoutError:
            logger.info("Listening timed out")
            return None
        except Exception as e:
            logger.error(f"Error during listening: {e}")
            return None
    
    def start_continuous_recognition(self, callback: Callable[[str], None]):
        """
        Start continuous speech recognition in background
        
        Args:
            callback: Function to call with recognized text
        """
        if self.is_running:
            logger.warning("Recognition already running")
            return
        
        self.is_running = True
        
        # Start recognition thread
        self.recognition_thread = threading.Thread(
            target=self._recognition_worker,
            args=(callback,),
            daemon=True
        )
        self.recognition_thread.start()
        
        # Start listening in background
        stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            self._audio_callback,
            phrase_time_limit=10  # Max phrase length in seconds
        )
        
        self.stop_listening = stop_listening
        logger.info("Started continuous speech recognition")
    
    def stop_continuous_recognition(self):
        """Stop continuous speech recognition"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stop background listening
        if hasattr(self, 'stop_listening'):
            self.stop_listening(wait_for_stop=True)
        
        # Signal thread to stop
        self.audio_queue.put(None)
        
        # Wait for thread to finish
        if self.recognition_thread:
            self.recognition_thread.join(timeout=5)
        
        logger.info("Stopped continuous speech recognition")
    
    def _audio_callback(self, recognizer, audio):
        """Callback for background listening"""
        # Add audio to queue for processing
        self.audio_queue.put(audio)
    
    def _recognition_worker(self, callback: Callable[[str], None]):
        """Worker thread for processing audio"""
        while self.is_running:
            try:
                # Get audio from queue
                audio = self.audio_queue.get(timeout=1)
                
                if audio is None:  # Stop signal
                    break
                
                # Recognize speech
                text = self.recognize_speech(audio)
                
                if text:
                    # Call callback with recognized text
                    callback(text)
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Recognition worker error: {e}")
    
    def get_microphone_list(self) -> list:
        """Get list of available microphones"""
        return sr.Microphone.list_microphone_names()
    
    def set_microphone(self, device_index: int):
        """Set specific microphone by index"""
        self.microphone = sr.Microphone(device_index=device_index)
        logger.info(f"Set microphone to device index: {device_index}")
