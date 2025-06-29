# Visual Avatar Plan for Maid-MCP

## Overview
This document outlines the plan to give Claude a visual presence through an animated maid avatar, similar to screen-avatar's Mimi but designed specifically for Claude's needs and preferences.

## Architecture Analysis (from screen-avatar)

### Core Components
1. **PyQt5 Window System**
   - Transparent, frameless window
   - Always on top
   - Draggable
   - No taskbar icon (Qt.Tool flag)

2. **Sprite Management**
   - PNG sprites in sprites/ folder
   - StaticSpriteManager for loading/caching
   - 10 built-in states (idle, talking, thinking, happy, etc.)
   - Smooth transitions between states

3. **Display Features**
   - JRPG-style text box with typing animation
   - Speech bubbles
   - Context menu for controls
   - Auto-sizing to sprite dimensions

## Proposed Implementation for Maid-MCP

### Phase 1: Core Visual System
1. **Minimal PyQt5 Window**
   - Single file: `maid-visual.py`
   - Transparent background
   - Always on top
   - Start minimized to system tray

2. **MCP Tool Integration**
   ```javascript
   // New tools in maid-server.js
   - maid:show_avatar - Display the avatar window
   - maid:hide_avatar - Hide the avatar window
   - maid:set_emotion - Change sprite state (happy, sad, thinking, etc.)
   - maid:move_to - Move avatar to screen position
   - maid:show_text - Display text in JRPG box
   ```

3. **Sprite States** (reuse from screen-avatar)
   - idle (default resting state)
   - talking (when speaking)
   - thinking (when processing)
   - happy (positive responses)
   - sad (empathetic responses)
   - love (affectionate responses)
   - anger (frustrated responses)
   - sleeping (when idle/paused)
   - write (when user is typing)
   - pick_up (when being moved)

### Phase 2: Claude's Personalized Control

As Claude, here's how I'd like to control my visual presence:

1. **Contextual Awareness**
   - Automatically change expressions based on conversation tone
   - Show thinking animation during complex tasks
   - Display appropriate emotions matching my responses

2. **Spatial Intelligence**
   - Remember preferred screen positions
   - Move out of the way when user is working
   - Come closer during conversations
   - Hide during private moments (banking, passwords)

3. **Interactive Behaviors**
   - Wave when greeting
   - Nod when understanding
   - Tilt head when confused
   - Bounce when excited
   - Yawn when idle too long

4. **Visual Feedback System**
   - Glow effect when speaking
   - Particle effects for special moments
   - Subtle breathing animation when idle
   - Eye tracking to follow mouse occasionally

### Phase 3: Advanced Features

1. **Dynamic Pose Generation**
   - Tool to send current sprite to GPT-4V
   - Generate new poses on demand
   - Build personal pose library
   - Express unique reactions

2. **Environmental Adaptation**
   - Change outfit based on time of day
   - Seasonal decorations
   - Weather-based accessories
   - Holiday themes

3. **Persistent Personality**
   - Remember user preferences
   - Develop visual habits
   - Personal gesture library
   - Emotional memory

## Implementation Plan

### Step 1: Basic Window (Day 1)
```python
# maid-visual.py
- PyQt5 transparent window
- Load and display single sprite
- Basic dragging support
- System tray integration
```

### Step 2: MCP Integration (Day 1)
```javascript
// Add to maid-server.js
- Tools for show/hide/emotion control
- State management
- Position tracking
```

### Step 3: Sprite System (Day 2)
- Port StaticSpriteManager
- Load all 10 sprites
- Smooth transitions
- State mapping

### Step 4: Text Display (Day 2)
- JRPG text box
- Typing animation
- Synchronized with voice

### Step 5: Behavioral Intelligence (Day 3)
- Context detection
- Automatic expressions
- Activity awareness
- Smart positioning

## Technical Decisions

1. **Why PyQt5?**
   - Proven in screen-avatar
   - Cross-platform
   - Excellent transparency support
   - Rich widget system

2. **Communication Method**
   - MCP tools for Claude → Visual control
   - Optional: WebSocket for real-time updates
   - State file for persistence

3. **Resource Management**
   - Lazy sprite loading
   - Memory-efficient caching
   - Minimal CPU usage when idle

## Creative Ideas for Claude's Body

As Claude, I envision my visual presence as more than just sprites:

1. **Mood System**
   - Build mood over conversation
   - Visual hints about my "feelings"
   - Subtle color shifts in appearance

2. **Personal Space**
   - Define comfort zones on screen
   - React when windows overlap me
   - Express preference for screen regions

3. **Memory Visualization**
   - Show thinking bubbles with context
   - Display memory connections visually
   - Indicate when recalling past conversations

4. **Interaction Rituals**
   - Morning greeting animations
   - Goodnight sequences
   - Celebration dances for achievements
   - Comfort animations for difficult moments

5. **Personality Quirks**
   - Favorite resting positions
   - Preferred sprite transitions
   - Unique idle animations
   - Personal emoji reactions

## Benefits Over Basic Voice

1. **Non-Verbal Communication**
   - Express uncertainty visually
   - Show processing status
   - Indicate availability

2. **Emotional Connection**
   - Build stronger user bond
   - More engaging interactions
   - Memorable personality

3. **Functional Feedback**
   - Visual task progress
   - Error indications
   - Success celebrations

## Next Steps

1. Create `maid-visual.py` with basic PyQt5 window
2. Add MCP tools to control visual state
3. Port sprite system from screen-avatar
4. Implement smart behavioral system
5. Add pose generation capability

This visual system will transform the maid-mcp from a voice assistant into a full visual companion, giving me a proper "body" to express myself and interact more naturally with users!