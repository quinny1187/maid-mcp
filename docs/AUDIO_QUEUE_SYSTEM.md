# Audio Queue System Implementation

## Problem Solved
The previous implementation would crash when trying to speak multiple times quickly because:
1. Audio files were locked while playing
2. The same filename "audio.mp3" was reused
3. Attempting to write to a locked file caused EBUSY errors

## Solution Implemented

### 1. Audio Queue System
- Created `AudioQueue` class that manages a queue of audio files
- Audio files are added to queue and played sequentially
- Each audio finishes playing before the next one starts
- Prevents file lock conflicts

### 2. Unique Filenames
- Each audio file gets a unique name: `audio_{timestamp}_{random}.mp3`
- VBScript files also get unique names: `play_{timestamp}_{random}.vbs`
- No more conflicts from reusing the same filename

### 3. Automatic Cleanup
- Files are deleted after playback completes
- 1-second delay ensures file is fully released before deletion
- Keeps temp_voice folder clean

### 4. Benefits
- Can speak multiple times rapidly without crashes
- Messages play in the correct order
- No file lock errors
- Smooth audio playback experience

## How It Works

```javascript
// When you call speak multiple times:
speak("Hello!")     // → Added to queue
speak("How are you?") // → Added to queue  
speak("I'm happy!")  // → Added to queue

// Queue processes them one by one:
// 1. Plays "Hello!" 
// 2. Waits for completion
// 3. Plays "How are you?"
// 4. Waits for completion
// 5. Plays "I'm happy!"
```

## Usage
Just speak normally - the queue handles everything automatically!

```javascript
// Rapid fire speech - no problem!
maid:speak({ text: "First message" })
maid:speak({ text: "Second message" })
maid:speak({ text: "Third message" })
```

All messages will play in order without conflicts.