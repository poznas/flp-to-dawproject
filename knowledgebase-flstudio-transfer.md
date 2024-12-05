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
    '.jar', '.bat', '.json', '.xml', '.kts', '.xsd', '.bat'      
    
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

#### src\fl2cu\__init__.py
```

```
---

#### src\fl2cu\__main__.py
```
# src/fl2cu/main.py
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
        clip_paths = {clip: clip.source_path 
                     for arr in project.arrangements 
                     for clip in arr.clips}
        
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
```
---

#### src\fl2cu\generator\audio_utils.py
```
from pathlib import Path
from typing import Dict, Any, Optional

class AudioAnalyzer:
    """Handles audio file analysis and metadata extraction."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_audio_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get audio file metadata using ffprobe."""
        if not file_path.exists():
            self.logger.error(f"Audio file not found: {file_path}")
            return None
            
        try:
            result = subprocess.run([
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(file_path)
            ], capture_output=True, text=True, check=True)
            
            data = json.loads(result.stdout)
            
            # Extract relevant metadata
            audio_stream = next(
                (s for s in data.get('streams', []) if s.get('codec_type') == 'audio'),
                None
            )
            
            if not audio_stream:
                self.logger.error(f"No audio stream found in {file_path}")
                return None
                
            return {
                'channels': int(audio_stream.get('channels', 2)),
                'sample_rate': int(audio_stream.get('sample_rate', 44100)),
                'duration': float(audio_stream.get('duration', 0.0)),
                'bit_depth': int(audio_stream.get('bits_per_sample', 16)),
                'codec': audio_stream.get('codec_name', 'pcm_s16le')
            }
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ffprobe failed for {file_path}: {e.stderr}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse ffprobe output: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error analyzing audio file {file_path}: {e}")
            return None

class AudioProcessor:
    """Handles audio file processing and conversion."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analyzer = AudioAnalyzer()

    def process_audio_file(
        self,
        source_path: Path,
        dest_path: Path,
        target_sample_rate: int = 44100,
        target_bit_depth: int = 24
    ) -> bool:
        """Process audio file ensuring consistent format."""
        try:
            # Get source metadata
            metadata = self.analyzer.get_audio_metadata(source_path)
            if not metadata:
                return False

            # Check if conversion is needed
            if (metadata['sample_rate'] == target_sample_rate and 
                metadata['bit_depth'] == target_bit_depth):
                # Just copy file if no conversion needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                dest_path.write_bytes(source_path.read_bytes())
                return True

            # Convert audio
            result = subprocess.run([
                'ffmpeg',
                '-i', str(source_path),
                '-ar', str(target_sample_rate),
                '-c:a', f'pcm_s{target_bit_depth}le',
                '-y',  # Overwrite output file
                str(dest_path)
            ], capture_output=True, text=True, check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Audio processing failed for {source_path}: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error processing audio file {source_path}: {e}")
            return False
```
---

