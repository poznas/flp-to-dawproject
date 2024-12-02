from typing import Dict, List, Optional
import aaf2
from pathlib import Path
import json
import struct

class AAFInspector:
    """Inspector for analyzing AAF file structure and content."""
    
    def __init__(self, aaf_path: str):
        """Initialize with path to AAF file."""
        self.aaf_path = Path(aaf_path)
        if not self.aaf_path.exists():
            raise FileNotFoundError(f"AAF file not found: {aaf_path}")
            
    def analyze_file(self) -> Dict:
        """Perform complete analysis of AAF file."""
        with aaf2.open(str(self.aaf_path), 'r') as f:
            analysis = {
                'file_info': self._get_file_info(),
                'composition': self._analyze_composition(f),
                'mobs': self._analyze_mobs(f),
                'media_references': self._analyze_media_refs(f),
                'potential_issues': self._check_common_issues(f)
            }
            return analysis
            
    def _get_file_info(self) -> Dict:
        """Get basic file information."""
        return {
            'filename': self.aaf_path.name,
            'size': self.aaf_path.stat().st_size,
            'last_modified': self.aaf_path.stat().st_mtime
        }
        
    def _analyze_composition(self, f: 'aaf2.File') -> Dict:
        """Analyze main composition structure."""
        try:
            comp = next(f.content.toplevel())
            return {
                'name': comp.name,
                'mob_id': str(comp.mob_id),
                'slots': len(comp.slots),
                'usage_code': getattr(comp, 'usage_code', None),
                'creation_time': getattr(comp, 'creation_time', None)
            }
        except StopIteration:
            return {'error': 'No composition found'}
            
    def _analyze_mobs(self, f: 'aaf2.File') -> List[Dict]:
        """Analyze all mobs (media objects) in the file."""
        mobs = []
        for mob in f.content.mobs:
            mob_data = {
                'name': getattr(mob, 'name', None),
                'mob_id': str(mob.mob_id),
                'type': mob.__class__.__name__,
                'slots': self._analyze_slots(mob),
                'attributes': self._get_mob_attributes(mob)
            }
            mobs.append(mob_data)
        return mobs
        
    def _analyze_slots(self, mob: 'aaf2.Mob') -> List[Dict]:
        """Analyze slots in a mob."""
        slots = []
        for slot in mob.slots:
            slot_data = {
                'name': getattr(slot, 'name', None),
                'slot_id': getattr(slot, 'slot_id', None),
                'segment': {
                    'type': slot.segment.__class__.__name__,
                    'length': getattr(slot.segment, 'length', None)
                }
            }
            # Add timing information if available
            if hasattr(slot, 'start_time'):
                slot_data['start_time'] = slot.start_time
            if hasattr(slot, 'duration'):
                slot_data['duration'] = slot.duration
            
            slots.append(slot_data)
        return slots
        
    def _get_mob_attributes(self, mob: 'aaf2.Mob') -> Dict:
        """Get mob attributes including user comments."""
        attributes = {}
        if hasattr(mob, 'user_comments'):
            attributes['user_comments'] = dict(mob.user_comments)
        if hasattr(mob, 'attributes'):
            attributes['mob_attributes'] = {
                k: str(v) for k, v in mob.attributes.items()
            }
        return attributes
        
    def _analyze_media_refs(self, f: 'aaf2.File') -> List[Dict]:
        """Analyze media references."""
        refs = []
        for mob in f.content.mobs:
            for slot in mob.slots:
                if hasattr(slot.segment, 'components'):
                    for comp in slot.segment.components:
                        if hasattr(comp, 'source_ref'):
                            ref_data = {
                                'mob_id': str(comp.source_ref.mob_id),
                                'slot_id': comp.source_ref.slot_id,
                                'start_time': getattr(comp, 'start_time', None),
                                'duration': getattr(comp, 'length', None)
                            }
                            refs.append(ref_data)
        return refs
        
    def _check_common_issues(self, f: 'aaf2.File') -> List[str]:
        """Check for common issues that might cause import problems."""
        issues = []
        
        # Check for composition
        try:
            next(f.content.toplevel())
        except StopIteration:
            issues.append("No composition found")
            
        # Check media references
        for mob in f.content.mobs:
            if isinstance(mob, aaf2.components.SourceMob):
                if not any(hasattr(slot.segment, 'components') 
                          for slot in mob.slots):
                    issues.append(f"Source mob '{mob.name}' has no components")
                    
        # Check for invalid durations
        for mob in f.content.mobs:
            for slot in mob.slots:
                if hasattr(slot, 'duration') and slot.duration <= 0:
                    issues.append(f"Invalid duration in mob '{mob.name}'")
                    
        # Check for broken references
        mob_ids = {str(mob.mob_id) for mob in f.content.mobs}
        for mob in f.content.mobs:
            for slot in mob.slots:
                if hasattr(slot.segment, 'components'):
                    for comp in slot.segment.components:
                        if (hasattr(comp, 'source_ref') and 
                            str(comp.source_ref.mob_id) not in mob_ids):
                            issues.append(f"Broken reference in mob '{mob.name}'")
                            
        return issues

    def save_analysis(self, output_path: str) -> None:
        """Save analysis to JSON file."""
        analysis = self.analyze_file()
        with open(output_path, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)