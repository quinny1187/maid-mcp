// Audio Queue System for sequential playback
import { exec } from 'child_process';
import { unlink, rmdir } from 'fs/promises';

export class AudioQueue {
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
