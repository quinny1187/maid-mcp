# Maid-MCP 🎀

A voice-enabled MCP (Model Context Protocol) server that gives Claude Desktop a maid personality with Japanese-accented English voice.

## Features

- 🎵 **Japanese-accented voice** - Authentic maid character voice using ja-JP neural voices
- 👻 **Completely hidden playback** - No windows appear during audio playback
- 🎭 **Emotion support** - Happy, sad, excited, angry, shy voice modulations
- 🔧 **MCP integration** - Works seamlessly with Claude Desktop

## Quick Start

1. **Install dependencies:**
   ```
   install.bat
   ```

2. **Configure Claude Desktop:**
   - Copy the config: `copy claude_desktop_config.json %APPDATA%\Claude\`
   - Or manually add the maid section to your existing config
   - See `docs/CLAUDE_CONFIG.md` for details

3. **Restart Claude Desktop**

4. **Test the voice:**
   - Ask Claude: "Use the speak tool to say hello"

## Testing Locally

Run the test to hear the maid voice:
```
cd tests
test-simple.bat
```

## How It Works

The voice system uses:
- **msedge-tts** - Microsoft Edge's text-to-speech for high-quality neural voices
- **VBScript** - Hidden audio playback using Windows Media Player COM object
- **wscript //B** - Batch mode execution (no UI)

See `docs/AUDIO_SOLUTION.md` for technical details.

### Voice Configuration

Default voice: **ja-JP-NanamiNeural** (Cute Japanese voice)
- Base pitch: +20Hz for authentic maid character
- Emotions add additional pitch/rate/volume adjustments

See `docs/JAPANESE_ACCENT.md` for voice configuration details.

## Available Tools

### speak
Convert text to speech with optional emotion
```javascript
{
  text: "Hello, Master!",
  emotion: "happy" // optional: neutral, happy, sad, excited, angry, shy
}
```

### list_voices
Get list of available voices

### set_voice
Change the current voice
```javascript
{
  voiceId: "ja-JP-MayuNeural" // or other available voices
}
```

## Project Structure

```
maid-mcp/
├── maid-server.js          # Main MCP server
├── package.json            # Node dependencies
├── install.bat             # Install script
├── start.bat               # Start server script
├── claude_desktop_config.json  # Example config
├── docs/                   # Documentation
│   ├── AUDIO_SOLUTION.md   # Technical details
│   ├── CLAUDE_CONFIG.md    # Setup instructions
│   └── JAPANESE_ACCENT.md  # Voice configuration
├── tests/                  # Test files
│   ├── test-simple.js      # Voice test script
│   └── test-simple.bat     # Test runner
├── auto_claude/            # Python automation scripts
└── temp_voice/             # Temporary audio files
```

## Additional Features

The `auto_claude/` folder contains Python scripts for programmatically controlling Claude Desktop:
- `ultra_fast_sender.py` - Send messages to Claude Desktop
- `working_event_handler.py` - Event queue system for automation

## License

MIT
