from pathlib import Path

import pytest

from src.models.project import Project
from src.models.arrangement import Arrangement
from src.models.clip import Clip

class TestClip:
    def test_clip_initialization(self, sample_wav_file):
        """Test basic clip initialization with valid data."""
        clip = Clip(
            name="test clip",
            position=1.5,
            duration=3.0,
            color="#FF0000",
            source_path=sample_wav_file
        )
        assert clip.name == "test_clip"  # Should be sanitized
        assert clip.position == 1.5
        assert clip.duration == 3.0
        assert clip.color == "#FF0000"
        assert clip.source_path == sample_wav_file
        assert clip.volume == 1.0  # Default value
        assert not clip.muted  # Default value

    def test_clip_validation(self):
        """Test clip validation for invalid inputs."""
        with pytest.raises(ValueError, match="Position cannot be negative"):
            Clip(name="test", position=-1.0, duration=1.0, color="#FF0000")

        with pytest.raises(ValueError, match="Duration must be positive"):
            Clip(name="test", position=0.0, duration=0.0, color="#FF0000")

        with pytest.raises(ValueError, match="Color must be in #RRGGBB format"):
            Clip(name="test", position=0.0, duration=1.0, color="FF0000")

    def test_clip_serialization(self, sample_clip):
        """Test clip serialization to and from dict."""
        # Add some metadata to test
        sample_clip = sample_clip.with_metadata('test_key', 'test_value')
        
        data = sample_clip.to_dict()
        restored_clip = Clip.from_dict(data)
        
        assert restored_clip == sample_clip
        assert restored_clip.get_metadata('test_key') == 'test_value'

    def test_clip_metadata(self, sample_clip):
        """Test metadata operations."""
        # Add metadata
        clip_with_meta = sample_clip.with_metadata('key1', 'value1')
        clip_with_more = clip_with_meta.with_metadata('key2', 'value2')
        
        assert clip_with_more.get_metadata('key1') == 'value1'
        assert clip_with_more.get_metadata('key2') == 'value2'
        assert clip_with_more.get_metadata('nonexistent') is None
        assert clip_with_more.get_metadata('nonexistent', 'default') == 'default'

    def test_clip_immutability(self, sample_clip):
        """Test that clip is immutable."""
        with pytest.raises(dataclasses.FrozenInstanceError):
            sample_clip.name = "new_name"

        with pytest.raises(dataclasses.FrozenInstanceError):
            sample_clip.position = 2.0

class TestArrangement:
    def test_arrangement_initialization(self):
        """Test basic arrangement initialization."""
        arr = Arrangement(name="TEST_ARR")
        assert arr.name == "TEST_ARR"
        assert len(arr.clips) == 0

    def test_add_remove_clip(self, sample_clip):
        """Test adding and removing clips from arrangement."""
        arr = Arrangement(name="TEST_ARR")
        
        # Add clip
        arr.add_clip(sample_clip)
        assert len(arr.clips) == 1
        assert arr.clips[0] == sample_clip
        assert arr.clips[0].arrangement_name == "TEST_ARR"
        
        # Basic equality should ignore arrangement name
        assert arr.clips[0] == sample_clip
        
        # Full equality should consider arrangement name
        assert not arr.clips[0].full_equals(sample_clip)
        
        # Remove clip
        arr.remove_clip(sample_clip)
        assert len(arr.clips) == 0

    def test_get_clip_by_name(self, sample_clip):
        """Test finding clips by name."""
        arr = Arrangement(name="TEST_ARR")
        arr.add_clip(sample_clip)
        
        found_clip = arr.get_clip_by_name(sample_clip.name)
        assert found_clip is not None
        assert found_clip == sample_clip
        
        assert arr.get_clip_by_name("nonexistent") is None

    def test_get_duration(self, sample_clip):
        """Test arrangement duration calculation."""
        arr = Arrangement(name="TEST_ARR")
        assert arr.get_duration() == 0.0
        
        arr.add_clip(sample_clip)  # At position 0.0
        assert arr.get_duration() == sample_clip.duration
        
        # Add another clip that extends beyond
        clip2 = Clip(
            name="clip2", 
            position=1.5, 
            duration=2.0, 
            color="#00FF00"
        )
        arr.add_clip(clip2)
        assert arr.get_duration() == 3.5  # 1.5 + 2.0

    def test_arrangement_validation(self, sample_clip):
        """Test arrangement validation."""
        arr = Arrangement(name="TEST_ARR")
        
        # Empty name
        with pytest.raises(ValueError, match="cannot be empty"):
            Arrangement(name="")
        
        # Duplicate clip names
        arr.add_clip(sample_clip)
        duplicate = Clip(
            name=sample_clip.name,
            position=1.0,
            duration=1.0,
            color="#00FF00"
        )
        
        with pytest.raises(ValueError, match="Duplicate clip names"):
            arr.add_clip(duplicate)
            arr.validate()

class TestProject:
    def test_project_initialization(self, temp_dir):
        """Test basic project initialization."""
        project = Project(
            name="test_project",
            source_path=temp_dir / "test.flp",
            output_dir=temp_dir / "output"
        )
        assert project.name == "test_project"
        assert len(project.arrangements) == 0

    def test_add_remove_arrangement(self, sample_arrangement):
        """Test adding and removing arrangements."""
        project = Project(name="test_project")
        
        # Add arrangement
        project.add_arrangement(sample_arrangement)
        assert len(project.arrangements) == 1
        assert project.arrangements[0] == sample_arrangement
        
        # Try adding duplicate
        with pytest.raises(ValueError, match="already exists"):
            project.add_arrangement(sample_arrangement)
            
        # Remove arrangement
        project.remove_arrangement(sample_arrangement)
        assert len(project.arrangements) == 0

    def test_get_arrangement_by_name(self, sample_arrangement):
        """Test finding arrangements by name."""
        project = Project(name="test_project")
        project.add_arrangement(sample_arrangement)
        
        found = project.get_arrangement_by_name(sample_arrangement.name)
        assert found is not None
        assert found == sample_arrangement
        
        assert project.get_arrangement_by_name("nonexistent") is None

    def test_validate_audio_files(self, sample_project, sample_wav_file):
        """Test audio file validation."""
        assert sample_project.validate_audio_files() == True
        
        # Test with missing file
        sample_wav_file.unlink()
        assert sample_project.validate_audio_files() == False

    def test_project_validation(self, sample_arrangement):
        """Test project validation."""
        project = Project(name="test_project")
        
        # Empty name
        with pytest.raises(ValueError, match="cannot be empty"):
            Project(name="")
        
        # Duplicate arrangement names
        project.add_arrangement(sample_arrangement)
        duplicate = Arrangement(name=sample_arrangement.name)
        
        with pytest.raises(ValueError, match="Duplicate arrangement names"):
            project.add_arrangement(duplicate)
            project.validate()

    def test_get_all_clip_paths(self, sample_project, sample_wav_file):
        """Test collecting all unique audio file paths."""
        paths = sample_project.get_all_clip_paths()
        assert len(paths) > 0
        assert sample_wav_file in paths