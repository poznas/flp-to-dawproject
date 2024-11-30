import pytest
from pathlib import Path

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
        data = sample_clip.to_dict()
        restored_clip = Clip.from_dict(data)
        
        assert restored_clip.name == sample_clip.name
        assert restored_clip.position == sample_clip.position
        assert restored_clip.duration == sample_clip.duration
        assert restored_clip.color == sample_clip.color
        assert str(restored_clip.source_path) == str(sample_clip.source_path)

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
        assert sample_clip.arrangement_name == "TEST_ARR"
        
        # Remove clip
        arr.remove_clip(sample_clip)
        assert len(arr.clips) == 0
        assert sample_clip.arrangement_name is None

    def test_get_duration(self, sample_clip):
        """Test arrangement duration calculation."""
        arr = Arrangement(name="TEST_ARR")
        assert arr.get_duration() == 0.0
        
        arr.add_clip(sample_clip)  # At position 0.0, duration 2.0
        assert arr.get_duration() == 2.0
        
        # Add another clip that extends beyond
        clip2 = Clip(name="clip2", position=1.5, duration=2.0, color="#00FF00")
        arr.add_clip(clip2)
        assert arr.get_duration() == 3.5  # 1.5 + 2.0

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

    def test_validate_audio_files(self, sample_project, sample_wav_file):
        """Test audio file validation."""
        assert sample_project.validate_audio_files() == True
        
        # Test with missing file
        sample_wav_file.unlink()
        assert sample_project.validate_audio_files() == False

    def test_project_serialization(self, sample_project):
        """Test project serialization to and from dict."""
        data = sample_project.to_dict()
        restored_project = Project.from_dict(data)
        
        assert restored_project.name == sample_project.name
        assert len(restored_project.arrangements) == len(sample_project.arrangements)
        assert restored_project.arrangements[0].name == sample_project.arrangements[0].name