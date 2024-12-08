# FL Studio to Cubase Migration Tool

A Python-based tool for transferring audio arrangements from FL Studio to Cubase using the open DAWproject format as an intermediate step.

## Features
- Exports FL Studio audio clips while preserving:
  - Clip positions and timing
  - Track organization
  - File references
  - Basic clip properties (volume, pan, mute)
- Exports to DAWproject format (.dawproject)
  - Industry standard open format
  - Vendor-neutral exchange format
  - Compatible with multiple DAWs including Cubase, Bitwig Studio, and Studio One
  - XML-based for easy debugging and modification

## Basic Usage
```bash
python -m fl2cu "path/to/project.flp" "path/to/output" --debug
```

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

## Limitations 

### Clip Support
- Only audio clips are converted
- MIDI patterns, automation, and other event types are ignored
- No support for clip effects or real-time processing

### Timing
- FL Studio stores offsets in milliseconds while DAWproject uses beats
- Some minor timing precision differences may occur during conversion
- All timing in output uses beats as the primary unit

### Properties 
- Colors are not preserved (Cubase ignores them anyway)
- Limited metadata transfer
- Basic properties only (position, length, mute state)
- No support for advanced features like automation

## Project Structure
```
flstudio-transfer/
├── src/
│   └── fl2cu/
│       ├── __init__.py
│       ├── __main__.py         # Main entry point
│       ├── generator/
│       │   ├── __init__.py
│       │   ├── dawproject_generator.py  # DAWproject generation
│       │   ├── xml/
│       │   │   ├── clip.py     # Clip XML generation
│       │   │   ├── generator.py # Core XML generation
│       │   │   ├── structure.py # Base XML structure
│       │   │   └── track.py    # Track XML generation
│       │   └── xml_utils.py    # XML helper utilities
│       ├── models/
│       │   ├── __init__.py
│       │   ├── arrangement.py  # Arrangement model
│       │   ├── base.py        # Base model functionality
│       │   ├── clip.py        # Clip model
│       │   ├── project.py     # Project model
│       │   ├── timing.py      # Timing information model
│       │   └── track.py       # Track model
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── arrangement_parser.py  # Arrangement parsing
│       │   ├── clip_parser.py       # Audio clip parsing
│       │   ├── pattern_parser.py    # Pattern parsing
│       │   ├── project_parser.py    # Main project parsing
│       │   └── timing_parser.py     # Timing data parsing
│       └── utils/
           ├── __init__.py
           └── logger.py        # Logging configuration
├── tests/
│   └── ...                    # Test files (to be added)
├── .pylintrc                  # Linting configuration
├── dev-requirements.txt       # Development dependencies
├── mypy.ini                   # Type checking configuration
├── pytest.ini                 # Test configuration
├── pyproject.toml            # Project configuration
├── requirements.txt          # Core dependencies
└── setup.py                 # Package setup

```

## Output Structure
```
output/
  ├── project.dawproject    # Contains:
  │   ├── project.xml      # Main project structure
  │   ├── metadata.xml     # Project metadata  
  │   └── audio/          # Referenced audio files
  └── debug/              # When --debug is used
      └── logs/          # Detailed conversion logs
```

## Contributing
PRs welcome - send a video of it working and I'll probably merge it. Fork as you like.

## License
MIT licensed - completely open source.

## Note to Image-Line
Will take this down instantly if you add ARA2 support 🙏