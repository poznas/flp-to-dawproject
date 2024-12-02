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