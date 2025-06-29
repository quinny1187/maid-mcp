# Animation System Implementation Plan

## Overview
Create a simple animation system for the maid avatar that can play sequences of PNG images with transparent backgrounds, simulating GIF-like animations while maintaining transparency.

## Design Philosophy
**SIMPLE IS BEST** - The system must be incredibly easy for Claude to understand and use without complex syntax or configuration.

## Proposed Implementation

### 1. Single MCP Tool Approach
Create one new tool: `animate_avatar` that handles all animation needs.

```javascript
// Example usage (proposed):
maid:animate_avatar({
  sequence: "search_1,search_2,search_1,search_2,search_3",
  duration: 3000,  // total animation duration in ms
  loop: false      // whether to repeat
})
```

### 2. Animation Definition Format

**Option A: Simple String Sequence** (RECOMMENDED)
- Just list the poses in order: `"search_1,search_2,search_1,search_2,search_3"`
- System automatically divides total duration equally among frames
- Easiest to understand and use

**Option B: Timing Per Frame**
- Include timing: `"search_1:500,search_2:500,search_1:500,search_2:500,search_3:1000"`
- More control but harder to use

**Option C: Structured Array**
- `[{pose: "search_1", ms: 500}, {pose: "search_2", ms: 500}]`
- Most flexible but most complex

### 3. Recommended Approach: Simple String Sequence

The simplest implementation that covers most use cases:

```javascript
maid:animate_avatar({
  sequence: "search_1,search_2,search_3",
  fps: 2  // frames per second (default: 2)
})
```

Benefits:
- Dead simple to use
- No complex timing calculations
- Can repeat poses just by listing them again
- FPS parameter is intuitive

### 4. Common Animation Patterns

```javascript
// Searching animation (alternating 1-2 then show 3)
"search_1,search_2,search_1,search_2,search_3"

// Continuous search loop
"search_1,search_2,search_3" with loop: true

// Quick flash effect
"happy,idle,happy,idle" with fps: 10

// Typing animation
"write,thinking,write,thinking" with fps: 1
```

### 5. Implementation Details

**Avatar Side (PyQt5)**:
- Add `/animate` endpoint to state server
- Animation thread that updates current sprite based on sequence
- Automatic cleanup when animation ends

**MCP Server Side**:
- New `animate_avatar` tool registration
- Validation of pose names
- Send animation data to avatar state server

**Key Features**:
- If avatar is hidden, it auto-shows when animation starts
- Animation stops if user manually changes pose
- Can interrupt animation with new animation
- Returns to 'idle' pose when animation completes (unless looping)

### 6. File Organization

New animation sprites should follow naming convention:
- `[base_pose]_[frame_number].png`
- Examples: `search_1.png`, `search_2.png`, `search_3.png`
- Place in existing `sprites/` directory

### 7. Why This Approach?

1. **Incredibly Simple**: Just list poses in order, set FPS
2. **Flexible**: Can create any pattern by repeating poses
3. **Intuitive**: FPS is easier to understand than milliseconds
4. **No Math**: Claude doesn't need to calculate frame timings
5. **Clean**: One tool does everything

### 8. Alternative Consideration: Preset Animations

Could also add preset animations for common actions:
```javascript
maid:animate_avatar({
  preset: "searching"  // built-in animation
})
```

But this adds complexity and reduces flexibility. Better to keep it simple with custom sequences.

## Conclusion

The recommended approach is a single `animate_avatar` tool that accepts:
- A comma-separated string of pose names
- An FPS value (frames per second)
- Optional loop flag

This gives maximum flexibility with minimum complexity, making it incredibly easy for Claude to create any animation pattern just by listing poses in order.

## Next Steps

1. Add `search_1.png`, `search_2.png`, `search_3.png` to sprites folder
2. Implement `/animate` endpoint in avatar state server
3. Add `animate_avatar` tool to MCP server
4. Test with various animation patterns
5. Document usage examples