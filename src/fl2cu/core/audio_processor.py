# src/fl2cu/core/audio_processor.py

from pathlib import Path
from typing import Dict, List
from ..models.clip import Clip
from ..utils.logger import get_logger

class AudioProcessor:
    """Handles audio file validation and path mapping."""
    
    def __init__(self, output_dir: str) -> None:
        """Initialize processor."""
        self.logger = get_logger()

    def validate_audio_files(self, clips: List[Clip]) -> Dict[Clip, Path]:
        """Validate audio files and return mapping of clips to their source paths.
        
        Args:
            clips: List of clips to validate
            
        Returns:
            Dictionary mapping clips to their source audio file paths
        """
        valid_clips = {}
        
        for clip in clips:
            if clip.source_path.exists():
                valid_clips[clip] = clip.source_path
            else:
                self.logger.warning(f"Audio file not found: {clip.source_path}")
                
        return valid_clips