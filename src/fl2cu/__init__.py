# src/fl2cu/__init__.py
from pathlib import Path
from typing import Dict, Union

from .core.project_parser import FLProjectParser
from .core.audio_processor import AudioProcessor
from .core.dawproject_generator import DAWProjectGenerator
from .utils.file_manager import FileManager
from .utils.logger import setup_logger
from .models.project import Project

def parse(file: Union[str, Path]) -> Project:
    """Parse an FL Studio project file."""
    parser = FLProjectParser(str(file))
    return parser.parse_project()

def save(project: Project, output_dir: Union[str, Path]) -> Dict[str, Path]:
    """Save project to output directory."""
    # Initialize components
    output_dir = Path(output_dir)
    file_manager = FileManager(output_dir)
    audio_processor = AudioProcessor(output_dir)
    
    # Create directory structure
    arrangement_dirs = file_manager.create_directory_structure(project)
    
    # Validate audio files
    clip_paths = audio_processor.validate_audio_files(
        [clip for arr in project.arrangements for clip in arr.clips]
    )
    
    # Generate DAWproject files
    output_files = {}
    for arrangement in project.arrangements:
        arr_dir = arrangement_dirs[arrangement]
        dawproject_path = arr_dir / f"{arrangement.name}.dawproject"
        
        # Get clip paths for this arrangement
        arrangement_clips = {
            clip: path for clip, path in clip_paths.items()
            if clip in arrangement.clips
        }
        
        # Generate DAWproject
        generator = DAWProjectGenerator(arrangement, arrangement_clips)
        generator.generate_dawproject(str(dawproject_path))
        
        output_files[arrangement.name] = dawproject_path
        
    return output_files

# Set up logging on import
setup_logger()