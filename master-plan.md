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
