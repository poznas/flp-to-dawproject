import pyflp
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from ..models.project import Project
from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..utils.logger import get_logger
from ..config import Config

class FLProjectParser:
    """Handles parsing of FL Studio project files using PyFLP library."""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.logger = get_logger()
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project file not found: {project_path}")
            
        try:
            self.fl_project = pyflp.parse(str(self.project_path))
            self.logger.info(f"Successfully opened FL Studio project: {self.project_path.name}")
        except Exception as e:
            self.logger.error(f"Failed to parse FL Studio project: {e}")
            raise
            
    def parse_project(self) -> Project:
        """Parse FL Studio project and extract metadata."""
        project = Project(
            name=self.project_path.stem,
            source_path=self.project_path
        )
        
        try:
            # Parse arrangements
            arrangements = self.extract_arrangements()
            for arrangement in arrangements:
                project.add_arrangement(arrangement)
                
            self.logger.info(f"Parsed {len(arrangements)} arrangements")
            return project
            
        except Exception as e:
            self.logger.error(f"Error parsing project: {e}")
            raise
            
    def extract_arrangements(self) -> List[Arrangement]:
        """Extract arrangement information from FL Studio project."""
        arrangements = []
        
        try:
            # Extract clips from patterns and arrangements
            for channel in self.fl_project.channels.samplers:
                # Skip empty or disabled channels
                if not channel.sample_path:
                    continue
                    
                # Get clip properties
                clip = Clip(
                    name=channel.name or Path(channel.sample_path).stem,
                    position=channel.start_offset / self.fl_project.tempo,  # Convert to seconds
                    duration=channel.length / self.fl_project.tempo,  # Convert to seconds
                    color=f"#{channel.color:06x}" if channel.color else "#808080",
                    source_path=Path(channel.sample_path),
                    volume=channel.volume
                )
                
                # Determine arrangement based on channel group or pattern
                arrangement_name = self._get_arrangement_name(channel)
                arrangement = self._get_or_create_arrangement(arrangements, arrangement_name)
                arrangement.add_clip(clip)
                
            return arrangements
            
        except Exception as e:
            self.logger.error(f"Error extracting arrangements: {e}")
            raise
            
    def _get_arrangement_name(self, channel: Any) -> str:
        """Determine arrangement name from channel properties."""
        # Try to get group name first
        if hasattr(channel, 'group') and channel.group:
            return str(channel.group)
            
        # Fall back to pattern name if available
        if hasattr(channel, 'pattern') and channel.pattern:
            return f"Pattern_{channel.pattern}"
            
        # Default arrangement name
        return "Main"
        
    def _get_or_create_arrangement(self, arrangements: List[Arrangement], name: str) -> Arrangement:
        """Get existing arrangement or create new one."""
        for arrangement in arrangements:
            if arrangement.name == name:
                return arrangement
                
        new_arrangement = Arrangement(name=name)
        arrangements.append(new_arrangement)
        return new_arrangement