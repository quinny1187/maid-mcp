# Maid Avatar System

A visual avatar system for maid-mcp that displays Mimi as an interactive desktop companion controlled through MCP tools.

## Features

- **Transparent PyQt5 window** with Mimi sprite
- **Always on top** but won't block work
- **Draggable** (automatically shows pick_up pose when dragging)
- **10 emotion poses** from screen-avatar project
- **State persistence** between hide/show operations
- **Non-intrusive controls** with multiple interaction methods

## Quick Start

### First Time Setup

1. **Install Node.js dependencies** (from maid-mcp root):
   ```batch
   cd C:\repos\maid-mcp
   npm install                    # Installs axios for HTTP communication
   ```

2. **Copy Mimi's sprites** (manually copy from screen-avatar/sprites/ to avatar/library/):

3. **Install Python dependencies**:
   ```batch
   install_avatar_deps.bat       # Installs PyQt5, flask, flask-cors, requests
   ```

### Starting the Avatar

```batch
cd C:\repos\maid-mcp\avatar
start_avatar.bat
```

This launches:
- State server on http://localhost:3338
- Avatar display window (appears at position 1000, 100)

### Testing the System

Once running, use Claude's avatar commands to test functionality.

## How to Use

### Window Controls

- **Right-click** - Hide the avatar (keeps running in background)
- **Double-click** - Close the avatar permanently
- **ESC key** - Close the avatar permanently
- **Left-click drag** - Move the avatar around

### Claude MCP Commands

Through Claude, you can control the avatar with natural language:

**Show/Hide:**
- "Show yourself" - Display the avatar
- "Hide for now" - Hide the avatar
- "Disappear" - Hide the avatar

**Change Emotions:**
- "Look happy!" - Change to happy pose
- "Show me you're thinking" - Change to thinking pose
- "Be excited!" - Change to excited pose

**Move Around:**
- "Move to the left side" - Reposition avatar
- "Go to the center" - Move to screen center
- "Move to position 500, 300" - Specific coordinates

### Available MCP Tools

The following tools are added to maid-server.js:

- `show_avatar` - Display avatar with initial pose and position
- `hide_avatar` - Hide the avatar (keeps running)
- `set_avatar_pose` - Change emotional expression
- `move_avatar` - Reposition on screen
- `list_avatar_poses` - List all available poses

### Available Poses

- **idle** - Default relaxed state
- **happy** - Joyful expression
- **sad** - Sad or sympathetic
- **thinking** - Deep in thought
- **talking** - Speaking (auto-used during voice)
- **sleeping** - Resting state
- **angry** - Frustrated expression
- **love** - Affectionate
- **pick_up** - Being moved (auto when dragging)
- **write** - Taking notes
- **master** - Default master pose

## System Architecture

```
Claude Desktop
     ↓ (MCP Tools)
maid-server.js 
     ↓ (HTTP POST to localhost:3338)
State Server (Flask)
     ↓ (Polling every 100ms)
Avatar Display (PyQt5)
```

### File Structure

```
maid-mcp/
└── avatar/
    ├── library/                    # Sprite PNG files
    ├── avatar_display.py          # PyQt5 avatar window
    ├── avatar_state_server.py     # Flask coordination server
    ├── start_avatar.bat           # Launches both components
    └── install_avatar_deps.bat    # Installs Python packages
```

## Important Behavior

### Auto-Show Feature
- Setting a pose automatically shows the avatar if hidden
- Moving the avatar automatically shows it if hidden
- No need to explicitly call `show_avatar` before expressing emotions
- Makes interaction more natural and intuitive

### Right-Click = Hide (Not Close!)
- Right-clicking **hides** the avatar but keeps it running
- The avatar can instantly reappear without restarting
- Perfect for hiding between conversations
- State (position, pose) is preserved

### Automatic Behaviors
- **Auto-show when setting pose** - Avatar appears automatically if hidden
- **Auto-show when moving** - Avatar appears automatically if repositioned
- Changes to `pick_up` pose when being dragged
- Switches to `talking` pose during voice playback
- Returns to previous pose after special actions

### Default Settings
- Initial position: (1000, 100) - top-right area
- Initial pose: idle
- Window size: 200x300 pixels
- Polling rate: 100ms

## Troubleshooting

**Avatar won't appear:**
- Ensure Python is installed and in PATH
- Check if port 3338 is free
- Run `start_avatar.bat` from the avatar folder
- Check for error messages in the console

**Avatar won't reappear after hiding:**
- Make sure you're using the updated avatar_display.py
- The state server must be running
- Try using Python directly to diagnose

**Can't move or interact with avatar:**
- Ensure the avatar window has focus
- Try clicking on the avatar first
- Check if state server is responding

**Sprites not loading:**
- Manually copy PNG files from C:\repos\screen-avatar\sprites\ to avatar\library\
- Verify PNG files exist in avatar/library/
- Check console for "Loaded sprite:" messages

## Adding Custom Poses

1. Add new PNG files to `avatar/library/`
2. Name them descriptively (e.g., `winking.png`, `thumbs_up.png`)
3. No code changes needed - poses are discovered automatically
4. Use `list_avatar_poses` to see all available poses

## Advanced Usage

### Running Components Separately

If you need to run components individually:

```batch
# Terminal 1: State Server
python avatar_state_server.py

# Terminal 2: Avatar Display
python avatar_display.py
```

### Restarting Just the Display

If you need to restart only the avatar display (e.g., after code changes):

```batch
# Close the current avatar (double-click or ESC)
# Then run:
python avatar_display.py
```

## Integration with Voice

The avatar automatically coordinates with the voice system:
- Shows `talking` pose during speech
- Returns to contextual pose after speaking
- Emotions in voice can trigger matching avatar poses

## Tips

- Keep the state server running between Claude conversations
- Right-click to quickly hide when you need screen space
- Drag Mimi to your preferred screen location
- The avatar remembers its last position
- Add custom sprites to personalize your assistant

## Future Enhancements

- Dynamic pose discovery with metadata
- Animated transitions between poses
- Seasonal/themed sprite sets
- Multi-monitor awareness
- Gesture sequences for complex emotions