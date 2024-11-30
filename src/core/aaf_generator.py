from pathlib import Path
from typing import Dict, Optional, TYPE_CHECKING

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
        self.audio_file_map = audio_file_map  # Maps clips to exported audio paths
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
    def generate_aaf(self, output_path: str) -> None:
        """Generate AAF file for arrangement.
        
        Args:
            output_path: Path where AAF file should be created
            
        Raises:
            FileNotFoundError: If audio files are missing
            OSError: If AAF generation fails
        """
        output_path = Path(output_path)
        
        try:
            import aaf2
            with aaf2.open(str(output_path), 'w') as f:
                # Create main composition
                main_composition = f.create.MasterMob(self.arrangement.name)
                f.content.mobs.append(main_composition)
                
                # Set basic project properties
                edit_rate = 25  # Standard frame rate 
                
                # Create tape source (for timecode)
                tape_mob = f.create.SourceMob()
                f.content.mobs.append(tape_mob)
                timecode_rate = 25
                start_time = 0
                
                # Add tape slots
                tape_mob.create_tape_slots(
                    "Master", 
                    edit_rate,
                    timecode_rate, 
                    media_kind='picture'
                )
                
                # Process each clip in the arrangement
                for clip in sorted(self.arrangement.clips, key=lambda x: x.position):
                    self._add_clip_to_composition(f, main_composition, clip, edit_rate)
                    
                self.logger.info(f"Generated AAF file at {output_path}")
                    
        except Exception as e:
            self.logger.error(f"Failed to generate AAF file: {e}")
            raise
            
    def _add_clip_to_composition(self, f: "aaf2.File", composition: "aaf2.MasterMob", 
                               clip: "Clip", edit_rate: int) -> None:
        """Add a clip to the AAF composition.
        
        Args:
            f: AAF file object
            composition: Master mob composition
            clip: Clip to add
            edit_rate: Frame rate for timing calculations
            
        Raises:
            FileNotFoundError: If audio file is missing
            ValueError: If clip data is invalid
        """
        try:
            # Get the exported audio file path
            audio_path = self.audio_file_map.get(clip)
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