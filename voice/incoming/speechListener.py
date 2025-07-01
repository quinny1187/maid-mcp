"""
Speech Listener Module
Listens for user speech and sends it to Claude Desktop
"""

import sys
import os
import time
import logging
import configparser
from datetime import datetime
from typing import Optional
import threading

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from voice.incoming.speechRecognition import SpeechRecognizer
from auto_claude.ultra_fast_sender import send_to_claude

# Try to import keyboard for hotkey support
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("WARNING: keyboard module not installed. Hotkey support disabled.")
    print("Run: pip install keyboard")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpeechListener:
    """Listens for speech and sends to Claude"""
    
    def __init__(self, config_file: str = 'voice_config.ini'):
        """
        Initialize speech listener
        
        Args:
            config_file: Path to configuration file
        """
        # Load configuration
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), config_file)
        
        if os.path.exists(config_path):
            self.config.read(config_path)
            logger.info(f"Loaded configuration from {config_file}")
        else:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            self._set_defaults()
        
        # Get settings from config
        recognition_config = self.config['recognition']
        listener_config = self.config['listener']
        
        # Initialize recognizer with config values
        self.recognizer = SpeechRecognizer(
            energy_threshold=int(recognition_config.get('energy_threshold', 4000)),
            dynamic_energy=recognition_config.getboolean('dynamic_energy', True),
            pause_threshold=float(recognition_config.get('pause_threshold', 0.8)),
            phrase_threshold=float(recognition_config.get('phrase_threshold', 0.3)),
            non_speaking_duration=float(recognition_config.get('non_speaking_duration', 0.5))
        )
        
        # Listener settings
        self.prefix = listener_config.get('prefix', '[VOICE]')
        self.min_confidence = float(listener_config.get('min_confidence', 0.5))
        self.cooldown = float(listener_config.get('cooldown', 1.0))
        self.last_message_time = 0
        self.is_listening = False
        self.is_muted = False
        
        # Log current settings
        logger.info(f"Energy threshold: {recognition_config.get('energy_threshold')}")
        logger.info(f"Cooldown: {self.cooldown}s")
        
    def _set_defaults(self):
        """Set default configuration values"""
        self.config['recognition'] = {
            'energy_threshold': '4000',
            'dynamic_energy': 'true',
            'pause_threshold': '0.8',
            'phrase_threshold': '0.3',
            'non_speaking_duration': '0.5'
        }
        self.config['listener'] = {
            'prefix': '[VOICE]',
            'min_confidence': '0.5',
            'cooldown': '1.0'
        }
        self.config['microphone'] = {
            'device_index': '-1',
            'ambient_duration': '2'
        }
        
    def initialize(self) -> bool:
        """Initialize speech recognition"""
        logger.info("Initializing speech listener...")
        
        # Initialize microphone
        if not self.recognizer.initialize():
            logger.error("Failed to initialize microphone")
            return False
        
        # Set specific microphone if configured
        mic_config = self.config['microphone']
        device_index = int(mic_config.get('device_index', -1))
        
        if device_index >= 0:
            logger.info(f"Using microphone device index: {device_index}")
            self.recognizer.set_microphone(device_index)
        
        # List available microphones
        mics = self.recognizer.get_microphone_list()
        logger.info(f"Available microphones: {mics}")
        
        # Set up hotkey if keyboard module is available
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.add_hotkey('shift+m', self.toggle_mute)
                logger.info("Hotkey registered: SHIFT+M to mute/unmute")
            except Exception as e:
                logger.warning(f"Failed to register hotkey: {e}")
        
        return True
    
    def toggle_mute(self):
        """Toggle mute state"""
        self.is_muted = not self.is_muted
        status = "MUTED" if self.is_muted else "UNMUTED"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Log with emphasis
        logger.info("=" * 40)
        logger.info(f"[{timestamp}] Microphone {status}")
        logger.info("=" * 40)
        
        # Also print to console for visibility
        print(f"\n{'='*40}")
        print(f"[{timestamp}] 🎤 Microphone {status}")
        print(f"{'='*40}\n")
    
    def on_speech_recognized(self, text: str):
        """
        Called when speech is recognized
        
        Args:
            text: Recognized text
        """
        # Check if muted
        if self.is_muted:
            logger.info(f"[MUTED] Ignored: {text}")
            return
            
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_message_time < self.cooldown:
            logger.info(f"Cooldown active, skipping: {text}")
            return
        
        # Format message
        message = f"{self.prefix} {text}"
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        logger.info(f"[{timestamp}] Recognized: {text}")
        
        # Send to Claude
        try:
            if send_to_claude(message):
                logger.info(f"Sent to Claude: {message}")
                self.last_message_time = current_time
            else:
                logger.error("Failed to send to Claude")
        except Exception as e:
            logger.error(f"Error sending to Claude: {e}")
    
    def start_listening(self):
        """Start continuous listening"""
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        logger.info("Starting speech listener...")
        logger.info(f"Energy threshold: {self.recognizer.recognizer.energy_threshold}")
        logger.info("Speak to send messages to Claude!")
        
        if KEYBOARD_AVAILABLE:
            logger.info("Press SHIFT+M to mute/unmute microphone")
        
        logger.info("Press Ctrl+C to stop")
        
        self.is_listening = True
        self.recognizer.start_continuous_recognition(self.on_speech_recognized)
    
    def stop_listening(self):
        """Stop listening"""
        if not self.is_listening:
            return
        
        logger.info("Stopping speech listener...")
        self.recognizer.stop_continuous_recognition()
        
        # Remove hotkey if registered
        if KEYBOARD_AVAILABLE:
            try:
                keyboard.remove_hotkey('shift+m')
            except:
                pass
                
        self.is_listening = False
    
    def listen_once(self, timeout: float = 30) -> Optional[str]:
        """
        Listen for a single phrase
        
        Args:
            timeout: Maximum time to wait for speech
            
        Returns:
            Recognized text or None
        """
        if self.is_muted:
            logger.info("Microphone is muted")
            return None
            
        logger.info(f"Listening for speech (timeout: {timeout}s)...")
        text = self.recognizer.listen_once(timeout=timeout)
        
        if text:
            self.on_speech_recognized(text)
            
        return text


def main():
    """Main function for testing"""
    print("=" * 50)
    print("  Voice Input Listener for Claude Desktop")
    print("=" * 50)
    print()
    
    listener = SpeechListener()
    
    # Initialize
    if not listener.initialize():
        logger.error("Failed to initialize speech listener")
        return
    
    # Print status
    print("\n✅ Voice input ready!")
    print(f"📊 Energy threshold: {listener.recognizer.recognizer.energy_threshold}")
    print(f"⏱️  Cooldown: {listener.cooldown}s")
    
    if KEYBOARD_AVAILABLE:
        print("\n🎤 HOTKEY: Press SHIFT+M to mute/unmute")
    else:
        print("\n⚠️  Install 'keyboard' module for hotkey support")
        
    print("\n🗣️  Speak to send messages to Claude!")
    print("🛑 Press Ctrl+C to stop\n")
    print("-" * 50)
    
    # Start listening
    listener.start_listening()
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("\nStopping...")
        listener.stop_listening()


if __name__ == "__main__":
    main()
