from dataclasses import dataclass
from typing import List

from .clip import Clip


class Track:
    """Represents a track containing clips."""
    
    def __init__(self, name: str, id: str, clips: List[Clip]):
        self.name = name
        self.id = id
        self.clips = clips