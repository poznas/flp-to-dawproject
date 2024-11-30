"""Core package for FL Studio to Cubase migration tool.

This package contains the core functionality for parsing FL Studio projects,
processing audio, and generating AAF files.
"""

from .project_parser import FLProjectParser
from .audio_processor import AudioProcessor
from .aaf_generator import AAFGenerator

__all__ = ['FLProjectParser', 'AudioProcessor', 'AAFGenerator']