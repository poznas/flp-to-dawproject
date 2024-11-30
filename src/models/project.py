from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import logging

from .arrangement import Arrangement
from ..utils.logger import get_logger

@dataclass
class Project:
    """Represents an FL Studio project with multiple arrangements."""
    
    name: str
    arrangements: List[Arrangement] = field(default_factory=list)
    source_path: Optional[Path] = None
    output_dir: Optional[Path] = None
    
    def __post_init__(self):
        """Setup after initialization."""
        self.logger = get_logger()
        
    def add_arrangement(self, arrangement: Arrangement) -> None:
        """Add an arrangement to the project."""
        if self.get_arrangement_by_name(arrangement.name):
            raise ValueError(f"Arrangement with name '{arrangement.name}' already exists")
        self.arrangements.append(arrangement)
        
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
            
        # Check for arrangement name uniqueness
        names = [arr.name for arr in self.arrangements]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate arrangement names are not allowed")
            
        # Validate each arrangement
        for arrangement in self.arrangements:
            arrangement.validate()
            
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
        missing = []
        for path in self.get_all_clip_paths():
            if not path.exists():
                missing.append(path)
                self.logger.warning(f"Audio file not found: {path}")
        return len(missing) == 0
        
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