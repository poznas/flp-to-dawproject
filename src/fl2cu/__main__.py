# src/fl2cu/__main__.py
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict

from .core.project_parser import FLProjectParser
from .core.dawproject_generator import DAWProjectGenerator
from .utils.file_manager import FileManager
from .utils.logger import setup_logger, get_logger

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert FL Studio projects to DAWproject format"
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to FL Studio project file (.flp)"
    )
    
    parser.add_argument(
        "output_dir",
        type=str,
        help="Output directory for generated files"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    return parser.parse_args()

def process_project(
    input_file: Path,
    output_dir: Path,
    debug: bool = False
) -> Dict[str, Path]:
    """Process FL Studio project and generate DAWproject files."""
    logger = get_logger()
    
    # Parse FL Studio project
    logger.debug(f"Starting to parse project file: {input_file}")
    parser = FLProjectParser(str(input_file))
    project = parser.parse_project()
    
    # Log project details
    logger.debug(f"Project name: {project.name}")
    logger.debug(f"Number of arrangements: {len(project.arrangements)}")
    for arr in project.arrangements:
        logger.debug(f"Arrangement '{arr.name}' contains {len(arr.clips)} clips")
        if debug:
            for clip in arr.clips:
                logger.debug(f"  Clip: {clip.name}")
                logger.debug(f"    Position: {clip.position}")
                logger.debug(f"    Duration: {clip.duration}")
                logger.debug(f"    Source path: {clip.source_path}")

    # Create file manager and directories
    logger.debug(f"Creating directory structure in {output_dir}")
    file_manager = FileManager(str(output_dir))
    arrangement_dirs = file_manager.create_directory_structure(project)
    logger.debug("Created directories:")
    for arr, path in arrangement_dirs.items():
        logger.debug(f"  {arr.name}: {path}")
    
    # Collect all clips
    logger.debug("Collecting clip information...")
    all_clips = []
    for arr in project.arrangements:
        logger.debug(f"Processing arrangement: {arr.name}")
        arr_clips = arr.clips
        logger.debug(f"Found {len(arr_clips)} clips in arrangement")
        all_clips.extend(arr_clips)
    
    logger.debug(f"Total clips found across all arrangements: {len(all_clips)}")
    
    # Create clip paths dictionary
    clip_paths = {}
    for clip in all_clips:
        if clip.source_path and clip.source_path.exists():
            clip_paths[clip] = clip.source_path
            logger.debug(f"Valid clip found: {clip.name} -> {clip.source_path}")
        else:
            logger.warning(f"Clip {clip.name} has invalid source path: {clip.source_path}")
    
    logger.debug(f"Valid clip paths found: {len(clip_paths)}")
    
    if not clip_paths:
        logger.error("No valid audio clips were found in the project")
        raise ValueError("No valid audio clips were found in the project")
    
    # Generate DAWproject files
    logger.info("Generating DAWproject files...")
    dawproject_paths = {}
    
    for arrangement in project.arrangements:
        try:
            logger.debug(f"Processing arrangement: {arrangement.name}")
            arr_dir = arrangement_dirs[arrangement]
            dawproject_path = arr_dir / f"{arrangement.name}.dawproject"
            
            # Get clips for this arrangement
            arrangement_clips = {
                clip: path for clip, path in clip_paths.items()
                if clip in arrangement.clips
            }
            
            logger.debug(f"Found {len(arrangement_clips)} clips for arrangement {arrangement.name}")
            
            # Generate DAWproject
            logger.debug(f"Generating DAWproject file: {dawproject_path}")
            generator = DAWProjectGenerator(arrangement, arrangement_clips)
            generator.generate_dawproject(str(dawproject_path))
            
            dawproject_paths[arrangement.name] = dawproject_path
            logger.info(f"Generated DAWproject for arrangement: {arrangement.name}")
            
        except Exception as e:
            logger.error(f"Failed to generate DAWproject for arrangement {arrangement.name}")
            logger.error(f"Error details: {str(e)}")
            if debug:
                logger.exception("Full traceback:")
            continue
    
    return dawproject_paths

def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logger()
    logger = get_logger()
    
    try:
        # Convert paths to absolute paths
        input_file = Path(args.input_file).resolve()
        output_dir = Path(args.output_dir).resolve()
        
        # Log paths in debug mode
        logger.debug(f"Input file: {input_file}")
        logger.debug(f"Input file exists: {input_file.exists()}")
        logger.debug(f"Input file size: {input_file.stat().st_size if input_file.exists() else 'N/A'}")
        logger.debug(f"Output directory: {output_dir}")
        
        # Validate input
        if not input_file.exists():
            logger.error(f"Input file not found: {input_file}")
            return 1
        
        if not input_file.suffix.lower() == '.flp':
            logger.error(f"Input file must be an FL Studio project (.flp)")
            return 1
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created/verified output directory: {output_dir}")
        
        # Process project
        dawproject_paths = process_project(
            input_file=input_file,
            output_dir=output_dir,
            debug=args.debug
        )
        
        if not dawproject_paths:
            logger.error("No DAWproject files were generated")
            return 1
        
        logger.info("Processing complete!")
        logger.info("\nGenerated DAWproject files:")
        for name, path in dawproject_paths.items():
            logger.info(f"- {name}: {path}")
            
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        return 130
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.debug:
            logger.exception("Detailed error information:")
        return 1

if __name__ == "__main__":
    sys.exit(main())