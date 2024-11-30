from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from .arrangement import Arrangement

class Project:
    """Represents an FL Studio project with multiple arrangements."""
    
    def __init__(self, name: str, arrangements: List[Arrangement] = None, 
                 source_path: Optional[Path] = None, output_dir: Optional[Path] = None):
        """Initialize project instance.
        
        Args:
            name: Project name
            arrangements: Optional list of arrangements
            source_path: Optional path to source FL Studio project file
            output_dir: Optional output directory path
        """
        # Import logger here to avoid circular import
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
        self.name = name
        self.arrangements = arrangements or []
        self.source_path = source_path
        self.output_dir = output_dir
        
    def add_arrangement(self, arrangement: Arrangement) -> None:
        """Add an arrangement to the project.
        
        Args:
            arrangement: Arrangement instance to add
            
        Raises:
            ValueError: If arrangement with same name already exists
        """
        if self.get_arrangement_by_name(arrangement.name):
            raise ValueError(f"Arrangement with name '{arrangement.name}' already exists")
        self.arrangements.append(arrangement)
        
    def remove_arrangement(self, arrangement: Arrangement) -> None:
        """Remove an arrangement from the project.
        
        Args:
            arrangement: Arrangement instance to remove
        """
        if arrangement in self.arrangements:
            self.arrangements.remove(arrangement)
            
    def get_arrangement_by_name(self, name: str) -> Optional[Arrangement]:
        """Find an arrangement by its name.
        
        Args:
            name: Name of arrangement to find
            
        Returns:
            Matching Arrangement instance or None if not found
        """
        for arrangement in self.arrangements:
            if arrangement.name == name:
                return arrangement
        return None
        
    def validate(self) -> None:
        """Validate project and all its arrangements.
        
        Raises:
            ValueError: If validation fails
        """
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
        """Get set of all unique audio file paths used in project.
        
        Returns:
            Set of paths to all audio files referenced in project
        """
        paths = set()
        for arrangement in self.arrangements:
            for clip in arrangement.clips:
                if clip.source_path:
                    paths.add(clip.source_path)
        return paths
        
    def validate_audio_files(self) -> bool:
        """Check if all referenced audio files exist.
        
        Returns:
            True if all audio files exist, False otherwise
        """
        missing = []
        for path in self.get_all_clip_paths():
            if not path.exists():
                missing.append(path)
                self.logger.warning(f"Audio file not found: {path}")
        return len(missing) == 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format for serialization.
        
        Returns:
            Dictionary representation of project
        """
        return {
            'name': self.name,
            'source_path': str(self.source_path) if self.source_path else None,
            'output_dir': str(self.output_dir) if self.output_dir else None,
            'arrangements': [arr.to_dict() for arr in self.arrangements]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project instance from dictionary data.
        
        Args:
            data: Dictionary containing project data
            
        Returns:
            New Project instance
        """
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