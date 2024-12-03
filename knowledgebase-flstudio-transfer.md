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

#### knowledgebase\dawproject\dawproject-README.md
# DAWproject

Open exchange format for user data between Digital Audio Workstations (DAWs)

## Motivation

The DAWproject format provides a (vendor-agnostic) way of transferring user data between different music applications (DAWs).

Currently, there is no file-format which is purpose-built for this task.
Standard MIDI files can represent note data, but it is often a lower-level representation (no ramps) of data than what the DAW uses internally, which forces consolidation on export. AAF only covers audio and doesn't have any concept of musical-time, which limits it to post-audio workflows . Most plug-ins do allow you to save presets to a shared location, but this has to be done for each instance. What most users end up doing is just exporting audio as stems.

The aim of this project is to export all translatable project data (audio/note/automation/plug-in) along with the structure surrounding it into a single DAWproject file.

The table below aims to explain the scope format from a music-production perspective and how it compares to other methods of data transfer.

|                                 |                                                               DAWproject                                                               |                      Standard MIDI Files                      |                    Advanced Authoring Format (AAF)                    |
|---------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------:|:---------------------------------------------------------------------:|
| Intended Use                    |                                                            Music Production                                                            |                        MIDI Sequencing                        |                         Video Post-Production                         |
| Time Format<br/>(seconds/beats) |                                                   Beats and seconds can be combined                                                    |                             Beats                             |                                Seconds                                |
| Audio                           |                  Audio<br/>Events/Clips<br/>Fades<br/>Crossfades<br/>Amplitude<br/>Pan<br/>Time Warping<br/>Transpose                  |                               -                               | Audio<br/>Events/Clips<br/>Fades<br/>Crossfades<br/>Amplitude<br/>Pan |
| Notes                           |                                                       Notes<br/>Note Expressions                                                       |                             Notes                             |                                   -                                   |
| Automation                      | Tempo<br/>Time Signature<br/>MIDI Messages<br/>Volume<br/>Pan<br/>Mute<br/>Sends<br/>Plug-in Parameters<br/>Built-in Device Parameters | Tempo<br/>Time Signature<br/>MIDI Messages<br/>SysEx Messages |              Volume<br/>Pan<br/>Video Related Parameters              |
| Plug-ins                        |                                       Stores full plug-in state<br/>and automation of parameters                                       |                               -                               |                                   -                                   |
| Built-in Devices                |                                 Generic EQ<br/>Generic Compressor<br/>Generic Gate<br/>Generic Limiter                                 |                               -                               |                                   -                                   |
| Clip Launcher                   |                                                            Clips<br/>Scenes                                                            |                               -                               |                                   -                                   |

## Status

The format is version 1.0 and is stable. 

## Goals

* Package all user data of a project/song into a single file.
  * Audio timeline data
  * Note timeline data
  * Note expression data
  * Automation timeline data
  * Audio data (embedded or referenced)
  * Plug-in states (always embedded)
* The format should be able to preserve as much user created data as feasible.
* The format should be able to express the track and timeline structures of the exporting DAW as is, leaving it up to the importer to use this data and flatten it as needed.
* Simple to implement
* Built upon established open standards
* Language agnostic, no special dependencies
* Open & free

## Non-goals

* Being the native file-format for a DAW
* Optimal performance (like a binary format could provide)
* Storing low-level MIDI events directly (but rather relying on higher level abstractions)
* Storing non-session data (view settings, preferences) 

## Format Specification

* File Extension: .dawproject
* Container: ZIP
* Format: XML (project.xml, metadata.xml)
* Text encoding: UTF-8
* The exporting DAW is free to choose the directory structure it wants for media and plug-in files.

