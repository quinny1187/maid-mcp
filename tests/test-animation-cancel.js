// test-animation-cancel.js
// Test animation cancellation with set_avatar_pose

import axios from 'axios';

async function testAnimationCancel() {
  console.log("Testing Animation Cancellation");
  console.log("==============================\n");
  
  try {
    // Start a looping animation
    console.log("1. Starting looping animation...");
    await axios.post('http://localhost:3338/animate', {
      sequence: ['happy', 'thinking', 'write'],
      fps: 2,
      loop: true
    });
    
    console.log("   Animation started: happy → thinking → write (looping)\n");
    
    // Wait 3 seconds
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Now set a pose which should cancel the animation
    console.log("2. Setting pose to 'idle' (should cancel animation)...");
    await axios.post('http://localhost:3338/state', {
      pose: 'idle',
      animation: null
    });
    
    console.log("   Pose set to idle, animation should be cancelled\n");
    
    // Check the current state
    console.log("3. Checking current state...");
    const response = await axios.get('http://localhost:3338/state');
    console.log("   Current state:", JSON.stringify(response.data, null, 2));
    
    // Wait a moment to see if animation resumes
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    console.log("\n✅ Test complete! Check if the avatar stayed in idle pose.");
    
  } catch (error) {
    console.error("❌ Error during testing:", error.message);
  }
}

// Run the test
testAnimationCancel();
