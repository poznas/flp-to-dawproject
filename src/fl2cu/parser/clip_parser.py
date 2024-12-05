from pathlib import Path
from typing import Optional, Callable
import logging
from ..models.clip import Clip

class FLClipParser:
    """Handles parsing of audio clips from FL Studio channels."""
    
    def __init__(self, fl_project: 'pyflp.Project', path_resolver: Callable):
        self.fl_project = fl_project
        self.ppq = getattr(fl_project, 'ppq', 96)
        self.path_resolver = path_resolver
        self.logger = logging.getLogger(__name__)

    def create_clip(self, channel, position: float) -> Optional[Clip]:
        """Create clip from FL Studio channel."""
        try:
            # Get channel name and sanitize for unique identification
            base_name = getattr(channel, 'name', '') or "unnamed_clip"
            base_name = base_name.replace(" ", "_")
            name = f"{base_name}_{position}"
            
            # Get sample path if available
            source_path = None
            if hasattr(channel, 'sample_path') and channel.sample_path:
                source_path = self.path_resolver(str(channel.sample_path))
                self.logger.debug(f"Sample path: {source_path}")

            if not source_path:
                self.logger.warning(f"Sample not found: {getattr(channel, 'sample_path', 'unknown')}")
                return None

            # Calculate timing
            position_seconds = float(position) / self.ppq
            duration = float(getattr(channel, 'length', self.ppq)) / self.ppq

            # Get color
            color = self._get_color(channel)
            
            # Get normalized volume
            volume = self._get_volume(channel)
            
            # Get mute state
            muted = not bool(getattr(channel, 'enabled', True))

            clip = Clip(
                name=name,
                position=position_seconds,
                duration=duration,
                color=color,
                source_path=source_path,
                volume=volume,
                muted=muted
            )
            
            self.logger.debug(f"Created clip {clip.name} at {position_seconds}s")
            return clip

        except Exception as e:
            self.logger.error(f"Failed to create clip: {e}")
            return None

    def _get_color(self, channel) -> str:
        """Extract color from channel."""
        try:
            if hasattr(channel, 'color'):
                color = channel.color
                if hasattr(color, 'r'):
                    return f"#{color.r:02x}{color.g:02x}{color.b:02x}"
                elif isinstance(color, int):
                    r = (color >> 16) & 255
                    g = (color >> 8) & 255
                    b = color & 255
                    return f"#{r:02x}{g:02x}{b:02x}"
        except Exception as e:
            self.logger.warning(f"Failed to get color: {e}")
        return "#FFFFFF"

    def _get_volume(self, channel) -> float:
        """Get normalized volume from channel."""
        try:
            if hasattr(channel, 'volume'):
                raw_volume = float(channel.volume)
                return raw_volume / 100.0 if raw_volume > 1.0 else raw_volume
        except Exception as e:
            self.logger.warning(f"Failed to get volume: {e}")
        return 1.0