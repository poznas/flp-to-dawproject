
# Lightweight DAW Project Example

## Overview

This is a simplified DAWProject XML file compatible with Cubase 14. It serves as an example of the correct structure that can be imported.

## Structure

### Application
- **Name:** Cubase Example Project
- **Version:** 14.0

### Transport
- **Tempo:** 120 BPM
- **Time Signature:** 4/4

### Tracks
#### Example Track
- **Content Type:** Audio
- **ID:** track1
- **Name:** Example Track
- **Color:** Blue (#0000FF)
- **Channel:**
  - **Audio Channels:** 2 (Stereo)
  - **Role:** Master
  - **Volume:** 0.8 (Linear scale, max 1.0)
  - **Pan:** 0.5 (Centered, normalized scale)

## Notes
This example is reduced in complexity to ensure easy parsing and quick import testing.
