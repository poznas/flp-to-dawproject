from xml.etree import ElementTree as ET
from ...models.clip import Clip

class ClipGenerator:
    """Handles creation of Clip XML elements."""
    
    def create_clip(self, clip: Clip) -> ET.Element:
        """Create Clip element from Clip model."""
        clip_el = ET.Element("Clip",
            time=str(clip.position),
            duration=str(clip.duration),
            playStart=str(clip.start_offset),
            fadeTimeUnit="beats",
            name=clip.name,
            enable=str(not clip.muted).lower()
        )
        
        inner_clips = ET.SubElement(clip_el, "Clips")
        audio_clip = self.create_audio_clip(clip)
        inner_clips.append(audio_clip)
        
        return clip_el
        
    def create_audio_clip(self, clip: Clip) -> ET.Element:
        """Create inner audio clip element with proper file reference."""
        inner_clip = ET.Element("Clip",
            contentTimeUnit="beats",
            time=str(clip.position),
            duration=str(clip.duration),
        )
        
        # Add audio element with channel/sample rate from metadata if available
        audio = ET.SubElement(inner_clip, "Audio",
            channels=str(clip.metadata.get('channels', 2)),
            sampleRate=str(clip.metadata.get('sample_rate', 48000))
        )
        
        # Use the output filename that preserves original format
        audio_path = f"audio/{clip.output_filename}"
        ET.SubElement(audio, "File",
            path=audio_path,
            external="false"
        )
        
        return inner_clip