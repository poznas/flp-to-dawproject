from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Optional
import logging
import shutil
import zipfile

from ..generator.xml_utils import XMLWriter
from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..models.timing import ProjectTiming
from .xml_builder import XMLBuilder

class DAWProjectGenerator:
    def __init__(self, arrangements: List[Arrangement], clip_paths: Dict[Clip, Path]):
        self.arrangements = arrangements
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def generate_dawproject(self, output_path: str) -> None:
        try:
            temp_dir = Path(output_path).parent / "temp_dawproject"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                # Generate XML files
                self._generate_xml_files(temp_dir)
                
                # Copy and process audio files
                self._process_audio_files(temp_dir)
                
                # Create final ZIP archive
                self._create_archive(temp_dir, output_path)
                
                self.logger.info(f"Successfully generated DAWproject at {output_path}")
                
            finally:
                if temp_dir.exists():
                    # keeping existing temp-dir for debugging
                    pass
                    # shutil.rmtree(temp_dir)
                    
        except Exception as e:
            self.logger.error(f"Failed to generate DAWproject: {e}")
            raise

    def _generate_xml_files(self, temp_dir: Path) -> None:
        # Generate project.xml
        project_xml = self._create_project_xml()
        project_path = temp_dir / "project.xml"
        XMLWriter.write_xml(project_xml, project_path)
        
        # Generate metadata.xml
        metadata_xml = self._create_metadata_xml()
        metadata_path = temp_dir / "metadata.xml"
        XMLWriter.write_xml(metadata_xml, metadata_path)

    def _create_project_xml(self) -> ET.Element:
        root = ET.Element("Project", version="1.0")
        
        # Add Application info
        ET.SubElement(root, "Application", name="FL Studio Converter", version="1.0")
        
        # Add Transport section
        if self.arrangements and hasattr(self.arrangements[0], 'project'):
            timing = self.arrangements[0].project.timing
            root.append(XMLBuilder.create_transport_element(timing))
        
        # Add Structure section
        structure = ET.SubElement(root, "Structure")
        
        # Add tracks for each arrangement
        for i, arr in enumerate(self.arrangements):
            structure.append(XMLBuilder.create_track_element(arr.name, i))
        
        # Add Arrangements
        for i, arr in enumerate(self.arrangements):
            arr_element = ET.SubElement(root, "Arrangement", id=f"arrangement-{i}")
            lanes = ET.SubElement(arr_element, "Lanes", timeUnit="beats", id=f"lanes-{i}")
            track_lanes = ET.SubElement(lanes, "Lanes", track=f"track-{i}", id=f"track-lanes-{i}")
            clips = ET.SubElement(track_lanes, "Clips", id=f"clips-{i}")
            
            # Fixed: Iterate through tracks to get clips
            for track in arr.get_tracks():
                for clip in track.clips:
                    clip_el = XMLBuilder.create_clip_element(clip, self.clip_paths.get(clip))
                    if clip_el is not None:
                        clips.append(clip_el)
        
        return root

    def _create_metadata_xml(self) -> ET.Element:
        root = ET.Element("MetaData")
        
        if self.arrangements:
            arr = self.arrangements[0]
            if hasattr(arr, 'project') and arr.project:
                ET.SubElement(root, "Title").text = arr.project.name
            else:
                ET.SubElement(root, "Title").text = arr.name
                
        return root

    def _process_audio_files(self, temp_dir: Path) -> None:
        audio_dir = temp_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        for clip, source_path in self.clip_paths.items():
            if source_path and source_path.exists():
                dest_path = audio_dir / f"{clip.name}.wav"
                shutil.copy2(source_path, dest_path)
            else:
                self.logger.warning(f"Audio file not found: {source_path}")

    def _create_archive(self, temp_dir: Path, output_path: str) -> None:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add XML files
            zf.write(temp_dir / "project.xml", "project.xml")
            zf.write(temp_dir / "metadata.xml", "metadata.xml")
            
            # Add audio files
            audio_dir = temp_dir / "audio"
            for audio_file in audio_dir.glob("*.wav"):
                zf.write(audio_file, f"audio/{audio_file.name}")