// test-giphy.js
// Test script for Giphy MCP server

import axios from 'axios';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables
dotenv.config({ path: join(__dirname, '.env') });

const GIPHY_API_KEY = process.env.GIPHY_API_KEY;

async function testGiphyAPI() {
    console.log('Testing Giphy API...\n');
    
    if (!GIPHY_API_KEY) {
        console.error('ERROR: GIPHY_API_KEY not found in .env file');
        console.log('Please add your API key to the .env file');
        return;
    }
    
    console.log(`Using API key: ${GIPHY_API_KEY.substring(0, 8)}...`);
    
    try {
        // Test search endpoint
        console.log('\nTesting search endpoint...');
        const response = await axios.get('https://api.giphy.com/v1/gifs/search', {
            params: {
                api_key: GIPHY_API_KEY,
                q: 'happy cat',
                limit: 3,
                rating: 'g'
            }
        });
        
        console.log(`Found ${response.data.data.length} GIFs`);
        
        response.data.data.forEach((gif, index) => {
            console.log(`\n${index + 1}. ${gif.title || 'Untitled'}`);
            console.log(`   URL: ${gif.images.fixed_height.url}`);
            console.log(`   Size: ${gif.images.fixed_height.width}x${gif.images.fixed_height.height}`);
        });
        
        console.log('\n✓ Giphy API is working correctly!');
        
        // Test avatar state server
        console.log('\nTesting avatar state server connection...');
        try {
            const health = await axios.get('http://localhost:3338/health');
            console.log('✓ Avatar state server is running');
        } catch (error) {
            console.log('✗ Avatar state server is not running');
            console.log('  Run start_avatar.bat to start it');
        }
        
    } catch (error) {
        console.error('\nERROR testing Giphy API:');
        if (error.response) {
            console.error(`Status: ${error.response.status}`);
            console.error(`Message: ${error.response.data.message || error.response.statusText}`);
            
            if (error.response.status === 401) {
                console.error('\nYour API key is invalid. Please check your .env file.');
            }
        } else {
            console.error(error.message);
        }
    }
}

// Run the test
console.log('Giphy MCP Server Test\n');
testGiphyAPI();
