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