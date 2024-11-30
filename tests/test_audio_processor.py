import pytest
import numpy as np
import wave
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor

from src.core.audio_processor import AudioProcessor
from src.models.clip import Clip

class TestAudioProcessor:
    def test_init(self, temp_dir):
        """Test AudioProcessor initialization."""
        processor = AudioProcessor(str(temp_dir))
        assert processor.output_dir == Path(temp_dir)
        assert processor.output_dir.exists()

    def test_single_clip_export(self, temp_dir, sample_wav_file, sample_clip):
        """Test exporting a single audio clip."""
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([sample_clip])
        
        assert len(result) == 1
        assert sample_clip in result
        exported_path = result[sample_clip]
        
        assert exported_path.exists()
        assert exported_path.suffix == '.wav'
        
        # Verify audio content
        with wave.open(str(sample_wav_file), 'rb') as original:
            with wave.open(str(exported_path), 'rb') as exported:
                # Check audio parameters
                assert original.getnchannels() == exported.getnchannels()
                assert original.getsampwidth() == exported.getsampwidth()
                assert original.getframerate() == exported.getframerate()
                assert original.getnframes() == exported.getnframes()

    def test_volume_adjustment(self, temp_dir, sample_wav_file):
        """Test volume adjustment during export."""
        # Create clip with modified volume
        clip = Clip(
            name="volume_test",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            source_path=sample_wav_file,
            volume=0.5  # 50% volume
        )
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        exported_path = result[clip]
        
        # Read and compare audio data
        with wave.open(str(sample_wav_file), 'rb') as original:
            orig_frames = np.frombuffer(original.readframes(original.getnframes()), dtype=np.int16)
            
        with wave.open(str(exported_path), 'rb') as exported:
            exported_frames = np.frombuffer(exported.readframes(exported.getnframes()), dtype=np.int16)
            
        # Check if exported audio is approximately half the amplitude
        # Allow for small differences due to floating point arithmetic
        assert np.allclose(exported_frames, orig_frames * 0.5, rtol=1e-3)

    def test_parallel_processing(self, temp_dir, sample_wav_file):
        """Test processing multiple clips in parallel."""
        # Create multiple test clips
        clips = [
            Clip(name=f"clip_{i}", position=float(i), duration=2.0, 
                 color="#FF0000", source_path=sample_wav_file)
            for i in range(5)
        ]
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips(clips, max_workers=2)
        
        assert len(result) == len(clips)
        for clip in clips:
            assert clip in result
            assert result[clip].exists()

    def test_missing_source_file(self, temp_dir, sample_wav_file):
        """Test handling of missing source files."""
        nonexistent = Path("nonexistent.wav")
        clip = Clip(
            name="missing_source",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            source_path=nonexistent
        )
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        
        assert len(result) == 0  # Should not process clip with missing source

    def test_invalid_audio_file(self, temp_dir):
        """Test handling of invalid audio files."""
        temp_dir.mkdir(parents=True, exist_ok=True)
        # Create invalid WAV file
        invalid_wav = temp_dir / "invalid.wav"
        invalid_wav.write_bytes(b"not a wav file")
        
        clip = Clip(
            name="invalid_audio",
            position=0.0,
            duration=2.0,
            color="#FF0000",
            source_path=invalid_wav
        )
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips([clip])
        
        assert len(result) == 0  # Should not process invalid audio file

    def test_validate_audio_files(self, temp_dir, sample_wav_file):
        """Test audio file validation."""
        processor = AudioProcessor(str(temp_dir))
        
        # Create test clips and export
        clips = [
            Clip(name="valid_clip", position=0.0, duration=2.0,
                 color="#FF0000", source_path=sample_wav_file)
        ]
        
        processor.export_audio_clips(clips)
        assert processor.validate_audio_files(clips) == True
        
        # Test with corrupted file
        output_file = next(temp_dir.glob("*.wav"))
        output_file.write_bytes(b"corrupted")
        assert processor.validate_audio_files(clips) == False

    def test_unique_output_paths(self, temp_dir, sample_wav_file):
        """Test handling of duplicate output filenames."""
        clips = [
            Clip(name="same_name", position=0.0, duration=2.0,
                 color="#FF0000", source_path=sample_wav_file),
            Clip(name="same_name", position=2.0, duration=2.0,
                 color="#FF0000", source_path=sample_wav_file)
        ]
        
        processor = AudioProcessor(str(temp_dir))
        result = processor.export_audio_clips(clips)
        
        assert len(result) == 2
        # Check that output paths are different
        paths = list(result.values())
        assert paths[0] != paths[1]