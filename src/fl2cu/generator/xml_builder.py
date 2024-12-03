from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Optional

from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..models.timing import ProjectTiming

class XMLBuilder:
    @staticmethod
    def create_transport_element(timing: ProjectTiming) -> ET.Element:
        transport = ET.Element("Transport")
        ET.SubElement(transport, "Tempo",
            unit="bpm",
            value=str(timing.tempo),
            min="20",
            max="999",
            id="tempo"
        )
        ET.SubElement(transport, "TimeSignature",
            numerator=str(timing.time_signature_numerator),
            denominator=str(timing.time_signature_denominator),
            id="timesig"
        )
        return transport

    @staticmethod
    def create_track_element(name: str, index: int) -> ET.Element:
        track = ET.Element("Track",
            contentType="audio",
            loaded="true",
            id=f"track-{index}",
            name=name,
            color="#a2eabf"
        )
        
        # Add Channel
        channel = ET.SubElement(track, "Channel",
            audioChannels="2",
            role="regular",
            solo="false",
            id=f"channel-{index}"
        )
        
        # Add default channel controls
        ET.SubElement(channel, "Volume", value="1.0", min="0.0", max="2.0", unit="linear")
        ET.SubElement(channel, "Pan", value="0.5", min="0.0", max="1.0", unit="normalized")
        ET.SubElement(channel, "Mute", value="false")
        
        return track

    @staticmethod
    def create_clip_element(clip: Clip, clip_path: Path) -> Optional[ET.Element]:
        if not clip_path.exists():
            return None
            
        clip_el = ET.Element("Clip",
            time=str(clip.position),
            duration=str(clip.duration),
            name=clip.name
        )
        
        if clip.volume != 1.0:
            clip_el.set("level", str(clip.volume))
        if clip.muted:
            clip_el.set("enable", "false")
        
        warps = ET.SubElement(clip_el, "Warps",
            contentTimeUnit="seconds",
            timeUnit="beats"
        )
        
        audio = ET.SubElement(warps, "Audio",
            channels="2",
            duration=str(clip.duration),
            sampleRate="44100",
            algorithm="stretch"
        )
        
        ET.SubElement(audio, "File",
            path=f"audio/{clip.name}.wav"
        )
        
        # Add warp points for time stretching
        ET.SubElement(warps, "Warp", time="0.0", contentTime="0.0")
        ET.SubElement(warps, "Warp", time=str(clip.duration), contentTime=str(clip.duration))
        
        return clip_el