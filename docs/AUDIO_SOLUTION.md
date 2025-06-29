# Audio Playback Solution - VBScript Hidden Playback

## Current Implementation
The maid-mcp voice system now uses VBScript with Windows Media Player COM object for **completely hidden** audio playback:

```javascript
// Create VBScript
const vbsScript = `
Set Sound = CreateObject("WMPlayer.OCX.7")
Sound.URL = "${audioFilePath}"
Sound.settings.volume = 100
Sound.Controls.play
While Sound.playState <> 1
  WScript.Sleep 100
Wend
`;

// Execute with wscript in batch mode (no UI)
exec(`wscript //B "${vbsPath}"`);
```

## Key Features
- **No windows appear** - Completely hidden playback
- **Full audio playback** - Waits for audio to complete
- **Universal Windows support** - Works on all Windows versions
- **No external dependencies** - Uses built-in Windows components

## How It Works
1. Generate MP3 audio with msedge-tts
2. Create a temporary VBScript file
3. VBScript uses `WMPlayer.OCX.7` COM object to play audio
4. Execute with `wscript //B` (batch mode = no UI)
5. Script waits for playback to complete
6. Clean up temporary files

## Why This Works
- **wscript //B** - Runs scripts in batch mode without any UI
- **WMPlayer.OCX.7** - Windows Media Player COM object (always available)
- **playState monitoring** - Ensures full playback before exit
- **No app selection** - Direct COM object access bypasses file associations

## Testing
Run the test to verify:
```
test-simple.bat
```

You should hear the audio playing with **NO windows appearing** at all!

## Benefits Over Previous Approaches
- ✅ No media player window
- ✅ No "select an app" dialog
- ✅ No PowerShell window flash
- ✅ Works on all Windows versions
- ✅ Plays MP3 files natively
- ✅ Full audio playback guaranteed

This is the ideal solution for background audio on Windows!
