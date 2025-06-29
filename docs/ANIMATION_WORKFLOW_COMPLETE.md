# Complete Animation Workflow Example

## Creating a Custom Animation (Like Happy Dance)

### Step 1: Check Available Poses
```javascript
maid:list_poses()
// Returns: anger, happy, idle, love, master, pick_up, search_1, search_2, search_3, sleeping, talking, thinking, write
```

### Step 2: Create Your Animation
```javascript
maid:save_animation({
  id: "happy_dance",
  name: "Happy Dance",
  frames: "happy,idle,happy,idle,love",
  fps: 4,
  loop: false
})
// Returns: Saved animation: Happy Dance (5 frames at 4 FPS)
```

### Step 3: Play Your Animation
```javascript
maid:play_animation({ id: "happy_dance" })
// Returns: Playing animation: Happy Dance
```

### Step 4: See All Animations
```javascript
maid:list_animations()
// Now shows:
// 📷 Single Poses: idle, happy, love, etc.
// 🎬 Built-in Sequences: treasure_hunt, greeting, etc.
// ⭐ Custom Animations: happy_dance <-- Your new animation!
```

## More Examples

### Create a Search Victory Animation
```javascript
maid:save_animation({
  id: "found_it",
  name: "Found It!",
  frames: "search_1,search_2,search_1,search_2,search_3,happy,happy",
  fps: 2
})
```

### Create a Thinking Loop
```javascript
maid:save_animation({
  id: "deep_thought",
  name: "Deep in Thought",
  frames: "thinking,write,thinking,write",
  fps: 1,
  loop: true
})
```

### Create a Love Confession
```javascript
maid:save_animation({
  id: "confession",
  name: "Love Confession",
  frames: "idle,talking,love,love,love",
  fps: 1.5
})
```

## The Tools You Need

1. **list_poses()** - See what sprites you can use
2. **save_animation()** - Create AND save new animations
3. **play_animation()** - Play any animation or pose
4. **list_animations()** - See all available animations

## Important Notes

- `save_animation` is your CREATE tool - it creates and saves in one action
- Once saved, animations persist across sessions
- You can play single poses without saving: `play_animation({ id: "love" })`
- But sequences need to be saved first before playing

## Quick Recipe for Happy Dance

```javascript
// 1. Create it
maid:save_animation({
  id: "mimi_happy_dance",
  name: "Mimi's Happy Dance",
  frames: "idle,happy,love,happy,idle",
  fps: 5
})

// 2. Play it
maid:play_animation({ id: "mimi_happy_dance" })

// 3. It's now permanently saved!
maid:list_animations()  // Will show under Custom Animations
```