#### src\fl2cu\generator\dawproject_generator.py
```
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Optional

from ..generator.xml_utils import XMLWriter

from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..models.timing import ProjectTiming
from .xml_builder import XMLBuilder

class DAWProjectGenerator:
    def __init__(self, arrangements: List[Arrangement], clip_paths: Dict[Clip, Path]):
        self.arrangements = arrangements
        self.clip_paths = clip_paths
        self.logger = logging.getLogger(__name__)

    def generate_dawproject(self, output_path: str) -> None:
        try:
            temp_dir = Path(output_path).parent / "temp_dawproject"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                # Generate XML files
                self._generate_xml_files(temp_dir)
                
                # Copy and process audio files
                self._process_audio_files(temp_dir)
                
                # Create final ZIP archive
                self._create_archive(temp_dir, output_path)
                
                self.logger.info(f"Successfully generated DAWproject at {output_path}")
                
            finally:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)
                    
        except Exception as e:
            self.logger.error(f"Failed to generate DAWproject: {e}")
            raise

    def _generate_xml_files(self, temp_dir: Path) -> None:
        # Generate project.xml
        project_xml = self._create_project_xml()
        project_path = temp_dir / "project.xml"
        XMLWriter.write_xml(project_xml, project_path)
        
        # Generate metadata.xml
        metadata_xml = self._create_metadata_xml()
        metadata_path = temp_dir / "metadata.xml"
        XMLWriter.write_xml(metadata_xml, metadata_path)

    def _create_project_xml(self) -> ET.Element:
        root = ET.Element("Project", version="1.0")
        
        # Add Application info
        ET.SubElement(root, "Application", name="FL Studio Converter", version="1.0")
        
        # Add Transport section
        if self.arrangements and hasattr(self.arrangements[0], 'project'):
            timing = self.arrangements[0].project.timing
            root.append(XMLBuilder.create_transport_element(timing))
        
        # Add Structure section
        structure = ET.SubElement(root, "Structure")
        
        # Add tracks for each arrangement
        for i, arr in enumerate(self.arrangements):
            structure.append(XMLBuilder.create_track_element(arr.name, i))
        
        # Add Arrangements
        for i, arr in enumerate(self.arrangements):
            arr_element = ET.SubElement(root, "Arrangement", id=f"arrangement-{i}")
            lanes = ET.SubElement(arr_element, "Lanes", timeUnit="beats", id=f"lanes-{i}")
            track_lanes = ET.SubElement(lanes, "Lanes", track=f"track-{i}", id=f"track-lanes-{i}")
            clips = ET.SubElement(track_lanes, "Clips", id=f"clips-{i}")
            
            for clip in arr.clips:
                clip_el = XMLBuilder.create_clip_element(clip, self.clip_paths.get(clip))
                if clip_el is not None:
                    clips.append(clip_el)
        
        return root

    def _create_metadata_xml(self) -> ET.Element:
        root = ET.Element("MetaData")
        
        if self.arrangements:
            arr = self.arrangements[0]
            if hasattr(arr, 'project') and arr.project:
                ET.SubElement(root, "Title").text = arr.project.name
            else:
                ET.SubElement(root, "Title").text = arr.name
                
        return root

    def _process_audio_files(self, temp_dir: Path) -> None:
        audio_dir = temp_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        for clip, source_path in self.clip_paths.items():
            if source_path.exists():
                dest_path = audio_dir / f"{clip.name}.wav"
                shutil.copy2(source_path, dest_path)
            else:
                self.logger.warning(f"Audio file not found: {source_path}")

    def _create_archive(self, temp_dir: Path, output_path: str) -> None:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add XML files
            zf.write(temp_dir / "project.xml", "project.xml")
            zf.write(temp_dir / "metadata.xml", "metadata.xml")
            
            # Add audio files
            audio_dir = temp_dir / "audio"
            for audio_file in audio_dir.glob("*.wav"):
                zf.write(audio_file, f"audio/{audio_file.name}")
```
---

