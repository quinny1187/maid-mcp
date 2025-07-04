# Giphy MCP Server

MCP server that integrates Giphy GIF search and display with the Maid avatar system.

## Features

- **GIF Search**: Search Giphy's vast library of animated GIFs
- **Avatar Integration**: Display GIFs in the avatar window
- **Timed Display**: Show GIFs for a specified duration
- **Smooth Transitions**: Seamless switch between GIF and avatar modes

## Setup

1. Get a Giphy API key from https://developers.giphy.com/
2. Create `.env` file with your API key:
   ```
   GIPHY_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```batch
   install.bat
   ```

## MCP Tools

### `search_gifs`
Search for GIFs on Giphy
- **query**: Search terms (required)
- **limit**: Number of results (default: 5, max: 10)
- **rating**: Content rating filter (g, pg, pg-13, r)

Returns numbered list of GIFs with preview and full URLs.

### `show_gif`
Display a GIF in the avatar window
- **gif_number**: Number from search results (1-based)
- **duration**: How long to display in seconds (default: 5)
- **url**: Direct URL of GIF (alternative to gif_number)

## How It Works

1. **Search**: Uses Giphy API to find relevant GIFs
2. **Display**: Sends GIF URL to avatar state server
3. **Avatar Integration**: 
   - Avatar window downloads and displays the GIF
   - Window expands to 400px width for better viewing
   - Original avatar is hidden during GIF playback
4. **Auto-restore**: After duration expires, avatar returns

## Example Usage

```javascript
// Search for celebration GIFs
await search_gifs({ query: "celebration confetti", limit: 5 });

// Show the first result for 5 seconds
await show_gif({ gif_number: 1, duration: 5 });
```

## Testing

Run the test script:
```batch
cd tests
test.bat
```

## Integration Notes

- Requires avatar system to be running (port 3338)
- GIFs are downloaded and cached temporarily
- Large GIFs (>500KB) use optimized playback mode
- Click on GIF to hide it early
- Animations queued during GIF playback start correctly after

## Performance

- Small GIFs (<500KB): Full frame caching for smooth playback
- Large GIFs (>500KB): No caching to prevent memory issues
- Avatar polling paused during GIF playback for best performance
