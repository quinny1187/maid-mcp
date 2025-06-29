# Quick Start After Restart

Once you restart Claude Desktop/MCP server:

## 1. Create Mimi's Happy Dance
```javascript
maid:create_animation({
  id: "happy_dance",
  name: "Happy Dance",
  frames: "happy,idle,happy,idle,love",
  fps: 4
})
```

## 2. Play It!
```javascript
maid:play_animation({ id: "happy_dance" })
```

## 3. Play Single Poses
```javascript
maid:play_animation({ id: "love" })     // Works automatically
maid:play_animation({ id: "thinking" }) // No need to create first
```

## 4. See Everything
```javascript
maid:list_poses()      // Raw PNG files
maid:list_animations() // All animations (including your new ones)
```

That's it! The key is that `create_animation` is your tool for making new sequences.
