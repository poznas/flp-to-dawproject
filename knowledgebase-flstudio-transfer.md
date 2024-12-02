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
Classifier: Topic :: Text Processing :: Markup :: XML
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.8
Classifier: License :: OSI Approved :: MIT License
Classifier: Operating System :: OS Independent
Requires-Python: >=3.8
Description-Content-Type: text/markdown
Requires-Dist: pyflp>=2.0.0
Requires-Dist: construct>=2.10.0
Requires-Dist: wave>=0.0.2
Requires-Dist: numpy>=1.21.0
Requires-Dist: lxml>=4.9.0
Requires-Dist: xmlschema>=2.5.0
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
Requires-Dist: pytest-xsd>=0.4.0; extra == "dev"
Requires-Dist: types-tqdm>=4.65.0; extra == "dev"
Requires-Dist: types-setuptools>=68.0.0; extra == "dev"
Requires-Dist: types-lxml>=4.9.0; extra == "dev"
Requires-Dist: sphinx>=7.1.0; extra == "dev"
Requires-Dist: sphinx-rtd-theme>=2.0.0; extra == "dev"

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
```
---

#### src\flstudio_cubase_migration.egg-info\SOURCES.txt
```
README.md
pyproject.toml
setup.py
src/fl2cu/__init__.py
src/fl2cu/__main__.py
src/fl2cu/config.py
src/fl2cu/core/__init__.py
src/fl2cu/core/aaf_generator.py
src/fl2cu/core/audio_processor.py
src/fl2cu/core/project_parser.py
src/fl2cu/core/xml_generator.py
src/fl2cu/models/__init__.py
src/fl2cu/models/arrangement.py
src/fl2cu/models/base.py
src/fl2cu/models/clip.py
src/fl2cu/models/project.py
src/fl2cu/utils/__init__.py
src/fl2cu/utils/file_manager.py
src/fl2cu/utils/logger.py
src/flstudio_cubase_migration.egg-info/PKG-INFO
src/flstudio_cubase_migration.egg-info/SOURCES.txt
src/flstudio_cubase_migration.egg-info/dependency_links.txt
src/flstudio_cubase_migration.egg-info/entry_points.txt
src/flstudio_cubase_migration.egg-info/requires.txt
src/flstudio_cubase_migration.egg-info/top_level.txt
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
fl2cubase = flstudio_cubase_migration.cli:main
```
---

#### src\flstudio_cubase_migration.egg-info\requires.txt
```
pyflp>=2.0.0
construct>=2.10.0
wave>=0.0.2
numpy>=1.21.0
lxml>=4.9.0
xmlschema>=2.5.0
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
pytest-xsd>=0.4.0
types-tqdm>=4.65.0
types-setuptools>=68.0.0
types-lxml>=4.9.0
sphinx>=7.1.0
sphinx-rtd-theme>=2.0.0
```
---

#### src\flstudio_cubase_migration.egg-info\top_level.txt
```
fl2cu
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

def generate_sine_wave():
    """Generate sine wave for testing."""
    def _generate(frequency=440.0, duration=1.0, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration))
        samples = np.sin(2 * np.pi * frequency * t)
        return (samples * 32767).astype(np.int16)
    return _generate

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

