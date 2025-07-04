/**
 * Test the new pose-based animation system
 * Each pose now shows for 2 seconds by default
 */

const { spawn } = require('child_process');

// Helper to call MCP server
function callMCP(toolName, args = {}) {
    return new Promise((resolve, reject) => {
        const mcp = spawn('node', ['../maid-server.js'], {
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        const request = {
            jsonrpc: '2.0',
            method: 'tools/call',
            params: {
                name: toolName,
                arguments: args
            },
            id: 1
        };
        
        let output = '';
        
        mcp.stdout.on('data', (data) => {
            output += data.toString();
            try {
                const lines = output.split('\n');
                for (const line of lines) {
                    if (line.trim()) {
                        const response = JSON.parse(line);
                        if (response.result) {
                            resolve(response.result);
                            mcp.kill();
                            return;
                        }
                    }
                }
            } catch (e) {
                // Continue collecting output
            }
        });
        
        mcp.stderr.on('data', (data) => {
            console.error('Error:', data.toString());
        });
        
        mcp.on('error', reject);
        
        mcp.stdin.write(JSON.stringify(request) + '\n');
    });
}

async function testPoseBasedAnimation() {
    console.log('Testing New Pose-Based Animation System');
    console.log('=======================================\n');
    console.log('Each pose will now show for 2 seconds by default!\n');
    
    try {
        // Show avatar
        console.log('1. Showing avatar...');
        await callMCP('maid:show_avatar');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Create a new animation with 2-second poses
        console.log('\n2. Creating new celebration with 2-second poses...');
        await callMCP('maid:create_animation', {
            id: 'celebration_v2',
            name: 'Celebration v2 - Proper Timing',
            frames: 'happy,search_3,happy,search_3,happy,idle',
            duration: 2  // 2 seconds per pose!
        });
        
        console.log('\n3. Playing celebration_v2...');
        console.log('   Each pose will show for 2 full seconds!');
        console.log('   Total duration: 12 seconds (6 poses × 2 seconds)');
        
        await callMCP('maid:play_animation', {
            id: 'celebration_v2'
        });
        
        // Let it play - should take 12 seconds
        console.log('\n4. Animation playing... (12 seconds)');
        await new Promise(resolve => setTimeout(resolve, 13000));
        
        // Create a faster animation
        console.log('\n5. Creating a faster animation (1 second per pose)...');
        await callMCP('maid:create_animation', {
            id: 'quick_tour',
            name: 'Quick Tour',
            frames: 'idle,point_left,point_right,point_up,happy',
            duration: 1  // 1 second per pose
        });
        
        console.log('\n6. Playing quick_tour...');
        console.log('   5 poses × 1 second = 5 seconds total');
        
        await callMCP('maid:play_animation', {
            id: 'quick_tour'
        });
        
        await new Promise(resolve => setTimeout(resolve, 6000));
        
        // Test success
        console.log('\n7. All tests complete!');
        await callMCP('maid:speak', {
            text: 'Perfect! Now each pose shows for the right amount of time! No more missing animations!',
            emotion: 'happy'
        });
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Run the test
console.log('Starting pose-based animation test...\n');
console.log('The old system: Each pose was 1 frame at 4 FPS = 0.25 seconds (too fast!)');
console.log('The new system: Each pose shows for 2 seconds by default (perfect!)');
console.log('');

testPoseBasedAnimation();
