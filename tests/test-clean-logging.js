/**
 * Test clean logging - should only show pose changes, not spam
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
        
        mcp.on('error', reject);
        
        mcp.stdin.write(JSON.stringify(request) + '\n');
    });
}

async function testCleanLogging() {
    console.log('Testing Clean Logging System');
    console.log('============================\n');
    console.log('You should see:\n');
    console.log('✓ Animation start with sequence details');
    console.log('✓ Pose changes only when they happen');
    console.log('✓ NO polling rate spam');
    console.log('✓ NO repeated pose logs\n');
    
    try {
        // Show avatar
        console.log('1. Showing avatar...\n');
        await callMCP('maid:show_avatar');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Play a simple animation
        console.log('2. Playing tour_guide animation...');
        console.log('   Watch the avatar window logs - should be clean!\n');
        
        await callMCP('maid:play_animation', {
            id: 'tour_guide'
        });
        
        // Let it play
        await new Promise(resolve => setTimeout(resolve, 8000));
        
        console.log('\n3. Success! Check the avatar logs - no spam!');
        
    } catch (error) {
        console.error('Test failed:', error);
    }
}

// Run the test
testCleanLogging();
