# Quick Test After Restart

Once you restart Claude Desktop or the MCP server, try these commands:

## Test the Love Animation
```
maid:play_animation({ id: "love" })
```

## List All Available Animations
```
maid:list_animations()
```

## Test a Sequence
```
maid:play_animation({ id: "treasure_hunt" })
```

## Save a Custom Animation
```
maid:save_animation({
  id: "heart_dance",
  name: "Heart Dance",
  frames: "love,idle,love,idle",
  fps: 3
})
```

Then play it:
```
maid:play_animation({ id: "heart_dance" })
```

## Show Avatar with Initial Animation
```
maid:show_avatar({ animation: "greeting" })
```
