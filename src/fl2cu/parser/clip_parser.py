from pathlib import Path
from typing import Optional, Callable
import logging
from ..models.clip import Clip

class FLClipParser:
    """Handles parsing of audio clips from FL Studio channels and playlist items."""
    
    def __init__(self, fl_project: 'pyflp.Project', path_resolver: Callable):
        self.fl_project = fl_project
        self.ppq = getattr(fl_project, 'ppq', 96)
        self.path_resolver = path_resolver
        self.logger = logging.getLogger(__name__)

    def create_clip(self, channel, position: float, track_name: Optional[str] = None) -> Optional[Clip]:
        """Create clip from FL Studio channel with optional track assignment."""
        try:
            # Get base name from channel and ensure uniqueness with position
            base_name = getattr(channel, 'name', '') or "unnamed_clip"
            base_name = base_name.replace(" ", "_")
            name = f"{base_name}_{int(position)}"
            
            # Get sample path if available
            source_path = None
            if hasattr(channel, 'sample_path') and channel.sample_path:
                source_path = self.path_resolver(str(channel.sample_path))
                self.logger.debug(f"Sample path: {source_path}")

            if not source_path:
                return None

            # Calculate timing (convert from PPQ to time)
            position_beats = float(position) / self.ppq  # Convert to beats
            duration = float(getattr(channel, 'length', self.ppq)) / self.ppq  # Length in beats
            
            # Get color (default if not set)
            color = self._get_color(channel)
            
            # Get normalized volume
            volume = self._get_volume(channel)
            
            # Get mute state
            muted = not bool(getattr(channel, 'enabled', True))

            # Create clip with track assignment
            clip = Clip(
                name=name,
                position=position_beats,
                duration=duration,
                color=color,
                source_path=source_path,
                track_name=track_name or "Default",
                volume=volume,
                muted=muted
            )
            
            self.logger.debug(f"Created clip {clip.name} at {position_beats} beats on track {clip.track_name}")
            return clip

        except Exception as e:
            self.logger.error(f"Failed to create clip: {e}")
            return None

    def _get_color(self, channel) -> str:
        """Extract color from channel with fallback to default."""
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
        return "#a2eabf"  # Default color matching sample

    def _get_volume(self, channel) -> float:
        """Get normalized volume from channel."""
        try:
            if hasattr(channel, 'volume'):
                raw_volume = float(channel.volume)
                # FL Studio uses 0-12800 range, normalize to 0-1
                return min(raw_volume / 10000.0, 1.0)
        except Exception as e:
            self.logger.warning(f"Failed to get volume: {e}")
        return 1.0