"""
Test and calibrate microphone sensitivity
Helps find the right energy threshold for your environment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import speech_recognition as sr
import time
import threading

def test_microphone_levels():
    """Test microphone and show energy levels"""
    print("=" * 50)
    print("  Microphone Calibration Tool")
    print("=" * 50)
    print()
    
    # Create recognizer
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 2000  # Start with low threshold for calibration
    recognizer.dynamic_energy_threshold = False  # Disable for consistent readings
    
    # Get microphone
    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"ERROR: Could not access microphone: {e}")
        return
    
    print("Initializing microphone...")
    
    # Adjust for ambient noise first
    with mic as source:
        print("Adjusting for ambient noise... Please be quiet for 2 seconds.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"Ambient energy level: ~{recognizer.energy_threshold:.0f}")
    
    print("\nMonitoring microphone energy levels...")
    print("Speak into the microphone to see the energy levels!")
    print("Press Ctrl+C to stop")
    print()
    print("Energy Level:")
    print("-" * 60)
    
    # Flag to control the monitoring loop
    monitoring = True
    
    def monitor_audio():
        """Monitor audio in a separate thread"""
        with mic as source:
            while monitoring:
                try:
                    # Read audio data
                    audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                    
                    # Get energy of audio
                    energy = recognizer.get_energy(audio)
                    
                    # Create visual bar
                    max_bar = 50
                    bar_length = int(energy / 200)  # Scale down for display
                    bar_length = min(bar_length, max_bar)
                    
                    # Color coding
                    if energy < 2000:
                        bar_char = "-"  # Too quiet
                    elif energy < 4000:
                        bar_char = "="  # Good range
                    elif energy < 8000:
                        bar_char = "≡"  # Loud
                    else:
                        bar_char = "█"  # Very loud
                    
                    bar = bar_char * bar_length
                    
                    # Print with carriage return to update same line
                    status = "SILENT" if energy < 1000 else "ACTIVE"
                    print(f"\r{energy:>6.0f} [{status:^7}] |{bar:<50}|", end="", flush=True)
                    
                except sr.WaitTimeoutError:
                    # No sound, show baseline
                    print(f"\r{0:>6.0f} [SILENT ] |{'':<50}|", end="", flush=True)
                except Exception as e:
                    # Ignore errors during monitoring
                    pass
    
    # Start monitoring in thread
    monitor_thread = threading.Thread(target=monitor_audio, daemon=True)
    monitor_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        monitoring = False
        print("\n\nCalibration stopped.")
    
    # Wait for thread to finish
    monitor_thread.join(timeout=1)
    
    # Recommendations
    print("\n" + "=" * 60)
    print("ENERGY LEVEL GUIDE:")
    print()
    print("  < 1000  - No sound detected")
    print("  1000-2000 - Very quiet (breathing, rustling)")
    print("  2000-4000 - Normal speaking voice")
    print("  4000-8000 - Loud speaking voice")
    print("  > 8000  - Very loud or close to microphone")
    print()
    print("RECOMMENDATIONS:")
    print()
    print("Set energy_threshold in voice_config.ini to:")
    print("- Just above your room's ambient level (when quiet)")
    print("- But below your normal speaking voice level")
    print()
    print("For example:")
    print("- If ambient is ~1500 and voice is ~3000, use 2000-2500")
    print("- If ambient is ~3000 and voice is ~6000, use 4000-5000")
    print()
    print("Current setting in config: Check voice_config.ini")

if __name__ == "__main__":
    test_microphone_levels()
    input("\nPress Enter to exit...")
