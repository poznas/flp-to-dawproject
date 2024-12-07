from typing import List, Optional
import logging

import pyflp

from ..models.track import Track
from ..models.arrangement import Arrangement
from .clip_parser import FLClipParser

class FLArrangementParser:
    """Handles parsing of FL Studio arrangements and their tracks."""
    
    def __init__(self, fl_project: 'pyflp.Project', clip_parser: FLClipParser):
        self.fl_project = fl_project
        self.clip_parser = clip_parser
        self.logger = logging.getLogger(__name__)

    def parse_arrangements(self) -> List[Arrangement]:
        """Extract all arrangements with their tracks and clips."""
        if not hasattr(self.fl_project, 'arrangements'):
            raise ValueError("Could not access arrangements in FL Studio project")
                
        arrangements = []
        fl_arrangements = list(self.fl_project.arrangements)
        self.logger.debug(f"Found {len(fl_arrangements)} FL Studio arrangements")
        
        for fl_arr in fl_arrangements:
            # Create arrangement
            arrangement_name = getattr(fl_arr, 'name', None) or "Unnamed Arrangement"
            arrangement = Arrangement(name=arrangement_name)
            self.logger.debug(f"\nProcessing arrangement: {arrangement_name}")
            
            # Get playlist data
            playlist_data = None
            if hasattr(fl_arr, 'tracks'):
                fl_tracks = list(fl_arr.tracks)
                self.logger.debug(f"Found {len(fl_tracks)} FL Studio tracks")
                
                # Process each track
                for track_idx, fl_track in enumerate(fl_tracks):
                    # Get track clips
                    track_clips = []
                    if hasattr(fl_track, '__iter__'):
                        items = list(fl_track)
                        if len(items) < 1:
                            continue
                        self.logger.debug(f"Track contains {len(items)} items")
                        
                        for item in items:
                            self.logger.debug(f"Processing item: {item}")
                            
                            # Try to create clip from item
                            clip = None
                            if hasattr(item, 'channel'):
                                self.logger.debug(f"Item has channel: {item.channel}")
                                clip = self.clip_parser.create_clip(
                                    channel=item.channel,
                                    position=item.position,
                                    length=item.length,  # Pass length from playlist item
                                    track_name=f"Track {track_idx}"
                                )
                            else:
                                raise ValueError(F"Unable to retrieve channel data from {item}")
                            
                            if clip:
                                track_clips.append(clip)
                                self.logger.debug(f"Created clip: {clip.name}")
                            
                    
                    # Only create track if it has clips
                    if track_clips:
                        track = Track(
                            name=getattr(fl_track, 'name', None) or f"Track {track_idx}",
                            id=f"track-{track_idx}",
                            clips=track_clips
                        )
                        arrangement.add_track(track)
                        self.logger.debug(f"Added track with {len(track_clips)} clips")
            
            if arrangement.has_tracks():
                arrangements.append(arrangement)
                self.logger.debug(
                    f"Successfully parsed arrangement '{arrangement.name}' with "
                    f"{len(arrangement.get_tracks())} tracks"
                )
            else:
                self.logger.debug("Skipping arrangement - no tracks with clips found")

        if not arrangements:
            raise ValueError("No valid arrangements found in FL Studio project")
                
        return arrangements