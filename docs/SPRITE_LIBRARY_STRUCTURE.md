# Sprite Library Organization

## Folder Structure
```
maid-mcp/
└── sprites/
    ├── idle.png
    ├── idle.json (optional metadata)
    ├── happy.png
    ├── happy.json
    ├── thinking.png
    ├── custom_pose_wink.png
    ├── custom_pose_wink.json
    └── ...
```

## Metadata Format (Optional)
Each pose can have an accompanying JSON file with extra information:

```json
// happy.json
{
  "description": "Joyful and cheerful expression",
  "category": "emotions",
  "tags": ["positive", "greeting", "success"],
  "usage": "Use for positive responses, greetings, and celebrations"
}
```

```json
// thinking.json
{
  "description": "Deep in thought, processing complex information",
  "category": "states", 
  "tags": ["processing", "calculating", "pondering"],
  "usage": "During complex problem solving or when considering options"
}
```

```json
// custom_pose_wink.json
{
  "description": "Playful wink with one eye closed",
  "category": "gestures",
  "tags": ["playful", "secret", "understanding"],
  "usage": "When sharing insider knowledge or being playful"
}
```

## Benefits of This System

1. **Easy Expansion**: Just drop new PNG files in the folder
2. **Self-Documenting**: I can discover what poses exist and their purpose
3. **Categories**: Can organize poses by type (emotions, actions, states)
4. **Custom Poses**: Easy to add user-created poses
5. **No Code Changes**: New poses work immediately

## Example Usage Flow

1. **Discovery**:
   ```
   Me: *calls list_avatar_poses*
   Response: "Found 15 poses including: wink, victory_sign, head_tilt..."
   ```

2. **Learning Context**:
   ```
   Me: *reads metadata to understand when to use each pose*
   ```

3. **Natural Usage**:
   ```
   User: "That's our little secret"
   Me: *sets emotion to "wink"* 
   Voice: "Your secret is safe with me!"
   ```

## Future Enhancements

- **Pose Combinations**: Layer multiple sprites (base + accessory)
- **Animated Poses**: Support GIF or sprite sheets
- **Pose Transitions**: Define smooth transitions between poses
- **Contextual Sets**: Load different pose sets for different moods/seasons