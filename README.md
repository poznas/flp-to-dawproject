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
import flstudio_cubase_migration as fl2cu

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