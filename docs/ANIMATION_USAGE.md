# Animation Usage Examples

## Simple Usage from Claude

Here's how easy it is to use the animation system:

### Example 1: Search Animation
```javascript
maid:start_animation({
  sequence: "search_1,search_2,search_1,search_2,search_3",
  fps: 2
})
```

### Example 2: Happy Dance
```javascript
maid:start_animation({
  sequence: "happy,idle,happy,idle",
  fps: 10
})
```

### Example 3: Thinking Loop
```javascript
maid:start_animation({
  sequence: "thinking,write,thinking,write",
  fps: 1,
  loop: true
})
```

### Example 4: Sleepy Animation
```javascript
maid:start_animation({
  sequence: "idle,sleeping,idle,sleeping,sleeping",
  fps: 0.5  // Very slow
})
```

### Example 5: Treasure Hunt Success
```javascript
maid:start_animation({
  sequence: "search_1,search_2,search_1,search_2,search_3,search_3",
  fps: 1.5
})
```

## How It Works

1. **sequence**: Just list the poses separated by commas
2. **fps**: How fast to play (frames per second)
   - 0.5 = very slow
   - 1-2 = normal speed  
   - 5+ = fast
3. **loop**: Keep repeating? (true/false)

## Stopping Animations

- **Left-click the avatar**: Cancels animation and returns to idle
- **Use set_avatar_pose**: Set any pose to stop animation
- **Use stop_animation**: Explicitly stop any running animation
- **Hide the avatar**: Stops animation and hides
- **Start a new animation**: Replaces the current one

## Tips

- You can repeat poses to make them last longer
- Higher FPS = faster animation
- Animation auto-shows the avatar if hidden
- Left-click avatar to cancel animation and return to idle
- Dragging avatar pauses animation updates until released

## Common Patterns

- **Alternating**: "pose1,pose2,pose1,pose2"
- **Build-up**: "pose1,pose1,pose2,pose2,pose3"
- **Flash**: "pose1,pose2" with high FPS
- **Emphasis**: "idle,action,action,action,idle"
