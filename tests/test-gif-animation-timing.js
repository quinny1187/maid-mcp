/**
 * Test GIF to Animation timing fix
 * This demonstrates that animations play correctly after GIF mode
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

async function testGifAnimationTiming() {
    console.log('Testing GIF to Animation timing fix...\n');
    
    try {
        // Show avatar
        console.log('1. Showing avatar...');
        await callMCP('maid:show_avatar');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Search for celebration GIF
        console.log('\n2. Searching for celebration GIF...');
        const gifs = await callMCP('giphy:search_gifs', {
            query: 'victory celebration',
            limit: 3
        });
        console.log('Found GIFs!');
        
        // Show GIF for 3 seconds
        console.log('\n3. Showing GIF for 3 seconds...');
        await callMCP('giphy:show_gif', {
            gif_number: 1,
            duration: 3
        });
        
        // Start celebration dance DURING GIF playback
        console.log('\n4. Starting celebration dance (during GIF)...');
        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second into GIF
        
        await callMCP('maid:play_animation', {
            id: 'celebration_dance'
        });
        
        console.log('\n5. Waiting for GIF to finish...');
        await new Promise(resolve => setTimeout(resolve, 3000)); // Wait for GIF to complete
        
        console.log('\n6. Animation should now play properly with all frames!');
        console.log('   - Before fix: Only showed 1 frame then went to idle');
        console.log('   - After fix: Shows all 6 frames of the celebration dance');
        
        // Let animation play out
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Speak success
        console.log('\n7. Testing complete!');
        await callMCP('maid:speak', {
            text: 'Yatta! The animation timing is fixed! Did you see my full celebration dance?',
            emotion: 'happy'
        });
        
        // Wait for speech
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Hide avatar
        await callMCP('maid:hide_avatar');
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Run the test
console.log('GIF to Animation Timing Fix Test');
console.log('================================\n');
console.log('This test demonstrates the fix for animation timing after GIF playback.');
console.log('The celebration_dance animation should play all 6 frames properly.\n');

testGifAnimationTiming();
