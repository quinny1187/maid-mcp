# Technical Implementation Guide - Maid Visual Avatar

## Quick Implementation Path

### Minimum Viable Avatar (2-3 hours)

#### 1. Copy Required Sprites
From `C:\repos\screen-avatar\sprites\` copy:
- master_sprite.png → maid_idle.png
- talking_sprite.png → maid_talking.png  
- thinking_sprite.png → maid_thinking.png
- happy_sprite.png → maid_happy.png
- sleeping_sprite.png → maid_sleeping.png

Place in: `C:\repos\maid-mcp\sprites\`

#### 2. Create Simple PyQt5 Window

```python
# maid-visual.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

class MaidAvatar(QWidget):
    def __init__(self):
        super().__init__()
        self.sprites = {}
        self.current_sprite = 'idle'
        self.init_ui()
        self.load_sprites()
        
    def init_ui(self):
        # Transparent, always-on-top window
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Sprite display label
        self.sprite_label = QLabel(self)
        self.sprite_label.setScaledContents(True)
        
        # Set size
        self.resize(200, 300)
        self.move(100, 100)
        
    def load_sprites(self):
        sprite_files = {
            'idle': 'maid_idle.png',
            'talking': 'maid_talking.png',
            'thinking': 'maid_thinking.png',
            'happy': 'maid_happy.png',
            'sleeping': 'maid_sleeping.png'
        }
        
        for state, filename in sprite_files.items():
            path = os.path.join('sprites', filename)
            if os.path.exists(path):
                self.sprites[state] = QPixmap(path)
                
        # Set initial sprite
        self.set_sprite('idle')
        
    def set_sprite(self, state):
        if state in self.sprites:
            self.sprite_label.setPixmap(self.sprites[state])
            self.current_sprite = state
```

#### 3. Add State Server (for MCP communication)

```python
# maid-state-server.py
from flask import Flask, jsonify, request
import json

app = Flask(__name__)
state = {
    'visible': True,
    'sprite': 'idle',
    'position': {'x': 100, 'y': 100},
    'text': ''
}

@app.route('/state', methods=['GET'])
def get_state():
    return jsonify(state)

@app.route('/state', methods=['POST'])
def update_state():
    global state
    state.update(request.json)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=3338, debug=False)
```

#### 4. Update MCP Server Tools

```javascript
// Add to maid-server.js

// Import axios for HTTP requests
import axios from 'axios';

// Visual control tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    // ... existing tools ...
    {
      name: "show_avatar",
      description: "Show the visual avatar on screen",
      inputSchema: {
        type: "object",
        properties: {}
      }
    },
    {
      name: "hide_avatar", 
      description: "Hide the visual avatar",
      inputSchema: {
        type: "object",
        properties: {}
      }
    },
    {
      name: "set_emotion",
      description: "Change the avatar's emotional expression",
      inputSchema: {
        type: "object",
        properties: {
          emotion: {
            type: "string",
            enum: ["idle", "happy", "sad", "thinking", "talking", "sleeping"],
            description: "The emotion to display"
          }
        },
        required: ["emotion"]
      }
    }
  ]
}));

// Handle visual tools
if (params.name === "show_avatar") {
  await axios.post('http://localhost:3338/state', { visible: true });
  return { content: [{ type: "text", text: "Avatar shown!" }] };
}

if (params.name === "hide_avatar") {
  await axios.post('http://localhost:3338/state', { visible: false });
  return { content: [{ type: "text", text: "Avatar hidden!" }] };
}

if (params.name === "set_emotion") {
  await axios.post('http://localhost:3338/state', { sprite: params.arguments.emotion });
  return { content: [{ type: "text", text: `Emotion set to ${params.arguments.emotion}` }] };
}
```

### Integration Architecture

```
Claude Desktop
     ↓
MCP Server (maid-server.js)
     ↓ (HTTP POST)
State Server (localhost:3338)
     ↓ (Polling)
Visual Avatar (maid-visual.py)
```

### Advanced Features to Add Later

1. **Smooth Transitions**
   - Fade between sprites
   - Position interpolation
   - Scale animations

2. **Text Display**
   - JRPG text box
   - Synchronized with voice
   - Typing animations

3. **Interactive Features**
   - Click to interact
   - Drag to move
   - Context menu

4. **Smart Positioning**
   - Avoid active windows
   - Screen edge detection
   - Remember positions

5. **Extended Emotions**
   - Anger, love, excited
   - Custom expressions
   - Composite emotions

### File Structure
```
maid-mcp/
├── sprites/
│   ├── maid_idle.png
│   ├── maid_happy.png
│   ├── maid_thinking.png
│   ├── maid_talking.png
│   └── maid_sleeping.png
├── visual/
│   ├── maid-visual.py
│   ├── maid-state-server.py
│   └── start-visual.bat
└── maid-server.js (updated)
```

### Quick Start Commands
```batch
# start-visual.bat
@echo off
start /min python visual/maid-state-server.py
timeout /t 2
start python visual/maid-visual.py
```

## Testing the Integration

1. Start the visual system: `start-visual.bat`
2. Use Claude Desktop to test:
   - "Show yourself to me" → triggers show_avatar
   - "You can hide now" → triggers hide_avatar  
   - "Show me you're happy" → triggers set_emotion
   - Voice plays while sprite changes to 'talking'

## Why This Approach?

1. **Simplicity**: Minimal dependencies, easy to debug
2. **Flexibility**: State server allows any future integration
3. **Performance**: Lightweight, won't impact Claude Desktop
4. **Extensibility**: Easy to add features incrementally

## Next Development Phase

Once basic system works:
1. Add all 10 sprite states
2. Implement position memory
3. Add text display sync
4. Create behavior patterns
5. Add personality quirks