from pathlib import Path
from typing import List, Optional, Dict, Any

from .arrangement import Arrangement

class BaseProject:
    """Base class containing core Project functionality."""
    def __init__(
        self,
        name: str,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        self.name = name
        self.source_path = Path(source_path) if source_path else None
        self.output_dir = Path(output_dir) if output_dir else None
        self._arrangements: List['Arrangement'] = []

    @property
    def arrangements(self) -> List['Arrangement']:
        return self._arrangements.copy()