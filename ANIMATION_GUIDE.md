# Maid-MCP Animation System Documentation

## Overview

The Maid-MCP animation system uses a **pose-based timing** approach where each distinct pose is displayed for a specified duration, creating smooth and natural animations.

## Key Concepts

### Poses vs Frames
- **Pose**: A distinct visual state (e.g., "happy", "idle", "point_left")
- **Frame**: In our system, this is deprecated - we use poses instead
- Each pose displays for a configurable duration (default: 2 seconds)

### Animation Structure
```json
{
  "id": "unique_identifier",
  "name": "Display Name",
  "frames": ["pose1", "pose2", "pose3"],
  "duration_per_pose": 1.5,
  "loop": false,
  "builtin": true
}
```

## Available Poses (16 total)

### Emotional States
- `idle` - Default pose with serving tray
- `happy` - Jumping with excitement
- `love` - Heart eyes expression
- `anger` - Hands on hips, stern look
- `thinking` - Hand on chin, contemplative
- `sleeping` - Resting with broom

### Actions
- `talking` - Explaining gesture
- `write` - Writing, back view
- `master` - Arms spread wide
- `pick_up` - Shown when dragging avatar

### Pointing Poses
- `point_left` - Pointing to the left
- `point_right` - Pointing to the right  
- `point_up` - Pointing upward/idea gesture

### Special Sequences
- `search_1` - Looking/searching pose 1
- `search_2` - Looking/searching pose 2
- `search_3` - Victory pose with treasure

## Built-in Animations

### Single Poses (2 seconds each)
- All individual poses can be played as animations

### Sequences

#### celebration_dance
- Poses: happy → search_3 → happy → search_3 → happy → idle
- Duration: 0.75s per pose (4.5s total)
- Energetic celebration sequence

#### tour_guide
- Poses: idle → point_up → talking → point_left → point_right → point_up → happy
- Duration: 1s per pose (7s total)
- Perfect for giving directions or tours

#### treasure_hunt
- Poses: thinking → search_1 → search_2 → search_1 → search_2 → search_3 → happy
- Duration: 1s per pose (7s total)
- Complete treasure hunting sequence

#### greeting
- Poses: master → idle → talking → idle
- Duration: 1s per pose (4s total)
- Polite maid greeting

#### happy_dance
- Poses: happy → idle → happy → idle
- Duration: 0.5s per pose (2s total)
- Quick celebratory dance

## Creating Custom Animations

Use the `create_animation` tool:

```javascript
create_animation({
  id: "my_animation",
  name: "My Custom Animation", 
  frames: "idle,happy,love,thinking,idle",
  duration: 1.5,  // 1.5 seconds per pose
  loop: false
})
```

### Tips for Good Animations
1. **Start and end with idle** for smooth transitions
2. **Use 0.5-1s** for fast animations, **1-2s** for normal pace
3. **Combine related poses** (e.g., all pointing poses for directions)
4. **Test different durations** to find the right feel

## Animation Timing

### Polling Rate
- Display polls at 50ms intervals (20Hz)
- Smooth enough to catch all pose transitions
- Minimal CPU usage

### Duration Guidelines
- **Single poses**: 2 seconds (default)
- **Fast sequences**: 0.5-0.75 seconds per pose
- **Normal sequences**: 1-1.5 seconds per pose
- **Slow/dramatic**: 2+ seconds per pose

## GIF Integration

When a GIF is playing:
1. Avatar animations are paused
2. GIF plays for specified duration
3. Any queued animation starts fresh after GIF ends
4. Smooth transition with no timing issues

## Technical Details

### State Management
- Animation start times tracked locally in display
- Server provides animation data and sequences
- Display calculates current pose based on elapsed time

### Performance Optimizations
- Only logs pose changes, not every frame
- Smart GIF caching based on file size
- Polling paused during GIF playback

## Troubleshooting

### Animation plays too fast
- Increase `duration_per_pose` value
- Default is 2 seconds, try 3 or 4

### Animation skips poses
- Check polling rate (should be 20Hz)
- Ensure avatar display is running latest version
- Restart both server and display

### GIF causes animation issues
- Fixed in latest version
- Animation timing resets after GIF mode
- All poses should play correctly

## Best Practices

1. **Name animations clearly** - Use descriptive IDs
2. **Document your animations** - Add comments about purpose
3. **Test thoroughly** - Watch full animation cycles
4. **Consider context** - Match animation speed to emotion
5. **Reuse poses** - Combine existing poses creatively

## Example Animation Recipes

### Shy Expression
```
frames: "thinking,idle,love,idle,thinking"
duration: 1.0
```

### Energetic Greeting  
```
frames: "idle,happy,master,talking,happy,idle"
duration: 0.75
```

### Contemplative Moment
```
frames: "idle,thinking,thinking,write,thinking,idle"  
duration: 2.0
```

### Victory Celebration
```
frames: "search_1,search_2,search_3,happy,happy,idle"
duration: 1.0
```

This system provides expressive, natural animations while being simple to understand and create!
