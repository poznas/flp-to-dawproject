# src/fl2cu/models/base.py
from .arrangement import Arrangement
from pathlib import Path
from typing import List, Optional, Dict, Any
from .timing import ProjectTiming

class BaseProject:
    """Base class containing core Project functionality."""
    def __init__(
        self,
        name: str,
        timing: Optional[ProjectTiming] = None,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        self.name = name
        self.timing = timing or ProjectTiming.default()
        self.source_path = Path(source_path) if source_path else None
        self.output_dir = Path(output_dir) if output_dir else None
        self._arrangements: List['Arrangement'] = []

    @property
    def arrangements(self) -> List['Arrangement']:
        """Get list of project arrangements."""
        return self._arrangements.copy()

    def add_arrangement(self, arrangement: 'Arrangement') -> None:
        """Add an arrangement to the project.
        
        Args:
            arrangement: Arrangement to add
            
        Raises:
            ValueError: If arrangement with same name already exists
        """
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)

    def remove_arrangement(self, arrangement: 'Arrangement') -> None:
        """Remove an arrangement from the project.
        
        Args:
            arrangement: Arrangement to remove
        """
        if arrangement in self._arrangements:
            self._arrangements.remove(arrangement)

    def validate(self) -> None:
        """Validate project integrity.
        
        Raises:
            ValueError: If validation fails
        """
        if not self.name:
            raise ValueError("Project name cannot be empty")
            
        if self.source_path and not isinstance(self.source_path, Path):
            raise TypeError("source_path must be a Path object")
            
        if self.output_dir and not isinstance(self.output_dir, Path):
            raise TypeError("output_dir must be a Path object")

        # Validate timing
        if not isinstance(self.timing, ProjectTiming):
            raise TypeError("timing must be a ProjectTiming object")
        if self.timing.tempo <= 0:
            raise ValueError("Project tempo must be positive")
            
        # Check for arrangement name uniqueness
        names = [arr.name for arr in self._arrangements]
        duplicate_names = set(name for name in names if names.count(name) > 1)
        if duplicate_names:
            raise ValueError(f"Duplicate arrangement names found: {', '.join(duplicate_names)}")

    def get_all_clip_paths(self) -> set[Path]:
        """Get set of all unique audio file paths used in project."""
        paths = set()
        for arrangement in self._arrangements:
            for clip in arrangement.clips:
                if clip.source_path:
                    paths.add(clip.source_path)
        return paths

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format."""
        return {
            'name': self.name,
            'timing': self.timing.to_dict(),
            'source_path': str(self.source_path) if self.source_path else None,
            'output_dir': str(self.output_dir) if self.output_dir else None,
            'arrangements': [arr.to_dict() for arr in self._arrangements]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseProject':
        """Create project instance from dictionary data."""
        timing_data = data.get('timing', {})
        timing = ProjectTiming(
            tempo=float(timing_data.get('tempo', {}).get('value', 120.0)),
            time_signature_numerator=int(timing_data.get('time_signature', {}).get('numerator', 4)),
            time_signature_denominator=int(timing_data.get('time_signature', {}).get('denominator', 4))
        )
        
        source_path = Path(data['source_path']) if data.get('source_path') else None
        output_dir = Path(data['output_dir']) if data.get('output_dir') else None
        
        return cls(
            name=data['name'],
            timing=timing,
            source_path=source_path,
            output_dir=output_dir
        )