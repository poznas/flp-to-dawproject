from pathlib import Path
import logging
from typing import Optional
from pyflp.project import Project as FLProject
from ..models.timing import ProjectTiming

class FLTimingParser:
    """Handles extraction of timing information from FL Studio projects."""
    
    def __init__(self, fl_project: FLProject):
        self.fl_project = fl_project
        self.logger = logging.getLogger(__name__)

    def parse_timing(self) -> ProjectTiming:
        """Extract timing information from FL Studio project."""
        try:
            # Get tempo from project (FLPs store this directly)
            tempo = float(self.fl_project.tempo)
            
            # Get time signature
            # FL Studio stores numerator and denominator separately
            time_sig_num = getattr(self.fl_project, 'time_signature_numerator', 4)
            time_sig_denom = getattr(self.fl_project, 'time_signature_denominator', 4)
            
            # Get PPQ (Pulses Per Quarter note)
            ppq = self.fl_project.ppq
            
            timing = ProjectTiming(
                tempo=tempo,
                time_signature_numerator=time_sig_num,
                time_signature_denominator=time_sig_denom,
                ppq=ppq
            )
            
            self.logger.debug(
                f"Parsed timing: {tempo} BPM, {time_sig_num}/{time_sig_denom}, PPQ: {ppq}"
            )
            return timing
            
        except Exception as e:
            self.logger.error(f"Failed to parse timing info: {e}")
            return ProjectTiming.default()