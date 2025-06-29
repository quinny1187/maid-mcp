# Animation System Usage Guide (Updated)

## Overview
Everything is now an animation! Single poses are just one-frame animations.

## Basic Usage

### Playing Animations
```javascript
// Single pose (replaces old set_avatar_pose)
maid:play_animation({ id: "happy" })

// Built-in sequence
maid:play_animation({ id: "treasure_hunt" })

// Custom saved animation
maid:play_animation({ id: "my_dance" })
```

### Stopping Animations
```javascript
maid:stop_animation()
```

### Saving Custom Animations
```javascript
maid:save_animation({
  id: "victory_dance",
  name: "Victory Dance",
  frames: "happy,love,happy,love",
  fps: 5,
  loop: false
})
```

### Listing Available Animations
```javascript
maid:list_animations()
// Shows:
// 📷 Single Poses (idle, happy, love, etc.)
// 🎬 Built-in Sequences (treasure_hunt, greeting, etc.)
// ⭐ Custom Animations (your saved animations)
```

## Built-in Animations

### Single Poses (1 frame each)
- `idle` - Standing with serving tray
- `happy` - Jumping with excitement
- `love` - Heart eyes
- `anger` - Hands on hips
- `thinking` - Hand on chin
- `talking` - Explaining gesture
- `sleeping` - Leaning on broom
- `write` - Writing (back view)
- `master` - Arms spread wide

### Pre-made Sequences
- `search_loop` - Continuous searching (loops)
- `treasure_hunt` - Complete search with victory
- `greeting` - Professional maid greeting
- `happy_dance` - Quick celebration
- `sleepy` - Getting tired animation

## Examples

### Show Avatar with Animation
```javascript
maid:show_avatar({ 
  animation: "greeting",
  x: 1200,
  y: 100 
})
```

### Create and Play Custom Animation
```javascript
// Save it
maid:save_animation({
  id: "search_victory",
  name: "Found It!",
  frames: "thinking,search_1,search_2,search_3,happy,happy",
  fps: 2
})

// Play it
maid:play_animation({ id: "search_victory" })
```

### Quick Emotions
```javascript
maid:play_animation({ id: "happy" })    // Single happy jump
maid:play_animation({ id: "love" })     // Heart eyes
maid:play_animation({ id: "thinking" }) // Contemplative
```

## Clean Logging

The new system provides clean logs:
- When animation starts: `Playing animation: Victory Dance`
- When animation completes: `Animation complete: victory_dance`
- No more sprite spam in the logs!

## Tips

- Use descriptive IDs for custom animations (e.g., "wake_up_routine")
- Higher FPS = faster animation (0.5-10 range works well)
- Loop animations for continuous effects
- Combine poses creatively for storytelling

## Migration from Old System

| Old Way | New Way |
|---------|---------|
| `set_avatar_pose({ pose: "happy" })` | `play_animation({ id: "happy" })` |
| `start_animation({ sequence: "..." })` | Save as animation, then play by ID |
| `list_avatar_poses()` | `list_animations()` (shows all options) |
