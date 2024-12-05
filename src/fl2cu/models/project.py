# src/fl2cu/models/project.py
from pathlib import Path
from typing import List, Optional, Dict, Any, Set

from fl2cu.models.base import BaseProject
from fl2cu.models.arrangement import Arrangement
from fl2cu.models.timing import ProjectTiming

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
    
    def add_arrangement(self, arrangement: Arrangement) -> None:
        """Add an arrangement to the project."""
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)
        
    def remove_arrangement(self, arrangement: Arrangement) -> None:
        """Remove an arrangement from the project."""
        if arrangement in self._arrangements:
            self._arrangements.remove(arrangement)
            
    def get_arrangement_by_name(self, name: str) -> Optional[Arrangement]:
        """Find an arrangement by its name."""
        for arrangement in self._arrangements:
            if arrangement.name == name:
                return arrangement
        return None
        
    def validate(self) -> None:
        """Validate project and all its arrangements."""
        super().validate()  # Call parent validation first
            
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
            for clip in arrangement.clips:
                if clip.source_path:
                    paths.add(clip.source_path)
        return paths
        
    def validate_audio_files(self) -> bool:
        """Check if all referenced audio files exist."""
        missing_files = []
        for path in self.get_all_clip_paths():
            if not path.exists():
                missing_files.append(path)
                self.logger.warning(f"Audio file not found: {path}")
                
        if missing_files:
            self.logger.error(f"Missing {len(missing_files)} audio files")
            return False
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format for serialization."""
        base_dict = super().to_dict()
        base_dict.update({
            'arrangements': [arr.to_dict() for arr in self._arrangements]
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project instance from dictionary data."""
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