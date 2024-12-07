from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from pathlib import Path

from .track import Track

if TYPE_CHECKING:
    from .project import Project

class Arrangement:
    """Represents an arrangement containing tracks and clips."""
    
    def __init__(self, name: str):
        self.name = name
        self._tracks: List[Track] = []
        self.project: Optional['Project'] = None  # Use string type annotation
        
    def add_track(self, track: Track) -> None:
        """Add a track to the arrangement."""
        self._tracks.append(track)
        
    def get_tracks(self) -> List[Track]:
        """Get list of tracks."""
        return self._tracks.copy()
        
    def has_tracks(self) -> bool:
        """Check if arrangement has any tracks with clips."""
        return any(track.clips for track in self._tracks)