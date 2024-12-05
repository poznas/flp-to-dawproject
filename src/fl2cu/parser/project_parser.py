from pathlib import Path
from typing import List, Optional, Dict, Union
import os
import logging
import pyflp

from .timing_parser import FLTimingParser
from .clip_parser import FLClipParser
from .arrangement_parser import FLArrangementParser
from ..models.project import Project

class FLProjectParser:
    """Main FL Studio project parser coordinating specialized parsers."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Project file not found: {file_path}")
            
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Loading FL Studio project: {file_path}")
        
        self.fl_project = pyflp.parse(file_path)
        self.logger.debug(f"Project version: {self.fl_project.version}")
        
        # Initialize specialized parsers
        self.timing_parser = FLTimingParser(self.fl_project)
        self.clip_parser = FLClipParser(self.fl_project, self.resolve_fl_studio_path)
        self.arrangement_parser = FLArrangementParser(self.fl_project, self.clip_parser)

    def resolve_fl_studio_path(self, path: Union[str, Path]) -> Optional[Path]:
        """Resolve FL Studio environment variables in paths."""
        if isinstance(path, Path):
            path = str(path)
            
        fl_variables = {
            "FLStudioUserData": "C:\\Users\\poznas\\Documents\\Image-Line\\Data\\FL Studio",
            "FLStudioInstallDir": os.getenv("PROGRAMFILES", "") + "\\Image-Line\\FL Studio 21",
        }
        
        try:
            for var_name, var_value in fl_variables.items():
                var_pattern = f"%{var_name}%"
                if var_pattern in path:
                    path = path.replace(var_pattern, var_value)
            resolved_path = Path(path)
            return resolved_path if resolved_path.exists() else None
        except Exception as e:
            self.logger.error(f"Failed to resolve path {path}: {e}")
            return None

    def parse_project(self) -> Project:
        """Parse FL Studio project using specialized parsers."""
        try:
            # Parse timing info
            timing = self.timing_parser.parse_timing()
            
            # Create project
            project = Project(
                name=self.file_path.stem,
                timing=timing,
                source_path=self.file_path
            )
            
            # Parse arrangements
            arrangements = self.arrangement_parser.parse_arrangements()
            for arrangement in arrangements:
                project.add_arrangement(arrangement)
            
            self.logger.info(f"Parsed project with {len(arrangements)} arrangements")
            for arr in arrangements:
                self.logger.debug(f"Arrangement '{arr.name}' has {len(arr.clips)} clips")
                
            return project
            
        except Exception as e:
            self.logger.error(f"Failed to parse project: {e}")
            raise