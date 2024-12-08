from pathlib import Path
from typing import Optional, Callable, Tuple
import re
import logging

from pyflp.arrangement import ChannelPLItem
from pyflp.channel import Sampler, Channel
from pyflp.project import Project
from ..models.clip import Clip

class FLClipParser:
    """Handles parsing of audio clips from FL Studio channels and playlist items."""
    
    def __init__(self, fl_project: Project, path_resolver: Callable):
        self.fl_project = fl_project
        self.ppq = getattr(fl_project, 'ppq', 96)
        self.tempo = float(getattr(fl_project, 'tempo', 120.0))
        self.path_resolver = path_resolver
        self.logger = logging.getLogger(__name__)

    def create_clip(self, item: ChannelPLItem, track_name: Optional[str] = None) -> Optional[Clip]:
        """Create clip model from FL Studio playlist item."""
        try:
            channel = item.channel
            
            # Get the source path and handle missing files
            raw_path = str(channel.sample_path) if hasattr(channel, 'sample_path') else None
            if not raw_path:
                self.logger.warning(f"No sample path for channel in track {track_name}")
                return None
                
            source_path = self.resolve_audio_path(raw_path)
            if not source_path:
                self.logger.warning(f"Could not resolve audio path: {raw_path}")
                return None

            # Get core timing values in beats
            position_beats = item.position / self.ppq
            duration = item.length / self.ppq 

            # Convert FL Studio ms offsets to beats
            start_offset, end_offset = self._get_normalized_offsets(item)

            clip = Clip(
                name=self._sanitize_filename(source_path.stem),
                position=position_beats,
                duration=duration,
                start_offset=start_offset,
                end_offset=end_offset,
                color=self._get_color(channel),
                source_path=source_path,
                format=source_path.suffix.lower().lstrip('.'),
                track_name=track_name or "Default",
                volume=self._get_normalized_volume(channel),
                muted=not bool(getattr(channel, 'enabled', True))
            )
            
            self.logger.debug(
                f"Created clip {clip.name} at pos={position_beats}b, "
                f"dur={duration}b, offsets=({start_offset}b, {end_offset}b)"
            )
            return clip

        except Exception as e:
            self.logger.error(f"Failed to create clip: {e}")
            return None

    def resolve_audio_path(self, raw_path: str) -> Optional[Path]:
        """Resolve audio file path, trying different extensions if needed."""
        try:
            # Try exact path first
            source_path = self.path_resolver(raw_path)
            if source_path and source_path.exists():
                return source_path

            # Try alternate extensions
            base_path = Path(raw_path)
            extensions = ['.wav', '.mp3', '.aif', '.aiff', '.flac', '.ogg']
            
            for ext in extensions:
                alt_path = base_path.with_suffix(ext)
                resolved = self.path_resolver(str(alt_path))
                if resolved and resolved.exists():
                    return resolved

            # Try case-insensitive extensions
            for ext in extensions:
                alt_path = base_path.with_suffix(ext.upper())
                resolved = self.path_resolver(str(alt_path))
                if resolved and resolved.exists():
                    return resolved
            
            self.logger.warning("⚠️ Parsing: Clip sample path doesn't exist")

            return source_path

        except Exception as e:
            self.logger.error(f"Error resolving audio path {raw_path}: {e}")
            return None

    def _get_normalized_offsets(self, item: ChannelPLItem) -> Tuple[float, float]:
        """Convert FL Studio millisecond offsets to beats."""
        if not hasattr(item, 'offsets'):
            return (0.0, 0.0)

        # Get raw offsets (in milliseconds)
        start_ms = float(item.offsets[0])
        end_ms = float(item.offsets[1])

        # Handle special FL Studio cases
        if start_ms == -1.0:  # Uncut sample start
            start_ms = 0.0
        if end_ms == -1.0:  # Uncut sample end 
            end_ms = 0.0

        # Convert milliseconds to beats using tempo
        # beats = ms * (tempo/60000)
        ms_to_beats = self.tempo / 60000.0

        start_beats = start_ms * ms_to_beats if start_ms != 0 else 0
        end_beats = end_ms * ms_to_beats if end_ms != 0 else 0

        self.logger.debug(
            f"Converting offsets: {start_ms}ms, {end_ms}ms -> "
            f"{start_beats}b, {end_beats}b @ {self.tempo}bpm"
        )

        return (max(0.0, start_beats), max(0.0, end_beats))

    def _get_color(self, channel: Channel) -> str:
        """Extract color in hex format from FL Studio channel."""
        if not hasattr(channel, 'color'):
            return "#a2eabf"  # Default color
            
        color = channel.color
        if hasattr(color, 'red'):
            r = int(color.red * 255)
            g = int(color.green * 255)
            b = int(color.blue * 255)
            return f"#{r:02x}{g:02x}{b:02x}"
        elif isinstance(color, int):
            r = (color >> 16) & 255
            g = (color >> 8) & 255
            b = color & 255
            return f"#{r:02x}{g:02x}{b:02x}"
        return "#a2eabf"

    def _get_normalized_volume(self, channel: Channel) -> float:
        """Get volume normalized to 0-1 range."""
        try:
            if hasattr(channel, 'volume'):
                raw_volume = float(channel.volume)
                return min(raw_volume / 10000.0, 1.0)  # FL uses 0-12800 range
        except Exception as e:
            self.logger.warning(f"Failed to get volume: {e}")
        return 1.0

    def _sanitize_filename(self, filename: str) -> str:
        """Create safe filename from original name."""
        sanitized = filename.replace(' ', '_')
        sanitized = re.sub(r'[^\w\-.]', '_', sanitized)
        return sanitized.lower()