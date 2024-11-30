import aaf2
from pathlib import Path

from src.core.aaf_generator import AAFGenerator
from src.models.arrangement import Arrangement
from src.models.clip import Clip

def compare_aaf_metadata(file1: Path, file2: Path) -> bool:
    """Compare two AAF files for structural equality."""
    with aaf2.open(str(file1), 'r') as f1, aaf2.open(str(file2), 'r') as f2:
        # Compare main composition
        comp1 = next(f1.content.toplevel())
        comp2 = next(f2.content.toplevel())
        
        if comp1.name != comp2.name:
            return False
            
        # Compare number of mobs
        if len(f1.content.mobs) != len(f2.content.mobs):
            return False
            
        # Compare mob structure
        mobs1 = sorted(f1.content.mobs, key=lambda m: getattr(m, 'name', ''))
        mobs2 = sorted(f2.content.mobs, key=lambda m: getattr(m, 'name', ''))
        
        for mob1, mob2 in zip(mobs1, mobs2):
            # Compare slots
            if len(mob1.slots) != len(mob2.slots):
                return False
                
            for slot1, slot2 in zip(mob1.slots, mob2.slots):
                # Compare basic properties
                if slot1.segment.length != slot2.segment.length:
                    return False
                    
                # Compare metadata if available
                if hasattr(slot1, 'user_comments') and hasattr(slot2, 'user_comments'):
                    if slot1.user_comments != slot2.user_comments:
                        return False
                        
        return True

class TestAAFGenerator:
    def test_aaf_matches_expected(self, temp_dir, sample_arrangement, expected_aaf_path):
        """Test that generated AAF matches expected structure."""
        output_path = temp_dir / "test_output.aaf"
        audio_map = {clip: clip.source_path for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        assert output_path.exists()
        assert compare_aaf_metadata(output_path, expected_aaf_path)
    
    def test_clip_positions_match_expected(self, temp_dir, expected_aaf_path):
        """Test that clip positions in generated AAF match expected positions."""
        # Create test arrangement matching expected AAF structure
        arrangement = Arrangement(name="TEST_ARRANGEMENT")
        
        clips = [
            Clip(name="clip1", position=0.0, duration=2.0, color="#FF0000"),
            Clip(name="clip2", position=3.0, duration=3.0, color="#00FF00", volume=0.8),
            Clip(name="clip3", position=7.0, duration=1.0, color="#0000FF", volume=0.5),
        ]
        
        for clip in clips:
            arrangement.add_clip(clip)
        
        output_path = temp_dir / "position_test.aaf"
        audio_map = {clip: clip.source_path for clip in clips}
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f_out, aaf2.open(str(expected_aaf_path), 'r') as f_exp:
            # Compare clip positions
            out_mobs = [m for m in f_out.content.mobs if hasattr(m, 'slots')]
            exp_mobs = [m for m in f_exp.content.mobs if hasattr(m, 'slots')]
            
            for out_mob, exp_mob in zip(out_mobs, exp_mobs):
                for out_slot, exp_slot in zip(out_mob.slots, exp_mob.slots):
                    assert out_slot.segment.length == exp_slot.segment.length
                    if hasattr(out_slot, 'position'):
                        assert out_slot.position == exp_slot.position