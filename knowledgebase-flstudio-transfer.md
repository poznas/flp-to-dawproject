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
- Automates the export process
- Preserves audio quality during transfer
- Generates debugging-friendly XML output

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
- construct>=2.10.0 - Binary data parsing
- wave>=0.0.2 - WAV file processing
- numpy>=1.21.0 - Audio data manipulation
- lxml>=4.9.0 - XML processing

## Usage

### Basic Usage
```python
# Parse FL Studio project
project = fl2cu.parse("path/to/project.flp")

# Export to XML files
output_files = fl2cu.save(project, "path/to/output", format="xml")

# Debug mode with extra logging
output_files = fl2cu.save(project, "path/to/output", format="xml", debug=True)
```

### Output Structure
```
output/
  ├── NAGRYWKI_MAIN/
  │   ├── audio_files/
  │   └── arrangement.xml
  ├── NAGRYWKI_CHOREK/
  │   ├── audio_files/
  │   └── arrangement.xml
  └── debug/
      ├── parser_logs/
      └── conversion_data/
```

## Development

### Running Tests
```batch
# Run all tests
pytest

# Run specific test file
pytest tests/test_xml_generator.py

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
│   │   └── xml_generator.py      # XML generation and manipulation
│   ├── models/
│   │   ├── __init__.py
│   │   ├── project.py           # Project data structures
│   │   ├── arrangement.py       # Arrangement-specific models
│   │   └── clip.py             # Audio clip data models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_manager.py     # File system operations
│   │   └── logger.py           # Logging configuration
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── xml_exporter.py     # XML export functionality
│   │   └── base.py            # Base exporter interface
│   └── config.py               # Global configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # PyTest configuration and shared fixtures
│   ├── test_project_parser.py  # Project parsing tests
│   ├── test_audio_processor.py # Audio processing tests
│   ├── test_xml_generator.py   # XML generation tests
│   ├── test_models.py         # Data model tests
│   ├── test_file_manager.py   # File system operation tests
│   ├── test_exporters.py      # Exporter tests
│   ├── integration/
│   │   └── test_full_workflow.py # End-to-end workflow tests
│   └── fixtures/               # Test data and mock files
│       ├── README.md          # Fixtures documentation
│       ├── sample_project.flp
│       ├── audio_clips/
│       │   ├── clip1.wav
│       │   └── clip2.wav
│       └── expected_output/
│           └── expected_arrangement.xml
├── examples/
│   └── sample_project/        # Example project files
├── docs/
│   ├── api_reference.md       # API documentation
│   └── xml_format.md         # XML format specification
├── requirements.txt           # Project dependencies
├── dev-requirements.txt       # Development dependencies
├── setup.py                  # Installation configuration
├── pytest.ini               # Test configuration
├── .pylintrc               # Pylint configuration
├── mypy.ini                # Type checking configuration
└── pyproject.toml         # Code formatting and build configuration
```

## Known Limitations
- FL Studio's project format limitations (see PyFLP documentation)
- Large projects should be processed in chunks (~1000 clips per arrangement)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
---

#### create_knowledgebase.py
```

# Essential file types to exclude from content inclusion
excluded_extensions = {
    # Image files
    '.png', '.jpg', '.jpeg', '.gif', '.bmp',       
    
    # Document and binary files
    '.rtf', '.pdf', '.bin', '.lock',               
    '.jar', '.bat', '.json', '.xml', '.kts',       
    
    # Python files
    '.pyc', '.pyo', '.pyd',                        
    '.egg', '.egg-info', '.whl',                   
    '.coverage', '.tox',                           
    
    # Audio files
    '.wav', '.mp3', '.ogg', '.flac', '.aif',
    '.aiff', '.m4a', '.wma', '.mid', '.midi',
    
    # DAW project files
    '.flp',                                        # FL Studio
    '.als',                                        # Ableton Live
    '.ptx', '.ptf',                               # Pro Tools
    '.cpr',                                        # Cubase
    '.rpp',                                        # Reaper
    '.logic', '.logicx',                          # Logic Pro
    
    # Common audio plugin formats
    '.vst', '.vst3', '.dll', '.component',
    '.au', '.aax',
}

# Excluded directories
excluded_directories = [
    '/.idea/',          # IDE-specific
    '/.gradle/',        # Gradle-specific
    '/__pycache__/',    # Python cache
    '/venv/',    
    '/venv_new/', # Virtual environment
    '/env/',            # Alternative virtual environment
    '/.pytest_cache/',  # pytest cache
    '/.mypy_cache/',    # mypy cache
    '/.tox/',           # tox testing
    '/build/',          # Build directories
    '/dist/',           # Distribution directories
    '/site-packages/',  # Installed packages
    '/lib/python',      # Python library files
    '/Scripts/',        # Python scripts directory
    '/Include/',        # Python include directory
]

# Excluded specific filenames
excluded_files = {
    'gradlew', 
    'gradlew.bat', 
    '2_stub_out_project.txt',
    '.gitignore',
    '.python-version',
    'pip.conf',
    'pyvenv.cfg',
    'MANIFEST.in',
    'activate',
    'activate.bat',
    'activate.ps1',
    'deactivate.bat'
}

# Regex patterns
annotation_pattern = r"^\s*@\w+.*"
logger_pattern = r"private static final Logger log = LoggerFactory.getLogger\(\w+\.class\);"
comment_block_start = r"^\s*/\*\*"
comment_block_end = r"\*/"
import_pattern = r"^\s*import\s+"

# Python-specific patterns to exclude
python_patterns = {
    'env_vars': r"^.*os\.environ\[.*\].*$",
}

def get_git_tracked_files(directory):
    """Get a list of all Git-tracked files in the specified directory."""
    try:
        result = subprocess.run(
            ["git", "-C", directory, "ls-files"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        tracked_files = result.stdout.splitlines()
        return [os.path.join(directory, file) for file in tracked_files]
    except subprocess.CalledProcessError:
        print(f"Warning: Could not get git tracked files from {directory}")
        return []

def is_excluded_path(file_path):
    """Check if file path should be excluded based on various criteria."""
    normalized_path = file_path.replace("\\", "/").lower()
    
    # Check for Python library paths
    library_indicators = [
        'site-packages',
        'dist-packages',
        'python3',
        'python2',
        'pip',
        'setuptools',
        'wheel',
        'lib/python',
        'scripts/',
        'include/'
    ]
    if any(indicator in normalized_path for indicator in library_indicators):
        return True

    # Check extension
    if os.path.splitext(file_path)[1].lower() in excluded_extensions:
        return True

    # Check filename
    if os.path.basename(file_path) in excluded_files:
        return True

    # Check directory path
    for excluded_dir in excluded_directories:
        if excluded_dir.lower() in normalized_path:
            return True

    # Check pip/virtualenv related files
    if re.search(r'(pip|virtualenv|venv|env).*\.(txt|ini|cfg)$', normalized_path):
        return True

    return False

def remove_initial_comment(content):
    """Removes the initial comment if it contains 'File:'."""
    comment_pattern = r"^(//|#|/\*|\*|<!--)\s*File:\s.*\n"
    lines = content.splitlines()
    filtered_lines = []
    skip = True
    for line in lines:
        if skip and re.match(comment_pattern, line):
            continue
        else:
            skip = False
            filtered_lines.append(line)
    return "\n".join(filtered_lines)

def filter_content(content):
    """Applies filters to remove sensitive and unnecessary content."""
    lines = content.splitlines()
    filtered_lines = []
    in_comment_block = False

    for line in lines:
        stripped_line = line.strip()

        # Skip sensitive content
        if any(re.match(pattern, stripped_line, re.IGNORECASE) 
               for pattern in python_patterns.values()):
            continue

        # Skip annotation lines
        if re.match(annotation_pattern, stripped_line):
            continue

        # Skip import lines
        if re.match(import_pattern, stripped_line):
            continue

        # Handle comment blocks
        if re.match(comment_block_start, stripped_line):
            in_comment_block = True
            continue
        if in_comment_block:
            if re.search(comment_block_end, stripped_line):
                in_comment_block = False
            continue

        # Simplify logger lines
        if re.match(logger_pattern, stripped_line):
            filtered_lines.append("\tstatic Logger log = ...")
            continue

        filtered_lines.append(line)

    return "\n".join(filtered_lines)

def format_content(relative_path, content, file_extension):
    """Formats the file content with appropriate markdown and code block structure."""
    if file_extension == ".md":
        formatted_content = f"#### {relative_path}\n{content}\n---\n\n"
    elif content.startswith("```") and content.endswith("```"):
        formatted_content = f"#### {relative_path}\n{content}\n---\n\n"
    else:
        formatted_content = f"#### {relative_path}\n```\n{content}\n```\n---\n\n"
    return formatted_content

def process_files(directory, output_file):
    """Process all files and generate the knowledgebase document."""
    files_data = []
    tracked_files = get_git_tracked_files(directory)

    for file_path in tracked_files:
        if not os.path.exists(file_path):
            continue

        if is_excluded_path(file_path):
            continue  # Skip excluded files entirely

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            content = remove_initial_comment(content)
            content = filter_content(content)

            relative_path = os.path.relpath(file_path, directory)
            file_extension = os.path.splitext(file_path)[1]
            files_data.append((relative_path, content, file_extension))
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue

    # Sort files to ensure master_plan.md appears at the top
    files_data.sort(key=lambda x: (x[0] != 'knowledgebase/master_plan.md', x[0]))

    # Compile final content
    knowledgebase_content = ""
    for relative_path, content, file_extension in files_data:
        knowledgebase_content += format_content(relative_path, content, file_extension)

    # Write compiled content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(knowledgebase_content)

if __name__ == "__main__":
    # Define your directory and output file
    target_module = "flstudio-transfer"
    directory_to_scan = os.path.join(os.path.expanduser('~'), 'Documents', target_module)
    output_file = f"knowledgebase-{target_module}.md"

    # Execute the script
    process_files(directory_to_scan, output_file)
```
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
pytest-xsd>=0.4.0     # XML schema validation in tests

