"""FL Studio to Cubase migration tool for transferring audio arrangements."""

from pathlib import Path
from typing import Union, Dict, Optional
import logging
import tempfile

from .core.project_parser import FLProjectParser
from .core.audio_processor import AudioProcessor
from .core.aaf_generator import AAFGenerator
from .models.project import Project
from .utils.file_manager import FileManager
from .utils.logger import setup_logger, get_logger
from .config import Config

def parse(file: Union[Path, str]) -> Project:
    """Parse an FL Studio project file into a Project model.
    
    Args:
        file: Path to the FL Studio project file
    
    Returns:
        Parsed Project instance
    
    Raises:
        FileNotFoundError: If project file not found
        ValueError: If project parsing fails
    """
    logger = get_logger()
    file_path = Path(file)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Project file not found: {file}")
        
    try:
        parser = FLProjectParser(str(file_path))
        project = parser.parse_project()
        logger.info(f"Successfully parsed project: {file_path.name}")
        return project
    except Exception as e:
        logger.error(f"Failed to parse project {file_path.name}: {e}")
        raise

def save(project: Project, output_dir: Union[Path, str], temp_dir: Optional[Union[Path, str]] = None) -> Dict[str, Path]:
    """Export project arrangements to AAF files with audio.
    
    Args:
        project: Project instance to export
        output_dir: Directory for output files
        temp_dir: Optional directory for temporary files (default is system temp)
    
    Returns:
        Dictionary mapping arrangement names to their AAF file paths
    
    Raises:
        ValueError: If project validation fails
        OSError: If file operations fail
    """
    logger = get_logger()
    output_dir = Path(output_dir)
    
    # Set up temporary directory
    if temp_dir:
        temp_dir = Path(temp_dir)
    else:
        temp_dir = Path(tempfile.mkdtemp())
    
    try:
        # Initialize components
        file_manager = FileManager(str(output_dir))
        audio_processor = AudioProcessor(str(temp_dir))
        
        # Validate project and paths
        project.validate()
        if not project.validate_audio_files():
            raise ValueError("Some audio files are missing")
        if not file_manager.validate_paths():
            raise OSError("Failed to validate output directories")
            
        # Create directory structure
        arrangement_dirs = file_manager.create_directory_structure(project)
        
        # Process audio files
        all_clips = [clip for arr in project.arrangements for clip in arr.clips]
        processed_clips = audio_processor.export_audio_clips(all_clips)
        
        if not processed_clips:
            raise ValueError("No audio clips were processed successfully")
            
        # Generate AAF files
        aaf_paths = {}
        for arrangement in project.arrangements:
            try:
                arr_dir = arrangement_dirs[arrangement]
                aaf_path = arr_dir / f"{arrangement.name}.aaf"
                
                # Get relevant processed clips for this arrangement
                arrangement_clips = {
                    clip: path for clip, path in processed_clips.items()
                    if clip in arrangement.clips
                }
                
                # Generate AAF
                generator = AAFGenerator(arrangement, arrangement_clips)
                generator.generate_aaf(str(aaf_path))
                
                aaf_paths[arrangement.name] = aaf_path
                logger.info(f"Generated AAF for arrangement: {arrangement.name}")
                
            except Exception as e:
                logger.error(f"Failed to generate AAF for arrangement {arrangement.name}: {e}")
                raise
                
        return aaf_paths
        
    finally:
        # Clean up temporary files
        if not temp_dir:
            file_manager.cleanup_temp_files(temp_dir)

# Initialize logger
setup_logger()