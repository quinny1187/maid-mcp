"""
Test speech recognition without sending to Claude
Useful for debugging microphone and recognition issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speechRecognition import SpeechRecognizer
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_speech_recognition():
    """Test speech recognition"""
    print("=" * 50)
    print("  Speech Recognition Test")
    print("=" * 50)
    print()
    
    recognizer = SpeechRecognizer()
    
    # Initialize
    print("Initializing microphone...")
    if not recognizer.initialize():
        print("ERROR: Failed to initialize microphone")
        return
    
    # List microphones
    print("\nAvailable microphones:")
    mics = recognizer.get_microphone_list()
    for i, mic in enumerate(mics):
        print(f"  {i}: {mic}")
    
    print("\nUsing default microphone")
    print("Adjusting for ambient noise (please be quiet)...")
    print()
    
    # Test single recognition
    print("TEST: Single phrase recognition")
    print("-" * 30)
    print("Speak now (you have 10 seconds)...")
    
    text = recognizer.listen_once(timeout=10)
    
    if text:
        print(f"\n✅ Recognized: '{text}'")
    else:
        print("\n❌ No speech detected or recognition failed")
    
    print("\nTest complete!")

if __name__ == "__main__":
    test_speech_recognition()
    input("\nPress Enter to exit...")
