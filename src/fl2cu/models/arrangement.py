# src/fl2cu/models/arrangement.py

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

from .clip import Clip

@dataclass(frozen=True)
class Arrangement:
    """Represents an arrangement of audio clips."""
    
    name: str
    clips: List[Clip] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate arrangement after initialization."""
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")

    def __hash__(self):
        """Make arrangement hashable by name."""
        return hash(self.name)
    
    def __eq__(self, other):
        """Compare arrangements by name."""
        if not isinstance(other, Arrangement):
            return NotImplemented
        return self.name == other.name

    def add_clip(self, clip: Clip) -> None:
        """Add a clip to the arrangement.
        
        Args:
            clip: Clip to add
            
        Raises:
            ValueError: If clip with same name already exists
        """
        if self.get_clip_by_name(clip.name):
            raise ValueError(f"Clip with name '{clip.name}' already exists")
        object.__setattr__(self, 'clips', list(self.clips) + [clip])

    def remove_clip(self, clip: Clip) -> None:
        """Remove a clip from the arrangement.
        
        Args:
            clip: Clip to remove
        """
        object.__setattr__(self, 'clips', [c for c in self.clips if c != clip])

    def get_clip_by_name(self, name: str) -> Optional[Clip]:
        """Find clip by name.
        
        Args:
            name: Name to search for
            
        Returns:
            Matching clip or None if not found
        """
        return next((clip for clip in self.clips if clip.name == name), None)

    def get_duration(self) -> float:
        """Get total arrangement duration.
        
        Returns:
            Duration in seconds
        """
        if not self.clips:
            return 0.0
        return max(clip.position + clip.duration for clip in self.clips)

    def validate(self) -> None:
        """Validate arrangement integrity.
        
        Raises:
            ValueError: If validation fails
        """
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")
            
        # Check for duplicate clip names
        names = [clip.name for clip in self.clips]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate clip names found")