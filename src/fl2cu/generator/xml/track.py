from xml.etree import ElementTree as ET
from ...models.track import Track

class TrackGenerator:
    """Handles creation of Track and Channel XML elements."""
    
    def create_track(self, track: Track) -> ET.Element:
        """Create Track element from Track model."""
        track_el = ET.Element("Track",
            contentType="audio",
            id=track.id,
            name=track.name,
            color=track.color if hasattr(track, 'color') else "#a2eabfff"
        )
        
        # Add channel
        track_el.append(self.create_channel(track))
        
        return track_el
        
    def create_channel(self, track: Track) -> ET.Element:
        """Create Channel element from Track model."""
        channel = ET.Element("Channel",
            role="regular",
            audioChannels="2",
            id=f"{track.id}_ch",
            name=track.name,
            destination="id0"
        )
        
        self._add_channel_settings(channel, track)
        return channel
        
    def _add_channel_settings(self, channel_el: ET.Element, track: Track) -> None:
        """Add channel settings, using track properties if available."""
        ET.SubElement(channel_el, "Mute",
            value=str(track.muted).lower() if hasattr(track, 'muted') else "false",
            name="Mute"
        )
        
        ET.SubElement(channel_el, "Pan",
            value=str(track.pan) if hasattr(track, 'pan') else "0.5",
            unit="normalized",
            min="0",
            max="1",
            name="Pan"
        )
        
        ET.SubElement(channel_el, "Volume",
            value=str(track.volume) if hasattr(track, 'volume') else "1",
            unit="linear",
            min="0",
            max="2",
            name="Volume"
        )
