// TTS Engine wrapper with queue
import { MsEdgeTTS, OUTPUT_FORMAT } from 'msedge-tts';
import { mkdir, writeFile } from 'fs/promises';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { AudioQueue } from './audioQueue.js';
import { VOICES, EMOTIONS, DEFAULT_VOICE } from './voiceConfig.js';

// Get the directory of this script
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export class VoiceEngine {
  constructor() {
    this.tts = new MsEdgeTTS();
    this.currentVoice = DEFAULT_VOICE;
    this.tempDir = join(dirname(dirname(__dirname)), 'temp_voice');
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
    
    try {
      this.currentVoice = voiceId;
      await this.tts.setMetadata(
        voiceId,
        OUTPUT_FORMAT.AUDIO_24KHZ_48KBITRATE_MONO_MP3
      );
      return true;
    } catch (error) {
      // Voice still changes despite the error
      this.currentVoice = voiceId;
      console.error('Voice metadata error (voice still changed):', error.message);
      return true;
    }
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
  
  getCurrentVoice() {
    return this.currentVoice;
  }
  
  getVoiceInfo(voiceId) {
    return VOICES[voiceId];
  }
  
  listVoices() {
    return Object.entries(VOICES).map(([id, info]) => ({
      id,
      ...info,
      note: info.language.startsWith('ja-JP') ? 'Japanese accent voice' : 'Standard voice'
    }));
  }
}
