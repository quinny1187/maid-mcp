# 🎌 maid-mcp Voice System - Japanese Accent Edition

## ✅ Updates Complete!

### 🎤 What's New:
1. **No Media Player Window** - Uses `node-wav-player` for background audio playback
2. **Japanese Accent Configuration** - Matches screen-avatar project settings:
   - Default voice: `ja-JP-NanamiNeural` (cute Japanese voice)
   - Base pitch: `+20Hz` (higher pitch for authentic Japanese accent)
   - Emotion modulation adds to base pitch

### 🗾 Japanese Accent Settings:
- **Nanami** (default): +20Hz pitch - Young, cute voice
- **Mayu**: +15Hz pitch - Gentle, soft voice  
- **Aoi**: +10Hz pitch - Energetic voice

### 📦 Installation:
```bash
cd C:\repos\maid-mcp
npm install
```

This installs:
- `@modelcontextprotocol/sdk` - MCP framework
- `msedge-tts` - Text-to-speech engine

### 🔊 Audio Playback:
- Uses Windows default audio player (opens minimized)
- Simple and reliable approach
- For completely hidden playback, consider future enhancements

### 🧪 Test the Voice:
```bash
node test-simple.js
```

You should hear:
- Japanese-accented English speech
- No media player window opens
- Audio plays directly in background

### 🎮 For Claude Desktop:
1. Copy `claude_desktop_config.json` to `%APPDATA%\Claude\`
2. Restart Claude Desktop
3. Use voice commands:
   - "Use the speak tool to say hello"
   - "Speak 'I am happy to help!' with happy emotion"
   - "Set voice to ja-JP-MayuNeural"

### 🎭 Emotion Effects:
- **neutral**: Base pitch only
- **happy**: +10Hz added (cheerful)
- **sad**: -5Hz (lower tone)
- **excited**: +15Hz (very energetic)
- **angry**: -10Hz (stern)
- **shy**: +5Hz, quieter

The voice system now matches the screen-avatar project's Japanese accent configuration! 🌸
