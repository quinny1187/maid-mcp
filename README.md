# Maid-MCP 🎀

A full-featured MCP (Model Context Protocol) server that gives Claude Desktop a maid personality codenamed Mimi with Japanese-accented voice, visual avatar presence, and speech recognition capabilities. Best used with a Claude Max plan, Opus 4 is very good about managing all the maid tools while coding things for you. This project is specifically meant to be for fun, not for productivity. There are already a million productivity mcp servers.

![Example Image](https://github.com/quinny1187/maid-mcp/blob/main/avatar/library/idle.png)

## Features

- 🎵 **Japanese-accented voice** - Character voice using ja-JP neural voices, its part of her charm the voice is hard to understand. You can also have her change her voice at any time.
- 🎭 **Visual avatar system** - Interactive Mimi sprite with 16+ poses and animations  
- 🎤 **Speech recognition** - Talk to Claude naturally with voice input
- 👻 **Hidden audio playback** - Voice plays without any windows appearing
- 🎯 **Audio queue system** - Speak multiple times rapidly without conflicts
- 🎮 **Interactive controls** - Drag, hide, show, and animate the avatar
- 🔧 **Full MCP integration** - Voice and avatar tools work seamlessly with Claude Desktop

## Quick Start

### 1. Install Dependencies

```batch
# Install Node.js dependencies (if not already done)
npm install

# Install Python dependencies for voice input
cd voice
install_voice_deps.bat
cd ..

# Install Python dependencies for avatar (if needed)
cd avatar
install_avatar_deps.bat
cd ..
```

### 2. Configure Claude Desktop

Add to your `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "maid": {
      "command": "node",
      "args": ["path/to/maid-mcp/maid-server.js"]
    }
  }
}
```

Replace `path/to/maid-mcp` with the actual path where you cloned this repository.

### 3. Launch Everything

```batch
# Recommended: Use Python launcher for best process management
start_all_python.bat

# Alternative: Use enhanced batch launcher
start_all.bat
```

This automatically:
- ✨ Cleans up any existing processes
- 👤 Launches avatar display window
- 🖥️ Starts avatar state server (port 3338)
- 🎤 Opens voice input listener

### 4. Stop Everything

```batch
stop_all.bat
```

## Voice Loop 🎤→💬→🎀→🔊

1. **You speak** → Microphone picks up voice
2. **Speech recognition** → Converts to text  
3. **Ultra fast sender** → Sends to Claude Desktop
4. **Claude (Mimi) processes** → Understands and responds
5. **Voice synthesis** → Mimi speaks with Japanese accent
6. **Avatar reacts** → Visual feedback with animations

## Available MCP Tools

### Voice Tools 🔊

| Tool | Description | Parameters |
|------|-------------|------------|
| `speak` | Convert text to speech | `text`, `emotion` (optional) |
| `list_voices` | Get available voices | None |
| `set_voice` | Change current voice | `voiceId` |

**Emotions**: neutral, happy, sad, excited, angry, shy

### Avatar Tools 🎭

| Tool | Description | Parameters |
|------|-------------|------------|
| `show_avatar` | Display avatar on screen | `animation`, `x`, `y` (all optional) |
| `hide_avatar` | Hide avatar (keeps running) | None |
| `play_animation` | Play animation or pose | `id` |
| `stop_animation` | Stop current animation | None |
| `move_avatar` | Reposition avatar | `x`, `y` |
| `create_animation` | Create custom sequence | `id`, `name`, `frames`, `fps`, `loop` |
| `list_animations` | List all animations | None |
| `list_poses` | List available sprites | None |

## Avatar Interaction

| Action | Result |
|--------|--------|
| **Right-click** | Hide avatar (stays running) |
| **Double-click** | Close avatar permanently |
| **Left-click** | Cancel animation |
| **Drag** | Move avatar (shows pick_up pose) |
| **ESC key** | Close avatar permanently |

## Project Structure

```
maid-mcp/
├── maid-server.js          # Main MCP server
├── package.json            # Node.js dependencies
├── start_all_python.bat    # Recommended launcher
├── start_all.bat           # Alternative launcher
├── stop_all.bat            # Stop all systems
│
├── voice/                  # Voice system module
│   ├── outgoing/          # Text-to-speech engine
│   ├── incoming/          # Speech recognition
│   ├── README.md          # Voice documentation
│   └── [utility scripts]  # Calibration & setup tools
│
├── avatar/                 # Visual avatar system
│   ├── avatar_display.py  # PyQt5 window
│   ├── avatar_state_server.py  # Coordination server
│   ├── library/           # Sprite assets
│   │   ├── *.png         # Sprite images
│   │   └── animations/   # Animation definitions
│   └── README.md         # Avatar documentation
│
├── auto_claude/           # Claude Desktop automation
│   └── ultra_fast_sender.py  # Message sending
│
├── temp_voice/           # Temporary audio files
├── junk/                 # Archive of old implementations
└── needed_poses.md       # Wishlist for new sprites
```

## Voice Configuration

### Adjust Microphone Sensitivity

```batch
cd voice
adjust_sensitivity.bat
```

**Recommended sensitivity values**:
- Very Quiet Room: 1000-2000
- Normal Room: 2000-4000
- Office: 4000-6000
- Noisy: 6000-10000

### Calibrate Microphone

```batch
cd voice
calibrate_voice.bat
```

### Voice Settings

Edit `voice/incoming/voice_config.ini`:
```ini
[recognition]
energy_threshold = 8000  # Microphone sensitivity
message_cooldown = 3.0   # Seconds between messages
```

## Troubleshooting

### Voice Input Not Working
1. Check microphone permissions in Windows
2. Run calibration to verify microphone levels
3. Adjust energy_threshold if needed
4. Ensure Python dependencies are installed

### Multiple Avatar Windows
1. Use `start_all_python.bat` for better process management
2. Run `stop_all.bat` before starting again
3. Check Task Manager for lingering Python processes

### Audio Playback Issues
1. Check `temp_voice/` folder for audio files
2. Verify Windows Media Player is installed
3. Restart Claude Desktop if audio queue stuck

### Avatar Not Appearing
1. Verify port 3338 is free
2. Check if sprites exist in `avatar/library/`
3. Look for avatar window behind other windows

## Development Notes

### Adding New Voices
Edit `voice/outgoing/voiceConfig.js` to add more Edge TTS voices

### Creating New Poses
1. Add PNG file to `avatar/library/`
2. Use filename (without .png) as animation ID

### Custom Animations
```javascript
// Example: Create a greeting sequence
create_animation({
  id: "greeting",
  name: "Greeting Sequence",
  frames: "idle,happy,love,idle",
  fps: 2,
  loop: false
})
```

## Recent Updates

- **v2.1.0** - Enhanced process management and cleanup
- **v2.0.0** - Modular voice system with speech recognition  
- **Unified launcher** - Single command starts everything
- **Voice loop** - Complete bi-directional voice communication
- **Cleaner structure** - Organized into logical modules

## Credits

- Avatar sprites from screen-avatar project
- Voice synthesis using Microsoft Edge TTS
- Speech recognition via Google Speech API

## License

MIT
