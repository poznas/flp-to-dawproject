# src/models/clip.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class Clip:
    """Represents an audio clip with position, duration and color information."""
    
    name: str
    position: float  # Position in seconds
    duration: float  # Duration in seconds 
    color: str      # Color in hex format (#RRGGBB)
    source_path: Optional[Path] = None
    volume: float = 1.0
    muted: bool = False
    arrangement_name: Optional[str] = None
    _metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate clip attributes after initialization."""
        # Sanitize name (convert spaces to underscores)
        object.__setattr__(self, 'name', self.name.replace(' ', '_'))
        
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")

    def with_arrangement(self, arrangement_name: str) -> 'Clip':
        """Create new clip instance with specified arrangement name."""
        return Clip(
            name=self.name,
            position=self.position,
            duration=self.duration,
            color=self.color,
            source_path=self.source_path,
            volume=self.volume,
            muted=self.muted,
            arrangement_name=arrangement_name,
            _metadata=dict(self._metadata)
        )

    def with_metadata(self, key: str, value: Any) -> 'Clip':
        """Create new clip instance with added metadata."""
        new_metadata = dict(self._metadata)
        new_metadata[key] = value
        return Clip(
            name=self.name,
            position=self.position,
            duration=self.duration,
            color=self.color,
            source_path=self.source_path,
            volume=self.volume,
            muted=self.muted,
            arrangement_name=self.arrangement_name,
            _metadata=new_metadata
        )

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self._metadata.get(key, default)
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert clip to dictionary format for serialization."""
        return {
            'name': self.name,
            'position': self.position,
            'duration': self.duration,
            'color': self.color,
            'source_path': str(self.source_path) if self.source_path else None,
            'volume': self.volume,
            'muted': self.muted,
            'arrangement_name': self.arrangement_name,
            'metadata': dict(self._metadata)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Clip':
        """Create clip instance from dictionary data."""
        source_path = Path(data['source_path']) if data.get('source_path') else None
        
        clip = cls(
            name=data['name'],
            position=float(data['position']),
            duration=float(data['duration']), 
            color=data['color'],
            source_path=source_path,
            volume=float(data.get('volume', 1.0)),
            muted=bool(data.get('muted', False)),
            arrangement_name=data.get('arrangement_name'),
            _metadata={}  # Initialize empty metadata
        )
        
        # Add metadata after creation
        metadata = data.get('metadata', {})
        return cls(
            name=clip.name,
            position=clip.position,
            duration=clip.duration,
            color=clip.color,
            source_path=clip.source_path,
            volume=clip.volume,
            muted=clip.muted,
            arrangement_name=clip.arrangement_name,
            _metadata=metadata
        )
    
    def __eq__(self, other: object) -> bool:
        """Compare clips ignoring arrangement_name when comparing within arrangements."""
        if not isinstance(other, Clip):
            return NotImplemented
        return (
            self.name == other.name and
            self.position == other.position and
            self.duration == other.duration and
            self.color == other.color and
            str(self.source_path) == str(other.source_path) and
            self.volume == other.volume and
            self.muted == other.muted
        )

    def full_equals(self, other: object) -> bool:
        """Compare clips including arrangement_name."""
        return (
            self == other and
            isinstance(other, Clip) and
            self.arrangement_name == other.arrangement_name
        )