from pathlib import Path
from typing import List, Optional, Dict, Any, Set, TYPE_CHECKING

from .base import BaseProject
from .timing import ProjectTiming

if TYPE_CHECKING:
    from .arrangement import Arrangement

class Project(BaseProject):
    """Project class extending base functionality."""
    def __init__(
        self,
        name: str,
        timing: Optional[ProjectTiming] = None,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        super().__init__(name=name, 
                        timing=timing,
                        source_path=source_path, 
                        output_dir=output_dir)
    
    def add_arrangement(self, arrangement: 'Arrangement') -> None:
        """Add an arrangement to the project."""
        from .arrangement import Arrangement
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)
        
    def remove_arrangement(self, arrangement: 'Arrangement') -> None:
        """Remove an arrangement from the project."""
        if arrangement in self._arrangements:
            self._arrangements.remove(arrangement)
            
    def get_arrangement_by_name(self, name: str) -> Optional['Arrangement']:
        """Find an arrangement by its name."""
        for arrangement in self._arrangements:
            if arrangement.name == name:
                return arrangement
        return None
        
    def validate(self) -> None:
        """Validate project and all its arrangements."""
        # Validate each arrangement
        for arrangement in self._arrangements:
            try:
                arrangement.validate()
            except ValueError as e:
                raise ValueError(f"Invalid arrangement '{arrangement.name}': {str(e)}")
            
    def get_all_clip_paths(self) -> Set[Path]:
        """Get set of all unique audio file paths used in project."""
        paths = set()
        for arrangement in self._arrangements:
            for clip in arrangement.get_tracks():
                if hasattr(clip, 'source_path') and clip.source_path:
                    paths.add(clip.source_path)
        return paths
        
    def validate_audio_files(self) -> bool:
        """Check if all referenced audio files exist."""
        missing_files = []
        for path in self.get_all_clip_paths():
            if not path.exists():
                missing_files.append(path)
                
        return len(missing_files) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format for serialization."""
        return {
            'name': self.name,
            'timing': self.timing.to_dict() if self.timing else None,
            'source_path': str(self.source_path) if self.source_path else None,
            'output_dir': str(self.output_dir) if self.output_dir else None,
            'arrangements': [arr.to_dict() for arr in self._arrangements]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project instance from dictionary data."""
        from .arrangement import Arrangement
        
        timing_data = data.get('timing', {})
        timing = ProjectTiming(
            tempo=float(timing_data.get('tempo', 120.0)),
            time_signature_numerator=int(timing_data.get('time_signature_numerator', 4)),
            time_signature_denominator=int(timing_data.get('time_signature_denominator', 4))
        )
        
        source_path = Path(data['source_path']) if data.get('source_path') else None
        output_dir = Path(data['output_dir']) if data.get('output_dir') else None
        
        project = cls(
            name=data['name'],
            timing=timing,
            source_path=source_path,
            output_dir=output_dir
        )
        
        # Add arrangements
        for arr_data in data.get('arrangements', []):
            arrangement = Arrangement.from_dict(arr_data)
            project.add_arrangement(arrangement)
            
        return project