# Avatar System for Maid-MCP

A PyQt5-based visual avatar system with GIF support and smooth animations.

## Features

- **Transparent Window**: Always-on-top, draggable avatar with no window frame
- **16 PNG Sprites**: Various emotional and action poses
- **Smooth Animations**: Pose-based timing system (not frame-based)
- **GIF Support**: Can display animated GIFs temporarily
- **MCP Integration**: Controlled via Claude Desktop tools

## Components

### 1. `avatar_display.py`
Main PyQt5 window that displays sprites and GIFs
- Polls state server at 50ms intervals (20Hz)
- Uses local animation timing for smooth playback
- Handles both sprites and animated GIFs
- Smart GIF caching based on file size

### 2. `avatar_state_server.py`
Flask server running on port 3338
- Manages avatar state (visible, pose, position, animation)
- Provides REST API for MCP server communication
- Handles GIF display requests

### 3. `library/` folder
- **16 PNG sprites**: idle, happy, love, anger, thinking, talking, sleeping, write, master, pick_up, search_1/2/3, point_left/right/up
- **animations/animations.jsonl**: Animation definitions with pose sequences

## Animation System

### Pose-Based Timing
- Each pose displays for a specified duration (default: 2 seconds)
- No more confusing FPS calculations
- Animations are sequences of poses, not frames

### Example Animation:
```json
{
  "id": "celebration_dance",
  "name": "Celebration Dance",
  "frames": ["happy", "search_3", "happy", "search_3", "happy", "idle"],
  "duration_per_pose": 0.75,
  "loop": false
}
```
This shows each pose for 0.75 seconds, total duration: 4.5 seconds

## Controls

- **Left-click**: Cancel animation or hide GIF
- **Right-click**: Hide avatar (keeps running)
- **Double-click**: Close permanently
- **Drag**: Move avatar (shows pick_up pose)
- **ESC**: Close

## Starting the Avatar

Run both components:
```batch
python avatar_state_server.py
python avatar_display.py
```

Or use the batch files:
```batch
start_avatar.bat
```

## Requirements

- Python 3.x
- PyQt5
- Flask
- Flask-CORS
- requests

Install with:
```batch
install_avatar_deps.bat
```

## Integration with MCP

The avatar is controlled through the maid-server.js MCP tools:
- `show_avatar` - Display avatar with optional animation
- `hide_avatar` - Hide the avatar
- `move_avatar` - Move to specific position
- `play_animation` - Play any animation
- `stop_animation` - Stop current animation
- `create_animation` - Create custom animations
- `list_animations` - List all available animations
- `list_poses` - List all sprite poses

## GIF Integration

Works with the Giphy MCP server to display animated GIFs:
- GIFs temporarily replace the avatar
- Window expands to 400px width for landscape GIFs
- Returns to avatar after GIF duration expires
- Smooth transition between GIF and animation modes
