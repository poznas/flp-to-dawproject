from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class Clip:
    """Represents an audio clip in an arrangement."""
    
    # Required core attributes that need to come first (no defaults)
    name: str                     # Unique name for the clip
    position: float               # Position in beats  
    duration: float               # Duration in beats
    source_path: Path            # Path to source audio file'
    track_name: str              # Name of containing track
    format: str
    # Optional attributes with defaults must come after required ones
    start_offset: float = 0.0    # Start offset in source audio
    end_offset: float = 0.0      # End offset in source audio
    track_id: Optional[str] = None  # XML ID reference for track
    color: str = "#a2eabf"      # Default color matching sample
    volume: float = 1.0         # Normalized volume (0-1)
    muted: bool = False         # Mute state
    arrangement_name: Optional[str] = None  # Parent arrangement name
    metadata: Dict[str, Any] = field(default_factory=dict, hash=False)  # Additional metadata

    def __post_init__(self):
        """Validate and normalize clip attributes."""
        if not self.name:
            raise ValueError("Clip name cannot be empty")
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.track_name:
            raise ValueError("Track name cannot be empty")
            
        # Since the class is frozen, we can't modify attributes directly
        # All validation that would modify values needs to be done before creating the instance
        if not isinstance(self.source_path, Path):
            object.__setattr__(self, 'source_path', Path(self.source_path))

    def __hash__(self):
        # Use the most unique attributes to generate hash
        return hash((self.name, self.position, self.track_name, str(self.source_path)))
    
    @property 
    def output_filename(self) -> str:
        """Get the filename to use in the DAWproject."""
        return f"{self.name}.{self.format}"