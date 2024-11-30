# File: src/config.py
"""
Global configuration settings.

Filepath: src/config.py
"""
from pathlib import Path

CONFIG = {
    'DEFAULT_OUTPUT_DIR': Path('./output'),
    'SUPPORTED_AUDIO_FORMATS': ['.wav', '.mp3', '.aiff'],
    'MAX_CLIPS_PER_ARRANGEMENT': 1000,
    'MIN_FL_STUDIO_VERSION': '20.8.0',
    'MIN_CUBASE_VERSION': '14.0.0'
}