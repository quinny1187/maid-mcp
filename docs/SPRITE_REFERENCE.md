# Mimi Avatar Sprite Reference

## Available Poses

### Basic Emotions & States

1. **idle** - Default standing pose
   - Holding silver serving tray with one hand
   - Pleasant, professional smile
   - Standard maid posture

2. **happy** - Extreme excitement
   - Jumping in the air with one leg raised
   - Both arms raised up in celebration
   - Big open-mouthed smile
   - Very energetic and dynamic

3. **love** - Adoring/affectionate 
   - Heart-shaped eyes (♥‿♥)
   - Hands clasped together at chest
   - Dreamy, loving expression
   - Slight forward lean

4. **anger** - Stern/upset
   - Hands firmly on hips
   - Serious, disapproving expression
   - Assertive power stance
   - No smile, slight frown

5. **thinking** - Contemplative
   - Right hand on chin
   - Thoughtful expression
   - Looking slightly upward
   - Classic thinking gesture

6. **sleeping** - Tired/resting
   - Eyes closed with "Zzz" symbols
   - Leaning on wooden broom for support
   - Peaceful sleeping expression
   - Standing but asleep

### Action Poses

7. **talking** - Explaining/presenting
   - Right hand extended palm-up
   - Gesturing as if explaining something
   - Friendly, helpful expression
   - Professional presentation pose

8. **write** - Writing/note-taking
   - Body turned to show back/side view
   - Appears to be writing or taking notes
   - Focused on task
   - Only pose showing back view

9. **master** - Welcome/greeting
   - Arms spread wide horizontally
   - Neutral pleasant expression
   - T-pose style stance
   - Welcoming gesture

10. **pick_up** - Being moved
    - Special pose for when avatar is dragged
    - (Not shown in provided images)

### Search Sequence

11. **search_1** - Searching start
    - Bending over open treasure chest
    - Looking/reaching inside
    - Face partially hidden

12. **search_2** - Searching middle  
    - Different angle/position at chest
    - Still searching inside
    - Slightly different pose

13. **search_3** - Search success!
    - Sitting on treasure chest
    - Holding golden trophy high
    - Victorious happy expression
    - Quest complete pose

## Missing Sprites

- **sad** - Listed but no sprite file exists yet

## Animation Ideas

### Greeting Sequence
`master,idle,talking,idle` - Welcome and explain

### Cleaning Animation  
`idle,sleeping,idle,sleeping` - Getting tired while working

### Search Success Story
`thinking,search_1,search_2,search_1,search_2,search_3,happy` - Think, search, find treasure!

### Love at First Sight
`idle,talking,love,love` - See something adorable

### Angry to Happy
`anger,thinking,idle,happy` - Mood improvement

## Technical Notes

- All sprites are PNG with transparent backgrounds
- Maid outfit: Black dress with white apron and frills
- Hair: Brown in side bun with maid headpiece
- Black thigh-high stockings
- Consistent art style across all poses
