import pytest
from pathlib import Path
import aaf2
from typing import Dict

from src.core.aaf_generator import AAFGenerator
from src.models.arrangement import Arrangement
from src.models.clip import Clip

class TestAAFGenerator:
    def test_aaf_creation(self, temp_dir, sample_arrangement, sample_wav_file):
        """Test basic AAF file creation."""
        output_path = temp_dir / "test.aaf"
        audio_map = {clip: sample_wav_file for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        
        # Verify AAF structure
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            assert composition is not None
            assert len(f.content.mobs) > 0

    def test_clip_metadata_preservation(self, temp_dir, sample_clip, sample_wav_file):
        """Test preservation of clip metadata in AAF."""
        arrangement = Arrangement(name="test_arrangement")
        arrangement.add_clip(sample_clip)
        
        output_path = temp_dir / "metadata_test.aaf"
        audio_map = {sample_clip: sample_wav_file}
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            
            # Verify composition name
            assert composition.name == arrangement.name
            
            # Check mob structure
            found_clip = False
            for mob in f.content.mobs:
                if hasattr(mob, 'user_comments'):
                    comments = mob.user_comments
                    if comments.get('Name') == sample_clip.name:
                        found_clip = True
                        assert comments.get('Color', '') == sample_clip.color
                        if sample_clip.muted:
                            assert comments.get('Muted') == 'true'
                        break
            
            assert found_clip, "Clip metadata not found in AAF"

    def test_timeline_position_preservation(self, temp_dir, sample_wav_file):
        """Test preservation of clip positions in timeline."""
        arrangement = Arrangement(name="position_test")
        
        # Create clips at specific positions
        clips = [
            Clip(name="clip1", position=0.0, duration=2.0, color="#FF0000"),
            Clip(name="clip2", position=3.0, duration=2.0, color="#00FF00"),
            Clip(name="clip3", position=6.0, duration=2.0, color="#0000FF")
        ]
        
        for clip in clips:
            arrangement.add_clip(clip)
            
        audio_map = {clip: sample_wav_file for clip in clips}
        output_path = temp_dir / "position_test.aaf"
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            # Verify relative positions are maintained
            previous_pos = -1
            for mob in f.content.mobs:
                if hasattr(mob, 'slots') and mob.slots:
                    for slot in mob.slots:
                        if hasattr(slot, 'position'):
                            assert slot.position > previous_pos
                            previous_pos = slot.position

    def test_missing_audio_files(self, temp_dir, sample_arrangement):
        """Test handling of missing audio files."""
        output_path = temp_dir / "missing_audio.aaf"
        audio_map = {clip: Path("nonexistent.wav") for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        
        with pytest.raises(FileNotFoundError):
            generator.generate_aaf(str(output_path))

    def test_invalid_output_path(self, temp_dir, sample_arrangement, sample_wav_file):
        """Test handling of invalid output paths."""
        invalid_path = temp_dir / "nonexistent" / "test.aaf"
        audio_map = {clip: sample_wav_file for clip in sample_arrangement.clips}
        
        generator = AAFGenerator(sample_arrangement, audio_map)
        
        with pytest.raises((OSError, IOError)):
            generator.generate_aaf(str(invalid_path))

    def test_volume_preservation(self, temp_dir, sample_wav_file):
        """Test preservation of clip volume settings."""
        arrangement = Arrangement(name="volume_test")
        clip = Clip(
            name="volume_clip",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            volume=0.5  # 50% volume
        )
        arrangement.add_clip(clip)
        
        output_path = temp_dir / "volume_test.aaf"
        audio_map = {clip: sample_wav_file}
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        with aaf2.open(str(output_path), 'r') as f:
            composition = next(f.content.toplevel())
            for mob in f.content.mobs:
                if hasattr(mob, 'slots'):
                    for slot in mob.slots:
                        if hasattr(slot, 'volume'):
                            assert abs(slot.volume - 0.5) < 0.01

    def test_large_arrangement(self, temp_dir, sample_wav_file):
        """Test handling of arrangements with many clips."""
        arrangement = Arrangement(name="large_test")
        
        # Create 100 test clips
        clips = []
        for i in range(100):
            clip = Clip(
                name=f"clip_{i}",
                position=float(i) * 2,  # Position them sequentially
                duration=1.5,
                color="#FF0000"
            )
            arrangement.add_clip(clip)
            clips.append(clip)
            
        audio_map = {clip: sample_wav_file for clip in clips}
        output_path = temp_dir / "large_test.aaf"
        
        generator = AAFGenerator(arrangement, audio_map)
        generator.generate_aaf(str(output_path))
        
        assert output_path.exists()
        assert output_path.stat().st_size > 0