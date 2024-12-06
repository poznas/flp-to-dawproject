# src/fl2cu/models/arrangement.py

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

from .track import Track

from .clip import Clip

class Arrangement:
    """Represents an arrangement containing tracks and clips."""
    
    def __init__(self, name: str):
        self.name = name
        self._tracks: List[Track] = []
        
    def add_track(self, track: Track) -> None:
        """Add a track to the arrangement."""
        self._tracks.append(track)
        
    def get_tracks(self) -> List[Track]:
        """Get list of tracks."""
        return self._tracks.copy()
        
    def has_tracks(self) -> bool:
        """Check if arrangement has any tracks with clips."""
        return any(track.clips for track in self._tracks)