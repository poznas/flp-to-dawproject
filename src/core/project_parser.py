from pathlib import Path
from typing import List, Dict, Any, Optional
import pyflp

from ..models.project import Project
from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..utils.logger import get_logger

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
            # Get playlist tracks
            playlist_tracks = self.fl_project.tracks if hasattr(self.fl_project, 'tracks') else []
            
            # Create default arrangement
            default_arrangement = Arrangement(name="Main")
            arrangements.append(default_arrangement)

            # Process each channel
            for channel in self.fl_project.channels.samplers:
                if not channel.sample_path:
                    continue

                # Get patterns containing this channel
                patterns = []
                if hasattr(channel, 'patterns'):
                    patterns = channel.patterns
                elif hasattr(channel, 'pattern'):
                    patterns = [channel.pattern] if channel.pattern else []

                # Calculate position based on pattern placement
                for pattern_idx in patterns:
                    # Try to find pattern in playlist
                    position = 0.0
                    for track in playlist_tracks:
                        for item in track.items:
                            if item.pattern == pattern_idx:
                                position = self._ticks_to_seconds(item.position)
                                break

                    # Create clip
                    clip = Clip(
                        name=channel.name or Path(channel.sample_path).stem,
                        position=position,
                        duration=self._ticks_to_seconds(channel.length if hasattr(channel, 'length') else 0),
                        color=f"#{channel.color:06x}" if hasattr(channel, 'color') and channel.color else "#808080",
                        source_path=Path(channel.sample_path),
                        volume=channel.volume if hasattr(channel, 'volume') else 1.0,
                        muted=channel.muted if hasattr(channel, 'muted') else False
                    )

                    # Add to appropriate arrangement
                    if hasattr(channel, 'group') and channel.group:
                        arrangement = self._get_or_create_arrangement(arrangements, str(channel.group))
                    else:
                        arrangement = default_arrangement
                    arrangement.add_clip(clip)

            return arrangements

        except Exception as e:
            self.logger.error(f"Error extracting arrangements: {e}")
            raise

    def _ticks_to_seconds(self, ticks: int) -> float:
        """Convert FL Studio ticks to seconds."""
        if not hasattr(self.fl_project, 'ppq') or not hasattr(self.fl_project, 'tempo'):
            return 0.0
            
        ticks_per_second = self.fl_project.ppq * (self.fl_project.tempo / 60.0)
        return ticks / ticks_per_second if ticks_per_second > 0 else 0.0

    def _get_or_create_arrangement(self, arrangements: List[Arrangement], name: str) -> Arrangement:
        """Get existing arrangement or create new one."""
        for arrangement in arrangements:
            if arrangement.name == name:
                return arrangement
                
        new_arrangement = Arrangement(name=name)
        arrangements.append(new_arrangement)
        return new_arrangement

    def _get_arrangement_name(self, channel: Any) -> str:
        """Determine arrangement name from channel properties."""
        if hasattr(channel, 'group') and channel.group:
            return str(channel.group)
            
        if hasattr(channel, 'pattern') and channel.pattern:
            return f"Pattern_{channel.pattern}"
            
        return "Main"