# Type checking
types-tqdm>=4.65.0    # Type stubs for tqdm
types-setuptools>=68.0.0  # Type stubs for setuptools
types-lxml>=4.9.0     # Type stubs for lxml

# Documentation
sphinx>=7.1.0         # Documentation generation
sphinx-rtd-theme>=2.0.0  # Documentation theme
```
---

#### master-plan.md
# FL Studio to Cubase Migration Tool

## Overview
A Python-based tool to accurately transfer audio arrangements from FL Studio to Cubase while preserving clip positions, colors, and organization across multiple arrangements. Uses XML as an intermediate format for debugging and validation.

## Objectives
- Maintain precise clip positions and timing
- Preserve color coding for visual organization
- Support multiple arrangements with folder structure
- Automate the export process to minimize manual work
- Handle large projects (~1000 clips) efficiently
- Provide detailed debugging information through XML output
- Enable easy troubleshooting of conversion issues

## Technical Stack
- Core: Python 3.8+
- FL Studio Project Parsing: PyFLP library
- Audio Processing: Direct file operations
- Export Format: XML (Extensible Markup Language)
- Project Structure: Directory-based with arrangement folders
- XML Processing: lxml library

## Core Features

### 1. FL Studio Project Parsing
- Parse .flp files using PyFLP
- Extract clip metadata:
  - Position information
  - Color coding
  - Names (simplified to last component)
  - Length/duration
  - Arrangement association
- Generate detailed debug logs during parsing

### 2. Audio Export System
- Batch audio file export
- Maintain original audio quality
- Preserve exact clip boundaries
- Support for multiple arrangements
- Audio file validation and verification

### 3. XML Generation
- Create XML files containing:
  - Clip positions
  - Color information
  - Track organization
  - Timing metadata
  - Audio file references
  - Debug information
- One XML file per arrangement
- Human-readable format for easy debugging

### 4. File Organization
- Create organized folder structure:
```
output/
  ├── NAGRYWKI_MAIN/
  │   ├── audio_files/
  │   └── arrangement.xml
  ├── NAGRYWKI_CHOREK_VERSE_2/
  │   ├── audio_files/
  │   └── arrangement.xml
  ├── debug/
  │   ├── parser_logs/
  │   │   └── parsing_debug.log
  │   └── conversion_data/
  │       └── metadata_dump.json
  └── ...
