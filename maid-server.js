// maid-mcp server - Voice synthesis with audio queue system
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { MsEdgeTTS, OUTPUT_FORMAT } from 'msedge-tts';
import { mkdir, writeFile, unlink, rmdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { exec } from 'child_process';
import axios from 'axios';

// Voice configuration with Japanese accent settings
const VOICES = {
  // Japanese voices (for authentic Japanese accent)
  'ja-JP-NanamiNeural': { name: 'Nanami', language: 'ja-JP', style: 'cute', pitch: '+20Hz' },
  'ja-JP-MayuNeural': { name: 'Mayu', language: 'ja-JP', style: 'gentle', pitch: '+15Hz' },
  'ja-JP-AoiNeural': { name: 'Aoi', language: 'ja-JP', style: 'energetic', pitch: '+10Hz' },
  // English voices
  'en-US-JennyNeural': { name: 'Jenny', language: 'en-US', style: 'cheerful', pitch: '+0Hz' },
  'en-US-AriaNeural': { name: 'Aria', language: 'en-US', style: 'warm', pitch: '+0Hz' },
  'en-GB-MaisieNeural': { name: 'Maisie', language: 'en-GB', style: 'young', pitch: '+5Hz' }
};

// Emotion settings (adjusted for Japanese accent feel)
const EMOTIONS = {
  neutral: { pitch: '+0Hz', rate: '+0%', volume: '+0%' },
  happy: { pitch: '+10Hz', rate: '+5%', volume: '+0%' },
  sad: { pitch: '-5Hz', rate: '-10%', volume: '-10%' },
  excited: { pitch: '+15Hz', rate: '+10%', volume: '+5%' },
  angry: { pitch: '-10Hz', rate: '+5%', volume: '+5%' },
  shy: { pitch: '+5Hz', rate: '-5%', volume: '-20%' }
};

// Audio Queue System
class AudioQueue {
  constructor() {
    this.queue = [];
    this.isPlaying = false;
  }
  
  add(audioPath, vbsPath, audioDir) {
    this.queue.push({ audioPath, vbsPath, audioDir });
    if (!this.isPlaying) {
      this.processQueue();
    }
  }
  
  async processQueue() {
    if (this.queue.length === 0) {
      this.isPlaying = false;
      return;
    }
    
    this.isPlaying = true;
    const { audioPath, vbsPath, audioDir } = this.queue.shift();
    
    // Execute VBScript and wait for completion
    exec(`wscript //B "${vbsPath}"`, {
      windowsHide: true
    }, async (error) => {
      if (error) {
        console.error('Audio playback error:', error.message);
      }
      
      // Clean up files after playback
      setTimeout(async () => {
        try {
          await unlink(vbsPath);
          await unlink(audioPath);
          // Remove the audio directory
          if (audioDir) {
            await rmdir(audioDir);
          }
        } catch (e) {
          // Ignore cleanup errors
        }
      }, 1000);
      
      // Process next item in queue
      setTimeout(() => {
        this.processQueue();
      }, 500); // Small gap between audio clips
    });
  }
}

// TTS Engine wrapper with queue
class VoiceEngine {
  constructor() {
    this.tts = new MsEdgeTTS();
    // Default to Japanese voice for Japanese accent
    this.currentVoice = 'ja-JP-NanamiNeural';
    this.tempDir = join(process.cwd(), 'temp_voice');
    this.audioQueue = new AudioQueue();
  }
  
  async initialize() {
    if (!existsSync(this.tempDir)) {
      await mkdir(this.tempDir, { recursive: true });
    }
    await this.setVoice(this.currentVoice);
  }
  
  async setVoice(voiceId) {
    if (!VOICES[voiceId]) {
      throw new Error(`Unknown voice: ${voiceId}`);
    }
    this.currentVoice = voiceId;
    await this.tts.setMetadata(
      voiceId,
      OUTPUT_FORMAT.AUDIO_24KHZ_48KBITRATE_MONO_MP3
    );
  }
  
  async speak(text, emotion = 'neutral') {
    try {
      const emotionSettings = EMOTIONS[emotion] || EMOTIONS.neutral;
      const voiceConfig = VOICES[this.currentVoice];
      
      // Combine base voice pitch with emotion pitch
      const basePitch = parseInt(voiceConfig.pitch);
      const emotionPitch = parseInt(emotionSettings.pitch);
      const combinedPitch = `+${basePitch + emotionPitch}Hz`;
      
      // Generate unique filename for this audio
      const timestamp = Date.now();
      const randomSuffix = Math.random().toString(36).substring(7);
      const uniqueId = `${timestamp}_${randomSuffix}`;
      
      // Create a subdirectory for this specific audio
      const audioDir = join(this.tempDir, uniqueId);
      await mkdir(audioDir, { recursive: true });
      
      // Generate audio - msedge-tts will create audio.mp3 in the directory
      const { audioFilePath } = await this.tts.toFile(
        audioDir,
        text,
        {
          rate: emotionSettings.rate,
          pitch: combinedPitch,
          volume: emotionSettings.volume
        }
      );
      
      // Create a VBScript that plays audio completely hidden
      const vbsScript = `
Set Sound = CreateObject("WMPlayer.OCX.7")
Sound.URL = "${audioFilePath}"
Sound.settings.volume = 100
Sound.settings.setMode "loop", False
Sound.Controls.play
While Sound.playState <> 1
  WScript.Sleep 100
Wend
`.trim();
      
      // Write VBScript to temp file with unique name
      const vbsPath = join(this.tempDir, `play_${uniqueId}.vbs`);
      await writeFile(vbsPath, vbsScript);
      
      // Add to queue instead of playing immediately
      this.audioQueue.add(audioFilePath, vbsPath, audioDir);
      
      // Log for debugging
      console.error(`Queued: ${uniqueId}/audio.mp3 with voice ${this.currentVoice} (${emotion} emotion)`);
      
      return { success: true, emotion, voice: this.currentVoice, audioFilePath };
    } catch (error) {
      throw error;
    }
  }
  
  cleanText(text) {
    // Remove markdown and convert emojis
    text = text.replace(/[*_`]/g, '');
    
    const replacements = {
      '♡': 'heart',
      '♥': 'heart',
      '★': 'star',
      '☆': 'star',
      '～': ' ',
      '〜': ' ',
      '・': ', ',
    };
    
    for (const [old, replacement] of Object.entries(replacements)) {
      text = text.replace(new RegExp(old, 'g'), replacement);
    }
    
    text = text.replace(/\s+/g, ' ').trim();
    
    if (text.length > 500) {
      text = text.substring(0, 500) + '...';
    }
    
    return text;
  }
}

// Create voice engine instance
const voiceEngine = new VoiceEngine();

// Create MCP server
const server = new Server(
  {
    name: 'maid-mcp',
    version: '1.0.0',
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
      {
        name: 'show_avatar',
        description: 'Show the visual avatar on screen',
        inputSchema: {
          type: 'object',
          properties: {
            pose: {
              type: 'string',
              description: 'Initial pose to display (default: idle)',
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
        name: 'set_avatar_pose',
        description: 'Change the avatar pose/emotion',
        inputSchema: {
          type: 'object',
          properties: {
            pose: {
              type: 'string',
              description: 'The pose to display (idle, happy, sad, thinking, talking, sleeping, angry, love, pick_up, write)'
            }
          },
          required: ['pose']
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
        name: 'list_avatar_poses',
        description: 'List all available avatar poses',
        inputSchema: {
          type: 'object',
          properties: {}
        }
      },
      {
        name: 'start_animation',
        description: 'Start animation sequence with avatar poses',
        inputSchema: {
          type: 'object',
          properties: {
            sequence: {
              type: 'string',
              description: 'Comma-separated list of poses (e.g. "search_1,search_2,search_3")'
            },
            fps: {
              type: 'number',
              description: 'Frames per second (default: 2)',
              default: 2
            },
            loop: {
              type: 'boolean',
              description: 'Whether to loop the animation (default: false)',
              default: false
            }
          },
          required: ['sequence']
        }
      },
      {
        name: 'stop_animation',
        description: 'Stop any running avatar animation',
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
        const voiceList = Object.entries(VOICES).map(([id, info]) => ({
          id,
          ...info,
          note: info.language.startsWith('ja-JP') ? 'Japanese accent voice' : 'Standard voice'
        }));
        
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(voiceList, null, 2)
          }]
        };
      }
      
      case 'set_voice': {
        await voiceEngine.setVoice(args.voiceId);
        const voiceInfo = VOICES[args.voiceId];
        
        return {
          content: [{
            type: 'text',
            text: `Voice set to: ${args.voiceId} (${voiceInfo.name}) - ${voiceInfo.language.startsWith('ja-JP') ? 'Japanese accent' : 'Standard'} voice`
          }]
        };
      }
      
      case 'show_avatar': {
        try {
          const pose = args.pose || 'idle';
          const x = args.x || 1000;
          const y = args.y || 100;
          
          await axios.post('http://localhost:3338/state', {
            visible: true,
            pose: pose,
            position: { x, y }
          });
          
          return {
            content: [{
              type: 'text',
              text: `Avatar shown at position (${x}, ${y}) with ${pose} pose`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: 'Failed to show avatar. Make sure avatar system is running (run avatar/start_avatar.bat)'
            }]
          };
        }
      }
      
      case 'hide_avatar': {
        try {
          // First stop any animation
          try {
            await axios.delete('http://localhost:3338/animate');
          } catch (e) {
            // Ignore error if no animation was running
          }
          
          // Then hide the avatar
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
      
      case 'set_avatar_pose': {
        try {
          // First stop any running animation
          try {
            await axios.delete('http://localhost:3338/animate');
          } catch (e) {
            // Ignore error if no animation was running
          }
          
          // Then set the pose
          await axios.post('http://localhost:3338/state', { 
            pose: args.pose,
            visible: true  // Auto-show when changing pose
          });
          
          return {
            content: [{
              type: 'text',
              text: `Avatar pose changed to: ${args.pose} (and shown if hidden)`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: 'Failed to set avatar pose. Make sure avatar system is running.'
            }]
          };
        }
      }
      
      case 'move_avatar': {
        try {
          // When moving, also make sure avatar is visible
          // Note: We don't clear animation here as moving shouldn't stop animations
          await axios.post('http://localhost:3338/state', {
            position: { x: args.x, y: args.y },
            visible: true  // Auto-show when moving
          });
          
          return {
            content: [{
              type: 'text',
              text: `Avatar moved to position (${args.x}, ${args.y}) (and shown if hidden)`
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
      
      case 'list_avatar_poses': {
        const availablePoses = [
          { name: 'idle', description: 'Standing politely with serving tray, pleasant smile' },
          { name: 'happy', description: 'Jumping with arms raised, one leg up, very excited' },

          { name: 'thinking', description: 'Hand on chin, contemplative pose' },
          { name: 'talking', description: 'Hand extended palm-up, explaining something' },
          { name: 'sleeping', description: 'Eyes closed with Zzz, leaning on broom' },
          { name: 'anger', description: 'Hands on hips, stern expression, assertive stance' },
          { name: 'love', description: 'Heart eyes, hands clasped together, adoring expression' },
          { name: 'pick_up', description: 'Being moved or lifted' },
          { name: 'write', description: 'Turned away, appears to be writing something' },
          { name: 'master', description: 'Arms spread wide horizontally, welcoming pose' },
          { name: 'search_1', description: 'Bending over treasure chest, searching inside' },
          { name: 'search_2', description: 'Different angle searching in treasure chest' },
          { name: 'search_3', description: 'Victory pose with golden trophy, sitting on chest' }
        ];
        
        const poseList = availablePoses.map(p => `• ${p.name}: ${p.description}`).join('\n');
        
        return {
          content: [{
            type: 'text',
            text: `Available avatar poses:\n\n${poseList}`
          }]
        };
      }
      
      case 'start_animation': {
        try {
          const sequence = args.sequence.split(',').map(s => s.trim());
          const fps = args.fps || 2;
          const loop = args.loop || false;
          
          // Validate poses exist (basic check)
          if (sequence.length === 0) {
            throw new Error('Animation sequence cannot be empty');
          }
          
          // Send animation request to avatar server
          await axios.post('http://localhost:3338/animate', {
            sequence: sequence,
            fps: fps,
            loop: loop
          });
          
          const duration = sequence.length / fps;
          
          return {
            content: [{
              type: 'text',
              text: `Started animation: ${sequence.join(' → ')} at ${fps} FPS${loop ? ' (looping)' : ''}`
            }]
          };
        } catch (error) {
          return {
            content: [{
              type: 'text',
              text: `Failed to start animation. Make sure avatar system is running. Error: ${error.message}`
            }]
          };
        }
      }
      
      case 'stop_animation': {
        try {
          // Send DELETE request to stop animation
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
    await voiceEngine.initialize();
    
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    console.error('maid-mcp server running - Voice with audio queue system ready!');
    console.error('Audio files are queued and played sequentially to avoid conflicts.');
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

main();
