from pathlib import Path
import shutil
import zipfile
import logging
from xml.etree import ElementTree as ET
from typing import Dict, List

from ..models.arrangement import Arrangement
from ..models.clip import Clip
from .xml.generator import DAWProjectXMLGenerator
from .xml_utils import XMLWriter


class DAWProjectGenerator:
    """Handles generation of complete DAWproject files."""
    
    def __init__(self, arrangements: List[Arrangement], clip_paths: Dict[Path, Clip]):
        """Initialize generator with arrangements and clip paths.
        
        Args:
            arrangements: List of arrangements to process
            clip_paths: Dictionary mapping source paths to clips
        """
        self.arrangements = arrangements
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)
        
        # Initialize XML generator
        self.xml_generator = DAWProjectXMLGenerator(arrangements, clip_paths)

    def generate_dawproject(self, output_path: str) -> None:
        """Generate DAWproject file at the specified path.
        
        Args:
            output_path: Path where the .dawproject file should be created
        """
        output_path = Path(output_path)
        
        # Create unique temp directory for this dawproject
        temp_dir = output_path.parent / f"temp_{output_path.stem}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Generate and write project.xml
            project_xml = self.xml_generator.generate_xml(output_path.stem)
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
            
        except Exception as e:
            self.logger.error(f"Failed to generate DAWproject: {e}")
            raise
        finally:
            # Keep temp files for debugging
            pass
            # if temp_dir.exists():
            #     shutil.rmtree(temp_dir)

    def _create_metadata_xml(self) -> ET.Element:
        """Create metadata XML element.
        
        Returns:
            ET.Element: Root metadata element
        """
        root = ET.Element("MetaData")
        
        if self.arrangements:
            arr = self.arrangements[0]
            if hasattr(arr, 'project') and arr.project:
                project = arr.project
                ET.SubElement(root, "Title").text = project.name
                
                if hasattr(project, 'artists'):
                    ET.SubElement(root, "Artist").text = project.artists
                    
                if hasattr(project, 'comments'):
                    ET.SubElement(root, "Comment").text = project.comments
            else:
                ET.SubElement(root, "Title").text = arr.name
        
        return root

    def _process_audio_files(self, temp_dir: Path) -> None:
        """Process and copy audio files to the temp directory."""
        audio_dir = temp_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        # Keep track of processed files to avoid duplicates 
        processed_files = set()
        
        for source_path, clip in self.clip_paths.items():
            if not source_path or not source_path.exists():
                self.logger.warning(f"Audio file not found: {source_path}")
                continue
                
            # Use clip's output filename with original format
            dest_filename = clip.output_filename
            dest_path = audio_dir / dest_filename
            
            # Skip if file already exists
            if dest_path.exists() or dest_filename in processed_files:
                self.logger.debug(f"Audio file already exists, skipping: {dest_filename}")
                continue
            
            # Simple file copy
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            processed_files.add(dest_filename)
            
            
    def _copy_audio_file(self, source_path: Path, dest_path: Path) -> None:
        """Copy audio file with validation.
        
        Args:
            source_path: Source audio file path
            dest_path: Destination path in DAWproject
        """
        if not source_path.exists():
            raise FileNotFoundError(f"Source audio file not found: {source_path}")
            
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        
        if not dest_path.exists():
            raise RuntimeError(f"Failed to copy audio file to {dest_path}")

    def _create_archive(self, temp_dir: Path, output_path: Path) -> None:
        """Create final ZIP archive.
        
        Args:
            temp_dir: Directory containing DAWproject contents
            output_path: Path for final .dawproject file
        """
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add project.xml
            zf.write(temp_dir / "project.xml", "project.xml")
            
            # Add metadata.xml
            zf.write(temp_dir / "metadata.xml", "metadata.xml")
            
            # Add audio files
            audio_dir = temp_dir / "audio"
            for audio_file in audio_dir.glob("*.wav"):
                zf.write(audio_file, f"audio/{audio_file.name}")