def sample_wav_file(tmp_path, generate_sine_wave):
    """Create test WAV file with known content."""
    wav_path = tmp_path / "test.wav"
    samples = generate_sine_wave()
    
    with wave.open(str(wav_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(samples.tobytes())
    
    return wav_path

def sample_clip(sample_wav_file):
    """Create test clip with known audio."""
    return Clip(
        name="test_clip",
        position=0.0,
        duration=1.0,
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

def flp_file_content():
    """Generate minimal valid FLP file content."""
    header = (
        b"FLhd"  # Magic
        b"\x06\x00\x00\x00"  # Header size
        b"\x00\x00"  # Format version
        b"\x01\x00"  # Number of channels
        b"\x60\x00"  # PPQ (96)
    )
    
    data = (
        b"FLdt"  # Data chunk magic
        b"\x00\x00\x00\x00"  # Empty data chunk
    )
    
    return header + data

def sample_project_path(tmp_path, flp_file_content):
    """Create sample FLP file for testing."""
    project_file = tmp_path / "test_project.flp"
    project_file.write_bytes(flp_file_content)
    return project_file
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
        clip = Clip(
            name="volume_test",
            position=0.0,
            duration=1.0,
            color="#FF0000",
            source_path=sample_wav_file,
            volume=0.5
        )

        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        exported_path = result[clip]

        # Read and compare audio data as float32 for accurate comparison
        with wave.open(str(sample_wav_file), 'rb') as original:
            orig_frames = np.frombuffer(original.readframes(original.getnframes()), dtype=np.int16)
            orig_float = orig_frames.astype(np.float32) / 32767.0

        with wave.open(str(exported_path), 'rb') as exported:
            exported_frames = np.frombuffer(exported.readframes(exported.getnframes()), dtype=np.int16)
            exported_float = exported_frames.astype(np.float32) / 32767.0

        # Compare using relative tolerance
        assert np.allclose(exported_float, orig_float * 0.5, rtol=1e-3)

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
        # Add some metadata to test
        sample_clip = sample_clip.with_metadata('test_key', 'test_value')
        
        data = sample_clip.to_dict()
        restored_clip = Clip.from_dict(data)
        
        assert restored_clip == sample_clip
        assert restored_clip.get_metadata('test_key') == 'test_value'

    def test_clip_metadata(self, sample_clip):
        """Test metadata operations."""
        # Add metadata
        clip_with_meta = sample_clip.with_metadata('key1', 'value1')
        clip_with_more = clip_with_meta.with_metadata('key2', 'value2')
        
        assert clip_with_more.get_metadata('key1') == 'value1'
        assert clip_with_more.get_metadata('key2') == 'value2'
        assert clip_with_more.get_metadata('nonexistent') is None
        assert clip_with_more.get_metadata('nonexistent', 'default') == 'default'

    def test_clip_immutability(self, sample_clip):
        """Test that clip is immutable."""
        with pytest.raises(dataclasses.FrozenInstanceError):
            sample_clip.name = "new_name"

        with pytest.raises(dataclasses.FrozenInstanceError):
            sample_clip.position = 2.0

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
        assert arr.clips[0].arrangement_name == "TEST_ARR"
        
        # Basic equality should ignore arrangement name
        assert arr.clips[0] == sample_clip
        
        # Full equality should consider arrangement name
        assert not arr.clips[0].full_equals(sample_clip)
        
        # Remove clip
        arr.remove_clip(sample_clip)
        assert len(arr.clips) == 0

    def test_get_clip_by_name(self, sample_clip):
        """Test finding clips by name."""
        arr = Arrangement(name="TEST_ARR")
        arr.add_clip(sample_clip)
        
        found_clip = arr.get_clip_by_name(sample_clip.name)
        assert found_clip is not None
        assert found_clip == sample_clip
        
        assert arr.get_clip_by_name("nonexistent") is None

    def test_get_duration(self, sample_clip):
        """Test arrangement duration calculation."""
        arr = Arrangement(name="TEST_ARR")
        assert arr.get_duration() == 0.0
        
        arr.add_clip(sample_clip)  # At position 0.0
        assert arr.get_duration() == sample_clip.duration
        
        # Add another clip that extends beyond
        clip2 = Clip(
            name="clip2", 
            position=1.5, 
            duration=2.0, 
            color="#00FF00"
        )
        arr.add_clip(clip2)
        assert arr.get_duration() == 3.5  # 1.5 + 2.0

    def test_arrangement_validation(self, sample_clip):
        """Test arrangement validation."""
        arr = Arrangement(name="TEST_ARR")
        
        # Empty name
        with pytest.raises(ValueError, match="cannot be empty"):
            Arrangement(name="")
        
        # Duplicate clip names
        arr.add_clip(sample_clip)
        duplicate = Clip(
            name=sample_clip.name,
            position=1.0,
            duration=1.0,
            color="#00FF00"
        )
        
        with pytest.raises(ValueError, match="Duplicate clip names"):
            arr.add_clip(duplicate)
            arr.validate()

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

    def test_get_arrangement_by_name(self, sample_arrangement):
        """Test finding arrangements by name."""
        project = Project(name="test_project")
        project.add_arrangement(sample_arrangement)
        
        found = project.get_arrangement_by_name(sample_arrangement.name)
        assert found is not None
        assert found == sample_arrangement
        
        assert project.get_arrangement_by_name("nonexistent") is None

    def test_validate_audio_files(self, sample_project, sample_wav_file):
        """Test audio file validation."""
        assert sample_project.validate_audio_files() == True
        
        # Test with missing file
        sample_wav_file.unlink()
        assert sample_project.validate_audio_files() == False

    def test_project_validation(self, sample_arrangement):
        """Test project validation."""
        project = Project(name="test_project")
        
        # Empty name
        with pytest.raises(ValueError, match="cannot be empty"):
            Project(name="")
        
        # Duplicate arrangement names
        project.add_arrangement(sample_arrangement)
        duplicate = Arrangement(name=sample_arrangement.name)
        
        with pytest.raises(ValueError, match="Duplicate arrangement names"):
            project.add_arrangement(duplicate)
            project.validate()

    def test_get_all_clip_paths(self, sample_project, sample_wav_file):
        """Test collecting all unique audio file paths."""
        paths = sample_project.get_all_clip_paths()
        assert len(paths) > 0
        assert sample_wav_file in paths
```
---

#### tests\test_project_parser.py
```
from pathlib import Path
from unittest.mock import Mock, patch

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