```

## Development Phases

### Phase 1: Core Infrastructure
1. Set up PyFLP project parsing
2. Implement basic audio file extraction
3. Create folder structure management
4. Add comprehensive logging system
5. Implement XML schema definition

### Phase 2: XML Generation
1. Implement XML metadata generation
2. Add clip position mapping
3. Integrate color preservation
4. Create track organization structure
5. Add debugging information
6. Validate XML against schema

### Phase 3: Debugging & Validation
1. Add parser debug logs
2. Implement metadata validation
3. Create conversion verification tools
4. Add data integrity checks
5. Generate human-readable debug output

### Phase 4: Cubase Integration
1. FL Studio to Cubase:
   - Export audio structure
   - Generate XML format
   - Document clip properties
   - Maintain arrangement organization

2. XML to Cubase Import:
   - Create Cubase import templates
   - Map XML data to Cubase format
   - Handle color mappings
   - Support track organization

3. Debugging Support:
   - Generate detailed logs
   - Track conversion steps
   - Validate output accuracy
   - Provide troubleshooting tools

## Technical Considerations

### Performance
- Batch processing for large projects
- Efficient memory usage for 1000+ clips
- Progress tracking for long operations
- XML generation optimization

### Error Handling
- Validate FL Studio project structure
- Check for missing audio files
- Handle corrupt project files
- Provide clear error messages
- Generate detailed debug logs

### XML Structure
- Clear, hierarchical organization
- Human-readable format
- Comprehensive metadata
- Validation support
- Easy debugging access

### Debug Features
- Detailed parsing logs
- Conversion step tracking
- Data validation reports
- Error location identification
- XML formatting for readability

### Compatibility
- Support FL Studio 20.8+ project format
- Compatible with Cubase Pro 14
- Handle various audio formats
- XML schema versioning

## Future Expansion Possibilities
1. GUI interface for easier operation
2. Additional export formats
3. Custom naming scheme configuration
4. Batch project processing
5. Enhanced debugging tools
6. Real-time conversion monitoring
7. Advanced error recovery options

## Known Limitations
1. FL Studio's limited API access requires parsing workarounds
2. Need to handle large project sizes carefully
3. XML file size may grow with project complexity

## Usage Instructions
```python
# Basic usage
project = fl2cu.parse("project.flp")
fl2cu.save(project, "output_dir", format="xml")

# Debug mode
fl2cu.save(project, "output_dir", format="xml", debug=True)

# XML validation
fl2cu.validate_xml("output_dir/arrangement.xml")
```

## Debug Tools
1. XML validation tool
2. Parsing log analyzer
3. Conversion step tracker
4. Audio file validator
5. Data integrity checker

## Documentation
1. XML schema reference
2. Debug log interpretation guide
3. Error code documentation
4. Troubleshooting procedures
5. Common issues and solutions
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
construct>=2.10.0  # Binary data parsing
wave>=0.0.2       # WAV file reading/writing
soundfile>=0.10.3  # Audio file reading/writing
numpy>=1.21.0     # Audio data manipulation
lxml>=4.9.0       # XML processing
xmlschema>=2.5.0  # XML schema validation

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
        "Topic :: Text Processing :: Markup :: XML",
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
            "fl2cubase=flstudio_cubase_migration.cli:main",
        ],
    },
    package_data={
        "flstudio_cubase_migration": [
            "schemas/*.xsd",  # XML schemas
            "templates/*.xml",  # XML templates
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

from core.project_parser import FLProjectParser
from core.audio_processor import AudioProcessor
from core.xml_generator import XMLGenerator
from models.project import Project
from utils.file_manager import FileManager
from utils.logger import setup_logger, get_logger
from config import Config

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

def save(project: Project, 
         output_dir: Union[Path, str], 
         temp_dir: Optional[Union[Path, str]] = None,
         debug: bool = False) -> Dict[str, Path]:
    """Export project arrangements to XML files with audio.
    
    Args:
        project: Project instance to export
        output_dir: Directory for output files
        temp_dir: Optional directory for temporary files (default is system temp)
        debug: Enable debug output in XML and logs
    
    Returns:
        Dictionary mapping arrangement names to their XML file paths
    
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
            
        # Generate XML files
        xml_paths = {}
        for arrangement in project.arrangements:
            try:
                arr_dir = arrangement_dirs[arrangement]
                xml_path = arr_dir / f"{arrangement.name}.xml"
                
                # Get relevant processed clips for this arrangement
                arrangement_clips = {
                    clip: path for clip, path in processed_clips.items()
                    if clip in arrangement.clips
                }
                
                # Generate XML
                generator = XMLGenerator(arrangement, arrangement_clips)
                generator.generate_xml(str(xml_path))
                
                xml_paths[arrangement.name] = xml_path
                logger.info(f"Generated XML for arrangement: {arrangement.name}")
                
                if debug:
                    debug_dir = output_dir / "debug" / arrangement.name
                    debug_dir.mkdir(parents=True, exist_ok=True)
                    generator.generate_debug_info(str(debug_dir))
                
            except Exception as e:
                logger.error(f"Failed to generate XML for arrangement {arrangement.name}: {e}")
                raise
                
        return xml_paths
        
    finally:
        # Clean up temporary files
        if not temp_dir:
            file_manager.cleanup_temp_files(temp_dir)

# Initialize logger
setup_logger()
```
---

#### src\fl2cu\__init__.py
```
# src/fl2cu/__init__.py
from pathlib import Path
from typing import Dict, Union

from .core.project_parser import FLProjectParser
from .core.audio_processor import AudioProcessor
from .core.aaf_generator import AAFGenerator
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
    
    # Generate AAF files
    output_files = {}
    for arrangement in project.arrangements:
        arr_dir = arrangement_dirs[arrangement]
        aaf_path = arr_dir / f"{arrangement.name}.aaf"
        
        # Get clip paths for this arrangement
        arrangement_clips = {
            clip: path for clip, path in clip_paths.items()
            if clip in arrangement.clips
        }
        
        # Generate AAF
        generator = AAFGenerator(arrangement, arrangement_clips)
        generator.generate_aaf(str(aaf_path))
        
        output_files[arrangement.name] = aaf_path
        
    return output_files

# Set up logging on import
setup_logger()
```
---

