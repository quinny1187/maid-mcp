# Voice System Module

The voice system provides both text-to-speech (TTS) for Mimi's responses and speech-to-text (STT) for user input. It's fully integrated with the avatar system and Claude Desktop.

## Structure

```
voice/
├── outgoing/                    # Mimi's text-to-speech (TTS)
│   ├── voiceEngine.js          # Main TTS engine using msedge-tts
│   ├── audioQueue.js           # Sequential audio playback queue
│   ├── voiceConfig.js          # Voice and emotion configurations
│   └── index.js                # Module exports
│
├── incoming/                    # User's speech-to-text (STT)
│   ├── speechRecognition.py    # Core speech recognition module
│   ├── speechListener.py       # Main listener that sends to Claude
│   ├── calibrate_microphone.py # Microphone calibration tool
│   ├── test_recognition.py     # Test speech recognition
│   ├── voice_config.ini        # Configuration file
│   └── requirements.txt        # Python dependencies
│
├── adjust_sensitivity.bat      # Quick sensitivity adjustment
├── adjust_sensitivity.py       # Python script for sensitivity
├── calibrate_voice.bat         # Run microphone calibration
├── fix_voice_import.bat        # Fix import issues
├── install_voice_deps.bat      # Install Python dependencies
├── install_hotkey.bat          # Install keyboard for hotkeys
├── test_voice_input.bat        # Test voice input system
│
├── index.js                    # Main voice module exports
├── README.md                   # This file
└── QUICK_REFERENCE.md          # Quick command reference
```

## Features

### Outgoing Voice (TTS)
- **Multiple Voices**: Japanese (Nanami), British (Maisie), American (Jenny)
- **Emotion Support**: Happy, sad, excited, angry, shy, neutral
- **Hidden Playback**: Uses VBScript for completely invisible audio
- **Audio Queue**: Prevents file conflicts with sequential playback
- **Real-time Generation**: Creates audio on-demand with unique filenames

### Incoming Voice (STT)
- **Continuous Listening**: Always ready for voice commands
- **Auto-send to Claude**: Automatically types messages in Claude Desktop
- **Multiple Engines**: Google (online) and Sphinx (offline) support
- **Configurable Sensitivity**: Adjustable microphone thresholds
- **Smart Detection**: Cooldown period prevents duplicate messages
- **Visual Feedback**: Shows listening status and recognized text

## Installation

### Prerequisites
- Node.js (for TTS)
- Python 3.8+ (for STT)
- Windows OS (for automation features)

### Install Dependencies

1. **Node.js Dependencies** (already installed with main project):
   ```bash
   npm install
   ```

2. **Python Dependencies** (for voice input):
   ```bash
   cd voice
   install_voice_deps.bat
   ```

   Or manually:
   ```bash
   cd voice/incoming
   pip install -r requirements.txt
   ```

3. **Optional: Install keyboard module** (for hotkey support):
   ```bash
   cd voice
   install_hotkey.bat
   ```

## Usage

### Start Complete System
From the main maid-mcp directory:
```bash
start_all.bat          # Enhanced batch launcher
# or
start_all_python.bat   # Python launcher with better process management
```

This launches:
1. Avatar display window
2. Avatar state server (port 3338)
3. Voice input listener

### Test Voice Output Only
```bash
cd tests
node test-simple.js
```

### Test Voice Input Only
```bash
cd voice
test_voice_input.bat
```

## Configuration

### Voice Output Settings

Edit `voice/outgoing/voiceConfig.js`:

```javascript
// Available voices
export const VOICES = {
  'ja-JP-NanamiNeural': { name: 'Nanami (Japanese)', ... },
  'en-GB-MaisieNeural': { name: 'Maisie (British)', ... },
  'en-US-JennyNeural': { name: 'Jenny (American)', ... }
};

// Emotion settings
export const EMOTION_SETTINGS = {
  happy: { pitchDelta: '+15Hz', rate: '+10%' },
  sad: { pitchDelta: '-10Hz', rate: '-10%' },
  // ... more emotions
};
```

### Voice Input Settings

Edit `voice/incoming/voice_config.ini`:

```ini
[recognition]
# Microphone sensitivity (higher = less sensitive)
energy_threshold = 8000

# Time between messages (seconds)
message_cooldown = 3.0

# Speech detection parameters
pause_threshold = 0.8
phrase_threshold = 0.3
non_speaking_duration = 0.5

[microphone]
# Leave empty for default mic
device_index = 

[engine]
# Recognition engine: google or sphinx
engine = google
```

## Calibration

### Quick Sensitivity Adjustment

1. **Run the adjustment tool**:
   ```bash
   cd voice
   adjust_sensitivity.bat
   ```

2. **Follow the prompts** to increase/decrease sensitivity

### Full Microphone Calibration

1. **Run calibration**:
   ```bash
   cd voice
   calibrate_voice.bat
   ```

2. **Watch the energy meter** while speaking

3. **Note your speaking level** and background noise

4. **Set threshold** slightly above background noise level

### Recommended Sensitivity Values
- **Very Quiet Room**: 1000-2000
- **Normal Room**: 2000-4000
- **Office Environment**: 4000-6000
- **Noisy Environment**: 6000-10000
- **Very Noisy**: 10000+

## Troubleshooting

### Voice Input Issues

1. **Not detecting speech**:
   - Run calibration to check microphone levels
   - Decrease energy_threshold in config
   - Check Windows microphone permissions

2. **Too sensitive** (picking up everything):
   - Increase energy_threshold
   - Use adjust_sensitivity.bat for quick changes
   - Increase message_cooldown to prevent spam

3. **Import errors**:
   - Run fix_voice_import.bat
   - Ensure all dependencies are installed

### Voice Output Issues

1. **No audio**:
   - Check Windows default audio device
   - Verify temp_voice folder exists
   - Check for antivirus blocking VBScript

2. **Audio cuts off**:
   - This shouldn't happen with current implementation
   - Check temp_voice folder for .vbs and .mp3 files

## Integration with Claude Desktop

The voice system integrates seamlessly:

1. **Voice Input**: Automatically types recognized speech into Claude
2. **Voice Output**: Triggered by MCP tools from Claude's responses
3. **Avatar Sync**: Speech animations play during voice output

## Advanced Features

### Custom Wake Words
Currently uses continuous listening. Future updates may add wake word detection.

### Offline Mode
Switch to Sphinx engine in voice_config.ini for offline recognition (less accurate).

### Multiple Languages
Voice output supports many languages through Edge TTS. Voice input currently optimized for English.

## Quick Command Reference

See `QUICK_REFERENCE.md` for a complete list of all commands and shortcuts.
