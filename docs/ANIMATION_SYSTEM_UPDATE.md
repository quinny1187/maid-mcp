# Animation System Update

## Key Changes

### New Tool: list_poses
Shows all available PNG sprite files in the avatar/library folder:
```javascript
maid:list_poses()
// Returns: anger, happy, idle, love, master, etc.
```

### Smart Animation Fallback
If you try to play an animation that doesn't exist but a pose with that name does, it will automatically create a single-frame animation:

```javascript
maid:play_animation({ id: "love" })
// If "love" animation doesn't exist but love.png does,
// it creates a temporary animation: frames: ["love"], fps: 1
```

### Two Ways to View Content
1. **list_poses** - Shows raw PNG files available
2. **list_animations** - Shows defined animations (from animations.jsonl)

## Usage Flow

1. Check available poses:
   ```javascript
   maid:list_poses()
   ```

2. Play any pose as an animation:
   ```javascript
   maid:play_animation({ id: "love" })
   maid:play_animation({ id: "thinking" })
   ```

3. Create custom animations from poses:
   ```javascript
   maid:save_animation({
     id: "love_dance",
     name: "Love Dance", 
     frames: "love,idle,love,idle",
     fps: 3
   })
   ```

## Benefits
- No need to pre-define every single pose as an animation
- Can directly play any pose that exists
- Still get clean logging: "Playing animation: Love"
- Backwards compatible with saved animations

## Directory Structure
```
avatar/
└── library/
    ├── anger.png
    ├── happy.png
    ├── love.png
    ├── ... (other pose PNGs)
    └── animations/
        └── animations.jsonl  (saved animation definitions)
```
