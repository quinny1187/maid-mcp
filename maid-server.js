// maid-mcp server - Voice synthesis with VBScript hidden audio playback
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { MsEdgeTTS, OUTPUT_FORMAT } from 'msedge-tts';
import { mkdir, writeFile, unlink } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { exec } from 'child_process';

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

// TTS Engine wrapper
class VoiceEngine {
  constructor() {
    this.tts = new MsEdgeTTS();
    // Default to Japanese voice for Japanese accent
    this.currentVoice = 'ja-JP-NanamiNeural';
    this.tempDir = join(process.cwd(), 'temp_voice');
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
      
      // Generate audio with combined settings
      const { audioFilePath } = await this.tts.toFile(
        this.tempDir, 
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
      
      // Write VBScript to temp file
      const vbsPath = join(this.tempDir, `play_${Date.now()}.vbs`);
      await writeFile(vbsPath, vbsScript);
      
      // Execute VBScript with wscript (completely hidden)
      exec(`wscript //B "${vbsPath}"`, {
        windowsHide: true
      }, async (error) => {
        if (error) {
          console.error('Audio playback error:', error.message);
        }
        // Clean up VBScript file after a delay
        setTimeout(async () => {
          try {
            await unlink(vbsPath);
          } catch (e) {
            // Ignore cleanup errors
          }
        }, 5000);
      });
      
      // Log for debugging
      console.error(`Playing: ${audioFilePath} with voice ${this.currentVoice} (${emotion} emotion) - using VBScript (no window)`);
      
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
    
    console.error('maid-mcp server running - Voice tools ready with Japanese accent support!');
    console.error('Using VBScript for completely hidden audio playback (no windows!)');
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

main();
