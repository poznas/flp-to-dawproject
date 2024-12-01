import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import wave
import numpy as np
import aaf2
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING
import shutil
import struct

if TYPE_CHECKING:
    from ..models.arrangement import Arrangement
    from ..models.clip import Clip

class AAFGenerator:
    """Generates AAF files for Cubase import with clip positions and metadata."""
    
    def __init__(self, arrangement: "Arrangement", audio_file_map: Dict["Clip", Path]):
        """Initialize AAF generator.
        
        Args:
            arrangement: Arrangement to process
            audio_file_map: Mapping of clips to their exported audio file paths
        """
        self.arrangement = arrangement
        self.audio_file_map = {
            hash(clip): path for clip, path in audio_file_map.items()
        }  # Store using clip hashes since Clip is now immutable
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
    # src/core/aaf_generator.py

    def generate_aaf(self, output_path: str) -> None:
        """Generate AAF file for arrangement."""
        output_path = Path(output_path)
        
        # Validate audio files first
        missing_files = []
        for clip in self.arrangement.clips:
            audio_path = self.audio_file_map.get(hash(clip))
            if not audio_path or not audio_path.exists():
                missing_files.append(clip.name)
                
        if missing_files:
            raise FileNotFoundError(f"Missing audio files for clips: {', '.join(missing_files)}")
        
        try:
            with aaf2.open(str(output_path), 'w') as f:
                # Create composition
                comp = f.create.Composition(self.arrangement.name)
                
                # Create tape mob (required for timeline)
                tape_mob = f.create.SourceMob()
                f.content.mobs.append(tape_mob)
                tape_slot = tape_mob.create_timeline_sound_slot(edit_rate=48000)
                
                # Create master mob
                master_mob = f.create.MasterMob(self.arrangement.name)
                f.content.mobs.append(master_mob)
                
                # Process clips
                sequence = []
                for clip in sorted(self.arrangement.clips, key=lambda x: x.position):
                    audio_path = self.audio_file_map.get(hash(clip))
                    if not audio_path or not audio_path.exists():
                        self.logger.warning(f"Audio file not found for clip {clip.name}, skipping")
                        continue
                        
                    try:
                        # Create source mob
                        source_mob = f.create.SourceMob()
                        f.content.mobs.append(source_mob)
                        
                        # Import audio
                        source_slot = source_mob.import_audio_essence(str(audio_path))
                        src_clip = source_slot.segment
                        
                        # Set timing
                        src_clip.start = int(clip.position * 48000)
                        src_clip.length = int(clip.duration * 48000)
                        
                        # Add to sequence
                        sequence.append(src_clip)
                        
                    except Exception as e:
                        self.logger.error(f"Failed to process clip {clip.name}: {e}")
                        
                # Create sequence
                if sequence:
                    comp_slot = comp.create_timeline_sound_slot(edit_rate=48000)
                    comp_slot.segment.components = sequence
                    
                self.logger.info(f"Generated AAF file at {output_path}")
                
        except Exception as e:
            self.logger.error(f"Failed to generate AAF file: {e}")
            raise
                
    def _add_clip_to_composition(self, f: "aaf2.File", composition: "aaf2.MasterMob", 
                               clip: "Clip", edit_rate: int) -> None:
        """Add a clip to the AAF composition."""
        try:
            # Get the exported audio file path using clip hash
            audio_path = self.audio_file_map.get(hash(clip))
            if not audio_path or not audio_path.exists():
                self.logger.warning(f"Audio file not found for clip {clip.name}, skipping")
                return
                
            # Create source mob for the audio file
            source_mob = f.create.SourceMob()
            f.content.mobs.append(source_mob)
            
            # Import the audio essence
            source_mob.import_audio_essence(
                str(audio_path),
                edit_rate
            )
            
            # Calculate position and length in edit rate units
            position_frames = int(clip.position * edit_rate)
            length_frames = int(clip.duration * edit_rate)
            
            # Create the clip reference
            clip_slot = source_mob.create_source_clip(1, position_frames)
            clip_slot.length = length_frames
            
            # Set clip metadata if supported by AAF version
            try:
                if hasattr(clip_slot, 'user_comments'):
                    clip_slot.user_comments['Name'] = clip.name
                    clip_slot.user_comments['Color'] = clip.color
                    if clip.muted:
                        clip_slot.user_comments['Muted'] = 'true'
            except Exception as e:
                self.logger.warning(f"Failed to set clip metadata: {e}")
                
            # Apply volume if different from default
            if clip.volume != 1.0:
                try:
                    clip_slot.volume = clip.volume
                except Exception as e:
                    self.logger.warning(f"Failed to set clip volume: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to add clip {clip.name} to AAF: {e}")
            raise