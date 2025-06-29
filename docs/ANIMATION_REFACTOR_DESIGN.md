# Animation System Refactor Design

## Overview
Refactor the avatar system to treat everything as animations, where single poses are just one-frame animations. This simplifies the architecture and makes it more flexible.

## Benefits
1. **Unified System** - No distinction between poses and animations
2. **Cleaner Logs** - Just "Playing animation: idle" instead of pose spam
3. **Fewer Tools** - Remove set_avatar_pose, everything uses play_animation
4. **Saved Animations** - Store custom animation sequences for reuse
5. **More Flexible** - Can easily create and save complex sequences

## New Architecture

### Animation Format
```json
{"id": "idle", "name": "Idle Pose", "frames": ["idle"], "fps": 1, "loop": false}
{"id": "happy", "name": "Happy Jump", "frames": ["happy"], "fps": 1, "loop": false}
{"id": "love", "name": "Heart Eyes", "frames": ["love"], "fps": 1, "loop": false}
{"id": "thinking", "name": "Thinking", "frames": ["thinking"], "fps": 1, "loop": false}
{"id": "search_loop", "name": "Searching Loop", "frames": ["search_1", "search_2"], "fps": 2, "loop": true}
{"id": "treasure_found", "name": "Found Treasure!", "frames": ["search_1", "search_2", "search_1", "search_2", "search_3", "happy"], "fps": 1.5, "loop": false}
{"id": "greeting", "name": "Maid Greeting", "frames": ["master", "idle", "talking", "idle"], "fps": 1, "loop": false}
```

### File Location
- `C:\repos\maid-mcp\avatar\library\animations\animations.jsonl`
- Located in avatar library alongside sprite images
- JSON Lines format for easy appending
- Keeps animations with other avatar assets

### New MCP Tools

1. **play_animation**
   ```javascript
   play_animation({ id: "idle" })  // Play built-in or saved animation
   play_animation({ id: "treasure_found" })  // Play custom sequence
   ```

2. **stop_animation**
   - Same as current

3. **save_animation**
   ```javascript
   save_animation({
     id: "my_dance",
     name: "My Custom Dance",
     frames: "happy,idle,happy,idle,love",
     fps: 3,
     loop: false
   })
   ```

4. **list_animations**
   - Returns all built-in poses + saved animations
   - Shows name, frames, fps, loop settings

### Implementation Steps

1. **Create animations.jsonl** with all built-in poses as single-frame animations
2. **Update state server** to log "Playing animation: X" instead of individual frames
3. **Refactor MCP server** to new tool structure
4. **Update avatar display** to only show animation changes in logs
5. **Remove set_avatar_pose** tool entirely

### Migration Path

1. First, add new tools alongside old ones
2. Test new system
3. Remove old tools once confirmed working
4. Update all documentation

### Example Usage

```javascript
// Single pose (replaces set_avatar_pose)
maid:play_animation({ id: "happy" })

// Built-in sequence
maid:play_animation({ id: "treasure_found" })

// Create and save new animation
maid:save_animation({
  id: "sleepy_maid",
  name: "Getting Sleepy",
  frames: "idle,sleeping,idle,sleeping,sleeping",
  fps: 0.5,
  loop: false
})

// Play saved animation
maid:play_animation({ id: "sleepy_maid" })

// List all available
maid:list_animations()
// Returns: idle, happy, love, thinking, treasure_found, greeting, sleepy_maid, etc.
```

### Log Output Example

Before:
```
Set sprite to: happy
Set sprite to: idle  
Set sprite to: happy
Set sprite to: idle
```

After:
```
Playing animation: happy_dance
Animation complete: happy_dance
```

## Questions for Implementation

1. Should we auto-generate IDs from names? (e.g., "My Dance" -> "my_dance")
2. Should we have categories? (poses, sequences, custom)
3. Maximum saved animations limit?
4. Allow overwriting existing animations?

## Conclusion

This refactor would make the system much cleaner and more powerful while reducing complexity. Everything becomes an animation, making it easier to understand and use.
