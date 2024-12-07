from pathlib import Path
import pprint
from typing import Optional, Callable, Tuple
from pyflp.arrangement import ChannelPLItem
from pyflp.channel import Sampler, Channel
import logging
import os
import re
from ..models.clip import Clip

class FLClipParser:
    """Handles parsing of audio clips from FL Studio channels and playlist items."""
    
    def __init__(self, fl_project: 'pyflp.Project', path_resolver: Callable):
        self.fl_project = fl_project
        self.ppq = getattr(fl_project, 'ppq', 96)
        self.path_resolver = path_resolver
        self.logger = logging.getLogger(__name__)

    def create_clip(self, item: ChannelPLItem, track_name: Optional[str] = None) -> Optional[Clip]:
        channel: Sampler = item.channel
        position = item.position
        length = item.length
        # Get base name from channel
        base_name = getattr(channel, 'name', '') or "unnamed_clip"
        base_name = re.sub(r'[^\w\-]', '_', base_name)
        name = f"{base_name}_{int(position)}"
        
        # Get sample path if available
        source_path = None
        if hasattr(channel, 'sample_path') and channel.sample_path:
            source_path = self.path_resolver(str(channel.sample_path))
            self.logger.debug(f"Sample path: {source_path}")

        if not source_path:
            return None

        # Get duration in beats
        if length is None:
            raise ValueError(f"Length not provided for clip from {item}")
        duration = length / self.ppq

        # Position in beats
        position_beats = position / self.ppq
        
        # Get clip offsets from the channel/item
        start_offset, end_offset = self._get_offsets(item)
        
        # Convert offsets from PPQ to beats
        start_offset_beats = start_offset / self.ppq if start_offset is not None else 0.0
        end_offset_beats = end_offset / self.ppq if end_offset is not None else duration
        
        
        # Get normalized volume
        volume = self._get_volume(channel)
        
        # Get mute state
        muted = not bool(getattr(channel, 'enabled', True))

        clip = Clip(
            name=name,
            position=position_beats,
            duration=duration,
            start_offset=start_offset_beats,
            end_offset=end_offset_beats,
            color=self._get_color(channel),
            source_path=source_path,
            track_name=track_name or "Default",
            volume=volume,
            muted=muted
        )
        
        self.logger.debug(
            f"Created clip {clip.name} at {position_beats} beats "
            f"with start_offset {clip.start_offset} on track {clip.track_name}"
        )
        return clip

    def _get_offsets(self, item: ChannelPLItem) -> Tuple[float, float]:
        """Get start and end offsets from FL Studio channel/item."""
        if hasattr(item, 'start_offset'):
            if item.start_offset > 0:
                self.logger.debug(f"Found start_offset = {item.start_offset}")
                return (item.start_offset, 0.0)
        if hasattr(item, 'offsets'):
            if item.offsets != (0.0, 0.0):
                self.logger.debug(f"Found channel.offsets = {item.offsets}")
                return item.offsets

        raise Exception(f"Failed to find any offset data in item {item}.")

    def _get_color(self, channel: Channel) -> str:
        """Get color from FL Studio channel."""
        if hasattr(channel, 'color'):
            color = channel.color
            if hasattr(color, 'red'):
                # Convert normalized floats (0-1) to integers (0-255) before formatting as hex
                r = int(color.red * 255)
                g = int(color.green * 255)
                b = int(color.blue * 255)
                return f"#{r:02x}{g:02x}{b:02x}"
            elif isinstance(color, int):
                r = (color >> 16) & 255
                g = (color >> 8) & 255
                b = color & 255
                return f"#{r:02x}{g:02x}{b:02x}"
        raise ValueError(f"no color for {channel}")

    def _get_volume(self, channel) -> float:
        """Get normalized volume from FL Studio channel."""
        try:
            if hasattr(channel, 'volume'):
                raw_volume = float(channel.volume)
                # FL Studio uses 0-12800 range, normalize to 0-1
                return min(raw_volume / 10000.0, 1.0)
        except Exception as e:
            self.logger.warning(f"Failed to get volume: {e}")
        return 1.0
