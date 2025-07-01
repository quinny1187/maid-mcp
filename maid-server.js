// maid-mcp server - Lean version with modular voice system
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { readFile, appendFile, readdir, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import axios from 'axios';
import { fileURLToPath } from 'url';

// Import voice system from modular structure
import { VoiceEngine, VOICES } from './voice/outgoing/index.js';

// Get the directory of this script
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Animation storage
class AnimationManager {
  constructor() {
    this.animationsFile = join(__dirname, 'avatar', 'library', 'animations', 'animations.jsonl');
    this.animationsDir = join(__dirname, 'avatar', 'library', 'animations');
    this.animations = new Map();
  }
  
  async ensureDirectory() {
    if (!existsSync(this.animationsDir)) {
      await mkdir(this.animationsDir, { recursive: true });
    }
  }
  
  async loadAnimations() {
    try {
      await this.ensureDirectory();
      
      console.error(`Loading animations from: ${this.animationsFile}`);
      
      if (existsSync(this.animationsFile)) {
        const content = await readFile(this.animationsFile, 'utf-8');
        const lines = content.split('\n').filter(line => line.trim());
        
        console.error(`Found ${lines.length} animation lines to load`);
        
        for (const line of lines) {
          try {
            const animation = JSON.parse(line);
            this.animations.set(animation.id, animation);
            console.error(`Loaded animation: ${animation.id}`);
          } catch (e) {
            console.error('Failed to parse animation line:', line, e);
          }
        }
      }
      console.error(`Total animations loaded: ${this.animations.size}`);
    } catch (error) {
      console.error('Failed to load animations:', error);
    }
  }
  
  async saveAnimation(animation) {
    try {
      await this.ensureDirectory();
      this.animations.set(animation.id, animation);
      const line = JSON.stringify(animation) + '\n';
      await appendFile(this.animationsFile, line);
      console.error(`Saved animation ${animation.id} to file`);
    } catch (error) {
      console.error('Failed to save animation:', error);
    }
  }
  
  getAnimation(id) {
    return this.animations.get(id);
  }
  
  listAnimations() {
    return Array.from(this.animations.values());
  }
}

// Create instances
const voiceEngine = new VoiceEngine();
const animationManager = new AnimationManager();

// Create MCP server
const server = new Server(
  {
    name: 'maid-mcp',
    version: '2.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // Voice tools
      {
        name: 'speak',
        description: 'Convert text to speech with optional emotion (Japanese accent default)',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: 'The text to speak'
            },
            emotion: {
              type: 'string',
              enum: ['neutral', 'happy', 'sad', 'excited', 'angry', 'shy'],
              description: 'Optional emotion for voice modulation',
              default: 'neutral'
            }
          },
          required: ['text']
        }
      },
      {
        name: 'list_voices',
        description: 'List available voices',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'set_voice',
        description: 'Set the current voice',
        inputSchema: {
          type: 'object',
          properties: {
            voiceId: {
              type: 'string',
              description: 'The voice ID to use (ja-JP voices for Japanese accent)'
            }
          },
          required: ['voiceId']
        }
      },
      // Avatar tools
      {
        name: 'show_avatar',
        description: 'Show the visual avatar on screen',
        inputSchema: {
          type: 'object',
          properties: {
            animation: {
              type: 'string',
              description: 'Initial animation to play (default: idle)',
              default: 'idle'
            },
            x: {
              type: 'number',
              description: 'X position on screen (default: 1000)',
              default: 1000
            },
            y: {
              type: 'number',
              description: 'Y position on screen (default: 100)',
              default: 100
            }
          }
        }
      },
      {
        name: 'hide_avatar',
        description: 'Hide the visual avatar',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'move_avatar',
        description: 'Move the avatar to a specific position',
        inputSchema: {
          type: 'object',
          properties: {
            x: {
              type: 'number',
              description: 'X position on screen'
            },
            y: {
              type: 'number',
              description: 'Y position on screen'
            }
          },
          required: ['x', 'y']
        }
      },
      {
        name: 'play_animation',
        description: 'Play an animation (single pose or sequence)',
        inputSchema: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              description: 'Animation ID (e.g. "idle", "happy", "treasure_hunt")'
            }
          },
          required: ['id']
        }
      },
      {
        name: 'stop_animation',
        description: 'Stop any running animation',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'create_animation',
        description: 'Create and save a custom animation sequence',
        inputSchema: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              description: 'Unique ID for the animation'
            },
            name: {
              type: 'string',
              description: 'Display name for the animation'
            },
            frames: {
              type: 'string',
              description: 'Comma-separated list of poses'
            },
            fps: {
              type: 'number',
              description: 'Frames per second (default: 2)',
              default: 2
            },
            loop: {
              type: 'boolean',
              description: 'Whether to loop (default: false)',
              default: false
            }
          },
          required: ['id', 'name', 'frames']
        }
      },
      {
        name: 'list_animations',
        description: 'List all available animations',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'list_poses',
        description: 'List all available sprite poses (PNG files)',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      }
    ]
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    switch (name) {
      // Voice tools
      case 'speak': {
        const text = voiceEngine.cleanText(args.text);
        const emotion = args.emotion || 'neutral';
        
        const result = await voiceEngine.speak(text, emotion);
        
        return {
          content: [{
            type: 'text',
            text: `Spoke: "${text}" with ${emotion} emotion using ${result.voice}`
          }]
        };
      }
      
      case 'list_voices': {
        const voiceList = voiceEngine.listVoices();
        
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(voiceList, null, 2)
          }]
        };
      }
      
      case 'set_voice': {
        try {
          await voiceEngine.setVoice(args.voiceId);
          const voiceInfo = voiceEngine.getVoiceInfo(args.voiceId);
          
          return {
            content: [{
              type: 'text',
              text: `Voice changed to: ${args.voiceId} (${voiceInfo.name}) - ${voiceInfo.language.startsWith('ja-JP') ? 'Japanese accent' : voiceInfo.language.startsWith('en-GB') ? 'British' : 'American'} voice\n${voiceInfo.style} style with ${voiceInfo.pitch} pitch adjustment`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: `Failed to set voice: ${error.message}`
            }]
          };
        }
      }
      
      // Avatar tools
      case 'show_avatar': {
        try {
          const animationId = args.animation || 'idle';
          const x = args.x || 1000;
          const y = args.y || 100;
          
          const animation = animationManager.getAnimation(animationId);
          if (!animation) {
            throw new Error(`Unknown animation: ${animationId}`);
          }
          
          await axios.post('http://localhost:3338/state', {
            visible: true,
            position: { x, y }
          });
          
          await axios.post('http://localhost:3338/play_animation', {
            id: animationId,
            name: animation.name,
            frames: animation.frames,
            fps: animation.fps,
            loop: animation.loop
          });
          
          return {
            content: [{
              type: 'text',
              text: `Avatar shown at position (${x}, ${y}) playing animation: ${animation.name}`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: 'Failed to show avatar. Make sure avatar system is running (run start.bat)'
            }]
          };
        }
      }
      
      case 'hide_avatar': {
        try {
          await axios.post('http://localhost:3338/state', { 
            visible: false
          });
          
          return {
            content: [{
              type: 'text',
              text: 'Avatar hidden'
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: 'Failed to hide avatar. Avatar system may not be running.'
            }]
          };
        }
      }
      
      case 'move_avatar': {
        try {
          await axios.post('http://localhost:3338/state', {
            position: { x: args.x, y: args.y },
            visible: true
          });
          
          return {
            content: [{
              type: 'text',
              text: `Avatar moved to position (${args.x}, ${args.y})`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: 'Failed to move avatar. Make sure avatar system is running.'
            }]
          };
        }
      }
      
      case 'play_animation': {
        try {
          let animation = animationManager.getAnimation(args.id);
          
          if (!animation) {
            const libraryPath = join(__dirname, 'avatar', 'library');
            const files = await readdir(libraryPath);
            const poseExists = files.includes(`${args.id}.png`);
            
            if (poseExists) {
              animation = {
                id: args.id,
                name: args.id.charAt(0).toUpperCase() + args.id.slice(1),
                frames: [args.id],
                fps: 1,
                loop: false
              };
            } else {
              throw new Error(`Unknown animation or pose: ${args.id}`);
            }
          }
          
          await axios.post('http://localhost:3338/play_animation', {
            id: animation.id,
            name: animation.name,
            frames: animation.frames,
            fps: animation.fps,
            loop: animation.loop
          });
          
          return {
            content: [{
              type: 'text',
              text: `Playing animation: ${animation.name}${animation.loop ? ' (looping)' : ''}`
            }]
          };
        } catch (error) {
          console.error('play_animation error:', error);
          return {
            content: [{
              type: 'text',
              text: `Failed to play animation: ${error.message}`
            }]
          };
        }
      }
      
      case 'stop_animation': {
        try {
          await axios.delete('http://localhost:3338/animate');
          
          return {
            content: [{
              type: 'text',
              text: 'Animation stopped'
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: 'Failed to stop animation. Make sure avatar system is running.'
            }]
          };
        }
      }
      
      case 'create_animation': {
        try {
          const frames = args.frames.split(',').map(f => f.trim());
          if (frames.length === 0) {
            throw new Error('Animation must have at least one frame');
          }
          
          const animation = {
            id: args.id,
            name: args.name,
            frames: frames,
            fps: args.fps || 2,
            loop: args.loop || false,
            builtin: false
          };
          
          await animationManager.saveAnimation(animation);
          
          return {
            content: [{
              type: 'text',
              text: `Created animation: "${animation.name}" (${frames.length} frames at ${animation.fps} FPS)\nID: ${animation.id}`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: `Failed to save animation: ${error.message}`
            }]
          };
        }
      }
      
      case 'list_animations': {
        const animations = animationManager.listAnimations();
        const categorized = {
          poses: animations.filter(a => a.builtin && a.frames.length === 1),
          sequences: animations.filter(a => a.builtin && a.frames.length > 1),
          custom: animations.filter(a => !a.builtin)
        };
        
        let output = "Available Animations:\n\n";
        
        if (categorized.poses.length > 0) {
          output += "📷 Single Poses:\n";
          categorized.poses.forEach(a => {
            output += `  • ${a.id} - ${a.name}\n`;
          });
          output += "\n";
        }
        
        if (categorized.sequences.length > 0) {
          output += "🎬 Built-in Sequences:\n";
          categorized.sequences.forEach(a => {
            output += `  • ${a.id} - ${a.name} (${a.frames.length} frames, ${a.fps} FPS${a.loop ? ', loops' : ''})\n`;
          });
          output += "\n";
        }
        
        if (categorized.custom.length > 0) {
          output += "⭐ Custom Animations:\n";
          categorized.custom.forEach(a => {
            output += `  • ${a.id} - ${a.name} (${a.frames.length} frames, ${a.fps} FPS${a.loop ? ', loops' : ''})\n`;
          });
        }
        
        return {
          content: [{
            type: 'text',
            text: output
          }]
        };
      }
      
      case 'list_poses': {
        try {
          const libraryPath = join(__dirname, 'avatar', 'library');
          const files = await readdir(libraryPath);
          const pngFiles = files.filter(f => f.endsWith('.png'));
          const poses = pngFiles.map(f => f.replace('.png', '')).sort();
          
          let output = "Available Sprite Poses:\n\n";
          poses.forEach(pose => {
            output += `  • ${pose}\n`;
          });
          output += `\nTotal: ${poses.length} poses`;
          
          return {
            content: [{
              type: 'text',
              text: output
          }]
        };
        } catch (error) {
          console.error('list_poses error:', error);
          return {
            content: [{
              type: 'text',
              text: `Failed to list poses: ${error.message}`
            }]
          };
        }
      }
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `Error: ${error.message}`
      }],
      isError: true
    };
  }
});

// Start the server
async function main() {
  try {
    console.error('Starting maid-mcp server v2.0...');
    console.error(`Working directory: ${process.cwd()}`);
    console.error(`Script directory: ${__dirname}`);
    
    await voiceEngine.initialize();
    await animationManager.loadAnimations();
    
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    console.error('maid-mcp server running - Voice and animation system ready!');
    console.error(`Loaded ${animationManager.animations.size} animations`);
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

main();
