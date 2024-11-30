from pathlib import Path
from typing import List, Dict, Optional, TYPE_CHECKING
import shutil

if TYPE_CHECKING:
    from ..models.project import Project
    from ..models.arrangement import Arrangement

class FileManager:
    """Handles file system operations and directory structure."""
    
    def __init__(self, base_dir: str):
        """Initialize file manager with base directory.
        
        Args:
            base_dir: Base directory for file operations
        """
        self.base_dir = Path(base_dir)
        # Import logger here to avoid circular import
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
    def create_directory_structure(self, project: "Project") -> Dict["Arrangement", Path]:
        """Create output directory structure for project and arrangements.
        
        Args:
            project: Project instance containing arrangements
            
        Returns:
            Dictionary mapping arrangements to their output directories
            
        Raises:
            OSError: If directory creation fails
        """
        # Create base output directory
        project_dir = self.base_dir / self._sanitize_path(project.name)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create arrangement directories
        arrangement_dirs = {}
        for arrangement in project.arrangements:
            arr_dir = project_dir / self._sanitize_path(arrangement.name)
            audio_dir = arr_dir / "audio_files"
            
            try:
                audio_dir.mkdir(parents=True, exist_ok=True)
                arrangement_dirs[arrangement] = arr_dir
                arrangement.folder_path = arr_dir
            except Exception as e:
                self.logger.error(f"Failed to create directory for arrangement {arrangement.name}: {e}")
                raise
                
        return arrangement_dirs
        
    def cleanup_temp_files(self, directory: Optional[Path] = None) -> None:
        """Clean up temporary files and directories.
        
        Args:
            directory: Optional specific directory to clean, defaults to temp dir
        """
        if not directory:
            from ..config import Config
            directory = Config.TEMP_DIR
            
        if not directory.exists():
            return
            
        try:
            shutil.rmtree(directory)
            self.logger.debug(f"Cleaned up temporary directory: {directory}")
        except Exception as e:
            self.logger.warning(f"Failed to clean up temporary directory {directory}: {e}")
            
    def validate_paths(self) -> bool:
        """Validate all required paths exist and are accessible.
        
        Returns:
            True if all paths are valid and accessible, False otherwise
        """
        try:
            # Check base directory
            if not self.base_dir.exists():
                self.base_dir.mkdir(parents=True)
                
            # Verify write permissions
            test_file = self.base_dir / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except Exception as e:
                self.logger.error(f"No write permission in base directory: {e}")
                return False
                
            # Check temp directory
            from ..config import Config
            temp_dir = Config.TEMP_DIR
            if not temp_dir.exists():
                temp_dir.mkdir(parents=True)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Path validation failed: {e}")
            return False
            
    def _sanitize_path(self, name: str) -> str:
        """Sanitize a string for use in file paths.
        
        Args:
            name: Original path string
            
        Returns:
            Sanitized path string
        """
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
            
        # Remove leading/trailing spaces and dots
        name = name.strip('. ')
        
        # Ensure name is not empty
        if not name:
            name = "unnamed"
            
        return name
        
    def copy_audio_file(self, source: Path, dest: Path) -> bool:
        """Copy audio file with error handling.
        
        Args:
            source: Source audio file path
            dest: Destination path
            
        Returns:
            True if copy succeeded, False otherwise
        """
        try:
            shutil.copy2(source, dest)
            return True
        except Exception as e:
            self.logger.error(f"Failed to copy audio file from {source} to {dest}: {e}")
            return False
            
    def ensure_unique_path(self, path: Path) -> Path:
        """Ensure path is unique by adding number suffix if needed.
        
        Args:
            path: Original path
            
        Returns:
            Unique path with number suffix if needed
        """
        if not path.exists():
            return path
            
        base = path.parent / path.stem
        ext = path.suffix
        counter = 1
        
        while True:
            new_path = Path(f"{base}_{counter}{ext}")
            if not new_path.exists():
                return new_path
            counter += 1