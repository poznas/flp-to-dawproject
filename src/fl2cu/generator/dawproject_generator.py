from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Optional
import logging
import shutil
import zipfile

from ..generator.dawproject_xml_generator import DAWProjectXMLGenerator

from ..generator.xml_utils import XMLWriter
from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..models.timing import ProjectTiming

class DAWProjectGenerator:
    def __init__(self, arrangements: List[Arrangement], clip_paths: Dict[Clip, Path]):
        self.arrangements = arrangements
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def generate_dawproject(self, output_path: str) -> None:
        """Generate DAWproject file at the specified path."""
        output_path = Path(output_path)
        
        # Create unique temp directory for this dawproject
        temp_dir = output_path.parent / f"temp_{output_path.stem}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Generate XML using dedicated generator
            xml_generator = DAWProjectXMLGenerator(self.arrangements, self.clip_paths)
            project_xml = xml_generator.generate_xml(output_path.stem)
            
            # Write project.xml
            project_path = temp_dir / "project.xml"
            XMLWriter.write_xml(project_xml, project_path)
            
            # Generate and write metadata.xml
            metadata_xml = self._create_metadata_xml()
            metadata_path = temp_dir / "metadata.xml"
            XMLWriter.write_xml(metadata_xml, metadata_path)
            
            # Process audio files
            self._process_audio_files(temp_dir)
            
            # Create final archive
            self._create_archive(temp_dir, output_path)
            
            self.logger.info(f"Successfully generated DAWproject at {output_path}")
            
        finally:
            if temp_dir.exists():
                pass
                # Remove temp directory when done, disabled to allow later simpler entry into the generated files, to see what might be wrong with `project.xml`
                # shutil.rmtree(temp_dir)

    @staticmethod
    def clear_output_directory(output_dir: Path) -> None:
        """Clear target directory before generating new files."""
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    def _create_metadata_xml(self) -> ET.Element:
        """Create metadata XML structure."""
        root = ET.Element("MetaData")
        if self.arrangements:
            arr = self.arrangements[0]
            if hasattr(arr, 'project') and arr.project:
                ET.SubElement(root, "Title").text = arr.project.name
            else:
                ET.SubElement(root, "Title").text = arr.name
        return root

    def _process_audio_files(self, temp_dir: Path) -> None:
        """Process and copy audio files to temp directory."""
        audio_dir = temp_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        for clip, source_path in self.clip_paths.items():
            if source_path and source_path.exists():
                dest_path = audio_dir / f"{clip.name}.wav"
                shutil.copy2(source_path, dest_path)
            else:
                self.logger.warning(f"Audio file not found: {source_path}")

    def _create_archive(self, temp_dir: Path, output_path: Path) -> None:
        """Create final ZIP archive."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(temp_dir / "project.xml", "project.xml")
            zf.write(temp_dir / "metadata.xml", "metadata.xml")
            
            audio_dir = temp_dir / "audio"
            for audio_file in audio_dir.glob("*.wav"):
                zf.write(audio_file, f"audio/{audio_file.name}")