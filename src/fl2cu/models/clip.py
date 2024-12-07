from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class Clip:
    """Represents an audio clip in an arrangement."""
    
    # Required core attributes
    name: str                     # Unique name for the clip
    position: float               # Position in beats
    duration: float               # Duration in beats
    source_path: Path            # Path to source audio file
    
    # Start and end offsets in the source audio file (in beats)
    start_offset: float = 0.0    # Start offset in source audio
    end_offset: float = 0.0      # End offset in source audio
    
    # Track and routing
    track_name: str              # Name of containing track
    track_id: Optional[str] = None  # XML ID reference for track
    
    # Optional attributes with defaults
    color: str = "#a2eabf"      # Default color matching sample
    volume: float = 1.0         # Normalized volume (0-1)
    muted: bool = False         # Mute state
    
    # Organization
    arrangement_name: Optional[str] = None  # Parent arrangement name
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional metadata

    def __post_init__(self):
        """Validate and normalize clip attributes."""
        # Validate required fields
        if not self.name:
            raise ValueError("Clip name cannot be empty")
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.track_name:
            raise ValueError("Track name cannot be empty")
            
        # Validate offsets
        if self.start_offset < 0:
            raise ValueError("Start offset cannot be negative")
        if self.end_offset < self.start_offset:
            raise ValueError("End offset cannot be less than start offset")
            
        # Normalize paths
        if isinstance(self.source_path, str):
            self.source_path = Path(self.source_path)
        
        # Normalize names
        self.name = self._sanitize_name(self.name)
        self.track_name = self._sanitize_name(self.track_name)
        
        # Validate color format
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
            
        # Normalize volume
        self.volume = max(0.0, min(1.0, float(self.volume)))  # Clamp to 0-1

    @property
    def offsets(self) -> Tuple[float, float]:
        """Get clip offsets in beats."""
        return (self.start_offset, self.end_offset)

    @offsets.setter 
    def offsets(self, value: Tuple[float, float]) -> None:
        """Set clip offsets in beats."""
        start, end = value
        if start < 0:
            raise ValueError("Start offset cannot be negative")
        if end < start:
            raise ValueError("End offset cannot be less than start offset")
        self.start_offset = start
        self.end_offset = end