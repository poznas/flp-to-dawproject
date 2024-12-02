import logging
import wave
import numpy as np
import soundfile as sf
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from ..models.clip import Clip

class AudioProcessor:
    """Handles audio file validation and conversion."""
    
    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.temp_dir = Path(tempfile.mkdtemp())

    def _convert_to_standard_wav(self, input_path: Path) -> Optional[Path]:
        """Convert audio file to standard PCM WAV format using soundfile."""
        # Create temp output path
        output_path = self.temp_dir / f"{input_path.stem}_converted.wav"
        
        # Read using soundfile (supports many formats)
        data, sample_rate = sf.read(str(input_path))
        
        # Convert to float32 for processing
        data = data.astype(np.float32)
        
        # If mono, reshape to 2D array
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        
        # Write as standard PCM WAV
        sf.write(str(output_path), data, sample_rate, subtype='PCM_16')
        
        return output_path

    def process_audio_clips(self, clips: list) -> dict:
        """Process and validate audio clips, converting formats if needed."""
        processed_clips = {}
        
        for clip in clips:
            if not clip.source_path or not clip.source_path.exists():
                self.logger.warning(f"Source file not found: {clip.source_path}")
                continue

             # Create output filename
            output_path = self.output_dir / f"{clip.name}.wav"
            
            # Convert to standard PCM WAV
            if self._convert_to_pcm_wav(clip.source_path, output_path):
                processed_clips[clip] = output_path
            else:
                self.logger.error(f"Failed to process {clip.name}")

        return processed_clips

    def validate_audio_files(self, clips: List[Clip]) -> Dict[Clip, Path]:
        """Validate processed audio files."""
        valid_clips = {}
        
        for clip, path in self.process_audio_clips(clips).items():
            with wave.open(str(path), 'rb') as wav_file:
                # Verify it's standard PCM format
                if wav_file.getcomptype() == 'NONE':
                    valid_clips[clip] = path
                
        return valid_clips