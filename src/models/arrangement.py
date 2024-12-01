# src/models/arrangement.py

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

from .clip import Clip

@dataclass
class Arrangement:
    """Represents an arrangement containing multiple audio clips."""
    
    name: str
    clips: List[Clip] = field(default_factory=list)
    folder_path: Optional[Path] = None
    
    def add_clip(self, clip: Clip) -> None:
        """Add a clip to the arrangement."""
        # Create new clip with arrangement name
        new_clip = clip.with_arrangement(self.name)
        self.clips.append(new_clip)
        
    def remove_clip(self, clip: Clip) -> None:
        """Remove a clip from the arrangement."""
        self.clips = [c for c in self.clips if c != clip]
            
    def get_clip_by_name(self, name: str) -> Optional[Clip]:
        """Find a clip by its name."""
        for clip in self.clips:
            if clip.name == name:
                return clip
        return None
        
    def get_duration(self) -> float:
        """Get total arrangement duration based on clip positions."""
        if not self.clips:
            return 0.0
            
        end_times = [clip.position + clip.duration for clip in self.clips]
        return max(end_times) if end_times else 0.0
    
    def validate(self) -> None:
        """Validate arrangement and all its clips."""
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")
            
        # Verify clip arrangement assignments
        for clip in self.clips:
            if clip.arrangement_name != self.name:
                raise ValueError(f"Clip {clip.name} has incorrect arrangement assignment")
            
        # Check for clip name uniqueness
        names = [clip.name for clip in self.clips]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate clip names are not allowed")