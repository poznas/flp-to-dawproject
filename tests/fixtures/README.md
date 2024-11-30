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