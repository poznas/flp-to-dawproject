from pathlib import Path
import logging
from typing import Optional
from ..models.clip import Clip

class FLClipParser:
    """Handles parsing of audio clips from FL Studio channels."""
    
    def __init__(self, fl_project: 'pyflp.Project'):
        self.fl_project = fl_project
        self.ppq = getattr(fl_project, 'ppq', 96)
        self.logger = logging.getLogger(__name__)

    def create_clip(self, channel, position: float) -> Optional[Clip]:
        """Create clip from FL Studio channel."""
        if not hasattr(channel, 'sample_path'):
            return None

        try:
            source_path = Path(channel.sample_path)
            if not source_path.exists():
                self.logger.warning(f"Sample not found: {source_path}")
                return None

            name = getattr(channel, 'name', '') or source_path.stem
            position_seconds = float(position) / self.ppq
            duration = float(getattr(channel, 'sample_length', self.ppq)) / self.ppq
            
            # Get channel color
            color = self._get_color(channel)
            
            # Get volume normalized to 0-1
            volume = self._get_volume(channel)

            clip = Clip(
                name=f"{name}_{position}",
                position=position_seconds,
                duration=duration,
                color=color,
                source_path=source_path,
                volume=volume,
                muted=not bool(getattr(channel, 'enabled', True))
            )
            
            self.logger.debug(f"Created clip {clip.name} at {position_seconds}s")
            return clip

        except Exception as e:
            self.logger.error(f"Failed to create clip: {e}")
            return None

    def _get_color(self, channel) -> str:
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
        try:
            if hasattr(channel, 'volume'):
                raw_volume = float(channel.volume)
                return raw_volume / 100.0 if raw_volume > 1.0 else raw_volume
        except Exception as e:
            self.logger.warning(f"Failed to get volume: {e}")
        return 1.0