* [DAWproject XML Reference](https://htmlpreview.github.io/?https://github.com/bitwig/dawproject/blob/main/Reference.html)
* [Project XML Schema](Project.xsd)
* [MetaData XML Schema](MetaData.xsd)

## Language Support

DAWproject is based on plain XML/ZIP and can be used with any programming language that can parse those.

The DOM of DAWproject is defined by a set of Java classes which have XML-related annotations and HTML-induced Javadoc comments.
Those are used (via reflection) to generate XML Documentation and Schemas. Potentially, the same approach could be used to generate code for other languages (contributions welcome).

## Building the Library, Documentation and Tests

Requires Java Runtime version 16 or later.

To build (using Gradle):

```
./gradlew build
```

## Example project

The exporting application is free to structure tracks and timelines in a way that fits its internal model.
The choice is left to the importing application to either use the level of structure provided (if applicable) or to flatten/convert it to match its model. 

As an example, here's the project.xml of a simple file saved in Bitwig Studio 5.0 with one instrument track and one audio track. As the audio clips in Bitwig Studio are themselves a timeline of audio events, you will notice that there are two levels of <Clips> elements, id25 representing the clip timeline on the arrangement, and id26 representing the  audio events inside the clip.

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Project version="1.0">
  <Application name="Bitwig Studio" version="5.0"/>
  <Transport>
    <Tempo max="666.000000" min="20.000000" unit="bpm" value="149.000000" id="id0" name="Tempo"/>
    <TimeSignature denominator="4" numerator="4" id="id1"/>
  </Transport>
  <Structure>
    <Track contentType="notes" loaded="true" id="id2" name="Bass" color="#a2eabf">
      <Channel audioChannels="2" destination="id15" role="regular" solo="false" id="id3">
        <Devices>
          <ClapPlugin deviceID="org.surge-synth-team.surge-xt" deviceName="Surge XT" deviceRole="instrument" loaded="true" id="id7" name="Surge XT">
            <Parameters/>
            <Enabled value="true" id="id8" name="On/Off"/>
            <State path="plugins/d19b1f6e-bbb6-42fe-a6c9-54b41d97a05d.clap-preset"/>
          </ClapPlugin>
        </Devices>
        <Mute value="false" id="id6" name="Mute"/>
        <Pan max="1.000000" min="0.000000" unit="normalized" value="0.500000" id="id5" name="Pan"/>
        <Volume max="2.000000" min="0.000000" unit="linear" value="0.659140" id="id4" name="Volume"/>
      </Channel>
    </Track>
    <Track contentType="audio" loaded="true" id="id9" name="Drumloop" color="#b53bba">
      <Channel audioChannels="2" destination="id15" role="regular" solo="false" id="id10">
        <Mute value="false" id="id13" name="Mute"/>
        <Pan max="1.000000" min="0.000000" unit="normalized" value="0.500000" id="id12" name="Pan"/>
        <Volume max="2.000000" min="0.000000" unit="linear" value="0.177125" id="id11" name="Volume"/>
      </Channel>
    </Track>
    <Track contentType="audio notes" loaded="true" id="id14" name="Master">
      <Channel audioChannels="2" role="master" solo="false" id="id15">
        <Mute value="false" id="id18" name="Mute"/>
        <Pan max="1.000000" min="0.000000" unit="normalized" value="0.500000" id="id17" name="Pan"/>
        <Volume max="2.000000" min="0.000000" unit="linear" value="1.000000" id="id16" name="Volume"/>
      </Channel>
    </Track>
  </Structure>
  <Arrangement id="id19">
    <Lanes timeUnit="beats" id="id20">
      <Lanes track="id2" id="id21">
        <Clips id="id22">
          <Clip time="0.0" duration="8.0" playStart="0.0">
            <Notes id="id23">
              <Note time="0.000000" duration="0.250000" channel="0" key="65" vel="0.787402" rel="0.787402"/>
              <Note time="1.000000" duration="0.250000" channel="0" key="65" vel="0.787402" rel="0.787402"/>
              <Note time="4.000000" duration="0.250000" channel="0" key="65" vel="0.787402" rel="0.787402"/>
              <Note time="5.000000" duration="0.250000" channel="0" key="65" vel="0.787402" rel="0.787402"/>
              <Note time="0.500000" duration="0.250000" channel="0" key="64" vel="0.787402" rel="0.787402"/>
              <Note time="4.500000" duration="0.250000" channel="0" key="64" vel="0.787402" rel="0.787402"/>
              <Note time="1.500000" duration="2.500000" channel="0" key="53" vel="0.787402" rel="0.787402"/>
              <Note time="5.500000" duration="0.250000" channel="0" key="53" vel="0.787402" rel="0.787402"/>
              <Note time="6.000000" duration="2.000000" channel="0" key="53" vel="0.787402" rel="0.787402"/>
            </Notes>
          </Clip>
        </Clips>
      </Lanes>
      <Lanes track="id9" id="id24">
        <Clips id="id25">
          <Clip time="0.0" duration="8.00003433227539" playStart="0.0" loopStart="0.0" loopEnd="8.00003433227539" fadeTimeUnit="beats" fadeInTime="0.0" fadeOutTime="0.0" name="Drumfunk3 170bpm">
            <Clips id="id26">
              <Clip time="0.0" duration="8.00003433227539" contentTimeUnit="beats" playStart="0.0" fadeTimeUnit="beats" fadeInTime="0.0" fadeOutTime="0.0">
                <Warps contentTimeUnit="seconds" timeUnit="beats" id="id28">
                  <Audio algorithm="stretch" channels="2" duration="2.823541666666667" sampleRate="48000" id="id27">
                    <File path="audio/Drumfunk3 170bpm.wav"/>
                  </Audio>
                  <Warp time="0.0" contentTime="0.0"/>
                  <Warp time="8.00003433227539" contentTime="2.823541666666667"/>
                </Warps>
              </Clip>
            </Clips>
          </Clip>
        </Clips>
      </Lanes>
      <Lanes track="id14" id="id29">
        <Clips id="id30"/>
      </Lanes>
    </Lanes>
  </Arrangement>
  <Scenes/>
</Project>
```

## DAW Support

DAWproject 1.0 is currently supported by the following DAWs

* Bitwig Studio 5.0.9
* PreSonus Studio One 6.5
* Steinberg Cubase 14

## Converters

There are various tools that can convert from and to DAWproject files

* https://github.com/SatyrDiamond/DawVert: various formats
* https://github.com/git-moss/ProjectConverter: Cockos Reaper
---

#### master-plan.md
# FL Studio to Cubase Migration Tool

## Overview
A Python-based tool to accurately transfer audio arrangements from FL Studio to Cubase while preserving clip positions, colors, and organization across multiple arrangements. Uses "DAWProject" as an intermediate format for debugging and validation.

## Objectives
- Maintain precise clip positions and timing
- Preserve color coding for visual organization
- Support multiple arrangements with folder structure
- Automate the export process to minimize manual work
- Handle large projects (~1000 clips) efficiently
- Enable easy troubleshooting of conversion issues

## Technical Stack
- Core: Python 3.8+
- FL Studio Project Parsing: PyFLP library
- Audio Processing: Direct file operations
- Export Format: DAWProject
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
- Generate detailed debug logs during parsing

### 2. Audio Export System
- Batch audio file export
- Maintain original audio quality
- Preserve exact clip boundaries
- Support for multiple arrangements
- Audio file validation and verification

### 3. DAWProject Generation
- Create DAWProject files containing:
  - Clip positions
  - Color information
  - Track organization
  - Timing metadata
  - Audio file references
  - Debug information
- DAWProject should contain all arrangements

### 4. File Organization
- Create organized folder structure:
```
output/
  ├── sample_project.dawproject
  └── ...
```

## Development Phases

### Phase 1: Core Infrastructure
1. Set up PyFLP project parsing
2. Implement basic audio file extraction
3. Create folder structure management
4. Add comprehensive logging system
5. Implement DAWProject schema definition

### Phase 2: DAWProject Generation
1. Implement DAWProject metadata generation
2. Add clip position mapping
3. Integrate color preservation
4. Create track organization structure
5. Add debugging information
6. Validate DAWProject against schema

### Phase 3: Debugging & Validation
1. Add parser debug logs
2. Implement metadata validation
3. Create conversion verification tools
4. Add data integrity checks
5. Generate human-readable debug output

## Technical Considerations

### Performance
- Batch processing for large projects
- Efficient memory usage for 1000+ clips
- Progress tracking for long operations
- DAWProject generation optimization

### Error Handling
- Validate FL Studio project structure
- Check for missing audio files
- Handle corrupt project files
- Provide clear error messages
- Generate detailed debug logs

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
3. DAWProject file size may grow with project complexity
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
```
---

#### src\fl2cu\__main__.py
```
# src/fl2cu/__main__.py
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
from .dawproject_generator import DAWProjectGenerator

__all__ = ['FLProjectParser', 'AudioProcessor', 'DAWProjectGenerator']
```
---

#### src\fl2cu\core\audio_processor.py
```
from pathlib import Path
from typing import Dict, List, Optional

from ..models.clip import Clip

class AudioProcessor:

    def validate_audio_files(self, clips: List[Clip]) -> Dict[Clip, Path]:
        """Validate processed audio files."""
        valid_clips = {}
        
        for clip, path in self.process_audio_clips(clips).items():
            with wave.open(str(path), 'rb') as wav_file:
                # Verify it's standard PCM format
                if wav_file.getcomptype() == 'NONE':
                    valid_clips[clip] = path
                
        return valid_clips
```
---

#### src\fl2cu\core\dawproject_generator.py
```
from pathlib import Path
from typing import Dict, Optional, Any
from xml.etree import ElementTree as ET
from ..models.arrangement import Arrangement
from ..models.clip import Clip

class DAWProjectGenerator:
    """Generates DAWproject format ZIP containers with XML and audio files."""
    
    def __init__(self, arrangement: Arrangement, clip_paths: Dict[Clip, Path]):
        self.arrangement = arrangement
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def _probe_audio(self, path: str) -> Dict[str, Any]:
        """Get audio file metadata using ffprobe."""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-of', 'json',
            '-show_format',
            '-show_streams',
            str(path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ffprobe failed for {path}: {e.stderr}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse ffprobe output: {e}")
            raise

    def _create_project_xml(self) -> ET.Element:
        """Create the project.xml content."""
        # Create root Project element
        root = ET.Element("Project", version="1.0")
        
        # Add Application metadata
        app = ET.SubElement(root, "Application", name="FL Studio Converter", version="1.0")
        
        # Create Transport element for tempo/time signature
        transport = ET.SubElement(root, "Transport")
        tempo = ET.SubElement(transport, "Tempo", unit="bpm", value="120", min="20", max="999")
        time_sig = ET.SubElement(transport, "TimeSignature", numerator="4", denominator="4")
        
        # Create Structure section
        structure = ET.SubElement(root, "Structure")
        
        # Create audio track
        track = ET.SubElement(structure, "Track", 
                            contentType="audio",
                            loaded="true",
                            id=f"track-{self.arrangement.name}",
                            name=self.arrangement.name)
        
        # Create channel for the track
        channel = ET.SubElement(track, "Channel",
                              audioChannels="2",
                              role="regular",
                              solo="false",
                              id=f"channel-{self.arrangement.name}")
        
        # Add standard channel controls
        ET.SubElement(channel, "Volume", value="1.0", min="0.0", max="2.0", unit="linear")
        ET.SubElement(channel, "Pan", value="0.5", min="0.0", max="1.0", unit="normalized")
        ET.SubElement(channel, "Mute", value="false")

        # Create Arrangement section
        arrangement = ET.SubElement(root, "Arrangement", id="main-arrangement")
        
        # Create Lanes section
        lanes = ET.SubElement(arrangement, "Lanes", timeUnit="beats")
        
        # Create track lanes
        track_lanes = ET.SubElement(lanes, "Lanes", track=f"track-{self.arrangement.name}")
        
        # Create clips container
        clips = ET.SubElement(track_lanes, "Clips")

        # Process each audio clip
        for clip in self.arrangement.clips:
            source_path = self.clip_paths.get(clip)
            if not source_path or not source_path.exists():
                self.logger.warning(f"Audio file not found for clip: {clip.name}")
                continue

            try:
                # Get audio metadata
                metadata = self._probe_audio(str(source_path))
                stream = metadata['streams'][0]
                
                # Create clip element
                clip_el = ET.SubElement(clips, "Clip",
                                      time=str(clip.position),
                                      duration=str(clip.duration),
                                      name=clip.name)
                
                # Create audio within clip
                audio = ET.SubElement(clip_el, "Audio",
                                    channels=str(stream.get('channels', 2)),
                                    duration=str(stream.get('duration', clip.duration)),
                                    sampleRate=str(stream.get('sample_rate', 44100)))
                
                # Add file reference - use relative path within ZIP
                audio_rel_path = f"audio/{clip.name}.wav"
                file_ref = ET.SubElement(audio, "File", path=audio_rel_path)
                
                self.logger.debug(f"Added clip {clip.name} at position {clip.position}")

            except Exception as e:
                self.logger.error(f"Failed to process clip {clip.name}: {str(e)}")
                raise

        return root

    def _create_metadata_xml(self) -> ET.Element:
        """Create the metadata.xml content."""
        root = ET.Element("MetaData")
        ET.SubElement(root, "Title").text = self.arrangement.name
        return root

    def generate_dawproject(self, output_path: str) -> None:
        """Generate DAWproject file (ZIP container with XML and audio)."""
        self.logger.info(f"Creating DAWproject file at {output_path}")
        
        try:
            # Create a temporary directory for preparing files
            temp_dir = Path(output_path).parent / f"temp_{self.arrangement.name}"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                # Create project.xml
                project_xml = self._create_project_xml()
                xml_str = ET.tostring(project_xml, encoding='unicode', method='xml')
                with open(temp_dir / "project.xml", 'w', encoding='utf-8') as f:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    f.write(xml_str)

                # Create metadata.xml
                metadata_xml = self._create_metadata_xml()
                xml_str = ET.tostring(metadata_xml, encoding='unicode', method='xml')
                with open(temp_dir / "metadata.xml", 'w', encoding='utf-8') as f:
                    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    f.write(xml_str)

                # Create audio directory and copy files
                audio_dir = temp_dir / "audio"
                audio_dir.mkdir(exist_ok=True)
                
                for clip, source_path in self.clip_paths.items():
                    if clip in self.arrangement.clips:
                        dest_path = audio_dir / f"{clip.name}.wav"
                        shutil.copy2(source_path, dest_path)

                # Create ZIP file
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    # Add XML files
                    zf.write(temp_dir / "project.xml", "project.xml")
                    zf.write(temp_dir / "metadata.xml", "metadata.xml")
                    
                    # Add audio files
                    for audio_file in audio_dir.glob("*.wav"):
                        zf.write(audio_file, f"audio/{audio_file.name}")

                self.logger.info("DAWproject file successfully generated")

            finally:
                # Clean up temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)

        except Exception as e:
            self.logger.error(f"Failed to generate DAWproject file: {str(e)}")
            raise
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

