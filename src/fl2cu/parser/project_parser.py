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
        
        # Parse FL Studio project
        try:
            self.fl_project = pyflp.parse(file_path)
            self.logger.debug(f"Project version: {self.fl_project.version}")
        except Exception as e:
            raise RuntimeError(f"Failed to parse FL Studio project: {e}")

        # Initialize specialized parsers
        self.timing_parser = FLTimingParser(self.fl_project)
        self.clip_parser = FLClipParser(self.fl_project, self.resolve_fl_studio_path)
        self.arrangement_parser = FLArrangementParser(self.fl_project, self.clip_parser)

    def resolve_fl_studio_path(self, path: str) -> Optional[Path]:
        """Resolve FL Studio environment variables in paths."""
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

    def parse_project(self) -> List[Project]:
        try:
            # Parse timing info
            timing = self.timing_parser.parse_timing()
            
            # Parse arrangements
            arrangements = self.arrangement_parser.parse_arrangements()
            
            # Create projects
            projects = []
            for arrangement in arrangements:
                # Create project with timing info
                project = Project(
                    name=f"{self.file_path.stem}_{arrangement.name}",
                    timing=timing,
                    source_path=self.file_path
                )
                
                # Set project reference on arrangement
                arrangement.project = project  
                
                # Add arrangement to project
                project.add_arrangement(arrangement)
                projects.append(project)
            
            return projects
                
        except Exception as e:
            self.logger.error(f"Failed to parse project: {e}")
            raise