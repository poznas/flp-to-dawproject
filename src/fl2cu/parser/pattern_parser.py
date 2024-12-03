from typing import List, Optional
import logging
from ..models.clip import Clip
from .clip_parser import FLClipParser

class FLPatternParser:
    """Handles parsing of patterns from FL Studio projects."""
    
    def __init__(self, fl_project: 'pyflp.Project', clip_parser: FLClipParser):
        self.fl_project = fl_project
        self.clip_parser = clip_parser
        self.logger = logging.getLogger(__name__)

    def create_clips_from_pattern(self, pattern, base_position: float = 0) -> List[Clip]:
        """Create clips from an FL Studio pattern."""
        clips = []
        
        try:
            if not pattern.name:
                return clips

            self.logger.debug(f"Processing pattern: {pattern.name}")
            
            for channel_id, channel in enumerate(pattern.channels):
                if not channel or not hasattr(channel, 'sample_path'):
                    continue
                    
                position = base_position + (pattern.position if hasattr(pattern, 'position') else 0)
                
                clip = self.clip_parser.create_clip_from_channel(
                    channel=channel,
                    position=position,
                    ppq=self.fl_project.ppq
                )
                
                if clip:
                    clips.append(clip)
                    self.logger.debug(f"Added clip {clip.name} from pattern {pattern.name}")

        except Exception as e:
            self.logger.error(f"Failed to create clips from pattern: {e}")
            
        return clips