#### src\fl2cu\generator\xml_builder.py
```
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Optional

from ..models.arrangement import Arrangement
from ..models.clip import Clip
from ..models.timing import ProjectTiming

class XMLBuilder:
    def create_transport_element(timing: ProjectTiming) -> ET.Element:
        transport = ET.Element("Transport")
        ET.SubElement(transport, "Tempo",
            unit="bpm",
            value=str(timing.tempo),
            min="20",
            max="999",
            id="tempo"
        )
        ET.SubElement(transport, "TimeSignature",
            numerator=str(timing.time_signature_numerator),
            denominator=str(timing.time_signature_denominator),
            id="timesig"
        )
        return transport

    def create_track_element(name: str, index: int) -> ET.Element:
        track = ET.Element("Track",
            contentType="audio",
            loaded="true",
            id=f"track-{index}",
            name=name,
            color="#a2eabf"
        )
        
        # Add Channel
        channel = ET.SubElement(track, "Channel",
            audioChannels="2",
            role="regular",
            solo="false",
            id=f"channel-{index}"
        )
        
        # Add default channel controls
        ET.SubElement(channel, "Volume", value="1.0", min="0.0", max="2.0", unit="linear")
        ET.SubElement(channel, "Pan", value="0.5", min="0.0", max="1.0", unit="normalized")
        ET.SubElement(channel, "Mute", value="false")
        
        return track

    def create_clip_element(clip: Clip, clip_path: Path) -> Optional[ET.Element]:
        if not clip_path.exists():
            return None
            
        clip_el = ET.Element("Clip",
            time=str(clip.position),
            duration=str(clip.duration),
            name=clip.name
        )
        
        if clip.volume != 1.0:
            clip_el.set("level", str(clip.volume))
        if clip.muted:
            clip_el.set("enable", "false")
        
        warps = ET.SubElement(clip_el, "Warps",
            contentTimeUnit="seconds",
            timeUnit="beats"
        )
        
        audio = ET.SubElement(warps, "Audio",
            channels="2",
            duration=str(clip.duration),
            sampleRate="44100",
            algorithm="stretch"
        )
        
        ET.SubElement(audio, "File",
            path=f"audio/{clip.name}.wav"
        )
        
        # Add warp points for time stretching
        ET.SubElement(warps, "Warp", time="0.0", contentTime="0.0")
        ET.SubElement(warps, "Warp", time=str(clip.duration), contentTime=str(clip.duration))
        
        return clip_el
```
---

#### src\fl2cu\generator\xml_utils.py
```
from xml.etree import ElementTree as ET
from typing import Optional
from pathlib import Path

class XMLFormatter:
    """Handles XML formatting and pretty printing."""
    
    def format_xml(elem: ET.Element, level: int = 0, indent: str = "  ") -> None:
        """Format XML element with proper indentation."""
        i = "\n" + level * indent
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                XMLFormatter.format_xml(subelem, level + 1, indent)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

class XMLWriter:
    """Handles XML file writing with proper formatting."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def write_xml(
        self,
        element: ET.Element,
        output_path: Path,
        encoding: str = 'UTF-8',
        xml_declaration: bool = True
    ) -> bool:
        """Write formatted XML to file."""
        try:
            # Format the XML
            XMLFormatter.format_xml(element)
            
            # Convert to string
            xml_str = ET.tostring(element, encoding='unicode')
            
            # Write to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding=encoding) as f:
                if xml_declaration:
                    f.write(f'<?xml version="1.0" encoding="{encoding}"?>\n')
                f.write(xml_str)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write XML to {output_path}: {e}")
            return False
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
# src/fl2cu/models/base.py
from typing import List, Optional, Dict, Any, Set
from pathlib import Path
from .arrangement import Arrangement
from .timing import ProjectTiming

class BaseProject:
    """Base class containing core Project functionality."""
    def __init__(
        self,
        name: str,
        timing: Optional[ProjectTiming] = None,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        self.name = name
        self.timing = timing or ProjectTiming.default()
        self.source_path = Path(source_path) if source_path else None
        self.output_dir = Path(output_dir) if output_dir else None
        self._arrangements: List['Arrangement'] = []

    def arrangements(self) -> List['Arrangement']:
        """Get list of project arrangements."""
        return self._arrangements.copy()

    def add_arrangement(self, arrangement: 'Arrangement') -> None:
        """Add an arrangement to the project.
        
        Args:
            arrangement: Arrangement to add
            
        Raises:
            ValueError: If arrangement with same name already exists
        """
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)

    def remove_arrangement(self, arrangement: 'Arrangement') -> None:
        """Remove an arrangement from the project.
        
        Args:
            arrangement: Arrangement to remove
        """
        if arrangement in self._arrangements:
            self._arrangements.remove(arrangement)

    def validate(self) -> None:
        """Validate project integrity.
        
        Raises:
            ValueError: If validation fails
        """
        if not self.name:
            raise ValueError("Project name cannot be empty")
            
        if self.source_path and not isinstance(self.source_path, Path):
            raise TypeError("source_path must be a Path object")
            
        if self.output_dir and not isinstance(self.output_dir, Path):
            raise TypeError("output_dir must be a Path object")

        # Validate timing
        if not isinstance(self.timing, ProjectTiming):
            raise TypeError("timing must be a ProjectTiming object")
        if self.timing.tempo <= 0:
            raise ValueError("Project tempo must be positive")
            
        # Check for arrangement name uniqueness
        names = [arr.name for arr in self._arrangements]
        duplicate_names = set(name for name in names if names.count(name) > 1)
        if duplicate_names:
            raise ValueError(f"Duplicate arrangement names found: {', '.join(duplicate_names)}")

    def get_all_clip_paths(self) -> Set[Path]:  # Changed from set[Path] to Set[Path]
        """Get set of all unique audio file paths used in project."""
        paths = set()
        for arrangement in self._arrangements:
            for clip in arrangement.clips:
                if clip.source_path:
                    paths.add(clip.source_path)
        return paths

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format."""
        return {
            'name': self.name,
            'timing': self.timing.to_dict(),
            'source_path': str(self.source_path) if self.source_path else None,
            'output_dir': str(self.output_dir) if self.output_dir else None,
            'arrangements': [arr.to_dict() for arr in self._arrangements]
        }

    def from_dict(cls, data: Dict[str, Any]) -> 'BaseProject':
        """Create project instance from dictionary data."""
        timing_data = data.get('timing', {})
        timing = ProjectTiming(
            tempo=float(timing_data.get('tempo', {}).get('value', 120.0)),
            time_signature_numerator=int(timing_data.get('time_signature', {}).get('numerator', 4)),
            time_signature_denominator=int(timing_data.get('time_signature', {}).get('denominator', 4))
        )
        
        source_path = Path(data['source_path']) if data.get('source_path') else None
        output_dir = Path(data['output_dir']) if data.get('output_dir') else None
        
        return cls(
            name=data['name'],
            timing=timing,
            source_path=source_path,
            output_dir=output_dir
        )
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

#### src\fl2cu\models\timing.py
```
from dataclasses import dataclass
from typing import Optional