#### src\fl2cu\__main__.py
```
"""FL Studio to Cubase migration tool - Main module."""

from pathlib import Path
from typing import Optional, Dict

from .core.project_parser import FLProjectParser
from .core.aaf_generator import AAFGenerator
from .utils.file_manager import FileManager
from .utils.logger import setup_logger, get_logger
from .aaf_inspector import AAFInspector

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert FL Studio projects to Cubase-compatible AAF format"
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
        "--inspect",
        action="store_true",
        help="Inspect generated AAF files after creation"
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
    """Process FL Studio project and generate AAF files."""
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
                logger.debug(f"    Color: {clip.color}")
                logger.debug(f"    Source path: {clip.source_path}")
                if hasattr(clip, 'volume'):
                    logger.debug(f"    Volume: {clip.volume}")
                if hasattr(clip, 'muted'):
                    logger.debug(f"    Muted: {clip.muted}")
    
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
        logger.error("Clip details for debugging:")
        for clip in all_clips:
            logger.error(f"  Clip: {clip.name}")
            logger.error(f"    Source path: {clip.source_path}")
            if clip.source_path:
                logger.error(f"    Path exists: {clip.source_path.exists()}")
        raise ValueError("No valid audio clips were found in the project")
    
    # Generate AAF files
    logger.info("Generating AAF files...")
    aaf_paths = {}
    
    for arrangement in project.arrangements:
        try:
            logger.debug(f"Processing arrangement: {arrangement.name}")
            arr_dir = arrangement_dirs[arrangement]
            aaf_path = arr_dir / f"{arrangement.name}.aaf"
            
            # Get clips for this arrangement
            arrangement_clips = {
                clip: path for clip, path in clip_paths.items()
                if clip in arrangement.clips
            }
            
            logger.debug(f"Found {len(arrangement_clips)} clips for arrangement {arrangement.name}")
            
            # Generate AAF
            logger.debug(f"Generating AAF file: {aaf_path}")
            generator = AAFGenerator(arrangement, arrangement_clips)
            generator.generate_aaf(str(aaf_path))
            
            aaf_paths[arrangement.name] = aaf_path
            logger.info(f"Generated AAF for arrangement: {arrangement.name}")
            
        except Exception as e:
            logger.error(f"Failed to generate AAF for arrangement {arrangement.name}")
            logger.error(f"Error details: {str(e)}")
            if debug:
                logger.exception("Full traceback:")
            continue
    
    return aaf_paths

def inspect_aaf_files(aaf_paths: Dict[str, Path], output_dir: Path) -> None:
    """Inspect generated AAF files and save analysis."""
    logger = get_logger()
    logger.info("Inspecting generated AAF files...")
    
    inspection_dir = output_dir / "aaf_inspection"
    inspection_dir.mkdir(exist_ok=True)
    logger.debug(f"Created inspection directory: {inspection_dir}")
    
    for arr_name, aaf_path in aaf_paths.items():
        try:
            logger.debug(f"Inspecting AAF file for arrangement: {arr_name}")
            inspector = AAFInspector(str(aaf_path))
            analysis_path = inspection_dir / f"{arr_name}_analysis.json"
            inspector.save_analysis(str(analysis_path))
            
            logger.info(f"Saved AAF analysis for {arr_name} to {analysis_path}")
            
        except Exception as e:
            logger.error(f"Failed to inspect AAF for {arr_name}")
            logger.error(f"Error details: {str(e)}")

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
        aaf_paths = process_project(
            input_file=input_file,
            output_dir=output_dir,
            debug=args.debug
        )
        
        if not aaf_paths:
            logger.error("No AAF files were generated")
            return 1
        
        # Inspect AAF files if requested
        if args.inspect:
            inspect_aaf_files(aaf_paths, output_dir)
        
        logger.info("Processing complete!")
        logger.info("\nGenerated AAF files:")
        for name, path in aaf_paths.items():
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
```
---

#### src\fl2cu\aaf_inspector.py
```
from typing import Dict, List, Optional
from pathlib import Path

class AAFInspector:
    """Inspector for analyzing AAF file structure and content."""
    
    def __init__(self, aaf_path: str):
        """Initialize with path to AAF file."""
        self.aaf_path = Path(aaf_path)
        if not self.aaf_path.exists():
            raise FileNotFoundError(f"AAF file not found: {aaf_path}")
            
    def analyze_file(self) -> Dict:
        """Perform complete analysis of AAF file."""
        with aaf2.open(str(self.aaf_path), 'r') as f:
            analysis = {
                'file_info': self._get_file_info(),
                'composition': self._analyze_composition(f),
                'mobs': self._analyze_mobs(f),
                'media_references': self._analyze_media_refs(f),
                'potential_issues': self._check_common_issues(f)
            }
            return analysis
            
    def _get_file_info(self) -> Dict:
        """Get basic file information."""
        return {
            'filename': self.aaf_path.name,
            'size': self.aaf_path.stat().st_size,
            'last_modified': self.aaf_path.stat().st_mtime
        }
        
    def _analyze_composition(self, f: 'aaf2.File') -> Dict:
        """Analyze main composition structure."""
        try:
            comp = next(f.content.toplevel())
            return {
                'name': comp.name,
                'mob_id': str(comp.mob_id),
                'slots': len(comp.slots),
                'usage_code': getattr(comp, 'usage_code', None),
                'creation_time': getattr(comp, 'creation_time', None)
            }
        except StopIteration:
            return {'error': 'No composition found'}
            
    def _analyze_mobs(self, f: 'aaf2.File') -> List[Dict]:
        """Analyze all mobs (media objects) in the file."""
        mobs = []
        for mob in f.content.mobs:
            mob_data = {
                'name': getattr(mob, 'name', None),
                'mob_id': str(mob.mob_id),
                'type': mob.__class__.__name__,
                'slots': self._analyze_slots(mob),
                'attributes': self._get_mob_attributes(mob)
            }
            mobs.append(mob_data)
        return mobs
        
    def _analyze_slots(self, mob: 'aaf2.Mob') -> List[Dict]:
        """Analyze slots in a mob."""
        slots = []
        for slot in mob.slots:
            slot_data = {
                'name': getattr(slot, 'name', None),
                'slot_id': getattr(slot, 'slot_id', None),
                'segment': {
                    'type': slot.segment.__class__.__name__,
                    'length': getattr(slot.segment, 'length', None)
                }
            }
            # Add timing information if available
            if hasattr(slot, 'start_time'):
                slot_data['start_time'] = slot.start_time
            if hasattr(slot, 'duration'):
                slot_data['duration'] = slot.duration
            
            slots.append(slot_data)
        return slots
        
    def _get_mob_attributes(self, mob: 'aaf2.Mob') -> Dict:
        """Get mob attributes including user comments."""
        attributes = {}
        if hasattr(mob, 'user_comments'):
            attributes['user_comments'] = dict(mob.user_comments)
        if hasattr(mob, 'attributes'):
            attributes['mob_attributes'] = {
                k: str(v) for k, v in mob.attributes.items()
            }
        return attributes
        
    def _analyze_media_refs(self, f: 'aaf2.File') -> List[Dict]:
        """Analyze media references."""
        refs = []
        for mob in f.content.mobs:
            for slot in mob.slots:
                if hasattr(slot.segment, 'components'):
                    for comp in slot.segment.components:
                        if hasattr(comp, 'source_ref'):
                            ref_data = {
                                'mob_id': str(comp.source_ref.mob_id),
                                'slot_id': comp.source_ref.slot_id,
                                'start_time': getattr(comp, 'start_time', None),
                                'duration': getattr(comp, 'length', None)
                            }
                            refs.append(ref_data)
        return refs
        
    def _check_common_issues(self, f: 'aaf2.File') -> List[str]:
        """Check for common issues that might cause import problems."""
        issues = []
        
        # Check for composition
        try:
            next(f.content.toplevel())
        except StopIteration:
            issues.append("No composition found")
            
        # Check media references
        for mob in f.content.mobs:
            if isinstance(mob, aaf2.components.SourceMob):
                if not any(hasattr(slot.segment, 'components') 
                          for slot in mob.slots):
                    issues.append(f"Source mob '{mob.name}' has no components")
                    
        # Check for invalid durations
        for mob in f.content.mobs:
            for slot in mob.slots:
                if hasattr(slot, 'duration') and slot.duration <= 0:
                    issues.append(f"Invalid duration in mob '{mob.name}'")
                    
        # Check for broken references
        mob_ids = {str(mob.mob_id) for mob in f.content.mobs}
        for mob in f.content.mobs:
            for slot in mob.slots:
                if hasattr(slot.segment, 'components'):
                    for comp in slot.segment.components:
                        if (hasattr(comp, 'source_ref') and 
                            str(comp.source_ref.mob_id) not in mob_ids):
                            issues.append(f"Broken reference in mob '{mob.name}'")
                            
        return issues

    def save_analysis(self, output_path: str) -> None:
        """Save analysis to JSON file."""
        analysis = self.analyze_file()
        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
```
---

