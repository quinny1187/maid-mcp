# Maid-MCP Giphy Integration

## Overview
The Maid-MCP system now includes Giphy integration, allowing the avatar to search for and display animated GIFs. When a GIF is shown, it temporarily replaces the maid avatar in an expanded window, then returns to normal avatar mode.

## Key Features
- **Dual-Mode System**: 
  - GIF MODE: Stops state polling for smooth GIF playback at full speed
  - AVATAR MODE: Normal polling for Mimi's animations
- **Dynamic Window Sizing**: Window doubles in width (200→400px) for landscape GIF viewing
- **Automatic Restoration**: Avatar returns after GIF duration expires

## Available Tools

### search_gifs
Search for GIFs on Giphy with filtering options.
```
search_gifs(query="happy cat", limit=5, rating="g")
```
- Returns numbered list of GIFs with preview and full URLs
- Maximum 10 results per search

### show_gif
Display a GIF in the avatar window.
```
show_gif(gif_number=1, duration=5)
```
Or with direct URL:
```
show_gif(url="https://media.giphy.com/...", duration=7)
```

## Usage Flow
1. Search for GIFs using keywords
2. Choose a GIF from the numbered results
3. GIF replaces avatar temporarily
4. Avatar automatically returns after duration

## Technical Details
- GIFs are downloaded and played from temporary files
- Original GIF size is preserved (no scaling) for optimal playback
- State polling pauses during GIF playback to prevent frame drops
- Avatar animations queue after GIF mode exits

## Setup Requirements
- Giphy API key in `giphy/.env`
- Avatar system running (`start_avatar.bat`)
- Node.js dependencies installed in giphy folder

## Example
```
// Search for celebration GIFs
search_gifs("celebration fireworks")

// Show the first result for 5 seconds
show_gif(gif_number=1, duration=5)

// After GIF ends, avatar returns and can play animations
play_animation("happy_dance")
```
