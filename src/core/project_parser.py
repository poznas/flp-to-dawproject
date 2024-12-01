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
        try:
            # Create project with minimal validation
            project = Project(
                name=self.project_path.stem,
                source_path=self.project_path
            )
            
            # Extract channel info first
            channels = []
            for channel in self.fl_project.channels:
                if hasattr(channel, 'sample_path') and channel.sample_path:
                    channels.append(channel)

            # Create arrangements based on channel groups
            arrangements = {}
            default_arr = Arrangement(name="Main")
            arrangements["Main"] = default_arr

            for channel in channels:
                # Determine arrangement
                arr_name = "Main"
                if hasattr(channel, 'group') and channel.group:
                    arr_name = str(channel.group)
                
                # Get or create arrangement
                if arr_name not in arrangements:
                    arrangements[arr_name] = Arrangement(name=arr_name)
                    
                arr = arrangements[arr_name]
                
                # Create clip
                clip = Clip(
                    name=channel.name or Path(channel.sample_path).stem,
                    position=self._get_channel_position(channel),
                    duration=self._get_channel_duration(channel),
                    color=self._get_channel_color(channel),
                    source_path=Path(channel.sample_path),
                    volume=getattr(channel, 'volume', 1.0),
                    muted=getattr(channel, 'muted', False)
                )
                
                arr.add_clip(clip)

            # Add arrangements to project
            for arr in arrangements.values():
                project.add_arrangement(arr)
                
            self.logger.info(f"Successfully parsed project with {len(project.arrangements)} arrangements")
            return project
            
        except Exception as e:
            self.logger.error(f"Failed to parse project: {e}")
            raise
            
    def extract_arrangements(self) -> List[Arrangement]:
        """Extract arrangement information from FL Studio project."""
        try:
            # Start with default arrangement 
            default_arr = Arrangement(name="Main")
            arrangements = [default_arr]
            
            # Get channels
            for channel in self.fl_project.channels:
                if not hasattr(channel, 'sample_path') or not channel.sample_path:
                    continue
                    
                # Get channel properties
                name = channel.name or Path(channel.sample_path).stem
                color = f"#{channel.color:06x}" if hasattr(channel, 'color') and channel.color else "#808080"
                volume = getattr(channel, 'volume', 1.0)
                muted = getattr(channel, 'muted', False)
                
                # Get pattern info for position
                pattern_pos = 0.0  # Default to start
                patterns = self.fl_project.arrangements[0].patterns if self.fl_project.arrangements else []
                for pattern in patterns:
                    if pattern.channel == channel:
                        pattern_pos = self._ticks_to_seconds(pattern.position)
                        break
                        
                # Create clip
                clip = Clip(
                    name=name,
                    position=pattern_pos,
                    duration=self._ticks_to_seconds(getattr(channel, 'length', 4 * self.fl_project.ppq)),
                    color=color,
                    source_path=Path(channel.sample_path),
                    volume=volume,
                    muted=muted
                )
                
                # Add to appropriate arrangement
                target_arr = default_arr
                if hasattr(channel, 'group') and channel.group:
                    arr_name = str(channel.group)
                    target_arr = next((arr for arr in arrangements if arr.name == arr_name), None)
                    if not target_arr:
                        target_arr = Arrangement(name=arr_name)
                        arrangements.append(target_arr)
                        
                target_arr.add_clip(clip)
                
        except Exception as e:
            self.logger.error(f"Error extracting arrangements: {e}")
            raise
            
        return arrangements

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
    
    def _get_channel_position(self, channel) -> float:
        """Get channel position in seconds."""
        position = 0.0
        try:
            if hasattr(channel, 'pattern_position'):
                position = channel.pattern_position
            elif hasattr(channel, 'patterns') and channel.patterns:
                position = min(p.position for p in channel.patterns if hasattr(p, 'position'))
        except Exception:
            pass
        return self._ticks_to_seconds(position)

    def _get_channel_duration(self, channel) -> float:
        """Get channel duration in seconds."""
        duration = self.fl_project.ppq * 4  # Default to 1 bar
        try:
            if hasattr(channel, 'length'):
                duration = channel.length
            elif hasattr(channel, 'sample_length'):
                duration = channel.sample_length
        except Exception:
            pass
        return self._ticks_to_seconds(duration)

    def _get_channel_color(self, channel) -> str:
        """Get channel color as hex string."""
        try:
            if hasattr(channel, 'color') and channel.color:
                return f"#{channel.color:06x}"
        except Exception:
            pass
        return "#808080"  # Default gray