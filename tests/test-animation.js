// test-animation.js
// Test the new animation system

import axios from 'axios';

async function testAnimation() {
  console.log("Testing Maid Avatar Animation System");
  console.log("=====================================\n");
  
  try {
    // First, show the avatar
    console.log("1. Showing avatar...");
    await axios.post('http://localhost:3338/state', {
      visible: true,
      pose: 'idle'
    });
    
    // Wait a moment
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Test 1: Simple search animation (non-looping)
    console.log("\n2. Testing search animation (non-looping)...");
    console.log("   Sequence: search_1 → search_2 → search_1 → search_2 → search_3");
    
    await axios.post('http://localhost:3338/animate', {
      sequence: ['search_1', 'search_2', 'search_1', 'search_2', 'search_3'],
      fps: 2,
      loop: false
    });
    
    // Wait for animation to complete (5 frames at 2 FPS = 2.5 seconds)
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Test 2: Looping animation
    console.log("\n3. Testing looping search animation...");
    console.log("   Sequence: search_1 → search_2 → search_3 (looping)");
    
    await axios.post('http://localhost:3338/animate', {
      sequence: ['search_1', 'search_2', 'search_3'],
      fps: 3,
      loop: true
    });
    
    // Let it loop for 5 seconds
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    // Stop the animation
    console.log("\n4. Stopping animation...");
    await axios.delete('http://localhost:3338/animate');
    
    // Test 3: Fast animation
    console.log("\n5. Testing fast happy animation...");
    console.log("   Sequence: happy → idle → happy → idle (fast)");
    
    await axios.post('http://localhost:3338/animate', {
      sequence: ['happy', 'idle', 'happy', 'idle'],
      fps: 10,
      loop: false
    });
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    console.log("\n✅ Animation tests complete!");
    console.log("\nNote: If you don't see animations, make sure:");
    console.log("- Avatar is running (start_avatar.bat)");
    console.log("- You have search_1.png, search_2.png, search_3.png in avatar/library/");
    
  } catch (error) {
    console.error("❌ Error during testing:", error.message);
    console.error("Make sure the avatar system is running!");
  }
}

// Run the test
testAnimation();
