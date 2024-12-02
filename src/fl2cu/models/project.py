# fl2cu/models/project.py
from pathlib import Path
from typing import List, Optional, Dict, Any, Set

from fl2cu.models.base import BaseProject
from fl2cu.models.arrangement import Arrangement

class Project(BaseProject):
    """Project class extending base functionality."""
    def __init__(
        self,
        name: str,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        super().__init__(name, source_path, output_dir)
        
    def add_arrangement(self, arrangement: Arrangement) -> None:
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)
        
    def remove_arrangement(self, arrangement: Arrangement) -> None:
        """Remove an arrangement from the project."""
        if arrangement in self.arrangements:
            self.arrangements.remove(arrangement)
            
    def get_arrangement_by_name(self, name: str) -> Optional[Arrangement]:
        """Find an arrangement by its name."""
        for arrangement in self.arrangements:
            if arrangement.name == name:
                return arrangement
        return None
        
    def validate(self) -> None:
        """Validate project and all its arrangements."""
        if not self.name:
            raise ValueError("Project name cannot be empty")
            
        if self.source_path and not isinstance(self.source_path, Path):
            raise TypeError("source_path must be a Path object")
            
        if self.output_dir and not isinstance(self.output_dir, Path):
            raise TypeError("output_dir must be a Path object")
            
        # Check for arrangement name uniqueness
        names = [arr.name for arr in self.arrangements]
        duplicate_names = set(name for name in names if names.count(name) > 1)
        if duplicate_names:
            raise ValueError(f"Duplicate arrangement names found: {', '.join(duplicate_names)}")
            
        # Validate each arrangement
        for arrangement in self.arrangements:
            try:
                arrangement.validate()
            except ValueError as e:
                raise ValueError(f"Invalid arrangement '{arrangement.name}': {str(e)}")
            
    def get_all_clip_paths(self) -> Set[Path]:
        """Get set of all unique audio file paths used in project."""
        paths = set()
        for arrangement in self.arrangements:
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
        return {
            'name': self.name,
            'source_path': str(self.source_path) if self.source_path else None,
            'output_dir': str(self.output_dir) if self.output_dir else None,
            'arrangements': [arr.to_dict() for arr in self.arrangements]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project instance from dictionary data."""
        source_path = Path(data['source_path']) if data.get('source_path') else None
        output_dir = Path(data['output_dir']) if data.get('output_dir') else None
        
        project = cls(
            name=data['name'],
            source_path=source_path,
            output_dir=output_dir
        )
        
        # Add arrangements
        for arr_data in data.get('arrangements', []):
            arrangement = Arrangement.from_dict(arr_data)
            project.add_arrangement(arrangement)
            
        return project