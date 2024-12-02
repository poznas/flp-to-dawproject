import logging
import os
from pathlib import Path
from typing import List, Optional, Dict, Union

import pyflp
from ..models.project import Project
from ..models.arrangement import Arrangement
from ..models.clip import Clip

logger = logging.getLogger(__name__)

class FLProjectParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Project file not found: {file_path}")
            
        logger.debug(f"Loading FL Studio project: {file_path}")
        self.fl_project = pyflp.parse(file_path)
        logger.debug(f"Project version: {self.fl_project.version}")

    def resolve_fl_studio_path(self, path: Union[str, Path]) -> Optional[Path]:
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
            logger.error(f"Failed to resolve path {path}: {e}")
            return None

    def _get_color_hex(self, color) -> str:
        try:
            if hasattr(color, 'r') and hasattr(color, 'g') and hasattr(color, 'b'):
                # Handle RGBA object
                return f"#{color.r:02x}{color.g:02x}{color.b:02x}"
            elif isinstance(color, int):
                # Handle integer color value
                r = (color >> 16) & 255
                g = (color >> 8) & 255
                b = color & 255
                return f"#{r:02x}{g:02x}{b:02x}"
            else:
                logger.warning(f"Unknown color format: {type(color)}. Using default.")
                return "#FFFFFF"
        except Exception as e:
            logger.error(f"Error converting color: {e}")
            return "#FFFFFF"

    def _create_clip_from_channel(self, channel, position: float) -> Optional[Clip]:
        try:
            logger.debug(f"Creating clip from channel at position {position}")
            
            # Get channel name and sanitize for unique identification
            base_name = channel.name if hasattr(channel, 'name') else "unnamed_clip"
            base_name = base_name.replace(" ", "_")
            name = f"{base_name}_{position}"
            logger.debug(f"Channel name: {channel.name}")

            # Get sample path if available
            source_path = None
            if hasattr(channel, 'sample_path') and channel.sample_path:
                source_path = self.resolve_fl_studio_path(str(channel.sample_path))
                logger.debug(f"Sample path: {source_path}")

            # Calculate position in seconds
            position_seconds = float(position) / self.fl_project.ppq
            logger.debug(f"Position in seconds: {position_seconds}")

            # Get duration
            duration = 1.0
            if hasattr(channel, 'length'):
                duration = float(channel.length) / self.fl_project.ppq
            elif hasattr(channel, 'sample_length'):
                duration = float(channel.sample_length) / self.fl_project.ppq
            logger.debug(f"Duration in seconds: {duration}")

            # Get color
            color = "#FFFFFF"
            try:
                if hasattr(channel, 'color'):
                    color = self._get_color_hex(channel.color)
            except Exception as e:
                logger.warning(f"Failed to get channel color: {e}")
            logger.debug(f"Color: {color}")

            # Get volume and normalize to 0-1 range
            volume = 1.0
            try:
                if hasattr(channel, 'volume'):
                    raw_volume = float(channel.volume)
                    volume = raw_volume / 100.0 if raw_volume > 1.0 else raw_volume
            except Exception as e:
                logger.warning(f"Failed to get channel volume: {e}")
            logger.debug(f"Volume: {volume}")

            # Get mute state
            muted = False
            if hasattr(channel, 'enabled'):
                muted = not channel.enabled
            logger.debug(f"Muted: {muted}")

            clip = Clip(
                name=name,
                position=position_seconds,
                duration=duration,
                color=color,
                source_path=source_path,
                volume=volume,
                muted=muted
            )
            logger.debug(f"Successfully created clip: {clip.name}")
            return clip

        except Exception as e:
            logger.error(f"Error creating clip from channel: {e}")
            return None

    def _process_native_arrangement(self, arr) -> Optional[Arrangement]:
        try:
            logger.debug(f"Processing native arrangement: {arr.name}")
            
            # Get arrangement name from FL Studio arrangement
            if not hasattr(arr, 'name') or not arr.name:
                logger.warning("Arrangement has no name, skipping")
                return None
                
            arrangement = Arrangement(name=arr.name)
            
            for track in arr.tracks:
                for item in track:
                    if hasattr(item, 'channel'):
                        logger.debug(f"Found channel item at position {item.position}")
                        clip = self._create_clip_from_channel(item.channel, item.position)
                        if clip:
                            arrangement.add_clip(clip)
                            logger.debug(f"Added clip {clip.name} to arrangement {arrangement.name}")
                    elif hasattr(item, 'pattern'):
                        logger.debug(f"Found pattern item at position {item.position}")
                        clips = self._create_clips_from_pattern(item.pattern, item.position)
                        for clip in clips:
                            arrangement.add_clip(clip)
                            logger.debug(f"Added pattern clip {clip.name} to arrangement {arrangement.name}")

            logger.debug(f"Finished processing arrangement {arr.name} with {len(arrangement.clips)} clips")
            return arrangement
        except Exception as e:
            logger.error(f"Error processing native arrangement: {e}")
            return None

    def _extract_from_patterns(self) -> List[Arrangement]:
        arrangements = []
        try:
            logger.debug("Extracting from patterns")
            for pattern in self.fl_project.patterns:
                if not pattern.name:
                    continue
                    
                logger.debug(f"Processing pattern: {pattern.name}")
                arrangement = Arrangement(name=pattern.name)
                
                clips = self._create_clips_from_pattern(pattern)
                if clips:
                    for clip in clips:
                        arrangement.add_clip(clip)
                    arrangements.append(arrangement)
                    logger.debug(f"Added arrangement from pattern {pattern.name} with {len(clips)} clips")
                    
        except Exception as e:
            logger.error(f"Error extracting from patterns: {e}")
            
        return arrangements

    def extract_arrangements(self) -> List[Arrangement]:
        arrangements = []
        
        logger.debug("Checking for FL Studio 12.9.1+ arrangements")
        if hasattr(self.fl_project, 'arrangements'):
            logger.debug(f"Found {len(self.fl_project.arrangements)} native arrangements")
            for arr in self.fl_project.arrangements:
                arrangement = self._process_native_arrangement(arr)
                if arrangement and arrangement.clips:
                    arrangements.append(arrangement)
                    logger.debug(f"Added arrangement {arrangement.name} with {len(arrangement.clips)} clips")

        # Fall back to patterns if no arrangements found
        if not arrangements:
            logger.debug("Falling back to pattern-based arrangements")
            pattern_arrangements = self._extract_from_patterns()
            arrangements.extend(pattern_arrangements)

        logger.info(f"Total arrangements extracted: {len(arrangements)}")
        for arr in arrangements:
            logger.debug(f"Arrangement '{arr.name}' has {len(arr.clips)} clips")
        return arrangements

    def parse_project(self) -> Project:
        project = Project(
            name=self.file_path.stem,
            source_path=self.file_path
        )

        try:
            arrangements = self.extract_arrangements()
            for arr in arrangements:
                project.add_arrangement(arr)
        except Exception as e:
            logger.error(f"Failed to extract arrangements: {e}")
            raise

        return project