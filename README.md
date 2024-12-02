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