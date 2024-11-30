from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

@dataclass
class Clip:
    """Represents an audio clip with position, duration and color information."""
    
    # Required fields
    name: str
    position: float  # Position in seconds
    duration: float  # Duration in seconds 
    color: str      # Color in hex format (#RRGGBB)
    
    # Optional fields with defaults
    source_path: Optional[Path] = None
    volume: float = 1.0
    muted: bool = False
    arrangement_name: Optional[str] = None
    
    # Internal state
    _metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate clip attributes."""
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")
            
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
            'metadata': self._metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Clip':
        """Create clip instance from dictionary data."""
        source_path = Path(data['source_path']) if data.get('source_path') else None
        metadata = data.get('metadata', {})
        
        clip = cls(
            name=data['name'],
            position=float(data['position']),
            duration=float(data['duration']), 
            color=data['color'],
            source_path=source_path,
            volume=float(data.get('volume', 1.0)),
            muted=bool(data.get('muted', False)),
            arrangement_name=data.get('arrangement_name')
        )
        clip._metadata = metadata
        return clip
        
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self._metadata.get(key, default)
        
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value for key."""
        self._metadata[key] = value