#### src\fl2cu\config.py
```
# src/fl2cu/config.py
"""Global configuration settings for FL Studio to Cubase migration"""

from pathlib import Path
from typing import List

class Config:
    """Global configuration settings"""
    
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
```
---

#### src\fl2cu\core\__init__.py
```
# src/fl2cu/core/__init__.py
"""Core functionality for FL Studio to Cubase migration."""

from .project_parser import FLProjectParser
from .audio_processor import AudioProcessor
from .aaf_generator import AAFGenerator

__all__ = ['FLProjectParser', 'AudioProcessor', 'AAFGenerator']
```
---

#### src\fl2cu\core\aaf_generator.py
```
from pathlib import Path
from typing import Dict, Tuple, Optional
from aaf2.file import AAFFile

from aaf2 import mobs, components, essence

from ..models.arrangement import Arrangement
from ..models.clip import Clip

logger = logging.getLogger(__name__)

class AAFGenerator:
    """Generates AAF files from arrangements."""
    
    def __init__(self, arrangement, clip_paths: Dict[Clip, Path]):
        self.arrangement = arrangement
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def _create_wave_descriptor(self, f: AAFFile, file_path: str) -> Tuple['aaf2.essence.WAVEDescriptor', int]:
        """Create WAVEDescriptor for audio file."""
        try:
            with wave.open(file_path, 'rb') as wav_file:
                channels = wav_file.getnchannels()
                sample_rate = wav_file.getframerate()
                bit_depth = wav_file.getsampwidth() * 8
                total_frames = wav_file.getnframes()

            # Create WAVEDescriptor using the factory
            descriptor = f.create.WAVEDescriptor()
            
            # Set properties using the AAF SDK method
            descriptor.sample_rate = sample_rate
            descriptor.channels = channels
            descriptor.quantization_bits = bit_depth
            descriptor.length = total_frames
            
            # Create and set the locator
            locator = f.create.NetworkLocator()
            locator.absolute_path = str(Path(file_path).resolve())
            descriptor.append_locator(locator)

            return descriptor, total_frames

        except Exception as e:
            self.logger.error(f"Failed to create WAVEDescriptor for {file_path}: {str(e)}")
            raise

    def generate_aaf(self, output_path: str) -> None:
        """Generate AAF file with the arrangement."""
        self.logger.info(f"Creating AAF file at {output_path}")
        
        try:
            with aaf2.open(output_path, 'w') as f:
                # Create the composition mob
                comp_mob = f.create.CompositionMob(self.arrangement.name)
                f.content.mobs.append(comp_mob)
                
                # Create a timeline mobslot for audio
                edit_rate = 48000  # Standard audio sample rate
                slot = comp_mob.create_timeline_slot(edit_rate)
                sequence = f.create.Sequence('sound')
                slot.segment = sequence

                # Process each clip
                for clip in self.arrangement.clips:
                    source_path = self.clip_paths.get(clip)
                    if not source_path or not source_path.exists():
                        self.logger.warning(f"Audio file not found for clip: {clip.name}")
                        continue

                    try:
                        # Create source mob for the clip
                        source_mob = f.create.SourceMob()
                        
                        # Create and attach WAVEDescriptor
                        descriptor, length = self._create_wave_descriptor(f, str(source_path))
                        source_mob.descriptor = descriptor
                        
                        # Add the source mob to the file
                        f.content.mobs.append(source_mob)
                        
                        # Create a timeline mobslot in the source mob
                        source_slot = source_mob.create_timeline_slot(edit_rate)
                        
                        # Create the source clip
                        source_ref = f.create.SourceClip()
                        source_ref.mob = source_mob
                        source_ref.slot = source_slot.slot_id
                        source_ref.length = length
                        
                        # Create the clip for the composition
                        comp_clip = f.create.SourceClip()
                        comp_clip.mob = source_mob
                        comp_clip.slot = source_slot.slot_id
                        comp_clip.start = int(clip.position * edit_rate)
                        comp_clip.length = int(clip.duration * edit_rate)

                        # Add the clip to the sequence
                        sequence.components.append(comp_clip)

                    except Exception as e:
                        self.logger.error(f"Failed to process clip {clip.name}: {str(e)}")
                        raise

                # Save the file
                f.save()
                self.logger.info("AAF file successfully generated")

        except Exception as e:
            self.logger.error(f"Failed to generate AAF file: {str(e)}")
            raise
```
---

#### src\fl2cu\core\audio_processor.py
```
from pathlib import Path
from typing import Dict, List, Optional

from ..models.clip import Clip

class AudioProcessor:
    """Handles audio file validation and conversion."""
    
    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def _convert_to_pcm_wav(self, input_path: Path, output_path: Path) -> bool:
        """Convert audio file to standard PCM WAV format."""
        try:
            # Read audio file using soundfile (supports many formats)
            data, sample_rate = sf.read(str(input_path))
            
            # Convert to float32 for processing
            data = data.astype(np.float32)

            # If mono, reshape to 2D array
            if len(data.shape) == 1:
                data = data.reshape(-1, 1)

            # Write as standard PCM WAV
            with wave.open(str(output_path), 'wb') as wav_file:
                wav_file.setnchannels(data.shape[1] if len(data.shape) > 1 else 1)
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                # Convert to 16-bit PCM
                pcm_data = (data * 32767).astype(np.int16)
                wav_file.writeframes(pcm_data.tobytes())
            
            return True

        except Exception as e:
            self.logger.error(f"Failed to convert {input_path}: {str(e)}")
            return False

    def process_audio_clips(self, clips: list) -> dict:
        """Process and validate audio clips, converting formats if needed."""
        processed_clips = {}
        
        for clip in clips:
            if not clip.source_path or not clip.source_path.exists():
                self.logger.warning(f"Source file not found: {clip.source_path}")
                continue

            try:
                # Create output filename
                output_path = self.output_dir / f"{clip.name}.wav"
                
                # Convert to standard PCM WAV
                if self._convert_to_pcm_wav(clip.source_path, output_path):
                    processed_clips[clip] = output_path
                else:
                    self.logger.error(f"Failed to process {clip.name}")

            except Exception as e:
                self.logger.error(f"Error processing {clip.name}: {str(e)}")
                continue

        return processed_clips

    def validate_audio_files(self, clips: List[Clip]) -> Dict[Clip, Path]:
        """Validate processed audio files."""
        valid_clips = {}
        
        for clip, path in self.process_audio_clips(clips).items():
            try:
                with wave.open(str(path), 'rb') as wav_file:
                    # Verify it's standard PCM format
                    if wav_file.getcomptype() == 'NONE':
                        valid_clips[clip] = path
            except Exception as e:
                self.logger.error(f"Invalid audio file {path}: {str(e)}")
                
        return valid_clips
```
---

