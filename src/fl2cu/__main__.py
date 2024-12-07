# src/fl2cu/main.py
from pathlib import Path
import argparse
import logging
import sys

from .parser.project_parser import FLProjectParser 
from .generator.dawproject_generator import DAWProjectGenerator
from .utils.logger import setup_logger, get_logger

def setup_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    setup_logger()

def process_project(input_file: Path, output_dir: Path) -> bool:
    logger = get_logger()
    
    parser = FLProjectParser(str(input_file))
    projects = parser.parse_project()  # Returns list of projects
    
    if not projects:
        logger.error("No arrangements found in project")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each project (one per arrangement)
    for project in projects:
        if not project.arrangements:
            continue
            
        # Fixed: Store clip paths in a list instead of using clips as keys
        clip_paths = []
        for arrangement in project.arrangements:
            for track in arrangement.get_tracks():
                for clip in track.clips:
                    clip_paths.append((clip.source_path, clip))
        
        generator = DAWProjectGenerator(
            arrangements=project.arrangements,
            clip_paths=dict(clip_paths)  # Convert to dictionary using source_path as key
        )

        output_file = output_dir / f"{project.name}.dawproject"
        generator.generate_dawproject(str(output_file))
        logger.info(f"Generated: {output_file}")
    
    return True
    
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("output_dir", type=str)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    setup_logging(args.debug)
    logger = get_logger()

    try:
        input_file = Path(args.input_file).resolve()
        output_dir = Path(args.output_dir).resolve()
        
        if not input_file.exists():
            logger.error(f"Input file not found: {input_file}")
            return 1

        if not input_file.suffix.lower() == '.flp':
            logger.error("Input must be .flp file")
            return 1
            
        logger.debug(f"Processing {input_file} -> {output_dir}")
        return 0 if process_project(input_file, output_dir) else 1

    except KeyboardInterrupt:
        logger.info("\nCancelled")
        return 130
    except Exception as e:
        logger.error(f"Error: {e}")
        if logger.level <= logging.DEBUG:
            logger.exception("Details:")
        return 1

if __name__ == "__main__":
    sys.exit(main())