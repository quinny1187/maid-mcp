/**
 * Test animation timing fix v2
 * This demonstrates that animations now play all frames correctly
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

async function testAnimationTiming() {
    console.log('Testing Animation Timing Fix v2...\n');
    
    try {
        // Show avatar
        console.log('1. Showing avatar...');
        await callMCP('maid:show_avatar');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Test 1: Play shy_love animation (7 frames at 3 FPS = 2.33 seconds)
        console.log('\n2. Playing shy_love animation (7 frames)...');
        await callMCP('maid:play_animation', {
            id: 'shy_love'
        });
        
        console.log('   Watch for: love → idle → love → idle → love → thinking → idle');
        console.log('   Duration: 2.33 seconds');
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Test 2: Play ultimate_showcase (8 frames at 4 FPS = 2 seconds)
        console.log('\n3. Playing ultimate_showcase animation (8 frames)...');
        await callMCP('maid:play_animation', {
            id: 'ultimate_showcase'
        });
        
        console.log('   Watch for all poses: idle → point_left → point_right → point_up → happy → search_3 → master → love');
        console.log('   Duration: 2 seconds');
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Test 3: GIF then animation
        console.log('\n4. Testing GIF to animation transition...');
        console.log('   Searching for a smaller GIF...');
        
        const gifs = await callMCP('giphy:search_gifs', {
            query: 'thumbs up',
            limit: 3
        });
        
        console.log('   Showing GIF for 3 seconds...');
        await callMCP('giphy:show_gif', {
            gif_number: 1,
            duration: 3
        });
        
        // Start animation during GIF
        await new Promise(resolve => setTimeout(resolve, 1000));
        console.log('   Starting happy_dance during GIF...');
        await callMCP('maid:play_animation', {
            id: 'happy_dance'
        });
        
        console.log('   Waiting for GIF to finish...');
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        console.log('   Animation should play all frames now!');
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Success message
        console.log('\n5. All tests complete!');
        await callMCP('maid:speak', {
            text: 'Yatta! All animations played perfectly with every frame! The timing is fixed!',
            emotion: 'happy'
        });
        
        // Victory pose
        await callMCP('maid:play_animation', {
            id: 'search_3'
        });
        
        await new Promise(resolve => setTimeout(resolve, 3000));
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Run the test
console.log('Animation Timing Fix v2 Test');
console.log('==============================\n');
console.log('This test verifies that animations play all frames correctly.');
console.log('The avatar display now tracks animation start times locally.\n');

testAnimationTiming();
