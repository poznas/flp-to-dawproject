from typing import List, Optional, TYPE_CHECKING
from pathlib import Path
from .timing import ProjectTiming

if TYPE_CHECKING:
    from .arrangement import Arrangement

class BaseProject:
    """Base class containing core Project functionality."""
    def __init__(
        self,
        name: str,
        timing: Optional[ProjectTiming] = None,
        source_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        self.name = name
        self.timing = timing or ProjectTiming.default()
        self.source_path = Path(source_path) if source_path else None
        self.output_dir = Path(output_dir) if output_dir else None
        self._arrangements: List['Arrangement'] = []

    @property
    def arrangements(self) -> List['Arrangement']:
        """Get list of project arrangements."""
        return self._arrangements.copy()

    def add_arrangement(self, arrangement: 'Arrangement') -> None:
        """Add an arrangement to the project."""
        if arrangement.name in [arr.name for arr in self._arrangements]:
            raise ValueError(f"Arrangement {arrangement.name} already exists")
        self._arrangements.append(arrangement)

    def remove_arrangement(self, arrangement: 'Arrangement') -> None:
        """Remove an arrangement from the project."""