#### src\fl2cu\core\project_parser.py
```
from pathlib import Path
from typing import List, Optional, Dict, Union

from ..models.project import Project
from ..models.arrangement import Arrangement
from ..models.clip import Clip

logger = logging.getLogger(__name__)

class FLProjectParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Project file not found: {file_path}")
            
        logger.debug(f"Loading FL Studio project: {file_path}")
        self.fl_project = pyflp.parse(file_path)
        logger.debug(f"Project version: {self.fl_project.version}")

    def resolve_fl_studio_path(self, path: Union[str, Path]) -> Optional[Path]:
        if isinstance(path, Path):
            path = str(path)
            
        fl_variables = {
            "FLStudioUserData": "C:\\Users\\poznas\\Documents\\Image-Line\\Data\\FL Studio",
            "FLStudioInstallDir": os.getenv("PROGRAMFILES", "") + "\\Image-Line\\FL Studio 21",
        }
        
        try:
            for var_name, var_value in fl_variables.items():
                var_pattern = f"%{var_name}%"
                if var_pattern in path:
                    path = path.replace(var_pattern, var_value)
            resolved_path = Path(path)
            return resolved_path if resolved_path.exists() else None
        except Exception as e:
            logger.error(f"Failed to resolve path {path}: {e}")
            return None

    def _get_color_hex(self, color) -> str:
        try:
            if hasattr(color, 'r') and hasattr(color, 'g') and hasattr(color, 'b'):
                # Handle RGBA object
                return f"#{color.r:02x}{color.g:02x}{color.b:02x}"
            elif isinstance(color, int):
                # Handle integer color value
                r = (color >> 16) & 255
                g = (color >> 8) & 255
                b = color & 255
                return f"#{r:02x}{g:02x}{b:02x}"
            else:
                logger.warning(f"Unknown color format: {type(color)}. Using default.")
                return "#FFFFFF"
        except Exception as e:
            logger.error(f"Error converting color: {e}")
            return "#FFFFFF"

    def _create_clip_from_channel(self, channel, position: float) -> Optional[Clip]:
        try:
            logger.debug(f"Creating clip from channel at position {position}")
            
            # Get channel name and sanitize for unique identification
            base_name = channel.name if hasattr(channel, 'name') else "unnamed_clip"
            base_name = base_name.replace(" ", "_")
            name = f"{base_name}_{position}"
            logger.debug(f"Channel name: {channel.name}")

            # Get sample path if available
            source_path = None
            if hasattr(channel, 'sample_path') and channel.sample_path:
                source_path = self.resolve_fl_studio_path(str(channel.sample_path))
                logger.debug(f"Sample path: {source_path}")

            # Calculate position in seconds
            position_seconds = float(position) / self.fl_project.ppq
            logger.debug(f"Position in seconds: {position_seconds}")

            # Get duration
            duration = 1.0
            if hasattr(channel, 'length'):
                duration = float(channel.length) / self.fl_project.ppq
            elif hasattr(channel, 'sample_length'):
                duration = float(channel.sample_length) / self.fl_project.ppq
            logger.debug(f"Duration in seconds: {duration}")

            # Get color
            color = "#FFFFFF"
            try:
                if hasattr(channel, 'color'):
                    color = self._get_color_hex(channel.color)
            except Exception as e:
                logger.warning(f"Failed to get channel color: {e}")
            logger.debug(f"Color: {color}")

            # Get volume and normalize to 0-1 range
            volume = 1.0
            try:
                if hasattr(channel, 'volume'):
                    raw_volume = float(channel.volume)
                    volume = raw_volume / 100.0 if raw_volume > 1.0 else raw_volume
            except Exception as e:
                logger.warning(f"Failed to get channel volume: {e}")
            logger.debug(f"Volume: {volume}")

            # Get mute state
            muted = False
            if hasattr(channel, 'enabled'):
                muted = not channel.enabled
            logger.debug(f"Muted: {muted}")

            clip = Clip(
                name=name,
                position=position_seconds,
                duration=duration,
                color=color,
                source_path=source_path,
                volume=volume,
                muted=muted
            )
            logger.debug(f"Successfully created clip: {clip.name}")
            return clip

        except Exception as e:
            logger.error(f"Error creating clip from channel: {e}")
            return None

    def _process_native_arrangement(self, arr) -> Optional[Arrangement]:
        try:
            logger.debug(f"Processing native arrangement: {arr.name}")
            
            # Get arrangement name from FL Studio arrangement
            if not hasattr(arr, 'name') or not arr.name:
                logger.warning("Arrangement has no name, skipping")
                return None
                
            arrangement = Arrangement(name=arr.name)
            
            for track in arr.tracks:
                for item in track:
                    if hasattr(item, 'channel'):
                        logger.debug(f"Found channel item at position {item.position}")
                        clip = self._create_clip_from_channel(item.channel, item.position)
                        if clip:
                            arrangement.add_clip(clip)
                            logger.debug(f"Added clip {clip.name} to arrangement {arrangement.name}")
                    elif hasattr(item, 'pattern'):
                        logger.debug(f"Found pattern item at position {item.position}")
                        clips = self._create_clips_from_pattern(item.pattern, item.position)
                        for clip in clips:
                            arrangement.add_clip(clip)
                            logger.debug(f"Added pattern clip {clip.name} to arrangement {arrangement.name}")

            logger.debug(f"Finished processing arrangement {arr.name} with {len(arrangement.clips)} clips")
            return arrangement
        except Exception as e:
            logger.error(f"Error processing native arrangement: {e}")
            return None

    def _extract_from_patterns(self) -> List[Arrangement]:
        arrangements = []
        try:
            logger.debug("Extracting from patterns")
            for pattern in self.fl_project.patterns:
                if not pattern.name:
                    continue
                    
                logger.debug(f"Processing pattern: {pattern.name}")
                arrangement = Arrangement(name=pattern.name)
                
                clips = self._create_clips_from_pattern(pattern)
                if clips:
                    for clip in clips:
                        arrangement.add_clip(clip)
                    arrangements.append(arrangement)
                    logger.debug(f"Added arrangement from pattern {pattern.name} with {len(clips)} clips")
                    
        except Exception as e:
            logger.error(f"Error extracting from patterns: {e}")
            
        return arrangements

    def extract_arrangements(self) -> List[Arrangement]:
        arrangements = []
        
        logger.debug("Checking for FL Studio 12.9.1+ arrangements")
        if hasattr(self.fl_project, 'arrangements'):
            logger.debug(f"Found {len(self.fl_project.arrangements)} native arrangements")
            for arr in self.fl_project.arrangements:
                arrangement = self._process_native_arrangement(arr)
                if arrangement and arrangement.clips:
                    arrangements.append(arrangement)
                    logger.debug(f"Added arrangement {arrangement.name} with {len(arrangement.clips)} clips")

        # Fall back to patterns if no arrangements found
        if not arrangements:
            logger.debug("Falling back to pattern-based arrangements")
            pattern_arrangements = self._extract_from_patterns()
            arrangements.extend(pattern_arrangements)

        logger.info(f"Total arrangements extracted: {len(arrangements)}")
        for arr in arrangements:
            logger.debug(f"Arrangement '{arr.name}' has {len(arr.clips)} clips")
        return arrangements

    def parse_project(self) -> Project:
        project = Project(
            name=self.file_path.stem,
            source_path=self.file_path
        )

        try:
            arrangements = self.extract_arrangements()
            for arr in arrangements:
                project.add_arrangement(arr)
        except Exception as e:
            logger.error(f"Failed to extract arrangements: {e}")
            raise

        return project
```
---

