// test-loop-fix.js
// Test animation looping fix

import axios from 'axios';

async function testLoopFix() {
  console.log("Testing Animation Loop Fix");
  console.log("==========================\n");
  
  try {
    // Clear any existing animation first
    console.log("1. Clearing any existing animation...");
    await axios.post('http://localhost:3338/state', {
      pose: 'idle',
      animation: null
    });
    
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Start a simple 3-frame loop
    console.log("\n2. Starting 3-frame loop animation...");
    console.log("   Sequence: search_1 → search_2 → search_3 (looping at 1 FPS)");
    
    await axios.post('http://localhost:3338/animate', {
      sequence: ['search_1', 'search_2', 'search_3'],
      fps: 1,
      loop: true
    });
    
    // Let it run for 8 seconds (should see 2+ full loops)
    console.log("\n3. Running for 8 seconds to observe looping...");
    await new Promise(resolve => setTimeout(resolve, 8000));
    
    // Now cancel with pose change
    console.log("\n4. Setting pose to 'love' to cancel animation...");
    await axios.post('http://localhost:3338/state', {
      pose: 'love',
      animation: null
    });
    
    console.log("\n✅ Test complete! Check if:");
    console.log("   - Animation looped properly (search_1, 2, 3, 1, 2, 3...)");
    console.log("   - Pose changed to 'love' and animation stopped");
    
  } catch (error) {
    console.error("❌ Error during testing:", error.message);
  }
}

// Run the test
testLoopFix();
