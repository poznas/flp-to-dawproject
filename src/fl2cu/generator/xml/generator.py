import logging
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List

from .structure import BaseStructureGenerator
from .track import TrackGenerator
from .clip import ClipGenerator
from ...models.arrangement import Arrangement
from ...models.clip import Clip

class DAWProjectXMLGenerator:
    """Main XML generator coordinating all components."""
    
    def __init__(self, arrangements: List[Arrangement], clip_paths: Dict[Clip, Path]):
        self.arrangements = arrangements
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)
        
        self.structure_gen = BaseStructureGenerator()
        self.track_gen = TrackGenerator()
        self.clip_gen = ClipGenerator()

    def generate_xml(self, project_name: str) -> ET.Element:
        """Generate complete DAWproject XML structure."""
        root = self.structure_gen.create_root()
        root.append(self.structure_gen.create_application_info())
        
        if not self.arrangements:
            return root
            
        arrangement = self.arrangements[0]
        timing = arrangement.project.timing
        
        # Add transport
        root.append(self.structure_gen.create_transport(timing))
        
        # Create structure with tracks
        structure = ET.SubElement(root, "Structure")
        tracks = arrangement.get_tracks()
        
        for track in tracks:
            track_el = self.track_gen.create_track(track)
            structure.append(track_el)
        
        # Create arrangement section
        arr_el = ET.SubElement(root, "Arrangement")
        lanes = ET.SubElement(arr_el, "Lanes", timeUnit="beats")
        
        # Add clips for each track
        for track in tracks:
            track_lanes = ET.SubElement(lanes, "Lanes", track=track.id)
            
            if track.clips:
                clips_el = ET.SubElement(track_lanes, "Clips")
                for clip in track.clips:
                    clip_el = self.clip_gen.create_clip(clip)
                    clips_el.append(clip_el)
        
        return root