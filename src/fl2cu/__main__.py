# src/fl2cu/main.py
import argparse
import logging
import sys
from pathlib import Path

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
    
    try:
        parser = FLProjectParser(str(input_file))
        project = parser.parse_project()
        
        if not project.arrangements:
            logger.error("No arrangements found in project")
            return False

        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Fixed: Access arrangements as a property and iterate over clips properly
        clip_paths = {
            clip: clip.source_path 
            for arrangement in project.arrangements
            for clip in arrangement.clips
        }
        
        generator = DAWProjectGenerator(
            arrangements=project.arrangements,
            clip_paths=clip_paths
        )

        output_file = output_dir / f"{project.name}.dawproject"
        generator.generate_dawproject(str(output_file))
        logger.info(f"Generated: {output_file}")
        return True

    except Exception as e:
        logger.error(f"Error processing project: {e}")
        if logger.level <= logging.DEBUG:
            logger.exception("Details:")
        return False

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