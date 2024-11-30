import wave
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import shutil
from concurrent.futures import ThreadPoolExecutor
import logging

from ..models.clip import Clip
from ..utils.logger import get_logger
from ..config import Config

class AudioProcessor:
    """Handles audio file operations including export and quality preservation."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.logger = get_logger()
        self.config = Config()
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def export_audio_clips(self, clips: List[Clip], max_workers: Optional[int] = None) -> Dict[Clip, Path]:
        """Export audio clips while preserving quality.
        Returns a dictionary mapping clips to their exported file paths."""
        
        result = {}
        failed_clips = []
        max_workers = max_workers or self.config.MAX_PARALLEL_EXPORTS

        # Process clips in parallel for better performance
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_clip = {
                executor.submit(self._process_clip, clip): clip 
                for clip in clips 
                if clip.source_path and clip.source_path.exists()
            }
            
            for future in future_to_clip:
                clip = future_to_clip[future]
                try:
                    output_path = future.result()
                    if output_path:
                        result[clip] = output_path
                    else:
                        failed_clips.append(clip)
                except Exception as e:
                    self.logger.error(f"Failed to process clip {clip.name}: {e}")
                    failed_clips.append(clip)

        if failed_clips:
            self.logger.warning(f"Failed to process {len(failed_clips)} clips")
            
        return result
        
    def _process_clip(self, clip: Clip) -> Optional[Path]:
        """Process a single audio clip."""
        try:
            source_path = clip.source_path
            if not source_path or not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")

            # Create unique output path
            output_path = self.output_dir / f"{clip.name}_{clip.source_path.stem}.wav"
            i = 1
            while output_path.exists():
                output_path = self.output_dir / f"{clip.name}_{clip.source_path.stem}_{i}.wav"
                i += 1

            # For WAV files, we can optimize by copying if no processing is needed
            if source_path.suffix.lower() == '.wav' and clip.volume == 1.0:
                shutil.copy2(source_path, output_path)
                self.logger.debug(f"Copied {clip.name} to {output_path}")
                return output_path

            # Otherwise, process the audio data
            with wave.open(str(source_path), 'rb') as wav_in:
                params = wav_in.getparams()
                frames = wav_in.readframes(wav_in.getnframes())
                
                # Apply volume adjustment if needed
                if clip.volume != 1.0:
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                    audio_data = (audio_data * clip.volume).astype(np.int16)
                    frames = audio_data.tobytes()

                with wave.open(str(output_path), 'wb') as wav_out:
                    wav_out.setparams(params)
                    wav_out.writeframes(frames)

            self.logger.debug(f"Processed {clip.name} to {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Error processing clip {clip.name}: {e}")
            return None
            
    def validate_audio_files(self, clips: List[Clip]) -> bool:
        """Validate all audio files in the output directory."""
        all_valid = True
        
        for clip in clips:
            output_path = self.output_dir / f"{clip.name}_{clip.source_path.stem}.wav"
            if not output_path.exists():
                self.logger.error(f"Missing output file for clip {clip.name}")
                all_valid = False
                continue
                
            try:
                with wave.open(str(output_path), 'rb') as wav:
                    if wav.getnframes() == 0:
                        self.logger.error(f"Empty audio file for clip {clip.name}")
                        all_valid = False
            except Exception as e:
                self.logger.error(f"Invalid audio file for clip {clip.name}: {e}")
                all_valid = False
                
        return all_valid