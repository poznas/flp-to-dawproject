from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
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
        clip.arrangement_name = self.name
        self.clips.append(clip)
        
    def remove_clip(self, clip: Clip) -> None:
        """Remove a clip from the arrangement."""
        if clip in self.clips:
            clip.arrangement_name = None
            self.clips.remove(clip)
            
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
        return max(clip.position + clip.duration for clip in self.clips)
    
    def validate(self) -> None:
        """Validate arrangement and all its clips."""
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")
            
        # Validate each clip
        for clip in self.clips:
            clip.validate()
            
        # Check for clip name uniqueness
        names = [clip.name for clip in self.clips]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate clip names are not allowed")
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert arrangement to dictionary format for serialization."""
        return {
            'name': self.name,
            'folder_path': str(self.folder_path) if self.folder_path else None,
            'clips': [clip.to_dict() for clip in self.clips]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Arrangement':
        """Create arrangement instance from dictionary data."""
        folder_path = Path(data['folder_path']) if data.get('folder_path') else None
        
        arrangement = cls(
            name=data['name'],
            folder_path=folder_path
        )
        
        # Add clips
        for clip_data in data.get('clips', []):
            clip = Clip.from_dict(clip_data)
            arrangement.add_clip(clip)
            
        return arrangement
    
    def get_clips_in_time_range(self, start: float, end: float) -> List[Clip]:
        """Get all clips that overlap with the given time range."""
        return [
            clip for clip in self.clips
            if clip.position < end and (clip.position + clip.duration) > start
        ]