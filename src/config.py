# File: src/config.py
"""
Global configuration settings.

Filepath: src/config.py
"""
from pathlib import Path
from typing import Dict, List, Any

class Config:
    """Global configuration settings for FL Studio to Cubase migration"""
    
    # File system settings
    DEFAULT_OUTPUT_DIR: Path = Path('./output')
    TEMP_DIR: Path = Path('./temp')
    
    # Audio settings
    SUPPORTED_AUDIO_FORMATS: List[str] = ['.wav']
    MAX_AUDIO_CHANNELS: int = 2
    SAMPLE_RATE: int = 44100
    BIT_DEPTH: int = 24
    
    # Project constraints
    MAX_CLIPS_PER_ARRANGEMENT: int = 1000
    MAX_ARRANGEMENTS: int = 50
    
    # Version requirements
    MIN_FL_STUDIO_VERSION: str = '20.8.0'
    MIN_CUBASE_VERSION: str = '14.0.0'
    
    # AAF settings
    AAF_VERSION: str = '1.1'
    SUPPORTED_COLOR_FORMATS: List[str] = ['RGB', 'HEX']
    
    # Performance settings
    BATCH_SIZE: int = 100  # Number of clips to process at once
    MAX_PARALLEL_EXPORTS: int = 4
    
    @classmethod
    def get_output_dir(cls, project_name: str) -> Path:
        """Get project-specific output directory"""
        return cls.DEFAULT_OUTPUT_DIR / project_name
    
    @classmethod
    def get_temp_dir(cls, project_name: str) -> Path:
        """Get project-specific temporary directory"""
        return cls.TEMP_DIR / project_name
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary for serialization"""
        return {
            name: value for name, value in vars(cls).items()
            if not name.startswith('_') and name.isupper()
        }