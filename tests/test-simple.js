// Test VBScript hidden audio playback
import { MsEdgeTTS, OUTPUT_FORMAT } from 'msedge-tts';
import { mkdir, writeFile, unlink } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { exec } from 'child_process';

async function testVoice() {
  console.log('Testing Japanese accent voice with VBScript (no windows)...\n');
  
  try {
    // Create temp directory
    const tempDir = join(process.cwd(), 'temp_voice');
    if (!existsSync(tempDir)) {
      await mkdir(tempDir, { recursive: true });
    }
    
    // Initialize TTS with Japanese voice
    const tts = new MsEdgeTTS();
    console.log('TTS instance created');
    
    // Use Japanese voice for authentic accent
    await tts.setMetadata(
      'ja-JP-NanamiNeural',
      OUTPUT_FORMAT.AUDIO_24KHZ_48KBITRATE_MONO_MP3
    );
    console.log('Japanese voice set (Nanami)');
    
    // Generate audio with Japanese accent pitch
    console.log('Generating audio with Japanese accent...');
    const { audioFilePath } = await tts.toFile(
      tempDir, 
      'Good morning, Master! I hope you had a wonderful rest. I have prepared everything for your day and I am ready to assist you with whatever you need. Please let me know how I can make your day more comfortable!',
      {
        pitch: '+30Hz',  // Base +20Hz + Happy +10Hz
        rate: '+5%',     // Happy emotion
        volume: '+0%'
      }
    );
    console.log('Audio generated at:', audioFilePath);
    
    // Create VBScript for hidden playback
    console.log('\nCreating VBScript for hidden playback...');
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
    
    const vbsPath = join(tempDir, `test_play_${Date.now()}.vbs`);
    await writeFile(vbsPath, vbsScript);
    console.log('VBScript created at:', vbsPath);
    
    // Execute with wscript //B for completely hidden execution
    console.log('\nPlaying audio with VBScript (completely hidden)...');
    exec(`wscript //B "${vbsPath}"`, {
      windowsHide: true
    }, async (error) => {
      if (error) {
        console.error('Playback error:', error.message);
      } else {
        console.log('✅ Audio playback started successfully!');
      }
      
      // Clean up after 10 seconds
      setTimeout(async () => {
        try {
          await unlink(vbsPath);
          console.log('VBScript cleaned up');
        } catch (e) {
          // Ignore
        }
      }, 10000);
    });
    
    console.log('\n✅ Voice test complete!');
    console.log('Audio is playing completely in the background.');
    console.log('NO windows should appear!');
    console.log('\nKey features:');
    console.log('- wscript //B runs VBScript in batch mode (no UI)');
    console.log('- WMPlayer.OCX.7 COM object plays audio');
    console.log('- Waits for playback to complete before exiting');
    console.log('- Completely hidden - no windows at all!');
    
  } catch (error) {
    console.error('\n❌ Voice test failed:', error?.message || error);
  }
}

testVoice();