class ProjectTiming:
    """Represents project timing information."""
    tempo: float
    time_signature_numerator: int
    time_signature_denominator: int
    ppq: Optional[int] = None  # Pulses Per Quarter note

    def default() -> 'ProjectTiming':
        """Create default timing with 120 BPM and 4/4 time signature."""
        return ProjectTiming(
            tempo=120.0,
            time_signature_numerator=4,
            time_signature_denominator=4
        )

    def to_dict(self) -> dict:
        """Convert timing info to dictionary format."""
        return {
            'tempo': {
                'value': str(self.tempo),
                'min': '20',
                'max': '999',
                'unit': 'bpm'
            },
            'time_signature': {
                'numerator': str(self.time_signature_numerator),
                'denominator': str(self.time_signature_denominator)
            }
        }
```
---

#### src\fl2cu\parser\arrangement_parser.py
```
from typing import List, Optional

from ..models.arrangement import Arrangement
from .clip_parser import FLClipParser

class FLArrangementParser:
    """Handles parsing of FL Studio arrangements."""
    
    def __init__(self, fl_project: 'pyflp.Project', clip_parser: FLClipParser):
        self.fl_project = fl_project
        self.clip_parser = clip_parser
        self.logger = logging.getLogger(__name__)

    def parse_arrangements(self) -> List[Arrangement]:
        """Extract all arrangements from FL Studio project."""
        arrangements = []
        
        # Try FL Studio 12.9+ arrangements first
        if hasattr(self.fl_project, 'arrangements'):
            arrangements.extend(self._parse_native_arrangements())
        
        # Fall back to playlist if no arrangements found
        if not arrangements and hasattr(self.fl_project, 'playlist'):
            arrangement = self._parse_playlist_as_arrangement()
            if arrangement and arrangement.clips:
                arrangements.append(arrangement)
        
        return arrangements

    def _parse_native_arrangements(self) -> List[Arrangement]:
        arrangements = []
        for arr in self.fl_project.arrangements:
            if not arr.name:
                continue
            
            arrangement = Arrangement(name=arr.name)
            self._process_tracks(arrangement, arr.tracks)
            
            if arrangement.clips:
                arrangements.append(arrangement)
                
        return arrangements

    def _parse_playlist_as_arrangement(self) -> Optional[Arrangement]:
        arrangement = Arrangement(name=self.fl_project.name)
        
        for item in self.fl_project.playlist:
            if hasattr(item, 'channel'):
                clip = self.clip_parser.create_clip(item.channel, item.position)
                if clip:
                    arrangement.add_clip(clip)
                    
        return arrangement if arrangement.clips else None

    def _process_tracks(self, arrangement: Arrangement, tracks):
        for track in tracks:
            for item in track:
                if hasattr(item, 'channel'):
                    clip = self.clip_parser.create_clip(item.channel, item.position)
                    if clip:
                        arrangement.add_clip(clip)
