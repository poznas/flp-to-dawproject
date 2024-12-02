from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class Clip:
    """Represents an audio clip in an arrangement."""
    name: str
    position: float
    duration: float
    color: str
    source_path: Path
    volume: float = 1.0
    muted: bool = False
    arrangement_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate clip attributes after initialization."""
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
        
        # Sanitize name (remove spaces and special characters)
        object.__setattr__(self, 'name', self._sanitize_name(self.name))

    def _sanitize_name(self, name: str) -> str:
        """Sanitize the clip name by replacing spaces and special characters."""
        return name.replace(' ', '_').replace('-', '_')

    def __eq__(self, other):
        """Compare clips ignoring arrangement_name."""
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

    def __hash__(self):
        """Hash based on immutable attributes."""
        return hash((
            self.name,
            self.position,
            self.duration,
            self.color,
            str(self.source_path),
            self.volume,
            self.muted
        ))

    def full_equals(self, other):
        """Compare clips including arrangement_name."""
        return self == other and self.arrangement_name == other.arrangement_name

    def with_arrangement(self, name: str) -> 'Clip':
        """Return a new clip with the specified arrangement name."""
        return Clip(
            name=self.name,
            position=self.position,
            duration=self.duration,
            color=self.color,
            source_path=self.source_path,
            volume=self.volume,
            muted=self.muted,
            arrangement_name=name,
            metadata=self.metadata.copy()
        )

    def with_metadata(self, key: str, value: Any) -> 'Clip':
        """Return a new clip with added metadata."""
        new_metadata = self.metadata.copy()
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
            metadata=new_metadata
        )

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self.metadata.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert clip to dictionary representation."""
        return {
            'name': self.name,
            'position': self.position,
            'duration': self.duration,
            'color': self.color,
            'source_path': str(self.source_path),
            'volume': self.volume,
            'muted': self.muted,
            'arrangement_name': self.arrangement_name,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Clip':
        """Create clip from dictionary representation."""
        data = data.copy()
        data['source_path'] = Path(data['source_path'])
        return cls(**data)