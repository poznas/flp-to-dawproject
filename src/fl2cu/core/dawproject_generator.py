from pathlib import Path
from typing import Dict, Optional, Any
import logging
import json
import subprocess
from xml.etree import ElementTree as ET
from ..models.arrangement import Arrangement
from ..models.clip import Clip

class DAWProjectGenerator:
    """Generates DAWproject format XML files from FL Studio arrangements."""
    
    def __init__(self, arrangement: Arrangement, clip_paths: Dict[Clip, Path]):
        self.arrangement = arrangement
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def _probe_audio(self, path: str) -> Dict[str, Any]:
        """Get audio file metadata using ffprobe."""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-of', 'json',
            '-show_format',
            '-show_streams',
            str(path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ffprobe failed for {path}: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse ffprobe output: {e}")
            raise

    def generate_dawproject(self, output_path: str) -> None:
        """Generate DAWproject file for the arrangement."""
        self.logger.info(f"Creating DAWproject file at {output_path}")
        
        try:
            # Create root Project element
            root = ET.Element("Project", version="1.0")
            
            # Add Application metadata
            app = ET.SubElement(root, "Application", name="FL Studio Converter", version="1.0")
            
            # Create Transport element for tempo/time signature
            transport = ET.SubElement(root, "Transport")
            tempo = ET.SubElement(transport, "Tempo", unit="bpm", value="120", min="20", max="999")
            time_sig = ET.SubElement(transport, "TimeSignature", numerator="4", denominator="4")
            
            # Create Structure section
            structure = ET.SubElement(root, "Structure")
            
            # Create audio track
            track = ET.SubElement(structure, "Track", 
                                contentType="audio",
                                loaded="true",
                                id=f"track-{self.arrangement.name}",
                                name=self.arrangement.name)
            
            # Create channel for the track
            channel = ET.SubElement(track, "Channel",
                                  audioChannels="2",
                                  role="regular",
                                  solo="false",
                                  id=f"channel-{self.arrangement.name}")
            
            # Add standard channel controls
            ET.SubElement(channel, "Volume", value="1.0", min="0.0", max="2.0", unit="linear")
            ET.SubElement(channel, "Pan", value="0.5", min="0.0", max="1.0", unit="normalized")
            ET.SubElement(channel, "Mute", value="false")

            # Create Arrangement section
            arrangement = ET.SubElement(root, "Arrangement", id="main-arrangement")
            
            # Create Lanes section
            lanes = ET.SubElement(arrangement, "Lanes", timeUnit="beats")
            
            # Create track lanes
            track_lanes = ET.SubElement(lanes, "Lanes", track=f"track-{self.arrangement.name}")
            
            # Create clips container
            clips = ET.SubElement(track_lanes, "Clips")

            # Process each audio clip
            for clip in self.arrangement.clips:
                source_path = self.clip_paths.get(clip)
                if not source_path or not source_path.exists():
                    self.logger.warning(f"Audio file not found for clip: {clip.name}")
                    continue

                try:
                    # Get audio metadata
                    metadata = self._probe_audio(str(source_path))
                    stream = metadata['streams'][0]
                    
                    # Create clip element
                    clip_el = ET.SubElement(clips, "Clip",
                                          time=str(clip.position),
                                          duration=str(clip.duration),
                                          name=clip.name)
                    
                    # Create audio within clip
                    audio = ET.SubElement(clip_el, "Audio",
                                        channels=str(stream.get('channels', 2)),
                                        duration=str(stream.get('duration', clip.duration)),
                                        sampleRate=str(stream.get('sample_rate', 44100)))
                    
                    # Add file reference
                    file_ref = ET.SubElement(audio, "File", path=str(source_path))
                    
                    self.logger.debug(f"Added clip {clip.name} at position {clip.position}")

                except Exception as e:
                    self.logger.error(f"Failed to process clip {clip.name}: {str(e)}")
                    raise

            # Create pretty XML
            from xml.dom import minidom
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            
            # Write the file
            with open(output_path, 'w') as f:
                f.write(xml_str)
                
            self.logger.info("DAWproject file successfully generated")

        except Exception as e:
            self.logger.error(f"Failed to generate DAWproject file: {str(e)}")
            raise