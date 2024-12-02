# src/fl2cu/utils/file_manager.py

import shutil
from pathlib import Path
from typing import Dict, Union

from ..models.project import Project
from ..models.arrangement import Arrangement
from .logger import get_logger

class FileManager:
    """Manages file system operations for the project."""
    
    def __init__(self, output_dir: Union[str, Path]) -> None:
        self.base_dir = Path(output_dir)
        self.logger = get_logger()

    def _sanitize_path(self, name: str) -> str:
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        sanitized = ''.join('_' if c in invalid_chars else c for c in name)
        return sanitized.strip()

    def create_directory_structure(self, project: Project) -> Dict[Arrangement, Path]:
        arrangement_dirs = {}
        
        try:
            # Create base project directory
            project_dir = self.base_dir / self._sanitize_path(project.name)
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Create directories for each arrangement
            for arrangement in project.arrangements:
                arr_dir = project_dir / self._sanitize_path(arrangement.name)
                arr_dir.mkdir(exist_ok=True)
                
                # Create audio files directory
                audio_dir = arr_dir / "audio_files"
                audio_dir.mkdir(exist_ok=True)
                
                arrangement_dirs[arrangement] = arr_dir
                
            self.logger.info(f"Created directory structure in {self.base_dir}")
            return arrangement_dirs
            
        except Exception as e:
            self.logger.error(f"Failed to create directory structure: {e}")
            raise OSError(f"Failed to create directory structure: {e}")

    def cleanup_temp_files(self, temp_dir: Union[str, Path]) -> None:
        try:
            shutil.rmtree(temp_dir)
            self.logger.info(f"Cleaned up temporary files in {temp_dir}")
        except Exception as e:
            self.logger.warning(f"Failed to clean up temporary files: {e}")

    def validate_paths(self) -> bool:
        try:
            self.base_dir.mkdir(parents=True, exist_ok=True)
            return self.base_dir.exists() and self.base_dir.is_dir()
        except Exception as e:
            self.logger.error(f"Path validation failed: {e}")
            return False