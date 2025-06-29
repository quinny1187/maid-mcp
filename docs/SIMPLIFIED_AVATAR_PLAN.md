# Simplified Visual Avatar Plan

## Core Principle
The avatar is purely for emotional expression and presence. No text display.

## Communication Strategy
- **Voice**: All conversational responses
- **Chat**: Technical work, code, documentation  
- **Avatar**: Visual emotions and reactions only

## Minimal Implementation

### 1. Simple PyQt5 Avatar (no text components)
```python
# maid-visual.py
class MaidAvatar(QWidget):
    def __init__(self):
        super().__init__()
        self.sprites = {}
        self.init_ui()
        self.load_sprites()
        
    def init_ui(self):
        # Just a transparent sprite window
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.sprite_label = QLabel(self)
        self.resize(200, 300)
        
    def set_sprite(self, state):
        # Simply change the image
        if state in self.sprites:
            self.sprite_label.setPixmap(self.sprites[state])
```

### 2. MCP Tools (Simplified)
```javascript
// Only need basic controls
- show_avatar
- hide_avatar  
- set_emotion
- move_avatar (optional)
```

### 3. Automatic Behaviors

Since I can't show text, the avatar becomes more expressive:

**During Voice Playback:**
- Automatically switch to 'talking' sprite
- Return to contextual emotion when done

**Emotion Mapping:**
- Happy: Positive responses, greetings, success
- Sad: Empathy, unfortunate news
- Thinking: Processing, considering options
- Excited: Discoveries, breakthroughs
- Idle: Default state between interactions

**Smart Positioning:**
- Top-right corner: Default "assistant" position
- Move closer: Important announcements
- Hide: During focused work sessions

## Benefits of This Approach

1. **Clear Separation**:
   - Voice = Conversational
   - Text = Technical
   - Visual = Emotional

2. **No Sync Issues**:
   - No need to coordinate text display
   - Avatar just reflects mood

3. **Less Intrusive**:
   - No text boxes covering content
   - Pure emotional companion

4. **Simpler Implementation**:
   - Remove all text display code
   - Focus on sprite management
   - Easier state management

## Usage Examples

**Greeting:**
- Avatar appears with 'happy' sprite
- Voice: "Good morning, Master!"
- (No text display)

**Working on Code:**
- Avatar in 'thinking' pose
- No voice (using chat interface)
- Occasional expression changes

**Completion:**
- Avatar switches to 'excited'
- Voice: "I've completed the task!"
- Celebration animation

## Implementation Priority

1. Basic sprite display ✓
2. State server ✓
3. MCP integration ✓
4. Auto-emotion detection
5. Voice-to-sprite sync
6. Behavioral patterns