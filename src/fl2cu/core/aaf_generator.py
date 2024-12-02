import logging
from pathlib import Path
import subprocess
import json
import shutil
import soundfile as sf
import numpy as np
import aaf2
from typing import Dict, Tuple, Optional, Any
from aaf2.file import AAFFile

import aaf2
from aaf2 import mobs, components, essence

from ..models.arrangement import Arrangement
from ..models.clip import Clip
from .audio_processor import AudioProcessor

logger = logging.getLogger(__name__)

class AAFGenerator:
    """Generates AAF files from arrangements using direct WAV linking."""
    
    def __init__(self, arrangement, clip_paths: Dict[Clip, Path]):
        self.arrangement = arrangement
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def _probe_audio(self, path: str) -> Dict[str, Any]:
        """Get audio file metadata using ffprobe."""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-of', 'json',
            '-show_format',
            '-show_streams',
            str(path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ffprobe failed for {path}: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse ffprobe output: {e}")
            raise

    def generate_aaf(self, output_path: str) -> None:
        """Generate AAF file with the arrangement."""
        self.logger.info(f"Creating AAF file at {output_path}")
        
        try:
            with aaf2.open(output_path, 'w') as f:
                # Create the composition mob for the arrangement
                comp_mob = f.create.CompositionMob(self.arrangement.name)
                f.content.mobs.append(comp_mob)
                
                # Create a timeline mobslot for audio
                edit_rate = 48000  # Standard audio sample rate
                slot = comp_mob.create_timeline_slot(edit_rate)
                sequence = f.create.Sequence('sound')
                slot.segment = sequence

                # Process each clip
                for clip in self.arrangement.clips:
                    source_path = self.clip_paths.get(clip)
                    if not source_path or not source_path.exists():
                        self.logger.warning(f"Audio file not found for clip: {clip.name}")
                        continue

                    try:
                        # Get audio metadata using ffprobe
                        metadata = self._probe_audio(str(source_path))
                        print(metadata)
                        
                        # Link the WAV file - this creates master mob, source mob, and tape mob
                        master_mob, source_mob, tape_mob = f.content.link_external_wav(metadata)
                        
                        # Create source clip referencing the master mob
                        clip_mob = f.create.SourceClip()
                        clip_mob.mob = master_mob
                        clip_mob.slot = 1  # Master mobs typically use slot 1
                        clip_mob.start = int(clip.position * edit_rate)
                        clip_mob.length = int(clip.duration * edit_rate)
                        
                        # Add the clip to the sequence
                        sequence.components.append(clip_mob)
                        
                        self.logger.debug(f"Added clip {clip.name} at position {clip.position}")

                    except Exception as e:
                        self.logger.error(f"Failed to process clip {clip.name}: {str(e)}")
                        raise e

                # Save the file
                f.save()
                self.logger.info("AAF file successfully generated")

        except Exception as e:
            self.logger.error(f"Failed to generate AAF file: {str(e)}")
            raise e