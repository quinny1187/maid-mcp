#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from 'axios';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// Get the directory of the current module
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from .env file
dotenv.config({ path: join(__dirname, '.env') });

const GIPHY_API_KEY = process.env.GIPHY_API_KEY;
const GIPHY_BASE_URL = 'https://api.giphy.com/v1/gifs';
const AVATAR_STATE_SERVER = 'http://localhost:3338';

// Create server instance
const server = new Server(
  {
    name: "giphy",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_gifs",
        description: "Search for GIFs on Giphy. Returns a list of GIFs for you to choose from.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Search query for GIFs"
            },
            limit: {
              type: "number",
              description: "Number of results to return (default: 5, max: 10)",
              default: 5
            },
            rating: {
              type: "string",
              description: "Content rating filter (g, pg, pg-13, r)",
              enum: ["g", "pg", "pg-13", "r"],
              default: "g"
            }
          },
          required: ["query"]
        }
      },
      {
        name: "show_gif",
        description: "Display a specific GIF in the avatar window by its number from search results",
        inputSchema: {
          type: "object",
          properties: {
            gif_number: {
              type: "number",
              description: "The number of the GIF from search results (1-based index)"
            },
            url: {
              type: "string",
              description: "Direct URL of the GIF to display"
            },
            duration: {
              type: "number",
              description: "How long to display the GIF in seconds (default: 5)",
              default: 5
            }
          },
          required: ["url"]
        }
      }
    ]
  };
});

// Store last search results
let lastSearchResults = [];

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "search_gifs") {
      if (!GIPHY_API_KEY) {
        throw new Error("GIPHY_API_KEY not found in environment variables. Please add it to giphy/.env file");
      }

      const { query, limit = 5, rating = "g" } = args;

      // Search for GIFs
      const response = await axios.get(`${GIPHY_BASE_URL}/search`, {
        params: {
          api_key: GIPHY_API_KEY,
          q: query,
          limit: Math.min(limit, 10),
          rating: rating
        }
      });

      const gifs = response.data.data;
      lastSearchResults = gifs; // Store for later use
      
      if (!gifs || gifs.length === 0) {
        return {
          content: [{
            type: "text",
            text: `No GIFs found for "${query}"`
          }]
        };
      }

      // Format the results for display with preview URLs
      const formattedResults = gifs.map((gif, index) => {
        const title = gif.title || 'Untitled';
        const previewUrl = gif.images.preview_gif?.url || gif.images.fixed_height_small.url;
        const fullUrl = gif.images.fixed_height.url;
        const dimensions = `${gif.images.fixed_height.width}x${gif.images.fixed_height.height}`;
        
        return `${index + 1}. **${title}**\n   Preview: ${previewUrl}\n   Full: ${fullUrl}\n   Size: ${dimensions}`;
      }).join('\n\n');

      return {
        content: [{
          type: "text",
          text: `Found ${gifs.length} GIFs for "${query}"! Use show_gif with the number to display one:\n\n${formattedResults}\n\nTip: Use show_gif(gif_number=1) to display the first result, or choose any number from the list.`
        }]
      };
    }
    
    else if (name === "show_gif") {
      const { gif_number, url, duration = 5 } = args;
      
      let gifUrl = url;
      
      // If gif_number is provided, get URL from last search results
      if (gif_number && !url) {
        if (!lastSearchResults || lastSearchResults.length === 0) {
          return {
            content: [{
              type: "text",
              text: "No search results available. Please search for GIFs first using search_gifs."
            }]
          };
        }
        
        const index = gif_number - 1; // Convert to 0-based index
        if (index < 0 || index >= lastSearchResults.length) {
          return {
            content: [{
              type: "text",
              text: `Invalid GIF number. Please choose a number between 1 and ${lastSearchResults.length}.`
            }]
          };
        }
        
        const selectedGif = lastSearchResults[index];
        gifUrl = selectedGif.images.fixed_height.url;
      }
      
      if (!gifUrl) {
        return {
          content: [{
            type: "text",
            text: "Please provide either a gif_number from search results or a direct URL."
          }]
        };
      }
      
      // Send the GIF URL to the avatar state server
      try {
        await axios.post(`${AVATAR_STATE_SERVER}/show_gif`, {
          url: gifUrl,
          duration: duration
        });
        
        return {
          content: [{
            type: "text",
            text: `Displaying GIF for ${duration} seconds! The GIF will replace my avatar temporarily.\n\nClick on the avatar to hide the GIF early, or wait for it to finish.`
          }]
        };
      } catch (avatarError) {
        console.error('Error displaying GIF in avatar:', avatarError);
        return {
          content: [{
            type: "text",
            text: `Could not display GIF in avatar window. Make sure the avatar is running (start_avatar.bat).\n\nGIF URL: ${gifUrl}`
          }]
        };
      }
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    console.error('Tool execution error:', error);
    return {
      content: [{
        type: "text",
        text: `Error: ${error.message}`
      }]
    };
  }
});

// Start the server
async function main() {
  console.error("Starting Giphy MCP server...");
  console.error(`Using API key: ${GIPHY_API_KEY ? GIPHY_API_KEY.substring(0, 8) + '...' : 'NOT SET'}`);
  
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("Giphy MCP server running");
}

main().catch(console.error);