#### src\fl2cu\core\xml_generator.py
```
from lxml import etree
from pathlib import Path
from typing import Dict
from ..models.arrangement import Arrangement
from ..models.clip import Clip

class XMLGenerator:
    def __init__(self, arrangement: Arrangement, clip_paths: Dict[Clip, Path]) -> None:
        """
        Initialize XMLGenerator with arrangement and clip paths.

        Args:
            arrangement: Arrangement object containing clips and metadata.
            clip_paths: Dictionary mapping Clip objects to their processed audio file paths.
        """
        self.arrangement = arrangement
        self.clip_paths = clip_paths

    def generate_xml(self, output_path: str) -> None:
        """
        Generate an XML representation of the arrangement.

        Args:
            output_path: Path where the XML file will be saved.
        """
        root = etree.Element("arrangement", name=self.arrangement.name)
        for clip in self.arrangement.clips:
            clip_element = etree.SubElement(root, "clip", name=clip.name)
            clip_element.set("position", str(clip.position))
            clip_element.set("duration", str(clip.duration))
            clip_element.set("color", clip.color)
            clip_element.set("volume", str(clip.volume))
            clip_element.set("muted", str(clip.muted).lower())

            if clip in self.clip_paths:
                clip_element.set("source_path", str(self.clip_paths[clip]))

        tree = etree.ElementTree(root)
        with open(output_path, "wb") as f:
            tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    def generate_debug_info(self, debug_dir: str) -> None:
        """
        Generate debug information related to the XML generation.

        Args:
            debug_dir: Directory where debug information will be saved.
        """
        debug_path = Path(debug_dir) / "debug_info.txt"
        with open(debug_path, "w") as f:
            f.write(f"Arrangement: {self.arrangement.name}\n")
            f.write(f"Number of Clips: {len(self.arrangement.clips)}\n")
            for clip in self.arrangement.clips:
                f.write(f"Clip: {clip.name}\n")
                f.write(f"  Position: {clip.position}\n")
                f.write(f"  Duration: {clip.duration}\n")
                f.write(f"  Color: {clip.color}\n")
                f.write(f"  Volume: {clip.volume}\n")
                f.write(f"  Muted: {clip.muted}\n")
                if clip in self.clip_paths:
                    f.write(f"  Source Path: {self.clip_paths[clip]}\n")
```
---

#### src\fl2cu\models\__init__.py
```
# fl2cu/models/__init__.py
"""Data models for FL Studio to Cubase migration."""
from fl2cu.models.base import BaseProject
from fl2cu.models.project import Project
from fl2cu.models.arrangement import Arrangement
from fl2cu.models.clip import Clip

__all__ = ['BaseProject', 'Project', 'Arrangement', 'Clip']
```
---

#### src\fl2cu\models\arrangement.py
```
# src/fl2cu/models/arrangement.py

from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

from .clip import Clip

class Arrangement:
    """Represents an arrangement of audio clips."""
    
    name: str
    clips: List[Clip] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate arrangement after initialization."""
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")

    def __hash__(self):
        """Make arrangement hashable by name."""
        return hash(self.name)
    
    def __eq__(self, other):
        """Compare arrangements by name."""
        if not isinstance(other, Arrangement):
            return NotImplemented
        return self.name == other.name

    def add_clip(self, clip: Clip) -> None:
        """Add a clip to the arrangement.
        
        Args:
            clip: Clip to add
            
        Raises:
            ValueError: If clip with same name already exists
        """
        if self.get_clip_by_name(clip.name):
            raise ValueError(f"Clip with name '{clip.name}' already exists")
        object.__setattr__(self, 'clips', list(self.clips) + [clip])

    def remove_clip(self, clip: Clip) -> None:
        """Remove a clip from the arrangement.
        
        Args:
            clip: Clip to remove
        """
        object.__setattr__(self, 'clips', [c for c in self.clips if c != clip])

    def get_clip_by_name(self, name: str) -> Optional[Clip]:
        """Find clip by name.
        
        Args:
            name: Name to search for
            
        Returns:
            Matching clip or None if not found
        """
        return next((clip for clip in self.clips if clip.name == name), None)

    def get_duration(self) -> float:
        """Get total arrangement duration.
        
        Returns:
            Duration in seconds
        """
        if not self.clips:
            return 0.0
        return max(clip.position + clip.duration for clip in self.clips)

    def validate(self) -> None:
        """Validate arrangement integrity.
        
        Raises:
            ValueError: If validation fails
        """
        if not self.name:
            raise ValueError("Arrangement name cannot be empty")
            
        # Check for duplicate clip names
        names = [clip.name for clip in self.clips]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate clip names found")
```
---

