# Animation Loading Issue Explained

## The Problem
- The `love` animation exists in animations.jsonl
- But `play_animation({ id: "love" })` returns "Unknown animation"
- Only animations created during the current session work

## Why This Happened
1. **Server Already Running** - When we refactored the animation system, the server was already running
2. **Animations Not Loaded** - The built-in animations in the file weren't loaded into memory
3. **Only New Ones Work** - Animations created with `create_animation` work because they're added to memory

## The Solution
**Restart Claude Desktop or the MCP server!**

When the server starts fresh, it will:
1. Call `loadAnimations()` 
2. Read the animations.jsonl file
3. Load all 17 animations into memory

## What Will Be Available After Restart

### Built-in Single Poses (9)
- idle, happy, love, anger, thinking, talking, sleeping, write, master

### Built-in Sequences (5)
- search_loop, treasure_hunt, greeting, happy_dance, sleepy

### Custom Animations (3)
- mimi_happy_dance, treasure_success, happy_dance_loop

## Testing After Restart
```javascript
maid:play_animation({ id: "love" })        // Will work!
maid:play_animation({ id: "treasure_hunt" }) // Built-in sequence
maid:list_animations()                      // Shows all 17
```

## Key Learning
The AnimationManager loads from file on startup, but changes during runtime only affect memory. Always restart after major system changes!
