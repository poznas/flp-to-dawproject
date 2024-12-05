from typing import List, Optional
import logging

import pyflp
from ..models.arrangement import Arrangement
from .clip_parser import FLClipParser

class FLArrangementParser:
    """Handles parsing of FL Studio arrangements."""
    
    def __init__(self, fl_project: 'pyflp.Project', clip_parser: FLClipParser):
        self.fl_project = fl_project
        self.clip_parser = clip_parser
        self.logger = logging.getLogger(__name__)

    def parse_arrangements(self) -> List[Arrangement]:
        """Extract all arrangements from FL Studio project."""
        arrangements = []
        
        # Try FL Studio 12.9+ arrangements first
        if hasattr(self.fl_project, 'arrangements'):
            arrangements.extend(self._parse_native_arrangements())
        
        # Fall back to playlist if no arrangements found
        if not arrangements and hasattr(self.fl_project, 'playlist'):
            arrangement = self._parse_playlist_as_arrangement()
            if arrangement and arrangement.clips:
                arrangements.append(arrangement)
        
        return arrangements

    def _parse_native_arrangements(self) -> List[Arrangement]:
        arrangements = []
        for arr in self.fl_project.arrangements:
            if not arr.name:
                continue
            
            arrangement = Arrangement(name=arr.name)
            self._process_tracks(arrangement, arr.tracks)
            
            if arrangement.clips:
                arrangements.append(arrangement)
                
        return arrangements

    def _parse_playlist_as_arrangement(self) -> Optional[Arrangement]:
        arrangement = Arrangement(name=self.fl_project.name)
        
        for item in self.fl_project.playlist:
            if hasattr(item, 'channel'):
                clip = self.clip_parser.create_clip(item.channel, item.position)
                if clip:
                    arrangement.add_clip(clip)
                    
        return arrangement if arrangement.clips else None

    def _process_tracks(self, arrangement: Arrangement, tracks):
        for track in tracks:
            for item in track:
                if hasattr(item, 'channel'):
                    clip = self.clip_parser.create_clip(item.channel, item.position)
                    if clip:
                        arrangement.add_clip(clip)