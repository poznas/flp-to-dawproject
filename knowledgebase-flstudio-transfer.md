#### .pylintrc
```
# File: .pylintrc
"""
Filepath: .pylintrc
"""
[
MASTER
]
# Python version to use for syntax checking
py-version = 3.8

# Add path to project source
init-hook='import sys; sys.path.append(".")'

# Use multiple processes to speed up Pylint
jobs=4

[MESSAGES CONTROL]
# Disable specific warnings
disable=
    C0111,  # missing-docstring
    C0103,  # invalid-name (for variables)
    R0903,  # too-few-public-methods
    R0913,  # too-many-arguments
    W0511,  # fixme (allows TODO comments)

[
FORMAT
]
# Maximum number of characters on a single line
max-line-length=100

# Expected format of line ending
expected-line-ending-format=LF

[
BASIC
]
# Regular expression which should only match function or class names
function-rgx=[a-z_][a-z0-9_]{2,50}$
class-rgx=[A-Z_][a-zA-Z0-9]+$

# Good variable names
good-names=i,j,k,ex,Run,_,fp,id

[
TYPECHECK
]
# List of module names for which member attributes should not be checked
ignored-modules=numpy,torch,tensorflow
```
---

#### README.md
# FL Studio to Cubase Migration Tool
A Python-based tool for transferring audio arrangements between FL Studio and Cubase while preserving clip positions, colors, and organization.

## Features
- Maintains precise clip positions and timing 
- Preserves color coding and visual organization
- Supports multiple arrangements with folder structure
- Handles large projects (~1000 clips) efficiently
- Automates the export/import process
- Preserves audio quality during transfer

## Requirements
- Python 3.8+
- FL Studio project files (.flp)
- Cubase Pro 14+ (for importing)

## Installation

### Development Setup
```batch
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt

# Install package in editable mode
pip install -e .
```

### Dependencies
Core dependencies are installed automatically:
- pyflp>=2.0.0 - FL Studio project parsing
- pyaaf2>=1.7.0 - AAF file handling
- construct>=2.10.0 - Binary data parsing
- wave>=0.0.2 - WAV file processing
- numpy>=1.21.0 - Audio data manipulation

## Usage

### Basic Usage
```python

# Parse FL Studio project
project = fl2cu.parse("path/to/project.flp")

# Export to AAF files
output_files = fl2cu.save(project, "path/to/output")
```

### Output Structure
```
output/
  ├── NAGRYWKI_MAIN/
  │   ├── audio_files/
  │   └── arrangement.aaf
  ├── NAGRYWKI_CHOREK/
  │   ├── audio_files/
  │   └── arrangement.aaf
  └── ...
```

## Development

### Running Tests
```batch
# Run all tests
pytest

# Run specific test file
pytest tests/test_project_parser.py

# Run with coverage report
pytest --cov=src
```

### Project Structure
```
flstudio_cubase_migration/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── project_parser.py     # FL Studio project parsing logic
│   │   ├── audio_processor.py    # Audio file handling and processing
│   │   └── aaf_generator.py      # AAF file generation and manipulation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py           # Project data structures
│   │   ├── arrangement.py       # Arrangement-specific models
│   │   └── clip.py             # Audio clip data models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_manager.py     # File system operations
│   │   └── logger.py           # Logging configuration
│   └── config.py               # Global configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # PyTest configuration and shared fixtures
│   ├── test_project_parser.py  # Project parsing tests
│   ├── test_audio_processor.py # Audio processing tests
│   ├── test_aaf_generator.py   # AAF generation tests
│   ├── test_models.py         # Data model tests
│   ├── test_file_manager.py   # File system operation tests
│   ├── integration/
│   │   └── test_full_workflow.py # End-to-end workflow tests
│   └── fixtures/               # Test data and mock files
│       ├── README.md          # Fixtures documentation
│       ├── sample_project.flp
│       ├── audio_clips/
│       │   ├── clip1.wav
│       │   └── clip2.wav
│       └── expected_output/
│           └── expected_arrangement.aaf
├── examples/
│   └── sample_project/        # Example project files
├── docs/
│   └── api_reference.md       # API documentation
├── requirements.txt           # Project dependencies
├── dev-requirements.txt       # Development dependencies
├── setup.py                  # Installation configuration
├── pytest.ini               # Test configuration
├── .pylintrc               # Pylint configuration
├── mypy.ini                # Type checking configuration
└── pyproject.toml         # Code formatting and build configuration
```

## Known Limitations
- Cubase's limited AAF color support requires initial setup
- FL Studio's project format limitations (see PyFLP documentation)
- Large projects should be processed in chunks (~1000 clips per arrangement)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
---

#### dev-requirements.txt
```
# Code quality
black==23.11.0        # Code formatting
pylint==3.0.2         # Static code analysis
mypy==1.7.0           # Type checking
isort==5.12.0         # Import sorting
pre-commit==3.5.0     # Pre-commit hooks

# Testing
pytest>=7.4.3
pytest-cov>=4.1.0

# Type checking
types-tqdm>=4.65.0    # Type stubs for tqdm
types-setuptools>=68.0.0  # Type stubs for setuptools

# Documentation
sphinx>=7.1.0         # Documentation generation
sphinx-rtd-theme>=2.0.0  # Documentation theme
```
---

#### docs\api_reference.md
# FL Studio to Cubase Migration Tool API Reference

## Core Functions

### Project Parsing

```python
from flstudio_cubase_migration import parse

# Parse FL Studio project
project = parse("path/to/project.flp")
```

### Project Export

```python
from flstudio_cubase_migration import save

# Save project as AAF files
save(project, output_dir="path/to/output")
```

## Models

### Project

Represents an FL Studio project with multiple arrangements.

```python
from flstudio_cubase_migration.models import Project

# Access project properties
print(project.name)
print(len(project.arrangements))

# Validate project
project.validate()
```

#### Methods

- `add_arrangement(arrangement)`: Add an arrangement to the project
- `remove_arrangement(arrangement)`: Remove an arrangement
- `get_arrangement_by_name(name)`: Find arrangement by name
- `validate()`: Validate project structure
- `validate_audio_files()`: Check if all referenced audio files exist

### Arrangement

Represents a collection of audio clips with shared organization.

```python
from flstudio_cubase_migration.models import Arrangement

# Create new arrangement
arrangement = Arrangement(name="NAGRYWKI_MAIN")

# Work with clips
arrangement.add_clip(clip)
arrangement.get_clip_by_name("vocal_01")
print(arrangement.get_duration())
```

#### Methods

- `add_clip(clip)`: Add a clip to the arrangement
- `remove_clip(clip)`: Remove a clip
- `get_clip_by_name(name)`: Find clip by name
- `get_duration()`: Get total arrangement duration
- `validate()`: Validate arrangement structure
- `get_clips_in_time_range(start, end)`: Get clips within time range

### Clip

Represents an individual audio clip with position and properties.

```python
from flstudio_cubase_migration.models import Clip

# Create new clip
clip = Clip(
    name="vocal_01",
    position=0.0,
    duration=4.0,
    color="#FF0000",
    source_path="path/to/audio.wav",
    volume=1.0
)
```

#### Properties