```
---

#### src\fl2cu\parser\clip_parser.py
```
from pathlib import Path
from typing import Optional
from ..models.clip import Clip

class FLClipParser:
    """Handles parsing of audio clips from FL Studio channels."""
    
    def __init__(self, fl_project: 'pyflp.Project'):
        self.fl_project = fl_project
        self.ppq = getattr(fl_project, 'ppq', 96)
        self.logger = logging.getLogger(__name__)

    def create_clip(self, channel, position: float) -> Optional[Clip]:
        """Create clip from FL Studio channel."""
        if not hasattr(channel, 'sample_path'):
            return None

        try:
            source_path = Path(channel.sample_path)
            if not source_path.exists():
                self.logger.warning(f"Sample not found: {source_path}")
                return None

            name = getattr(channel, 'name', '') or source_path.stem
            position_seconds = float(position) / self.ppq
            duration = float(getattr(channel, 'sample_length', self.ppq)) / self.ppq
            
            # Get channel color
            color = self._get_color(channel)
            
            # Get volume normalized to 0-1
            volume = self._get_volume(channel)

            clip = Clip(
                name=f"{name}_{position}",
                position=position_seconds,
                duration=duration,
                color=color,
                source_path=source_path,
                volume=volume,
                muted=not bool(getattr(channel, 'enabled', True))
            )
            
            self.logger.debug(f"Created clip {clip.name} at {position_seconds}s")
            return clip

        except Exception as e:
            self.logger.error(f"Failed to create clip: {e}")
            return None

    def _get_color(self, channel) -> str:
        try:
            if hasattr(channel, 'color'):
                color = channel.color
                if hasattr(color, 'r'):
                    return f"#{color.r:02x}{color.g:02x}{color.b:02x}"
                elif isinstance(color, int):
                    r = (color >> 16) & 255
                    g = (color >> 8) & 255
                    b = color & 255
                    return f"#{r:02x}{g:02x}{b:02x}"
        except Exception as e:
            self.logger.warning(f"Failed to get color: {e}")
        return "#FFFFFF"

    def _get_volume(self, channel) -> float:
        try:
            if hasattr(channel, 'volume'):
                raw_volume = float(channel.volume)
                return raw_volume / 100.0 if raw_volume > 1.0 else raw_volume
        except Exception as e:
            self.logger.warning(f"Failed to get volume: {e}")
        return 1.0
```
---

#### src\fl2cu\parser\pattern_parser.py
```
from typing import List, Optional
from ..models.clip import Clip
from .clip_parser import FLClipParser

class FLPatternParser:
    """Handles parsing of patterns from FL Studio projects."""
    
    def __init__(self, fl_project: 'pyflp.Project', clip_parser: FLClipParser):
        self.fl_project = fl_project
        self.clip_parser = clip_parser
        self.logger = logging.getLogger(__name__)

    def create_clips_from_pattern(self, pattern, base_position: float = 0) -> List[Clip]:
        """Create clips from an FL Studio pattern."""
        clips = []
        
        try:
            if not pattern.name:
                return clips

            self.logger.debug(f"Processing pattern: {pattern.name}")
            
            for channel_id, channel in enumerate(pattern.channels):
                if not channel or not hasattr(channel, 'sample_path'):
                    continue
                    
                position = base_position + (pattern.position if hasattr(pattern, 'position') else 0)
                
                clip = self.clip_parser.create_clip_from_channel(
                    channel=channel,
                    position=position,
                    ppq=self.fl_project.ppq
                )
                
                if clip:
                    clips.append(clip)
                    self.logger.debug(f"Added clip {clip.name} from pattern {pattern.name}")

        except Exception as e:
            self.logger.error(f"Failed to create clips from pattern: {e}")
            
        return clips
