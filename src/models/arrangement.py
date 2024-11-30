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
        # Since Clip is now immutable, we need to create a new one with the arrangement name
        new_clip = Clip(
            name=clip.name,
            position=clip.position,
            duration=clip.duration,
            color=clip.color,
            source_path=clip.source_path,
            volume=clip.volume,
            muted=clip.muted,
            arrangement_name=self.name
        )
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
            
        # Calculate end time for each clip (position + duration)
        end_times = [clip.position + clip.duration for clip in self.clips]
        return max(end_times) if end_times else 0.0
    
    def validate(self) -> None:
        """Validate arrangement and all its clips."""
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")
            
        # Validate each clip
        for clip in self.clips:
            # Clip is now validated on creation due to dataclass post_init
            
            # Verify clip belongs to this arrangement
            if clip.arrangement_name != self.name:
                raise ValueError(f"Clip {clip.name} has incorrect arrangement assignment")
            
        # Check for clip name uniqueness
        names = [clip.name for clip in self.clips]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate clip names are not allowed")
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert arrangement to dictionary format for serialization."""
        return {
            'name': self.name,
            'folder_path': str(self.folder_path) if self.folder_path else None,
            'clips': [clip.__dict__ for clip in self.clips]
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
            clip = Clip(
                name=clip_data['name'],
                position=clip_data['position'],
                duration=clip_data['duration'],
                color=clip_data['color'],
                source_path=Path(clip_data['source_path']) if clip_data.get('source_path') else None,
                volume=clip_data.get('volume', 1.0),
                muted=clip_data.get('muted', False),
                arrangement_name=clip_data.get('arrangement_name')
            )
            arrangement.add_clip(clip)
            
        return arrangement