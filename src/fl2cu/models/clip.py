from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any

@dataclass
class Clip:
    """Represents an audio clip in an arrangement.
    
    Maps between FL Studio playlist items/channels and DAWproject clip elements.
    """
    # Required core attributes
    name: str                     # Unique name for the clip
    position: float               # Position in beats
    duration: float               # Duration in beats
    source_path: Path            # Path to source audio file
    
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

    def _sanitize_name(self, name: str) -> str:
        """Sanitize a name for use in DAWproject XML."""
        # Replace spaces and special characters
        sanitized = name.replace(' ', '_')\
                       .replace('-', '_')\
                       .replace('.', '_')\
                       .replace('(', '')\
                       .replace(')', '')\
                       .replace('[', '')\
                       .replace(']', '')\
                       .replace('/', '_')\
                       .replace('\\', '_')
        
        # Remove any double underscores
        while '__' in sanitized:
            sanitized = sanitized.replace('__', '_')
            
        # Remove any leading/trailing underscores
        return sanitized.strip('_')

    def __eq__(self, other: object) -> bool:
        """Compare clips based on core attributes including track assignment."""
        if not isinstance(other, Clip):
            return NotImplemented
        return (
            self.name == other.name and
            self.position == other.position and
            self.duration == other.duration and
            self.track_name == other.track_name and
            str(self.source_path) == str(other.source_path) and
            self.volume == other.volume and
            self.muted == other.muted
        )

    def __hash__(self) -> int:
        """Hash based on immutable attributes including track."""
        return hash((
            self.name,
            self.position,
            self.duration,
            self.track_name,
            str(self.source_path),
            self.volume,
            self.muted
        ))

    def clone(self, **updates) -> 'Clip':
        """Create a new clip with updated attributes."""
        data = self.__dict__.copy()
        data.update(updates)
        return Clip(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert clip to dictionary representation."""
        return {
            'name': self.name,
            'position': self.position,
            'duration': self.duration,
            'color': self.color,
            'source_path': str(self.source_path),
            'track_name': self.track_name,
            'track_id': self.track_id,
            'volume': self.volume,
            'muted': self.muted,
            'arrangement_name': self.arrangement_name,
            'metadata': self.metadata.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Clip':
        """Create clip from dictionary representation."""
        data = data.copy()
        data['source_path'] = Path(data['source_path'])
        return cls(**data)

    def validate(self) -> List[str]:
        """Validate clip data and return list of any issues found."""
        issues = []
        
        if not self.name:
            issues.append("Missing clip name")
        if self.position < 0:
            issues.append("Negative position")
        if self.duration <= 0:
            issues.append("Invalid duration")
        if not self.track_name:
            issues.append("Missing track assignment")
        if not self.source_path.exists():
            issues.append(f"Audio file not found: {self.source_path}")
        if not 0 <= self.volume <= 1:
            issues.append(f"Volume {self.volume} out of range [0,1]")
            
        return issues

    def get_end_position(self) -> float:
        """Get the end position of this clip in beats."""
        return self.position + self.duration

    def overlaps(self, other: 'Clip') -> bool:
        """Check if this clip overlaps with another clip on the same track."""
        if self.track_name != other.track_name:
            return False
            
        return (
            self.position < other.get_end_position() and
            other.position < self.get_end_position()
        )