```
---

#### src\fl2cu\parser\project_parser.py
```
from pathlib import Path
from .timing_parser import FLTimingParser
from .clip_parser import FLClipParser
from .arrangement_parser import FLArrangementParser
from ..models.project import Project

class FLProjectParser:
    """Main FL Studio project parser coordinating specialized parsers."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Project file not found: {file_path}")
            
        self.logger = logging.getLogger(__name__)
        self.fl_project = pyflp.parse(file_path)
        
        # Initialize specialized parsers
        self.timing_parser = FLTimingParser(self.fl_project)
        self.clip_parser = FLClipParser(self.fl_project)
        self.arrangement_parser = FLArrangementParser(self.fl_project, self.clip_parser)

    def parse_project(self) -> Project:
        """Parse FL Studio project using specialized parsers."""
        try:
            # Parse timing info
            timing = self.timing_parser.parse_timing()
            
            # Create project
            project = Project(
                name=self.file_path.stem,
                timing=timing,
                source_path=self.file_path
            )
            
            # Parse arrangements
            arrangements = self.arrangement_parser.parse_arrangements()
            for arrangement in arrangements:
                project.add_arrangement(arrangement)
            
            self.logger.info(f"Parsed project with {len(arrangements)} arrangements")
            return project
            
        except Exception as e:
            self.logger.error(f"Failed to parse project: {e}")
            raise
```
---

#### src\fl2cu\parser\timing_parser.py
```
from pathlib import Path
from typing import Optional
from pyflp.project import Project as FLProject
from ..models.timing import ProjectTiming

class FLTimingParser:
    """Handles extraction of timing information from FL Studio projects."""
    
    def __init__(self, fl_project: FLProject):
        self.fl_project = fl_project
        self.logger = logging.getLogger(__name__)

    def parse_timing(self) -> ProjectTiming:
        """Extract timing information from FL Studio project."""
        try:
            # Get tempo from project (FLPs store this directly)
            tempo = float(self.fl_project.tempo)
            
            # Get time signature
            # FL Studio stores numerator and denominator separately
            time_sig_num = getattr(self.fl_project, 'time_signature_numerator', 4)
            time_sig_denom = getattr(self.fl_project, 'time_signature_denominator', 4)
            
            # Get PPQ (Pulses Per Quarter note)
            ppq = self.fl_project.ppq
            
            timing = ProjectTiming(
                tempo=tempo,
                time_signature_numerator=time_sig_num,
                time_signature_denominator=time_sig_denom,
                ppq=ppq
            )
            
            self.logger.debug(
                f"Parsed timing: {tempo} BPM, {time_sig_num}/{time_sig_denom}, PPQ: {ppq}"
            )
            return timing
            
        except Exception as e:
            self.logger.error(f"Failed to parse timing info: {e}")
            return ProjectTiming.default()
```
---

#### src\fl2cu\utils\__init__.py
```
# fl2cu/utils/__init__.py
"""Utility functions and helpers."""
from fl2cu.utils.logger import setup_logger, get_logger

__all__ = ['setup_logger', 'get_logger']
```
---

#### src\fl2cu\utils\logger.py
```
# src/fl2cu/utils/logger.py
from pathlib import Path
from typing import Optional

def setup_logger(log_file: Optional[Path] = None) -> logging.Logger:
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
    return logging.getLogger('fl2cu')

def log_error(error: Exception, context: Optional[str] = None) -> None:
    logger = get_logger()
    error_message = f"{error.__class__.__name__}: {str(error)}"
    if context:
        error_message = f"{context} - {error_message}"
    logger.error(error_message, exc_info=True)
```
---

