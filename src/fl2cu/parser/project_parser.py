from pathlib import Path
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
        self.fl_project = pyflp.parse(file_path)
        
        # Initialize specialized parsers
        self.timing_parser = FLTimingParser(self.fl_project)
        self.clip_parser = FLClipParser(self.fl_project)
        self.arrangement_parser = FLArrangementParser(self.fl_project, self.clip_parser)

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
            return project
            
        except Exception as e:
            self.logger.error(f"Failed to parse project: {e}")
            raise