#### src\fl2cu\models\base.py
```
from pathlib import Path
from typing import List, Optional, Dict, Any

from .arrangement import Arrangement

class BaseProject:
    """Base class containing core Project functionality."""
    def __init__(
        self,
        name: str,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        self.name = name
        self.source_path = Path(source_path) if source_path else None
        self.output_dir = Path(output_dir) if output_dir else None
        self._arrangements: List['Arrangement'] = []

    def arrangements(self) -> List['Arrangement']:
        return self._arrangements.copy()
```
---

#### src\fl2cu\models\clip.py
```
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any

class Clip:
    """Represents an audio clip in an arrangement."""
    name: str
    position: float
    duration: float
    color: str
    source_path: Path
    volume: float = 1.0
    muted: bool = False
    arrangement_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate clip attributes after initialization."""
        if self.position < 0:
            raise ValueError("Position cannot be negative")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError("Color must be in #RRGGBB format")
        
        # Sanitize name (remove spaces and special characters)
        object.__setattr__(self, 'name', self._sanitize_name(self.name))

    def _sanitize_name(self, name: str) -> str:
        """Sanitize the clip name by replacing spaces and special characters."""
        return name.replace(' ', '_').replace('-', '_')

    def __eq__(self, other):
        """Compare clips ignoring arrangement_name."""
        if not isinstance(other, Clip):
            return NotImplemented
        return (
            self.name == other.name and
            self.position == other.position and
            self.duration == other.duration and
            self.color == other.color and
            str(self.source_path) == str(other.source_path) and
            self.volume == other.volume and
            self.muted == other.muted
        )

    def __hash__(self):
        """Hash based on immutable attributes."""
        return hash((
            self.name,
            self.position,
            self.duration,
            self.color,
            str(self.source_path),
            self.volume,
            self.muted
        ))

    def full_equals(self, other):
        """Compare clips including arrangement_name."""
        return self == other and self.arrangement_name == other.arrangement_name

    def with_arrangement(self, name: str) -> 'Clip':
        """Return a new clip with the specified arrangement name."""
        return Clip(
            name=self.name,
            position=self.position,
            duration=self.duration,
            color=self.color,
            source_path=self.source_path,
            volume=self.volume,
            muted=self.muted,
            arrangement_name=name,
            metadata=self.metadata.copy()
        )

    def with_metadata(self, key: str, value: Any) -> 'Clip':
        """Return a new clip with added metadata."""
        new_metadata = self.metadata.copy()
        new_metadata[key] = value
        return Clip(
            name=self.name,
            position=self.position,
            duration=self.duration,
            color=self.color,
            source_path=self.source_path,
            volume=self.volume,
            muted=self.muted,
            arrangement_name=self.arrangement_name,
            metadata=new_metadata
        )

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key."""
        return self.metadata.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Convert clip to dictionary representation."""
        return {
            'name': self.name,
            'position': self.position,
            'duration': self.duration,
            'color': self.color,
            'source_path': str(self.source_path),
            'volume': self.volume,
            'muted': self.muted,
            'arrangement_name': self.arrangement_name,
            'metadata': self.metadata
        }

    def from_dict(cls, data: Dict[str, Any]) -> 'Clip':
        """Create clip from dictionary representation."""
        data = data.copy()
        data['source_path'] = Path(data['source_path'])
        return cls(**data)
```
---

#### src\fl2cu\models\project.py
```
# fl2cu/models/project.py
from pathlib import Path
from typing import List, Optional, Dict, Any, Set

from fl2cu.models.base import BaseProject
from fl2cu.models.arrangement import Arrangement

class Project(BaseProject):
    """Project class extending base functionality."""
    def __init__(
        self,
        name: str,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        super().__init__(name, source_path, output_dir)
        
    def add_arrangement(self, arrangement: Arrangement) -> None:
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)
        
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

#### src\fl2cu\utils\__init__.py
```
# fl2cu/utils/__init__.py
"""Utility functions and helpers."""
from fl2cu.utils.file_manager import FileManager
from fl2cu.utils.logger import setup_logger, get_logger

__all__ = ['FileManager', 'setup_logger', 'get_logger']
```
---

#### src\fl2cu\utils\file_manager.py
```
# src/fl2cu/utils/file_manager.py

from pathlib import Path
from typing import Dict, Union

from ..models.project import Project
from ..models.arrangement import Arrangement
from .logger import get_logger

class FileManager:
    """Manages file system operations for the project."""
    
    def __init__(self, output_dir: Union[str, Path]) -> None:
        self.base_dir = Path(output_dir)
        self.logger = get_logger()

    def _sanitize_path(self, name: str) -> str:
        # Replace invalid characters with underscores
        invalid_chars = '<>:"/\\|?*'
        sanitized = ''.join('_' if c in invalid_chars else c for c in name)
        return sanitized.strip()

    def create_directory_structure(self, project: Project) -> Dict[Arrangement, Path]:
        arrangement_dirs = {}
        
        try:
            # Create base project directory
            project_dir = self.base_dir / self._sanitize_path(project.name)
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Create directories for each arrangement
            for arrangement in project.arrangements:
                arr_dir = project_dir / self._sanitize_path(arrangement.name)
                arr_dir.mkdir(exist_ok=True)
                
                # Create audio files directory
                audio_dir = arr_dir / "audio_files"
                audio_dir.mkdir(exist_ok=True)
                
                arrangement_dirs[arrangement] = arr_dir
                
            self.logger.info(f"Created directory structure in {self.base_dir}")
            return arrangement_dirs
            
        except Exception as e:
            self.logger.error(f"Failed to create directory structure: {e}")
            raise OSError(f"Failed to create directory structure: {e}")

    def cleanup_temp_files(self, temp_dir: Union[str, Path]) -> None:
        try:
            shutil.rmtree(temp_dir)
            self.logger.info(f"Cleaned up temporary files in {temp_dir}")
        except Exception as e:
            self.logger.warning(f"Failed to clean up temporary files: {e}")

    def validate_paths(self) -> bool:
        try:
            self.base_dir.mkdir(parents=True, exist_ok=True)
            return self.base_dir.exists() and self.base_dir.is_dir()
        except Exception as e:
            self.logger.error(f"Path validation failed: {e}")
            return False
```
---

#### src\fl2cu\utils\logger.py
```
# src/fl2cu/utils/logger.py
from pathlib import Path
from typing import Optional

def setup_logger(log_file: Optional[Path] = None) -> logging.Logger:
    """Set up and configure logger.
    
    Args:
        log_file: Optional path to log file. If None, logs to console only.
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('fl2cu')
    
    if not logger.handlers:  # Only add handlers if none exist
        logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler (if requested)
        if log_file is not None:
            try:
                log_file = Path(log_file)
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(str(log_file))
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
    return logging.getLogger('fl2cu')

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