- `name`: Clip name (string)
- `position`: Time position in seconds (float)
- `duration`: Duration in seconds (float)
- `color`: Color in hex format (#RRGGBB)
- `source_path`: Path to source audio file (Path)
- `volume`: Volume multiplier (float)
- `muted`: Mute state (boolean)

#### Methods

- `validate()`: Validate clip properties
- `to_dict()`: Convert to dictionary format
- `from_dict(data)`: Create from dictionary data

## Processing Components

### AudioProcessor

Handles audio file operations and quality preservation.

```python
from flstudio_cubase_migration.core import AudioProcessor

processor = AudioProcessor("path/to/output")
exported_paths = processor.export_audio_clips(clips)
```

#### Methods

- `export_audio_clips(clips, max_workers=None)`: Export audio clips maintaining quality
- `validate_audio_files(clips)`: Validate exported audio files

### AAFGenerator

Generates AAF files for Cubase import.

```python
from flstudio_cubase_migration.core import AAFGenerator

generator = AAFGenerator(arrangement, audio_file_map)
generator.generate_aaf("output.aaf")
```

#### Methods

- `generate_aaf(output_path)`: Generate AAF file with audio references

## Utility Functions

### FileManager

Handles file system operations and directory structure.

```python
from flstudio_cubase_migration.utils import FileManager

manager = FileManager("path/to/output")
arrangement_dirs = manager.create_directory_structure(project)
```

#### Methods

- `create_directory_structure(project)`: Create output directory structure
- `cleanup_temp_files()`: Clean up temporary files
- `validate_paths()`: Validate required paths exist

## Error Handling

All components raise appropriate exceptions for error conditions:

- `FileNotFoundError`: Missing files
- `ValueError`: Invalid parameters or data
- `OSError`: File system operation failures

Example error handling:

```python
try:
    project = parse("project.flp")
    save(project, "output")
except FileNotFoundError as e:
    print(f"Missing file: {e}")
except ValueError as e:
    print(f"Invalid data: {e}")
except OSError as e:
    print(f"Operation failed: {e}")
```

## Best Practices

1. Always validate projects before export:
```python
project = parse("project.flp")
project.validate()
if not project.validate_audio_files():
    print("Warning: Some audio files are missing")
```

2. Use parallel processing for large projects:
```python
processor = AudioProcessor("output")
processor.export_audio_clips(clips, max_workers=4)
```

3. Clean up temporary files:
```python
manager = FileManager("output")
try:
    # Process files...
finally:
    manager.cleanup_temp_files()
```

4. Handle large arrangements efficiently:
```python
for arrangement in project.arrangements:
    # Process one arrangement at a time
    result = processor.export_audio_clips(arrangement.clips)
    generator.generate_aaf(f"{arrangement.name}.aaf")
```
---

#### master-plan.md
# FL Studio to Cubase Migration Tool

## Overview
A Python-based tool to accurately transfer audio arrangements from FL Studio to Cubase while preserving clip positions, colors, and organization across multiple arrangements.

## Objectives
- Maintain precise clip positions and timing
- Preserve color coding for visual organization
- Support multiple arrangements with folder structure
- Automate the export/import process to minimize manual work
- Handle large projects (~1000 clips) efficiently

## Technical Stack
- Core: Python 3.8+
- FL Studio Project Parsing: PyFLP library
- Audio Processing: Direct file operations
- Export Format: AAF (Advanced Authoring Format)
- Project Structure: Directory-based with arrangement folders

## Core Features

### 1. FL Studio Project Parsing
- Parse .flp files using PyFLP
- Extract clip metadata:
  - Position information
  - Color coding
  - Names (simplified to last component)
  - Length/duration
  - Arrangement association

### 2. Audio Export System
- Batch audio file export
- Maintain original audio quality
- Preserve exact clip boundaries
- Support for multiple arrangements

### 3. AAF Generation
- Create AAF files containing:
  - Clip positions
  - Color information
  - Track organization
  - Timing metadata
- One AAF file per arrangement

### 4. File Organization
- Create organized folder structure:
```
output/
  ├── NAGRYWKI_MAIN/
  │   ├── audio_files/
  │   └── arrangement.aaf
  ├── NAGRYWKI_CHOREK_VERSE_2/
  │   ├── audio_files/
  │   └── arrangement.aaf
  └── ...
```

## Development Phases

### Phase 1: Core Infrastructure
1. Set up PyFLP project parsing
2. Implement basic audio file extraction
3. Create folder structure management
4. Add logging and error handling

### Phase 2: AAF Generation
1. Implement AAF metadata generation
2. Add clip position mapping
3. Integrate color preservation
4. Create track organization structure

### Phase 3: Optimization & Testing
1. Optimize for large projects
2. Add progress reporting
3. Implement error recovery
4. Test with various project sizes

### Phase 4: Bi-directional Integration
1. FL Studio to Cubase:
   - Test audio export structure
   - Verify position accuracy
   - Validate color preservation
   - Test arrangement organization

2. Cubase back to FL Studio:
   - Parse Cubase project structure
   - Extract modified clip positions
   - Capture any color/organization changes
   - Support reimporting into FL Studio project
   
3. Round-trip Workflow Support:
   - Track version history
   - Maintain clip relationships
   - Handle new clips created in Cubase
   - Preserve both DAWs' specific metadata

## Technical Considerations

### Performance
- Batch processing for large projects
- Efficient memory usage for 1000+ clips
- Progress tracking for long operations

### Error Handling
- Validate FL Studio project structure
- Check for missing audio files
- Handle corrupt project files
- Provide clear error messages

### Compatibility
- Support FL Studio 20.8+ project format
- Compatible with Cubase Pro 14
- Handle various audio formats

## Future Expansion Possibilities
1. GUI interface for easier operation
2. Additional export formats (OMF, EDL)
3. Custom naming scheme configuration
4. Batch project processing
5. Integration with other DAWs

## Known Limitations
1. Cubase's limited AAF color support requires initial setup
2. No native FL Studio API access
3. Need to handle large project sizes carefully

## Usage Instructions
[To be developed based on implementation]
---

#### mypy.ini
```
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True

# Per-module options
[mypy.plugins.numpy.*]
ignore_missing_imports = True

[mypy-pyflp.*]
ignore_missing_imports = True
```
---

#### pyproject.toml
```
[build-system]
requires = ["setuptools>=45", "wheel", "pip>=21"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
# A regex preceded with ^/ will apply only to files and directories
# in the root of the project.
^/tests/fixtures/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
```
---

#### pytest.ini
```
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test
python_functions = test_*
addopts = -v --strict-markers
markers =
    integration: marks tests as integration tests
    slow: marks tests as slow running
```
---

#### requirements.txt
```
# Core dependencies
pyflp>=2.0.0      # FL Studio project file parsing
construct>=2.10.0  # Binary data parsing for AAF generation
pyaaf2>=1.7.0     # AAF file reading/writing
sortedcontainers>=2.4.0  # Required by pyflp

# Audio processing
wave>=0.0.2       # WAV file reading/writing
numpy>=1.21.0     # Audio data manipulation

# Utility libraries
tqdm>=4.65.0      # Progress bars for long operations
pathlib>=1.0.1    # Path manipulation (stdlib for Python 3.8+)
typing-extensions>=4.5.0  # Enhanced type hints for Python 3.8
```
---

#### setup.py
```
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

with open("dev-requirements.txt", "r", encoding="utf-8") as fh:
    dev_requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="flstudio-cubase-migration",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Tool for transferring audio arrangements between FL Studio and Cubase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flstudio-cubase-migration",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
    },
    entry_points={
        "console_scripts": [
            "fl2cubase=flstudio_cubase_migration.core.project_parser:main",
        ],
    },
)
```
---

#### src\__init__.py
```
"""FL Studio to Cubase migration tool for transferring audio arrangements."""

from pathlib import Path
from typing import Union, Dict, Optional

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
```
---

#### src\config.py
```
# File: src/config.py
"""
Global configuration settings.

Filepath: src/config.py
"""
from pathlib import Path
from typing import Dict, List, Any

class Config:
    """Global configuration settings for FL Studio to Cubase migration"""
    
    # File system settings
    DEFAULT_OUTPUT_DIR: Path = Path('./output')
    TEMP_DIR: Path = Path('./temp')
    
    # Audio settings
    SUPPORTED_AUDIO_FORMATS: List[str] = ['.wav']
    MAX_AUDIO_CHANNELS: int = 2
    SAMPLE_RATE: int = 44100
    BIT_DEPTH: int = 24
    
    # Project constraints
    MAX_CLIPS_PER_ARRANGEMENT: int = 1000
    MAX_ARRANGEMENTS: int = 50
    
    # Version requirements
    MIN_FL_STUDIO_VERSION: str = '20.8.0'
    MIN_CUBASE_VERSION: str = '14.0.0'
    
    # AAF settings
    AAF_VERSION: str = '1.1'
    SUPPORTED_COLOR_FORMATS: List[str] = ['RGB', 'HEX']
    
    # Performance settings
    BATCH_SIZE: int = 100  # Number of clips to process at once
    MAX_PARALLEL_EXPORTS: int = 4
    
    def get_output_dir(cls, project_name: str) -> Path:
        """Get project-specific output directory"""
        return cls.DEFAULT_OUTPUT_DIR / project_name
    
    def get_temp_dir(cls, project_name: str) -> Path:
        """Get project-specific temporary directory"""
        return cls.TEMP_DIR / project_name
    
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization"""
        return {
            name: value for name, value in vars(cls).items()
            if not name.startswith('_') and name.isupper()
        }
```
---

#### src\core\__init__.py
```
"""Core package for FL Studio to Cubase migration tool."""

from .project_parser import FLProjectParser
from .audio_processor import AudioProcessor
from .aaf_generator import AAFGenerator

__all__ = ['FLProjectParser', 'AudioProcessor', 'AAFGenerator']
```
---

#### src\core\aaf_generator.py
```
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.arrangement import Arrangement
    from ..models.clip import Clip

class AAFGenerator:
    """Generates AAF files for Cubase import with clip positions and metadata."""
    
    def __init__(self, arrangement: "Arrangement", audio_file_map: Dict["Clip", Path]):
        """Initialize AAF generator.
        
        Args:
            arrangement: Arrangement to process
            audio_file_map: Mapping of clips to their exported audio file paths
        """
        self.arrangement = arrangement
        self.audio_file_map = {
            hash(clip): path for clip, path in audio_file_map.items()
        }  # Store using clip hashes since Clip is now immutable
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
    def generate_aaf(self, output_path: str) -> None:
        """Generate AAF file for arrangement.
        
        Args:
            output_path: Path where AAF file should be created
            
        Raises:
            FileNotFoundError: If audio files are missing
            OSError: If AAF generation fails
        """
        output_path = Path(output_path)
        
        try:
            with aaf2.open(str(output_path), 'w') as f:
                # Create main composition
                main_composition = f.create.MasterMob(self.arrangement.name)
                f.content.mobs.append(main_composition)
                
                # Set basic project properties
                edit_rate = 25  # Standard frame rate 
                
                # Create tape source (for timecode)
                tape_mob = f.create.SourceMob()
                f.content.mobs.append(tape_mob)
                timecode_rate = 25
                start_time = 0
                
                # Add tape slots
                tape_mob.create_tape_slots(
                    "Master", 
                    edit_rate,
                    timecode_rate, 
                    media_kind='picture'
                )
                
                # Process each clip in the arrangement
                for clip in sorted(self.arrangement.clips, key=lambda x: x.position):
                    self._add_clip_to_composition(f, main_composition, clip, edit_rate)
                    
                self.logger.info(f"Generated AAF file at {output_path}")
                    
        except Exception as e:
            self.logger.error(f"Failed to generate AAF file: {e}")
            raise
            
    def _add_clip_to_composition(self, f: "aaf2.File", composition: "aaf2.MasterMob", 
                               clip: "Clip", edit_rate: int) -> None:
        """Add a clip to the AAF composition."""
        try:
            # Get the exported audio file path using clip hash
            audio_path = self.audio_file_map.get(hash(clip))
            if not audio_path or not audio_path.exists():
                self.logger.warning(f"Audio file not found for clip {clip.name}, skipping")
                return
                
            # Create source mob for the audio file
            source_mob = f.create.SourceMob()
            f.content.mobs.append(source_mob)
            
            # Import the audio essence
            source_mob.import_audio_essence(
                str(audio_path),
                edit_rate
            )
            
            # Calculate position and length in edit rate units
            position_frames = int(clip.position * edit_rate)
            length_frames = int(clip.duration * edit_rate)
            
            # Create the clip reference
            clip_slot = source_mob.create_source_clip(1, position_frames)
            clip_slot.length = length_frames
            
            # Set clip metadata if supported by AAF version
            try:
                if hasattr(clip_slot, 'user_comments'):
                    clip_slot.user_comments['Name'] = clip.name
                    clip_slot.user_comments['Color'] = clip.color
                    if clip.muted:
                        clip_slot.user_comments['Muted'] = 'true'
            except Exception as e:
                self.logger.warning(f"Failed to set clip metadata: {e}")
                
            # Apply volume if different from default
            if clip.volume != 1.0:
                try:
                    clip_slot.volume = clip.volume
                except Exception as e:
                    self.logger.warning(f"Failed to set clip volume: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to add clip {clip.name} to AAF: {e}")
            raise
```
---

#### src\core\audio_processor.py
```
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor

from ..models.clip import Clip
from ..utils.logger import get_logger
from ..config import Config

class AudioProcessor:
    """Handles audio file operations including export and quality preservation."""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.logger = get_logger()
        self.config = Config()
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def export_audio_clips(self, clips: List[Clip], max_workers: Optional[int] = None) -> Dict[Clip, Path]:
        """Export audio clips while preserving quality.
        Returns a dictionary mapping clips to their exported file paths."""
        
        result: Dict[Clip, Path] = {}
        failed_clips = []
        max_workers = max_workers or self.config.MAX_PARALLEL_EXPORTS

        # Process clips in parallel for better performance
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_clip = {
                executor.submit(self._process_clip, clip): clip 
                for clip in clips 
                if clip.source_path and clip.source_path.exists()
            }
            
            for future in future_to_clip:
                clip = future_to_clip[future]
                try:
                    output_path = future.result()
                    if output_path:
                        result[clip] = output_path
                    else:
                        failed_clips.append(clip)
                except Exception as e:
                    self.logger.error(f"Failed to process clip {clip.name}: {e}")
                    failed_clips.append(clip)

        if failed_clips:
            self.logger.warning(f"Failed to process {len(failed_clips)} clips")
            
        return result
        
    def _process_clip(self, clip: Clip) -> Optional[Path]:
        """Process a single audio clip."""
        try:
            source_path = clip.source_path
            if not source_path or not source_path.exists():
                raise FileNotFoundError(f"Source file not found: {source_path}")

            # Create unique output path
            output_path = self.output_dir / f"{clip.name}_{clip.source_path.stem}.wav"
            i = 1
            while output_path.exists():
                output_path = self.output_dir / f"{clip.name}_{clip.source_path.stem}_{i}.wav"
                i += 1

            # For WAV files, we can optimize by copying if no processing is needed
            if source_path.suffix.lower() == '.wav' and clip.volume == 1.0 and not clip.muted:
                shutil.copy2(source_path, output_path)
                self.logger.debug(f"Copied {clip.name} to {output_path}")
                return output_path

            # Otherwise, process the audio data
            with wave.open(str(source_path), 'rb') as wav_in:
                params = wav_in.getparams()
                frames = wav_in.readframes(wav_in.getnframes())

                if clip.volume != 1.0 or clip.muted:
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                    volume = 0.0 if clip.muted else clip.volume
                    audio_data = (audio_data * volume).astype(np.int16)
                    frames = audio_data.tobytes()

                with wave.open(str(output_path), 'wb') as wav_out:
                    wav_out.setparams(params)
                    wav_out.writeframes(frames)

            self.logger.debug(f"Processed {clip.name} to {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"Error processing clip {clip.name}: {e}")
            return None

    def validate_audio_files(self, clips: List[Clip]) -> bool:
        """Validate all audio files in the output directory."""
        all_valid = True
        
        for clip in clips:
            if not clip.source_path:
                self.logger.error(f"No source path for clip {clip.name}")
                all_valid = False
                continue

            try:
                with wave.open(str(clip.source_path), 'rb') as wav:
                    if wav.getnframes() == 0:
                        self.logger.error(f"Empty audio file for clip {clip.name}")
                        all_valid = False
            except Exception as e:
                self.logger.error(f"Invalid audio file for clip {clip.name}: {e}")
                all_valid = False
                
        return all_valid
```
---

#### src\core\project_parser.py
```
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..models.project import Project
from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..utils.logger import get_logger

class FLProjectParser:
    """Handles parsing of FL Studio project files using PyFLP library."""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.logger = get_logger()
        
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project file not found: {project_path}")
            
        try:
            self.fl_project = pyflp.parse(str(self.project_path))
            self.logger.info(f"Successfully opened FL Studio project: {self.project_path.name}")
        except Exception as e:
            self.logger.error(f"Failed to parse FL Studio project: {e}")
            raise
            
    def parse_project(self) -> Project:
        """Parse FL Studio project and extract metadata."""
        project = Project(
            name=self.project_path.stem,
            source_path=self.project_path
        )
        
        try:
            # Parse arrangements
            arrangements = self.extract_arrangements()
            for arrangement in arrangements:
                project.add_arrangement(arrangement)
                
            self.logger.info(f"Parsed {len(arrangements)} arrangements")
            return project
            
        except Exception as e:
            self.logger.error(f"Error parsing project: {e}")
            raise
            
    def extract_arrangements(self) -> List[Arrangement]:
        """Extract arrangement information from FL Studio project."""
        arrangements = []

        try:
            # Get playlist tracks
            playlist_tracks = self.fl_project.tracks if hasattr(self.fl_project, 'tracks') else []
            
            # Create default arrangement
            default_arrangement = Arrangement(name="Main")
            arrangements.append(default_arrangement)

            # Process each channel
            for channel in self.fl_project.channels.samplers:
                if not channel.sample_path:
                    continue

                # Get patterns containing this channel
                patterns = []
                if hasattr(channel, 'patterns'):
                    patterns = channel.patterns
                elif hasattr(channel, 'pattern'):
                    patterns = [channel.pattern] if channel.pattern else []

                # Calculate position based on pattern placement
                for pattern_idx in patterns:
                    # Try to find pattern in playlist
                    position = 0.0
                    for track in playlist_tracks:
                        for item in track.items:
                            if item.pattern == pattern_idx:
                                position = self._ticks_to_seconds(item.position)
                                break

                    # Create clip
                    clip = Clip(
                        name=channel.name or Path(channel.sample_path).stem,
                        position=position,
                        duration=self._ticks_to_seconds(channel.length if hasattr(channel, 'length') else 0),
                        color=f"#{channel.color:06x}" if hasattr(channel, 'color') and channel.color else "#808080",
                        source_path=Path(channel.sample_path),
                        volume=channel.volume if hasattr(channel, 'volume') else 1.0,
                        muted=channel.muted if hasattr(channel, 'muted') else False
                    )

                    # Add to appropriate arrangement
                    if hasattr(channel, 'group') and channel.group:
                        arrangement = self._get_or_create_arrangement(arrangements, str(channel.group))
                    else:
                        arrangement = default_arrangement
                    arrangement.add_clip(clip)

            return arrangements

        except Exception as e:
            self.logger.error(f"Error extracting arrangements: {e}")
            raise

    def _ticks_to_seconds(self, ticks: int) -> float:
        """Convert FL Studio ticks to seconds."""
        if not hasattr(self.fl_project, 'ppq') or not hasattr(self.fl_project, 'tempo'):
            return 0.0
            
        ticks_per_second = self.fl_project.ppq * (self.fl_project.tempo / 60.0)
        return ticks / ticks_per_second if ticks_per_second > 0 else 0.0

    def _get_or_create_arrangement(self, arrangements: List[Arrangement], name: str) -> Arrangement:
        """Get existing arrangement or create new one."""
        for arrangement in arrangements:
            if arrangement.name == name:
                return arrangement
                
        new_arrangement = Arrangement(name=name)
        arrangements.append(new_arrangement)
        return new_arrangement

    def _get_arrangement_name(self, channel: Any) -> str:
        """Determine arrangement name from channel properties."""
        if hasattr(channel, 'group') and channel.group:
            return str(channel.group)
            
        if hasattr(channel, 'pattern') and channel.pattern:
            return f"Pattern_{channel.pattern}"
            
        return "Main"
```
---

#### src\flstudio_cubase_migration.egg-info\PKG-INFO
```
Metadata-Version: 2.1
Name: flstudio-cubase-migration
Version: 0.1.0
Summary: Tool for transferring audio arrangements between FL Studio and Cubase
Home-page: https://github.com/yourusername/flstudio-cubase-migration
Author: Your Name
Author-email: your.email@example.com
Classifier: Development Status :: 3 - Alpha
Classifier: Intended Audience :: End Users/Desktop
Classifier: Topic :: Multimedia :: Sound/Audio
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.8
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Requires-Python: >=3.8
Description-Content-Type: text/markdown
Requires-Dist: pyflp>=2.0.0
Requires-Dist: construct>=2.10.0
Requires-Dist: pyaaf2>=1.7.0
Requires-Dist: sortedcontainers>=2.4.0
Requires-Dist: wave>=0.0.2
Requires-Dist: numpy>=1.21.0
Requires-Dist: tqdm>=4.65.0
Requires-Dist: pathlib>=1.0.1
Requires-Dist: typing-extensions>=4.5.0
Provides-Extra: dev
Requires-Dist: black==23.11.0; extra == "dev"
Requires-Dist: pylint==3.0.2; extra == "dev"
Requires-Dist: mypy==1.7.0; extra == "dev"
Requires-Dist: isort==5.12.0; extra == "dev"
Requires-Dist: pre-commit==3.5.0; extra == "dev"
Requires-Dist: pytest>=7.4.3; extra == "dev"
Requires-Dist: pytest-cov>=4.1.0; extra == "dev"
Requires-Dist: types-tqdm>=4.65.0; extra == "dev"
Requires-Dist: types-setuptools>=68.0.0; extra == "dev"
Requires-Dist: sphinx>=7.1.0; extra == "dev"
Requires-Dist: sphinx-rtd-theme>=2.0.0; extra == "dev"

# File: README.md
# FL Studio to Cubase Migration Tool
A Python-based tool for transferring audio arrangements between FL Studio and Cubase while preserving clip positions, colors, and organization.

## Installation
[TODO: Add installation instructions]

## Usage
[TODO: Add usage instructions]

## Project Structure


flstudio_cubase_migration/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── project_parser.py     # FL Studio project parsing logic
│   │   ├── audio_processor.py    # Audio file handling and processing
│   │   └── aaf_generator.py      # AAF file generation and manipulation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py           # Project data structures
│   │   ├── arrangement.py       # Arrangement-specific models
│   │   └── clip.py             # Audio clip data models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_manager.py     # File system operations
│   │   └── logger.py           # Logging configuration
│   └── config.py               # Global configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # PyTest configuration and shared fixtures
│   ├── test_project_parser.py  # Project parsing tests
│   ├── test_audio_processor.py # Audio processing tests
│   ├── test_aaf_generator.py   # AAF generation tests
│   ├── test_models.py         # Data model tests
│   ├── test_file_manager.py   # File system operation tests
│   ├── integration/
│   │   └── test_full_workflow.py # End-to-end workflow tests
│   └── fixtures/               # Test data and mock files
│       ├── README.md          # Fixtures documentation
│       ├── sample_project.flp
│       ├── audio_clips/
│       │   ├── clip1.wav
│       │   └── clip2.wav
│       └── expected_output/
│           └── expected_arrangement.aaf
├── examples/
│   └── sample_project/        # Example project files
├── docs/
│   └── api_reference.md       # API documentation
├── requirements.txt           # Project dependencies
├── dev-requirements.txt     # Development dependencies
├── setup.py                 # Installation configuration
├── pytest.ini              # Test configuration
├── .pylintrc              # Pylint configuration
├── mypy.ini               # Type checking configuration
└── pyproject.toml         # Code formatting and build configuration
```
---

#### src\flstudio_cubase_migration.egg-info\SOURCES.txt
```
README.md
pyproject.toml
setup.py
src/core/__init__.py
src/core/aaf_generator.py
src/core/audio_processor.py
src/core/project_parser.py
src/flstudio_cubase_migration.egg-info/PKG-INFO
src/flstudio_cubase_migration.egg-info/SOURCES.txt
src/flstudio_cubase_migration.egg-info/dependency_links.txt
src/flstudio_cubase_migration.egg-info/entry_points.txt
src/flstudio_cubase_migration.egg-info/requires.txt
src/flstudio_cubase_migration.egg-info/top_level.txt
src/models/__init__.py
src/models/arrangement.py
src/models/clip.py
src/models/project.py
src/utils/__init__.py
src/utils/file_manager.py
src/utils/logger.py
tests/test_aaf_generator.py
tests/test_audio_processor.py
tests/test_file_manager.py
tests/test_models.py
tests/test_project_parser.py
```
---

#### src\flstudio_cubase_migration.egg-info\dependency_links.txt
```

```
---

#### src\flstudio_cubase_migration.egg-info\entry_points.txt
```
[console_scripts]
fl2cubase = flstudio_cubase_migration.core.project_parser:main
```
---

#### src\flstudio_cubase_migration.egg-info\requires.txt
```
pyflp>=2.0.0
construct>=2.10.0
pyaaf2>=1.7.0
sortedcontainers>=2.4.0
wave>=0.0.2
numpy>=1.21.0
tqdm>=4.65.0
pathlib>=1.0.1
typing-extensions>=4.5.0

[dev]
black==23.11.0
pylint==3.0.2
mypy==1.7.0
isort==5.12.0
pre-commit==3.5.0
pytest>=7.4.3
pytest-cov>=4.1.0
types-tqdm>=4.65.0
types-setuptools>=68.0.0
sphinx>=7.1.0
sphinx-rtd-theme>=2.0.0
```
---

#### src\flstudio_cubase_migration.egg-info\top_level.txt
```
core
models
utils
```
---

#### src\models\__init__.py
```
"""Models package for FL Studio to Cubase migration tool.

This package contains the core data models used to represent FL Studio projects,
arrangements, and clips during the migration process.
"""

from .clip import Clip
from .arrangement import Arrangement
from .project import Project

__all__ = ['Clip', 'Arrangement', 'Project']
```
---

#### src\models\arrangement.py
```
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path

from .clip import Clip

class Arrangement:
    """Represents an arrangement containing multiple audio clips."""
    
    name: str
    clips: List[Clip] = field(default_factory=list)
    folder_path: Optional[Path] = None
    
    def add_clip(self, clip: Clip) -> None:
        """Add a clip to the arrangement."""
        # Since Clip is now immutable, we need to create a new one with the arrangement name
        new_clip = Clip(
            name=clip.name,
            position=clip.position,
            duration=clip.duration,
            color=clip.color,
            source_path=clip.source_path,
            volume=clip.volume,
            muted=clip.muted,
            arrangement_name=self.name
        )
        self.clips.append(new_clip)
        
    def remove_clip(self, clip: Clip) -> None:
        """Remove a clip from the arrangement."""
        self.clips = [c for c in self.clips if c != clip]
            
    def get_clip_by_name(self, name: str) -> Optional[Clip]:
        """Find a clip by its name."""
        for clip in self.clips:
            if clip.name == name:
                return clip
        return None
        
    def get_duration(self) -> float:
        """Get total arrangement duration based on clip positions."""
        if not self.clips:
            return 0.0
            
        # Calculate end time for each clip (position + duration)
        end_times = [clip.position + clip.duration for clip in self.clips]
        return max(end_times) if end_times else 0.0
    
    def validate(self) -> None:
        """Validate arrangement and all its clips."""
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")
            
        # Validate each clip
        for clip in self.clips:
            # Clip is now validated on creation due to dataclass post_init
            
            # Verify clip belongs to this arrangement
            if clip.arrangement_name != self.name:
                raise ValueError(f"Clip {clip.name} has incorrect arrangement assignment")
            
        # Check for clip name uniqueness
        names = [clip.name for clip in self.clips]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate clip names are not allowed")
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert arrangement to dictionary format for serialization."""
        return {
            'name': self.name,
            'folder_path': str(self.folder_path) if self.folder_path else None,
            'clips': [clip.__dict__ for clip in self.clips]
        }
    
    def from_dict(cls, data: Dict[str, Any]) -> 'Arrangement':
        """Create arrangement instance from dictionary data."""
        folder_path = Path(data['folder_path']) if data.get('folder_path') else None
        
        arrangement = cls(
            name=data['name'],
            folder_path=folder_path
        )
        
        # Add clips
        for clip_data in data.get('clips', []):
            clip = Clip(
                name=clip_data['name'],
                position=clip_data['position'],
                duration=clip_data['duration'],
                color=clip_data['color'],
                source_path=Path(clip_data['source_path']) if clip_data.get('source_path') else None,
                volume=clip_data.get('volume', 1.0),
                muted=clip_data.get('muted', False),
                arrangement_name=clip_data.get('arrangement_name')
            )
            arrangement.add_clip(clip)
            
        return arrangement
```
---

#### src\models\clip.py
```
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

class Clip:
    """Represents an audio clip with position, duration and color information."""
    
    # Required fields
    name: str
    position: float  # Position in seconds
    duration: float  # Duration in seconds 
    color: str      # Color in hex format (#RRGGBB)
    
    # Optional fields with defaults
    source_path: Optional[Path] = None
    volume: float = 1.0
    muted: bool = False
    arrangement_name: Optional[str] = None
    
    # Internal state
    _metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate clip attributes after initialization."""
        # Sanitize name (convert spaces to underscores)
        object.__setattr__(self, 'name', self.name.replace(' ', '_'))
        
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")

    def __hash__(self):
        """Make clip hashable based on its attributes."""
        return hash((self.name, self.position, self.duration, self.color, 
                    str(self.source_path), self.volume, self.muted))

    def validate(self) -> None:
        """Validate clip attributes."""
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
        if self.volume < 0:
            raise ValueError("Volume cannot be negative")
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert clip to dictionary format for serialization."""
        return {
            'name': self.name,
            'position': self.position,
            'duration': self.duration,
            'color': self.color,
            'source_path': str(self.source_path) if self.source_path else None,
            'volume': self.volume,
            'muted': self.muted,
            'arrangement_name': self.arrangement_name,
            'metadata': self._metadata
        }
    
    def from_dict(cls, data: Dict[str, Any]) -> 'Clip':
        """Create clip instance from dictionary data."""
        source_path = Path(data['source_path']) if data.get('source_path') else None
        metadata = data.get('metadata', {})
        
        clip = cls(
            name=data['name'],
            position=float(data['position']),
            duration=float(data['duration']), 
            color=data['color'],
            source_path=source_path,
            volume=float(data.get('volume', 1.0)),
            muted=bool(data.get('muted', False)),
            arrangement_name=data.get('arrangement_name')
        )
        clip._metadata = metadata
        return clip
        
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self._metadata.get(key, default)
        
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value for key."""
        self._metadata[key] = value
```
---

#### src\models\project.py
```
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from .arrangement import Arrangement

class Project:
    """Represents an FL Studio project with multiple arrangements."""
    
    def __init__(self, name: str, arrangements: Optional[List[Arrangement]] = None, 
                 source_path: Optional[Path] = None, output_dir: Optional[Path] = None):
        """Initialize project instance."""
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
        if not name:
            raise ValueError("Project name cannot be empty")
            
        self.name = name.strip()
        self.arrangements = arrangements or []
        self.source_path = source_path
        self.output_dir = output_dir
        
        # Initial validation
        self.validate()
        
    def add_arrangement(self, arrangement: Arrangement) -> None:
        """Add an arrangement to the project."""
        if self.get_arrangement_by_name(arrangement.name):
            raise ValueError(f"Arrangement with name '{arrangement.name}' already exists")
            
        # Validate arrangement before adding
        arrangement.validate()
        self.arrangements.append(arrangement)
        
    def remove_arrangement(self, arrangement: Arrangement) -> None:
        """Remove an arrangement from the project."""
        if arrangement in self.arrangements:
            self.arrangements.remove(arrangement)
            
    def get_arrangement_by_name(self, name: str) -> Optional[Arrangement]:
        """Find an arrangement by its name."""
        for arrangement in self.arrangements:
            if arrangement.name == name:
                return arrangement
        return None
        
    def validate(self) -> None:
        """Validate project and all its arrangements."""
        if not self.name:
            raise ValueError("Project name cannot be empty")
            
        if self.source_path and not isinstance(self.source_path, Path):
            raise TypeError("source_path must be a Path object")
            
        if self.output_dir and not isinstance(self.output_dir, Path):
            raise TypeError("output_dir must be a Path object")
            
        # Check for arrangement name uniqueness
        names = [arr.name for arr in self.arrangements]
        duplicate_names = set(name for name in names if names.count(name) > 1)
        if duplicate_names:
            raise ValueError(f"Duplicate arrangement names found: {', '.join(duplicate_names)}")
            
        # Validate each arrangement
        for arrangement in self.arrangements:
            try:
                arrangement.validate()
            except ValueError as e:
                raise ValueError(f"Invalid arrangement '{arrangement.name}': {str(e)}")
            
    def get_all_clip_paths(self) -> Set[Path]:
        """Get set of all unique audio file paths used in project."""
        paths = set()
        for arrangement in self.arrangements:
            for clip in arrangement.clips:
                if clip.source_path:
                    paths.add(clip.source_path)
        return paths
        
    def validate_audio_files(self) -> bool:
        """Check if all referenced audio files exist."""
        missing_files = []
        for path in self.get_all_clip_paths():
            if not path.exists():
                missing_files.append(path)
                self.logger.warning(f"Audio file not found: {path}")
                
        if missing_files:
            self.logger.error(f"Missing {len(missing_files)} audio files")
            return False
        return True
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format for serialization."""
        return {
            'name': self.name,
            'source_path': str(self.source_path) if self.source_path else None,
            'output_dir': str(self.output_dir) if self.output_dir else None,
            'arrangements': [arr.to_dict() for arr in self.arrangements]
        }
    
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create project instance from dictionary data."""
        source_path = Path(data['source_path']) if data.get('source_path') else None
        output_dir = Path(data['output_dir']) if data.get('output_dir') else None
        
        project = cls(
            name=data['name'],
            source_path=source_path,
            output_dir=output_dir
        )
        
        # Add arrangements
        for arr_data in data.get('arrangements', []):
            arrangement = Arrangement.from_dict(arr_data)
            project.add_arrangement(arrangement)
            
        return project
```
---

#### src\utils\__init__.py
```
"""Utils package for FL Studio to Cubase migration tool.

This package contains utility functionality for file management, logging,
and other support functions.
"""

from .file_manager import FileManager
from .logger import setup_logger, get_logger, log_error

__all__ = ['FileManager', 'setup_logger', 'get_logger', 'log_error']
```
---

#### src\utils\file_manager.py
```
from pathlib import Path
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.project import Project
    from ..models.arrangement import Arrangement

class FileManager:
    """Handles file system operations and directory structure."""
    
    def __init__(self, base_dir: str):
        """Initialize file manager with base directory.
        
        Args:
            base_dir: Base directory for file operations
        """
        self.base_dir = Path(base_dir)
        # Import logger here to avoid circular import
        from ..utils.logger import get_logger
        self.logger = get_logger()
        
    def create_directory_structure(self, project: "Project") -> Dict["Arrangement", Path]:
        """Create output directory structure for project and arrangements.
        
        Args:
            project: Project instance containing arrangements
            
        Returns:
            Dictionary mapping arrangements to their output directories
            
        Raises:
            OSError: If directory creation fails
        """
        # Create base output directory
        project_dir = self.base_dir / self._sanitize_path(project.name)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create arrangement directories
        arrangement_dirs = {}
        for arrangement in project.arrangements:
            arr_dir = project_dir / self._sanitize_path(arrangement.name)
            audio_dir = arr_dir / "audio_files"
            
            try:
                audio_dir.mkdir(parents=True, exist_ok=True)
                arrangement_dirs[arrangement] = arr_dir
                arrangement.folder_path = arr_dir
            except Exception as e:
                self.logger.error(f"Failed to create directory for arrangement {arrangement.name}: {e}")
                raise
                
        return arrangement_dirs
        
    def cleanup_temp_files(self, directory: Optional[Path] = None) -> None:
        """Clean up temporary files and directories.
        
        Args:
            directory: Optional specific directory to clean, defaults to temp dir
        """
        if not directory:
            from ..config import Config
            directory = Config.TEMP_DIR
            
        if not directory.exists():
            return
            
        try:
            shutil.rmtree(directory)
            self.logger.debug(f"Cleaned up temporary directory: {directory}")
        except Exception as e:
            self.logger.warning(f"Failed to clean up temporary directory {directory}: {e}")
            
    def validate_paths(self) -> bool:
        """Validate all required paths exist and are accessible.
        
        Returns:
            True if all paths are valid and accessible, False otherwise
        """
        try:
            # Check base directory
            if not self.base_dir.exists():
                self.base_dir.mkdir(parents=True)
                
            # Verify write permissions
            test_file = self.base_dir / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except Exception as e:
                self.logger.error(f"No write permission in base directory: {e}")
                return False
                
            # Check temp directory
            from ..config import Config
            temp_dir = Config.TEMP_DIR
            if not temp_dir.exists():
                temp_dir.mkdir(parents=True)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Path validation failed: {e}")
            return False
            
    def _sanitize_path(self, name: str) -> str:
        """Sanitize a string for use in file paths.
        
        Args:
            name: Original path string
            
        Returns:
            Sanitized path string
        """
        # Replace invalid characters with underscore
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
            
        # Remove leading/trailing spaces and dots
        name = name.strip('. ')
        
        # Ensure name is not empty
        if not name:
            name = "unnamed"
            
        return name
        
    def copy_audio_file(self, source: Path, dest: Path) -> bool:
        """Copy audio file with error handling.
        
        Args:
            source: Source audio file path
            dest: Destination path
            
        Returns:
            True if copy succeeded, False otherwise
        """
        try:
            shutil.copy2(source, dest)
            return True
        except Exception as e:
            self.logger.error(f"Failed to copy audio file from {source} to {dest}: {e}")
            return False
            
    def ensure_unique_path(self, path: Path) -> Path:
        """Ensure path is unique by adding number suffix if needed.
        
        Args:
            path: Original path
            
        Returns:
            Unique path with number suffix if needed
        """
        if not path.exists():
            return path
            
        base = path.parent / path.stem
        ext = path.suffix
        counter = 1
        
        while True:
            new_path = Path(f"{base}_{counter}{ext}")
            if not new_path.exists():
                return new_path
            counter += 1
```
---

#### src\utils\logger.py
```
from pathlib import Path
from typing import Optional

def setup_logger(log_file: Optional[Path] = None, debug_mode: bool = False) -> logging.Logger:
    """Configure application-wide logging with console and optional file output.
    
    Args:
        log_file: Optional path to log file
        debug_mode: Whether to enable debug logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('fl_cubase_migration')
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler if log_file is specified
    if log_file:
        try:
            # Ensure directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Failed to set up file logging to {log_file}: {e}")
    
    return logger

def get_logger() -> logging.Logger:
    """Get the configured logger instance.
    
    Returns:
        Logger instance
    """
    logger = logging.getLogger('fl_cubase_migration')
    
    # If logger has no handlers, set up a basic configuration
    if not logger.handlers:
        setup_logger()
        
    return logger

def log_error(error: Exception, context: Optional[str] = None) -> None:
    """Log an error with optional context information.
    
    Args:
        error: Exception to log
        context: Optional context information
    """
    logger = get_logger()
    error_message = f"{error.__class__.__name__}: {str(error)}"
    if context:
        error_message = f"{context} - {error_message}"
    logger.error(error_message, exc_info=True)
```
---

#### tests\__init__.py
```
"""Test suite for FL Studio to Cubase migration tool."""

from pathlib import Path
from typing import Iterator

def get_fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"

def get_test_data_path(filename: str) -> Path:
    """Get path to a test data file."""
    return get_fixtures_dir() / filename

def iter_test_files(pattern: str) -> Iterator[Path]:
    """Iterate over test files matching glob pattern."""
    return get_fixtures_dir().glob(pattern)

__all__ = [
    'get_fixtures_dir',
    'get_test_data_path',
    'iter_test_files'
]
```
---

#### tests\conftest.py
```
from pathlib import Path

from src.models.clip import Clip
from src.models.arrangement import Arrangement
from src.models.project import Project

def generate_sine_wave(frequency: float = 440, duration: float = 1.0, sample_rate: int = 44100) -> np.ndarray:
    """Generate a sine wave array."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * frequency * t)

def save_wav(filename: Path, audio_data: np.ndarray, channels: int = 1, sample_rate: int = 44100) -> None:
    """Save audio data as WAV file."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    scaled = np.int16(audio_data * 32767)
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(scaled.tobytes())

def fixtures_dir() -> Path:
    """Get fixtures directory."""
    return Path(__file__).parent / "fixtures"

def temp_dir(tmp_path_factory) -> Path:
    """Create temporary directory for test outputs."""
    test_dir = tmp_path_factory.mktemp("test_output")
    return test_dir

def sample_wav_file(temp_dir: Path) -> Path:
    """Create a simple test WAV file."""
    wav_path = temp_dir / "test.wav"
    audio_data = generate_sine_wave(440, 1.0)
    save_wav(wav_path, audio_data)
    return wav_path

def sample_clip(sample_wav_file: Path) -> Clip:
    """Create a sample clip instance."""
    return Clip(
        name="test_clip",
        position=0.0,
        duration=2.0,  # Fixed duration to match test expectations
        color="#FF0000",
        source_path=sample_wav_file,
        volume=1.0,
        muted=False
    )

def sample_arrangement(sample_clip: Clip) -> Arrangement:
    """Create a sample arrangement instance."""
    arrangement = Arrangement(name="TEST_ARRANGEMENT")
    arrangement.add_clip(sample_clip)
    return arrangement

def sample_project(sample_arrangement: Arrangement, temp_dir: Path) -> Project:
    """Create a sample project instance."""
    project = Project(
        name="test_project",
        source_path=temp_dir / "test.flp",
        output_dir=temp_dir / "output"
    )
    project.add_arrangement(sample_arrangement)
    return project

def expected_aaf_path(fixtures_dir: Path) -> Path:
    """Get path to expected AAF file."""
    return fixtures_dir / "expected_output" / "expected_arrangement.aaf"

def cleanup_temp_files(temp_dir: Path):
    """Clean up temporary files after each test."""
    yield
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
```
---

#### tests\fixtures\README.md
# Test Fixtures

This directory contains test fixtures used across the test suite. The fixtures are automatically generated or required to be present for tests to run successfully.

## File Structure
```
fixtures/
├── sample_project.flp          # Sample FL Studio project with multiple arrangements
├── audio_clips/               # Test audio files (auto-generated)
│   ├── clip1.wav             # Mono, 2 seconds, 440Hz
│   ├── clip2.wav             # Stereo, 3 seconds, 880Hz
│   ├── clip3.wav             # Mono, 1 second, 330Hz
│   └── clip4.wav             # Stereo, 2 seconds, dual frequency
└── expected_output/
    └── expected_arrangement.aaf  # Expected AAF output for validation
```

## Fixture Details

### sample_project.flp
FL Studio project containing:
- Pattern 1 "NAGRYWKI_MAIN":
  - 3 audio clips at different positions
  - Various colors and volumes
- Pattern 2 "NAGRYWKI_CHOREK":
  - 2 audio clips at different positions
  - Different color coding

### audio_clips/
Auto-generated test audio files with following properties:
- clip1.wav:
  - Mono channel
  - 2 seconds duration
  - 440Hz sine wave
  - 44.1kHz sample rate, 16-bit

- clip2.wav:
  - Stereo channels
  - 3 seconds duration
  - 880Hz sine wave
  - Right channel at 50% volume
  - 44.1kHz sample rate, 16-bit

- clip3.wav:
  - Mono channel
  - 1 second duration
  - 330Hz sine wave
  - 44.1kHz sample rate, 16-bit

- clip4.wav:
  - Stereo channels
  - 2 seconds duration
  - Left: 440Hz, Right: 880Hz
  - 44.1kHz sample rate, 16-bit

### expected_arrangement.aaf
AAF file representing "NAGRYWKI_MAIN" pattern exported from Cubase, used to validate correct AAF generation and structure.

## Generation
Audio files are automatically generated during test runs via fixtures in conftest.py. The sample_project.flp and expected_arrangement.aaf must be manually provided.
---

#### tests\fixtures\expected_output\expected_arrangement.aaf
```

```
---

#### tests\generate_fixtures.py
```
from pathlib import Path

def generate_test_audio_files(fixtures_dir: Path) -> None:
    """Generate test audio files for testing."""
    audio_dir = fixtures_dir / "audio_clips"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate 1-second sine wave at 440Hz (A4 note)
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    sine_wave = np.sin(2 * np.pi * 440 * t)
    
    # Create test WAV files
    for i in range(1, 5):
        wav_path = audio_dir / f"clip{i}.wav"
        with wave.open(str(wav_path), 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_data = (sine_wave * 32767).astype(np.int16)
            wav_file.writeframes(wav_data.tobytes())

def generate_sample_flp(fixtures_dir: Path) -> None:
    """Generate a sample FL Studio project file for testing."""
    
    project = pyflp.Project()
    project.tempo = 140
    
    # Add a few channels with samples
    for i in range(3):
        channel = project.channels.samplers.add()
        channel.name = f"Test Channel {i+1}"
        channel.sample_path = str(fixtures_dir / "audio_clips" / f"clip{i+1}.wav")
        channel.start_offset = i * 100  # stagger the clips
        channel.length = 100
        channel.volume = 1.0
        channel.color = 0xFF0000  # red
    
    # Save the project
    with open(fixtures_dir / "sample_project.flp", "wb") as f:
        f.write(project.save())

if __name__ == "__main__":
    # Get the fixtures directory relative to this file
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate test files
    generate_test_audio_files(fixtures_dir)
    generate_sample_flp(fixtures_dir)
    print(f"Test fixtures generated in {fixtures_dir}")
```
---

#### tests\integration\test_full_workflow.py
```
from pathlib import Path

from src.core.project_parser import FLProjectParser
from src.core.audio_processor import AudioProcessor
from src.core.aaf_generator import AAFGenerator
from src.utils.file_manager import FileManager

def compare_aaf_metadata(file1: Path, file2: Path) -> bool:
    """Compare two AAF files for structural equality."""
    with aaf2.open(str(file1), 'r') as f1, aaf2.open(str(file2), 'r') as f2:
        # Compare main composition
        comp1 = next(f1.content.toplevel())
        comp2 = next(f2.content.toplevel())
        
        if comp1.name != comp2.name:
            return False
            
        # Compare number of mobs
        if len(f1.content.mobs) != len(f2.content.mobs):
            return False
            
        # Compare mob structure
        mobs1 = sorted(f1.content.mobs, key=lambda m: getattr(m, 'name', ''))
        mobs2 = sorted(f2.content.mobs, key=lambda m: getattr(m, 'name', ''))
        
        for mob1, mob2 in zip(mobs1, mobs2):
            # Compare slots
            if len(mob1.slots) != len(mob2.slots):
                return False
                
            for slot1, slot2 in zip(mob1.slots, mob2.slots):
                # Compare basic properties
                if slot1.segment.length != slot2.segment.length:
                    return False
                    
                # Compare metadata if available
                if hasattr(slot1, 'user_comments') and hasattr(slot2, 'user_comments'):
                    if slot1.user_comments != slot2.user_comments:
                        return False
                        
        return True

class TestFullWorkflow:
    def test_complete_migration_flow(self, sample_project_path, temp_dir):
        """Test complete workflow from FL Studio project to AAF files."""
        # Set up output directories
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        try:
            # 1. Parse FL Studio project
            parser = FLProjectParser(str(sample_project_path))
            project = parser.parse_project()
            
            assert project is not None
            assert len(project.arrangements) > 0
            
            # 2. Process audio files
            audio_processor = AudioProcessor(str(temp_dir / "audio"))
            clip_map = {}
            
            for arrangement in project.arrangements:
                processed_clips = audio_processor.export_audio_clips(arrangement.clips)
                clip_map[arrangement] = processed_clips
                
                assert len(processed_clips) == len(arrangement.clips)
                assert all(path.exists() for path in processed_clips.values())
            
            # 3. Generate AAF files
            file_manager = FileManager(str(output_dir))
            arrangement_dirs = file_manager.create_directory_structure(project)
            
            for arrangement in project.arrangements:
                # Generate AAF
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, clip_map[arrangement])
                generator.generate_aaf(str(aaf_path))
                
                assert aaf_path.exists()
                
                # Verify AAF structure
                with aaf2.open(str(aaf_path), 'r') as f:
                    composition = next(f.content.toplevel())
                    assert composition.name == arrangement.name
                    assert len(f.content.mobs) > 0
                    
            # 4. Verify output structure
            for arrangement in project.arrangements:
                arr_dir = arrangement_dirs[arrangement]
                assert arr_dir.exists()
                assert any(arr_dir.glob("*.aaf"))
                assert (arr_dir / "audio_files").exists()
                
        except Exception as e:
            pytest.fail(f"Workflow failed: {str(e)}")

    def test_complete_workflow_output_matches_expected(self, sample_project_path, temp_dir, expected_aaf_path):
        """Test that complete workflow produces expected AAF structure."""
        # Set up output directories
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        try:
            # Parse FL Studio project
            parser = FLProjectParser(str(sample_project_path))
            project = parser.parse_project()
            
            # Process audio files
            audio_processor = AudioProcessor(str(temp_dir / "audio"))
            clip_map = {}
            
            for arrangement in project.arrangements:
                processed_clips = audio_processor.export_audio_clips(arrangement.clips)
                clip_map[arrangement] = processed_clips
            
            # Generate AAF files
            file_manager = FileManager(str(output_dir))
            arrangement_dirs = file_manager.create_directory_structure(project)
            
            for arrangement in project.arrangements:
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, clip_map[arrangement])
                generator.generate_aaf(str(aaf_path))
                
                # Compare with expected AAF
                assert compare_aaf_metadata(aaf_path, expected_aaf_path)
                
        except Exception as e:
            pytest.fail(f"Workflow failed: {str(e)}")

    def test_large_project_handling(self, temp_dir, sample_wav_file):
        """Test handling of large projects with multiple arrangements and clips."""
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        # Create test project structure
        project_path = temp_dir / "large_project.flp"
        shutil.copy2(sample_wav_file, project_path)
        
        # Create test project with multiple arrangements
        project = FLProjectParser(str(project_path)).parse_project()
        
        # Add test arrangements
        for i in range(5):  # 5 arrangements
            arrangement = project.arrangements[i]
            for j in range(200):  # 200 clips each
                clip = arrangement.clips[j]
                clip.source_path = sample_wav_file
        
        try:
            # Process project
            audio_processor = AudioProcessor(str(temp_dir / "audio"))
            file_manager = FileManager(str(output_dir))
            
            # Export audio and generate AAFs
            arrangement_dirs = file_manager.create_directory_structure(project)
            
            for arrangement in project.arrangements:
                processed_clips = audio_processor.export_audio_clips(
                    arrangement.clips,
                    max_workers=4  # Use parallel processing
                )
                
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, processed_clips)
                generator.generate_aaf(str(aaf_path))
                
                # Verify output
                assert aaf_path.exists()
                assert aaf_path.stat().st_size > 0
                
            assert len(list(output_dir.rglob("*.aaf"))) == len(project.arrangements)
            
        except Exception as e:
            pytest.fail(f"Large project handling failed: {str(e)}")
            
    def test_error_recovery(self, temp_dir, sample_project_path):
        """Test system recovery from various error conditions."""
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        parser = FLProjectParser(str(sample_project_path))
        project = parser.parse_project()
        
        # Test recovery from missing audio files
        audio_processor = AudioProcessor(str(temp_dir / "audio"))
        processed_clips = audio_processor.export_audio_clips(
            [clip for arr in project.arrangements for clip in arr.clips]
        )
        
        # Should continue with available files
        assert len(processed_clips) > 0
        
        # Test recovery from AAF generation errors
        file_manager = FileManager(str(output_dir))
        arrangement_dirs = file_manager.create_directory_structure(project)
        
        for arrangement in project.arrangements:
            try:
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, processed_clips)
                generator.generate_aaf(str(aaf_path))
            except Exception as e:
                # Should log error and continue with next arrangement
                continue
                
        # Verify at least some AAFs were generated
        assert any(output_dir.rglob("*.aaf"))

    def test_metadata_preservation_workflow(self, temp_dir, sample_wav_file):
        """Test preservation of metadata through the complete workflow."""
        # Create test project with specific metadata
        project_path = temp_dir / "metadata_test.flp"
        shutil.copy2(sample_wav_file, project_path)
        
        parser = FLProjectParser(str(project_path))
        project = parser.parse_project()
        
        # Add test data with specific metadata
        arrangement = project.arrangements[0]
        test_clip = arrangement.clips[0]
        test_clip.color = "#FF0000"
        test_clip.volume = 0.8
        test_clip.muted = True
        
        # Process through workflow
        output_dir = temp_dir / "output"
        audio_processor = AudioProcessor(str(temp_dir / "audio"))
        processed_clips = audio_processor.export_audio_clips([test_clip])
        
        file_manager = FileManager(str(output_dir))
        arrangement_dirs = file_manager.create_directory_structure(project)
        
        aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
        generator = AAFGenerator(arrangement, processed_clips)
        generator.generate_aaf(str(aaf_path))
        
        # Verify metadata in AAF
        with aaf2.open(str(aaf_path), 'r') as f:
            composition = next(f.content.toplevel())
            for mob in f.content.mobs:
                if hasattr(mob, 'user_comments'):
                    comments = mob.user_comments
                    if comments.get('Name') == test_clip.name:
                        assert comments.get('Color') == "#FF0000"
                        assert comments.get('Muted') == 'true'
                        if hasattr(mob, 'volume'):
                            assert abs(mob.volume - 0.8) < 0.01
```
---

#### tests\test_aaf_generator.py
```
from pathlib import Path
from typing import Dict

from src.core.aaf_generator import AAFGenerator
from src.models.arrangement import Arrangement
from src.models.clip import Clip

class TestAAFGenerator:
    def test_aaf_creation(self, temp_dir, sample_arrangement, sample_wav_file):
        """Test basic AAF file creation."""
        output_path = temp_dir / "test.aaf"
        audio_map = {clip: sample_wav_file for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        
        # Verify AAF structure
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            assert composition is not None
            assert len(f.content.mobs) > 0

    def test_clip_metadata_preservation(self, temp_dir, sample_clip, sample_wav_file):
        """Test preservation of clip metadata in AAF."""
        arrangement = Arrangement(name="test_arrangement")
        arrangement.add_clip(sample_clip)
        
        output_path = temp_dir / "metadata_test.aaf"
        audio_map = {sample_clip: sample_wav_file}
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            
            # Verify composition name
            assert composition.name == arrangement.name
            
            # Check mob structure
            found_clip = False
            for mob in f.content.mobs:
                if hasattr(mob, 'user_comments'):
                    comments = mob.user_comments
                    if comments.get('Name') == sample_clip.name:
                        found_clip = True
                        assert comments.get('Color', '') == sample_clip.color
                        if sample_clip.muted:
                            assert comments.get('Muted') == 'true'
                        break
            
            assert found_clip, "Clip metadata not found in AAF"

    def test_timeline_position_preservation(self, temp_dir, sample_wav_file):
        """Test preservation of clip positions in timeline."""
        arrangement = Arrangement(name="position_test")
        
        # Create clips at specific positions
        clips = [
            Clip(name="clip1", position=0.0, duration=2.0, color="#FF0000"),
            Clip(name="clip2", position=3.0, duration=2.0, color="#00FF00"),
            Clip(name="clip3", position=6.0, duration=2.0, color="#0000FF")
        ]
        
        for clip in clips:
            arrangement.add_clip(clip)
            
        audio_map = {clip: sample_wav_file for clip in clips}
        output_path = temp_dir / "position_test.aaf"
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            # Verify relative positions are maintained
            previous_pos = -1
            for mob in f.content.mobs:
                if hasattr(mob, 'slots') and mob.slots:
                    for slot in mob.slots:
                        if hasattr(slot, 'position'):
                            assert slot.position > previous_pos
                            previous_pos = slot.position

    def test_missing_audio_files(self, temp_dir, sample_arrangement):
        """Test handling of missing audio files."""
        output_path = temp_dir / "missing_audio.aaf"
        audio_map = {clip: Path("nonexistent.wav") for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        
        with pytest.raises(FileNotFoundError):
            generator.generate_aaf(str(output_path))

    def test_invalid_output_path(self, temp_dir, sample_arrangement, sample_wav_file):
        """Test handling of invalid output paths."""
        invalid_path = temp_dir / "nonexistent" / "test.aaf"
        audio_map = {clip: sample_wav_file for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        
        with pytest.raises((OSError, IOError)):
            generator.generate_aaf(str(invalid_path))

    def test_volume_preservation(self, temp_dir, sample_wav_file):
        """Test preservation of clip volume settings."""
        arrangement = Arrangement(name="volume_test")
        clip = Clip(
            name="volume_clip",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            volume=0.5  # 50% volume
        )
        arrangement.add_clip(clip)
        
        output_path = temp_dir / "volume_test.aaf"
        audio_map = {clip: sample_wav_file}
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            for mob in f.content.mobs:
                if hasattr(mob, 'slots'):
                    for slot in mob.slots:
                        if hasattr(slot, 'volume'):
                            assert abs(slot.volume - 0.5) < 0.01

    def test_large_arrangement(self, temp_dir, sample_wav_file):
        """Test handling of arrangements with many clips."""
        arrangement = Arrangement(name="large_test")
        
        # Create 100 test clips
        clips = []
        for i in range(100):
            clip = Clip(
                name=f"clip_{i}",
                position=float(i) * 2,  # Position them sequentially
                duration=1.5,
                color="#FF0000"
            )
            arrangement.add_clip(clip)
            clips.append(clip)
            
        audio_map = {clip: sample_wav_file for clip in clips}
        output_path = temp_dir / "large_test.aaf"
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
```
---

#### tests\test_audio_processor.py
```
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from src.core.audio_processor import AudioProcessor
from src.models.clip import Clip

class TestAudioProcessor:
    def test_init(self, temp_dir):
        """Test AudioProcessor initialization."""
        processor = AudioProcessor(str(temp_dir))
        assert processor.output_dir == Path(temp_dir)
        assert processor.output_dir.exists()

    def test_single_clip_export(self, temp_dir, sample_wav_file, sample_clip):
        """Test exporting a single audio clip."""
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([sample_clip])
        
        assert len(result) == 1
        assert sample_clip in result
        exported_path = result[sample_clip]
        
        assert exported_path.exists()
        assert exported_path.suffix == '.wav'
        
        # Verify audio content
        with wave.open(str(sample_wav_file), 'rb') as original:
            with wave.open(str(exported_path), 'rb') as exported:
                # Check audio parameters
                assert original.getnchannels() == exported.getnchannels()
                assert original.getsampwidth() == exported.getsampwidth()
                assert original.getframerate() == exported.getframerate()
                assert original.getnframes() == exported.getnframes()

    def test_volume_adjustment(self, temp_dir, sample_wav_file):
        """Test volume adjustment during export."""
        # Create clip with modified volume
        clip = Clip(
            name="volume_test",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            source_path=sample_wav_file,
            volume=0.5  # 50% volume
        )
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        exported_path = result[clip]
        
        # Read and compare audio data
        with wave.open(str(sample_wav_file), 'rb') as original:
            orig_frames = np.frombuffer(original.readframes(original.getnframes()), dtype=np.int16)
            
        with wave.open(str(exported_path), 'rb') as exported:
            exported_frames = np.frombuffer(exported.readframes(exported.getnframes()), dtype=np.int16)
            
        # Check if exported audio is approximately half the amplitude
        # Allow for small differences due to floating point arithmetic
        assert np.allclose(exported_frames, orig_frames * 0.5, rtol=1e-3)

    def test_parallel_processing(self, temp_dir, sample_wav_file):
        """Test processing multiple clips in parallel."""
        # Create multiple test clips
        clips = [
            Clip(name=f"clip_{i}", position=float(i), duration=2.0, 
                 color="#FF0000", source_path=sample_wav_file)
            for i in range(5)
        ]
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips(clips, max_workers=2)
        
        assert len(result) == len(clips)
        for clip in clips:
            assert clip in result
            assert result[clip].exists()

    def test_missing_source_file(self, temp_dir, sample_wav_file):
        """Test handling of missing source files."""
        nonexistent = Path("nonexistent.wav")
        clip = Clip(
            name="missing_source",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            source_path=nonexistent
        )
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        
        assert len(result) == 0  # Should not process clip with missing source

    def test_invalid_audio_file(self, temp_dir):
        """Test handling of invalid audio files."""
        temp_dir.mkdir(parents=True, exist_ok=True)
        # Create invalid WAV file
        invalid_wav = temp_dir / "invalid.wav"
        invalid_wav.write_bytes(b"not a wav file")
        
        clip = Clip(
            name="invalid_audio",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            source_path=invalid_wav
        )
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        
        assert len(result) == 0  # Should not process invalid audio file

    def test_validate_audio_files(self, temp_dir, sample_wav_file):
        """Test audio file validation."""
        processor = AudioProcessor(str(temp_dir))
        
        # Create test clips and export
        clips = [
            Clip(name="valid_clip", position=0.0, duration=2.0,
                 color="#FF0000", source_path=sample_wav_file)
        ]
        
        processor.export_audio_clips(clips)
        assert processor.validate_audio_files(clips) == True
        
        # Test with corrupted file
        output_file = next(temp_dir.glob("*.wav"))
        output_file.write_bytes(b"corrupted")
        assert processor.validate_audio_files(clips) == False

    def test_unique_output_paths(self, temp_dir, sample_wav_file):
        """Test handling of duplicate output filenames."""
        clips = [
            Clip(name="same_name", position=0.0, duration=2.0,
                 color="#FF0000", source_path=sample_wav_file),
            Clip(name="same_name", position=2.0, duration=2.0,
                 color="#FF0000", source_path=sample_wav_file)
        ]
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips(clips)
        
        assert len(result) == 2
        # Check that output paths are different
        paths = list(result.values())
        assert paths[0] != paths[1]
```
---

#### tests\test_file_manager.py
```
# File: tests/test_file_manager.py
"""
Tests for file system operations.

Filepath: tests/test_file_manager.py
"""
from src.utils.file_manager import FileManager

def test_directory_creation(tmp_path):
    """Test creation of directory structure"""
    manager = FileManager(tmp_path)
    # TODO: Add assertions for directory creation

def test_path_validation(tmp_path):
    """Test path validation functionality"""
    manager = FileManager(tmp_path)
    # TODO: Add assertions for path validation
```
---

#### tests\test_models.py
```
from pathlib import Path

from src.models.project import Project
from src.models.arrangement import Arrangement
from src.models.clip import Clip

class TestClip:
    def test_clip_initialization(self, sample_wav_file):
        """Test basic clip initialization with valid data."""
        clip = Clip(
            name="test clip",
            position=1.5,
            duration=3.0,
            color="#FF0000",
            source_path=sample_wav_file
        )
        assert clip.name == "test_clip"  # Should be sanitized
        assert clip.position == 1.5
        assert clip.duration == 3.0
        assert clip.color == "#FF0000"
        assert clip.source_path == sample_wav_file
        assert clip.volume == 1.0  # Default value
        assert not clip.muted  # Default value

    def test_clip_validation(self):
        """Test clip validation for invalid inputs."""
        with pytest.raises(ValueError, match="Position cannot be negative"):
            Clip(name="test", position=-1.0, duration=1.0, color="#FF0000")

        with pytest.raises(ValueError, match="Duration must be positive"):
            Clip(name="test", position=0.0, duration=0.0, color="#FF0000")

        with pytest.raises(ValueError, match="Color must be in #RRGGBB format"):
            Clip(name="test", position=0.0, duration=1.0, color="FF0000")

    def test_clip_serialization(self, sample_clip):
        """Test clip serialization to and from dict."""
        data = sample_clip.to_dict()
        restored_clip = Clip.from_dict(data)
        
        assert restored_clip.name == sample_clip.name
        assert restored_clip.position == sample_clip.position
        assert restored_clip.duration == sample_clip.duration
        assert restored_clip.color == sample_clip.color
        assert str(restored_clip.source_path) == str(sample_clip.source_path)

class TestArrangement:
    def test_arrangement_initialization(self):
        """Test basic arrangement initialization."""
        arr = Arrangement(name="TEST_ARR")
        assert arr.name == "TEST_ARR"
        assert len(arr.clips) == 0

    def test_add_remove_clip(self, sample_clip):
        """Test adding and removing clips from arrangement."""
        arr = Arrangement(name="TEST_ARR")
        
        # Add clip
        arr.add_clip(sample_clip)
        assert len(arr.clips) == 1
        assert arr.clips[0] == sample_clip
        assert sample_clip.arrangement_name == "TEST_ARR"
        
        # Remove clip
        arr.remove_clip(sample_clip)
        assert len(arr.clips) == 0
        assert sample_clip.arrangement_name is None

    def test_get_duration(self, sample_clip):
        """Test arrangement duration calculation."""
        arr = Arrangement(name="TEST_ARR")
        assert arr.get_duration() == 0.0
        
        arr.add_clip(sample_clip)  # At position 0.0, duration 2.0
        assert arr.get_duration() == 2.0
        
        # Add another clip that extends beyond
        clip2 = Clip(name="clip2", position=1.5, duration=2.0, color="#00FF00")
        arr.add_clip(clip2)
        assert arr.get_duration() == 3.5  # 1.5 + 2.0

class TestProject:
    def test_project_initialization(self, temp_dir):
        """Test basic project initialization."""
        project = Project(
            name="test_project",
            source_path=temp_dir / "test.flp",
            output_dir=temp_dir / "output"
        )
        assert project.name == "test_project"
        assert len(project.arrangements) == 0

    def test_add_remove_arrangement(self, sample_arrangement):
        """Test adding and removing arrangements."""
        project = Project(name="test_project")
        
        # Add arrangement
        project.add_arrangement(sample_arrangement)
        assert len(project.arrangements) == 1
        assert project.arrangements[0] == sample_arrangement
        
        # Try adding duplicate
        with pytest.raises(ValueError, match="already exists"):
            project.add_arrangement(sample_arrangement)
            
        # Remove arrangement
        project.remove_arrangement(sample_arrangement)
        assert len(project.arrangements) == 0

    def test_validate_audio_files(self, sample_project, sample_wav_file):
        """Test audio file validation."""
        assert sample_project.validate_audio_files() == True
        
        # Test with missing file
        sample_wav_file.unlink()
        assert sample_project.validate_audio_files() == False

    def test_project_serialization(self, sample_project):
        """Test project serialization to and from dict."""
        data = sample_project.to_dict()
        restored_project = Project.from_dict(data)
        
        assert restored_project.name == sample_project.name
        assert len(restored_project.arrangements) == len(sample_project.arrangements)
        assert restored_project.arrangements[0].name == sample_project.arrangements[0].name
```
---

#### tests\test_project_parser.py
```
from pathlib import Path

from src.core.project_parser import FLProjectParser
from src.models.project import Project
from src.models.arrangement import Arrangement
from src.models.clip import Clip

class TestFLProjectParser:
    def test_project_loading(self, sample_project_path):
        """Test that FL Studio project file loads correctly."""
        parser = FLProjectParser(str(sample_project_path))
        assert parser.fl_project is not None
        assert isinstance(parser.fl_project, pyflp.Project)

    def test_missing_project_file(self):
        """Test handling of missing project file."""
        with pytest.raises(FileNotFoundError):
            FLProjectParser("nonexistent.flp")

    def test_invalid_project_file(self, temp_dir):
        """Test handling of invalid project file."""
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        invalid_file = temp_dir / "invalid.flp"
        invalid_file.write_bytes(b"not a valid flp file")
        
        with pytest.raises(Exception):
            FLProjectParser(str(invalid_file))

    def test_extract_arrangements(self, sample_project_path):
        """Test extracting arrangements from project."""
        parser = FLProjectParser(str(sample_project_path))
        arrangements = parser.extract_arrangements()
        
        assert isinstance(arrangements, list)
        assert all(isinstance(arr, Arrangement) for arr in arrangements)
        
        # Test arrangement properties
        if arrangements:  # If sample project contains arrangements
            arr = arrangements[0]
            assert isinstance(arr.name, str)
            assert len(arr.name) > 0
            assert hasattr(arr, 'clips')

    def test_clip_extraction(self, sample_project_path):
        """Test that clips are extracted with correct properties."""
        parser = FLProjectParser(str(sample_project_path))
        arrangements = parser.extract_arrangements()
        
        # Find an arrangement with clips
        clips = []
        for arr in arrangements:
            clips.extend(arr.clips)
            
        if clips:  # If sample project contains clips
            clip = clips[0]
            assert isinstance(clip, Clip)
            assert isinstance(clip.name, str)
            assert isinstance(clip.position, float)
            assert isinstance(clip.duration, float)
            assert isinstance(clip.color, str)
            assert clip.color.startswith('#')
            assert len(clip.color) == 7  # #RRGGBB format

    def test_arrangement_name_generation(self, sample_project_path):
        """Test arrangement name generation logic."""
        parser = FLProjectParser(str(sample_project_path))
        
        # Test direct arrangement name generation
        channel_group = type('MockChannel', (), {'group': 'TestGroup'})
        name = parser._get_arrangement_name(channel_group)
        assert name == 'TestGroup'
        
        # Test fallback to pattern name
        channel_pattern = type('MockChannel', (), {'group': None, 'pattern': 1})
        name = parser._get_arrangement_name(channel_pattern)
        assert name == 'Pattern_1'
        
        # Test default name
        channel_empty = type('MockChannel', (), {'group': None, 'pattern': None})
        name = parser._get_arrangement_name(channel_empty)
        assert name == 'Main'

    def test_parse_project(self, sample_project_path):
        """Test complete project parsing."""
        parser = FLProjectParser(str(sample_project_path))
        project = parser.parse_project()
        
        assert isinstance(project, Project)
        assert project.name == sample_project_path.stem
        assert project.source_path == sample_project_path
        assert len(project.arrangements) >= 0
        
        # Verify project structure
        for arrangement in project.arrangements:
            assert isinstance(arrangement, Arrangement)
            assert arrangement.name
            
            for clip in arrangement.clips:
                assert isinstance(clip, Clip)
                assert clip.position >= 0
                assert clip.duration > 0
                assert clip.name
                assert clip.color.startswith('#')

    def test_project_validation(self, sample_project_path):
        """Test that parsed project validates correctly."""
        parser = FLProjectParser(str(sample_project_path))
        project = parser.parse_project()
        
        # Should not raise any exceptions
        project.validate()
        
        # Test audio file validation if sample files exist
        validation_result = project.validate_audio_files()
        assert isinstance(validation_result, bool)
```
---

