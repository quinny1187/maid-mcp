// Voice configuration with Japanese accent settings
export const VOICES = {
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
export const EMOTIONS = {
  neutral: { pitch: '+0Hz', rate: '+0%', volume: '+0%' },
  happy: { pitch: '+10Hz', rate: '+5%', volume: '+0%' },
  sad: { pitch: '-5Hz', rate: '-10%', volume: '-10%' },
  excited: { pitch: '+15Hz', rate: '+10%', volume: '+5%' },
  angry: { pitch: '-10Hz', rate: '+5%', volume: '+5%' },
  shy: { pitch: '+5Hz', rate: '-5%', volume: '-20%' }
};

// Default voice for maid character
export const DEFAULT_VOICE = 'ja-JP-NanamiNeural';
