# Voice Input Quick Reference 🎤

## Controls

### 🔇 Mute/Unmute
**SHIFT + M** - Toggle microphone on/off

### Status Indicators
- **[MUTED]** - Microphone is muted (speech ignored)
- **[timestamp]** - Normal operation, speech is sent to Claude

## Commands

### Start Everything
```bash
start_all.bat
```

### Calibrate Sensitivity  
```bash
calibrate_voice.bat
```

### Test Voice Only
```bash
test_voice_input.bat
```

### Install Hotkey Support
```bash
install_hotkey.bat
```

## Configuration

Edit `voice/incoming/voice_config.ini`:

```ini
[recognition]
energy_threshold = 4000  # Sensitivity (higher = less sensitive)

[listener]
cooldown = 1.0  # Seconds between messages
```

## Troubleshooting

### Too Sensitive?
- Increase `energy_threshold` (try 5000-8000)

### Not Picking Up Voice?
- Decrease `energy_threshold` (try 2000-3000)

### Hotkey Not Working?
- Run `install_hotkey.bat`
- May need to run as administrator

## Tips
- Speak clearly but naturally
- Wait for "Listening..." message
- Check window for recognized text
- Use SHIFT+M when you need privacy!
