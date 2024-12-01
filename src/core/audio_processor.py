from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import wave
import numpy as np
import shutil

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
        """Export audio clips while preserving quality."""
        result: Dict[Clip, Path] = {}
        max_workers = max_workers or self.config.MAX_PARALLEL_EXPORTS

        # Process clips in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_clip = {
                executor.submit(self._process_clip, clip): clip 
                for clip in clips
                if clip.source_path and clip.source_path.exists()
            }

            for future in concurrent.futures.as_completed(future_to_clip):
                clip = future_to_clip[future]
                try:
                    output_path = future.result()
                    if output_path:
                        # Validate output file
                        try:
                            with wave.open(str(output_path), 'rb') as wav:
                                if wav.getnframes() > 0:
                                    result[clip] = output_path
                                else:
                                    self.logger.error(f"Generated empty audio file for {clip.name}")
                        except wave.Error:
                            self.logger.error(f"Invalid audio file generated for {clip.name}")
                            output_path.unlink(missing_ok=True)
                except Exception as e:
                    self.logger.error(f"Failed to process clip {clip.name}: {e}")

        
    def _process_clip(self, clip: Clip) -> Optional[Path]:
        """Process a single audio clip."""
        try:
            if not clip.source_path or not clip.source_path.exists():
                self.logger.error(f"Source file not found: {clip.source_path}")
                return None

            # Create unique output path
            output_path = self._get_unique_output_path(clip)

            try:
                with wave.open(str(clip.source_path), 'rb') as wav_in:
                    params = wav_in.getparams()
                    frames = wav_in.readframes(wav_in.getnframes())
                    audio_data = np.frombuffer(frames, dtype=np.int16)

                    if clip.muted:
                        audio_data = np.zeros_like(audio_data)
                    elif clip.volume != 1.0:
                        # Convert to float32 for processing
                        float_data = audio_data.astype(np.float32) / 32767.0
                        # Apply volume
                        float_data *= clip.volume
                        # Convert back to int16 with proper scaling
                        audio_data = (float_data * 32767.0).clip(-32768, 32767).astype(np.int16)

                with wave.open(str(output_path), 'wb') as wav_out:
                    wav_out.setparams(params)
                    wav_out.writeframes(audio_data.tobytes())

                self.logger.debug(f"Processed {clip.name} to {output_path}")
                return output_path

            except (wave.Error, IOError) as e:
                self.logger.error(f"Error processing audio file: {e}")
                return None

        except Exception as e:
            self.logger.error(f"Error processing clip {clip.name}: {e}")
            return None

    def _get_unique_output_path(self, clip: Clip) -> Path:
        """Generate unique output path for clip."""
        base_name = clip.name
        base_stem = clip.source_path.stem if clip.source_path else "output"
        
        # Include position in filename to ensure uniqueness for same-named clips
        position_str = f"{clip.position:.3f}".replace('.', '_')
        unique_id = f"{base_name}_{base_stem}_{position_str}"
        
        output_path = self.output_dir / f"{unique_id}.wav"
        counter = 0
        
        while output_path.exists():
            counter += 1
            output_path = self.output_dir / f"{unique_id}_{counter}.wav"
            
        return output_path
    
    def validate_audio_files(self, clips: List[Clip]) -> bool:
        """Validate all audio files in the output directory."""
        all_valid = True
        
        for clip in clips:
            if not clip.source_path:
                self.logger.error(f"No source path for clip {clip.name}")
                all_valid = False
                continue

            try:
                with wave.open(str(clip.source_path), 'rb') as wav:
                    if wav.getnframes() == 0:
                        self.logger.error(f"Empty audio file for clip {clip.name}")
                        all_valid = False
            except Exception as e:
                self.logger.error(f"Invalid audio file for clip {clip.name}: {e}")
                all_valid = False
                
        return all_valid