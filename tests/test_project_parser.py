import pytest
from pathlib import Path
import pyflp

from src.core.project_parser import FLProjectParser
from src.models.project import Project
from src.models.arrangement import Arrangement
from src.models.clip import Clip

class TestFLProjectParser:
    def test_project_loading(self, sample_project_path):
        """Test that FL Studio project file loads correctly."""
        parser = FLProjectParser(str(sample_project_path))
        assert parser.fl_project is not None
        assert isinstance(parser.fl_project, pyflp.Project)

    def test_missing_project_file(self):
        """Test handling of missing project file."""
        with pytest.raises(FileNotFoundError):
            FLProjectParser("nonexistent.flp")

    def test_invalid_project_file(self, temp_dir):
        """Test handling of invalid project file."""
        invalid_file = temp_dir / "invalid.flp"
        invalid_file.write_bytes(b"not a valid flp file")
        
        with pytest.raises(Exception):
            FLProjectParser(str(invalid_file))

    def test_extract_arrangements(self, sample_project_path):
        """Test extracting arrangements from project."""
        parser = FLProjectParser(str(sample_project_path))
        arrangements = parser.extract_arrangements()
        
        assert isinstance(arrangements, list)
        assert all(isinstance(arr, Arrangement) for arr in arrangements)
        
        # Test arrangement properties
        if arrangements:  # If sample project contains arrangements
            arr = arrangements[0]
            assert isinstance(arr.name, str)
            assert len(arr.name) > 0
            assert hasattr(arr, 'clips')

    def test_clip_extraction(self, sample_project_path):
        """Test that clips are extracted with correct properties."""
        parser = FLProjectParser(str(sample_project_path))
        arrangements = parser.extract_arrangements()
        
        # Find an arrangement with clips
        clips = []
        for arr in arrangements:
            clips.extend(arr.clips)
            
        if clips:  # If sample project contains clips
            clip = clips[0]
            assert isinstance(clip, Clip)
            assert isinstance(clip.name, str)
            assert isinstance(clip.position, float)
            assert isinstance(clip.duration, float)
            assert isinstance(clip.color, str)
            assert clip.color.startswith('#')
            assert len(clip.color) == 7  # #RRGGBB format

    def test_arrangement_name_generation(self, sample_project_path):
        """Test arrangement name generation logic."""
        parser = FLProjectParser(str(sample_project_path))
        
        # Test direct arrangement name generation
        channel_group = type('MockChannel', (), {'group': 'TestGroup'})
        name = parser._get_arrangement_name(channel_group)
        assert name == 'TestGroup'
        
        # Test fallback to pattern name
        channel_pattern = type('MockChannel', (), {'group': None, 'pattern': 1})
        name = parser._get_arrangement_name(channel_pattern)
        assert name == 'Pattern_1'
        
        # Test default name
        channel_empty = type('MockChannel', (), {'group': None, 'pattern': None})
        name = parser._get_arrangement_name(channel_empty)
        assert name == 'Main'

    def test_parse_project(self, sample_project_path):
        """Test complete project parsing."""
        parser = FLProjectParser(str(sample_project_path))
        project = parser.parse_project()
        
        assert isinstance(project, Project)
        assert project.name == sample_project_path.stem
        assert project.source_path == sample_project_path
        assert len(project.arrangements) >= 0
        
        # Verify project structure
        for arrangement in project.arrangements:
            assert isinstance(arrangement, Arrangement)
            assert arrangement.name
            
            for clip in arrangement.clips:
                assert isinstance(clip, Clip)
                assert clip.position >= 0
                assert clip.duration > 0
                assert clip.name
                assert clip.color.startswith('#')

    def test_project_validation(self, sample_project_path):
        """Test that parsed project validates correctly."""
        parser = FLProjectParser(str(sample_project_path))
        project = parser.parse_project()
        
        # Should not raise any exceptions
        project.validate()
        
        # Test audio file validation if sample files exist
        validation_result = project.validate_audio_files()
        assert isinstance(validation_result, bool)