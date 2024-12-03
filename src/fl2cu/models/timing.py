from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ProjectTiming:
    """Represents project timing information."""
    tempo: float
    time_signature_numerator: int
    time_signature_denominator: int
    ppq: Optional[int] = None  # Pulses Per Quarter note

    @staticmethod
    def default() -> 'ProjectTiming':
        """Create default timing with 120 BPM and 4/4 time signature."""
        return ProjectTiming(
            tempo=120.0,
            time_signature_numerator=4,
            time_signature_denominator=4
        )

    def to_dict(self) -> dict:
        """Convert timing info to dictionary format."""
        return {
            'tempo': {
                'value': str(self.tempo),
                'min': '20',
                'max': '999',
                'unit': 'bpm'
            },
            'time_signature': {
                'numerator': str(self.time_signature_numerator),
                'denominator': str(self.time_signature_denominator)
            }
        }