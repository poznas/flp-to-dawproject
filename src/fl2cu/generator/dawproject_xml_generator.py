import logging
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Optional

from ..models.arrangement import Arrangement
from ..models.clip import Clip

class DAWProjectXMLGenerator:
    def __init__(self, arrangements: List['Arrangement'], clip_paths: Dict['Clip', Path]):
        self.arrangements = arrangements
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def generate_xml(self, project_name: str) -> ET.Element:
        root = ET.Element("Project", version="1.0")
        
        # Application info
        app = ET.SubElement(root, "Application", 
            name="FL Studio Converter", 
            version="1.0"
        )
        
        # Transport section with tempo and time signature
        transport = self._create_transport_element()
        root.append(transport)
        
        # Structure section containing tracks
        structure = ET.SubElement(root, "Structure")
        
        # Generate tracks and clips for first arrangement
        if self.arrangements:
            arrangement = self.arrangements[0]
            tracks = arrangement.get_tracks()
            
            for track_idx, track in enumerate(tracks):
                # Get track color from FL Studio track
                track_color = getattr(track, 'color', None)
                if track_color:
                    self.logger.debug(f"Using track color: {track_color}")
                    color_str = f"#{int(track_color.red*255):02x}{int(track_color.green*255):02x}{int(track_color.blue*255):02x}"
                else:
                    color_str = "#a2eabf"  # Default color

                track_el = ET.SubElement(structure, "Track",
                    contentType="audio",
                    loaded="true",
                    id=f"track-{track_idx}",
                    name=track.name or f"Track_{track_idx}",
                    color=color_str
                )
                
                # Add channel settings
                channel = ET.SubElement(track_el, "Channel",
                    audioChannels="2",
                    role="regular",
                    id=f"channel-{track_idx}"
                )
                
                ET.SubElement(channel, "Volume", max="1.000000", min="0.000000", unit="linear", value="1.000000")
                ET.SubElement(channel, "Pan", max="1.000000", min="0.000000", unit="normalized", value="0.500000")
                ET.SubElement(channel, "Mute", value="false")

        # Create arrangement section
        arrangement = ET.SubElement(root, "Arrangement", id="arrangement-0")
        lanes = ET.SubElement(arrangement, "Lanes", timeUnit="beats", id="lanes-0")
        
        # Process clips for each track
        for track_idx, track in enumerate(tracks):
            track_lanes = ET.SubElement(lanes, "Lanes", 
                track=f"track-{track_idx}",
                id=f"track-lanes-{track_idx}"
            )
            
            clips = ET.SubElement(track_lanes, "Clips", id=f"clips-{track_idx}")
            
            # Add clips
            for clip in track.clips:
                self.logger.debug(f"Processing clip {clip.name} for track track-{track_idx}")
                
                # Create clip element with proper duration
                clip_el = ET.SubElement(clips, "Clip",
                    time=str(clip.position),
                    duration=str(clip.duration),  # Use actual duration
                    name=clip.name
                )
                
                # Add inner clips structure for audio
                inner_clips = ET.SubElement(clip_el, "Clips")
                audio_clip = ET.SubElement(inner_clips, "Clip",
                    time="0.000000",
                    duration=str(clip.duration),  # Use actual duration
                    contentTimeUnit="beats",
                    playStart="0.000000"
                )
                
                # Add audio element with time stretching support
                audio = ET.SubElement(audio_clip, "Audio",
                    algorithm="stretch",  # Enable time stretching
                    channels="2",
                    duration=str(clip.duration),  # Use actual duration 
                    sampleRate="44100"
                )
                
                # Add file reference
                ET.SubElement(audio, "File",
                    path=f"audio/{clip.name}.wav"
                )
                
                self.logger.debug(f"Added clip {clip.name} to track track-{track_idx}")

        # Add empty scenes section 
        ET.SubElement(root, "Scenes")
        
        return root

    def _create_transport_element(self) -> ET.Element:
        """Create transport element with tempo and time signature settings."""
        transport = ET.Element("Transport")
        
        # Add tempo
        tempo = ET.SubElement(transport, "Tempo",
            max="960.000000",
            min="1.000000",
            unit="bpm",
            value="130.000000",
            id="tempo-1"
        )
        
        # Add time signature
        time_sig = ET.SubElement(transport, "TimeSignature",
            denominator="4",
            numerator="4",
            id="ts-1"
        )
        
        return transport