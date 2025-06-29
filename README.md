# Maid-MCP 🎀

A full-featured MCP (Model Context Protocol) server that gives Claude Desktop a maid personality with Japanese-accented voice and visual avatar presence.

## Features

- 🎵 **Japanese-accented voice** - Authentic maid character voice using ja-JP neural voices
- 🎭 **Visual avatar system** - Interactive Mimi sprite with 10 emotional expressions
- 👻 **Hidden audio playback** - Voice plays without any windows appearing
- 🎯 **Audio queue system** - Speak multiple times rapidly without conflicts
- 🎮 **Interactive controls** - Drag, hide, show, and position the avatar
- 🔧 **Full MCP integration** - Voice and avatar tools work seamlessly with Claude Desktop

## Quick Start

### 1. Install Dependencies

```batch
# Install Node.js dependencies
install.bat

# Install Python dependencies for avatar
cd avatar
install_avatar_deps.bat
```

### 2. Copy Avatar Sprites

Manually copy PNG files from `C:\repos\screen-avatar\sprites\` to `avatar\library\`

### 3. Configure Claude Desktop

```batch
# Copy the example config
copy claude_desktop_config.json %APPDATA%\Claude\

# Or manually add the maid section to your existing config
# See docs/CLAUDE_CONFIG.md for details
```

### 4. Start Avatar System

```batch
cd avatar
start_avatar.bat
```

This starts:
- State server on http://localhost:3338
- Visual avatar window (Mimi appears on screen)

### 5. Restart Claude Desktop

The MCP server will load automatically with voice and avatar tools.

## Available Tools

### Voice Tools

#### speak
Convert text to speech with optional emotion
```javascript
{
  text: "Hello, Master!",
  emotion: "happy" // optional: neutral, happy, sad, excited, angry, shy
}
```

#### list_voices
Get list of available voices

#### set_voice
Change the current voice
```javascript
{
  voiceId: "ja-JP-MayuNeural" // or other available voices
}
```

### Avatar Tools

#### show_avatar
Display the avatar on screen
```javascript
{
  pose: "happy",  // optional: initial pose
  x: 1000,       // optional: X position
  y: 100         // optional: Y position
}
```

#### hide_avatar
Hide the avatar (keeps running in background)

#### set_avatar_pose
Change avatar emotional expression
```javascript
{
  pose: "thinking" // idle, happy, sad, thinking, talking, sleeping, angry, love, pick_up, write
}
```

#### move_avatar
Reposition the avatar
```javascript
{
  x: 500,
  y: 300
}
```

#### list_avatar_poses
List all available avatar poses

## Avatar Interaction

- **Right-click** - Hide avatar (stays running)
- **Double-click** - Close avatar permanently
- **Drag** - Move avatar (shows pick_up pose)
- **ESC key** - Close avatar permanently

## How It Works

### Voice System
- **msedge-tts** - Microsoft Edge's text-to-speech for neural voices
- **VBScript** - Hidden audio playback using WMPlayer.OCX
- **Audio Queue** - Sequential playback prevents file conflicts
- **Unique filenames** - Each audio gets timestamp-based unique name

### Avatar System
- **PyQt5** - Transparent, always-on-top window
- **Flask server** - State coordination between MCP and display
- **Mimi sprites** - 10 emotional states from screen-avatar project
- **Auto-show** - Avatar appears when pose/position changes while hidden

## Project Structure

```
maid-mcp/
├── maid-server.js          # Main MCP server with voice & avatar tools
├── package.json            # Node dependencies
├── install.bat             # Install script
├── claude_desktop_config.json  # Example config
├── avatar/                 # Visual avatar system
│   ├── avatar_display.py   # PyQt5 avatar window
│   ├── avatar_state_server.py  # Flask coordination server
│   ├── start_avatar.bat    # Launch avatar system
│   ├── library/            # Sprite PNG files
│   └── README.md           # Avatar documentation
├── docs/                   # Documentation
│   ├── AUDIO_SOLUTION.md   # Voice technical details
│   ├── AUDIO_QUEUE_SYSTEM.md  # Queue implementation
│   ├── CLAUDE_CONFIG.md    # Setup instructions
│   └── JAPANESE_ACCENT.md  # Voice configuration
├── tests/                  # Test files
│   ├── test-simple.js      # Voice test script
│   └── test-simple.bat     # Test runner
├── auto_claude/            # Python automation scripts
└── temp_voice/             # Temporary audio files
```

## Technical Details

### Voice Features
- Japanese accent using ja-JP-NanamiNeural (+20Hz base pitch)
- Emotion modulation through pitch/rate/volume adjustments
- Automatic audio file cleanup after playback
- Queue system for smooth consecutive speech

### Avatar Features
- 10 sprite states with smooth transitions
- Persistent between Claude conversations (right-click to hide)
- Automatic sprite change to "talking" during voice playback
- Position and state memory
- No taskbar icon (clean desktop)

## Troubleshooting

### Voice Issues
- If voice crashes with rapid speech, restart Claude Desktop
- Check `temp_voice/` folder for leftover audio files

### Avatar Issues
- If avatar won't appear, check if port 3338 is free
- If pick_up pose doesn't work, restart avatar display
- For sprite loading issues, verify PNG files in `avatar/library/`

### General
- Both systems can run independently
- State server must be running for avatar tools to work
- Avatar persists between Claude conversations when hidden

## Additional Tools

The `auto_claude/` folder contains Python scripts for programmatic control:
- `ultra_fast_sender.py` - Send messages to Claude Desktop
- `working_event_handler.py` - Event queue system for automation

## Development

Created by integrating:
- Voice synthesis from maid personality concept
- Avatar system from screen-avatar project
- MCP protocol for Claude Desktop integration

## License

MIT