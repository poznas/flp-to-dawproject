import logging
from pathlib import Path
from typing import Dict, Optional

import aaf2
from aaf2 import mobs, components, essence

from ..models.arrangement import Arrangement
from ..models.clip import Clip

logger = logging.getLogger(__name__)

class AAFGenerator:
    """Generates AAF files from arrangements."""
    
    def __init__(self, arrangement: Arrangement, clip_paths: Dict[Clip, Path]):
        """Initialize the AAF generator.
        
        Args:
            arrangement: The arrangement to convert
            clip_paths: Mapping of clips to their audio file paths
        """
        self.arrangement = arrangement
        self.clip_paths = clip_paths
        self.edit_rate = 48000  # Standard audio sample rate for professional audio
        
    def generate_aaf(self, output_path: str) -> None:
        """Generate an AAF file for the arrangement.
        
        Args:
            output_path: Path where the AAF file will be saved
        """
        with aaf2.open(output_path, 'w') as f:
            # Create main composition
            comp_mob = f.create.CompositionMob()
            comp_mob.name = self.arrangement.name
            f.content.mobs.append(comp_mob)
            
            # Create timeline
            timeline = f.create.Sequence(media_kind='sound')
            comp_mob.usage = ['Usage_TopLevel']
            
            try:
                for clip in self.arrangement.clips:
                    source_path = self.clip_paths.get(clip)
                    if not source_path or not source_path.exists():
                        logger.warning(f"Skipping clip {clip.name} - source file not found")
                        continue
                        
                    try:
                        # Create source mob for the audio file
                        source_mob = f.create.SourceMob()
                        f.content.mobs.append(source_mob)
                        
                        # Create essence descriptor
                        descriptor = f.create.PCMDescriptor()
                        descriptor.sample_rate = self.edit_rate
                        descriptor.channels = 2  # Stereo
                        descriptor.quantization_bits = 16
                        source_mob.descriptor = descriptor
                        
                        # Create source clip
                        source_clip = f.create.SourceClip()
                        source_clip.mob = source_mob
                        source_clip.length = int(clip.duration * self.edit_rate)
                        
                        # Create timeline slot
                        slot = source_mob.create_timeline_slot(
                            edit_rate=self.edit_rate,
                            length=source_clip.length
                        )
                        slot.segment = source_clip
                        
                        # Create reference to the source in the composition
                        comp_clip = f.create.SourceClip()
                        comp_clip.mob = source_mob
                        comp_clip.slot = slot
                        comp_clip.length = source_clip.length
                        comp_clip.start = int(clip.position * self.edit_rate)
                        
                        # Set clip metadata
                        comp_clip.user_comments = {
                            'Name': clip.name,
                            'Color': clip.color,
                            'Muted': str(clip.muted).lower(),
                            'Volume': str(clip.volume)
                        }
                        
                        # Add to timeline
                        timeline.components.append(comp_clip)
                        
                    except Exception as e:
                        logger.error(f"Error adding clip {clip.name}: {str(e)}")
                        continue
                        
                # Set the timeline as the composition's first slot
                comp_slot = comp_mob.create_timeline_slot(
                    edit_rate=self.edit_rate,
                    length=sum(c.length for c in timeline.components)
                )
                comp_slot.segment = timeline
                
            except Exception as e:
                logger.error(f"Failed to generate AAF: {str(e)}")
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