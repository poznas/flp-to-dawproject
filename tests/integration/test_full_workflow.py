from pathlib import Path
import pytest
import aaf2
import shutil

from src.core.project_parser import FLProjectParser
from src.core.audio_processor import AudioProcessor
from src.core.aaf_generator import AAFGenerator
from src.utils.file_manager import FileManager

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

class TestFullWorkflow:
    def test_complete_migration_flow(self, sample_project_path, temp_dir):
        """Test complete workflow from FL Studio project to AAF files."""
        # Set up output directories
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        try:
            # 1. Parse FL Studio project
            parser = FLProjectParser(str(sample_project_path))
            project = parser.parse_project()
            
            assert project is not None
            assert len(project.arrangements) > 0
            
            # 2. Process audio files
            audio_processor = AudioProcessor(str(temp_dir / "audio"))
            clip_map = {}
            
            for arrangement in project.arrangements:
                processed_clips = audio_processor.export_audio_clips(arrangement.clips)
                clip_map[arrangement] = processed_clips
                
                assert len(processed_clips) == len(arrangement.clips)
                assert all(path.exists() for path in processed_clips.values())
            
            # 3. Generate AAF files
            file_manager = FileManager(str(output_dir))
            arrangement_dirs = file_manager.create_directory_structure(project)
            
            for arrangement in project.arrangements:
                # Generate AAF
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, clip_map[arrangement])
                generator.generate_aaf(str(aaf_path))
                
                assert aaf_path.exists()
                
                # Verify AAF structure
                with aaf2.open(str(aaf_path), 'r') as f:
                    composition = next(f.content.toplevel())
                    assert composition.name == arrangement.name
                    assert len(f.content.mobs) > 0
                    
            # 4. Verify output structure
            for arrangement in project.arrangements:
                arr_dir = arrangement_dirs[arrangement]
                assert arr_dir.exists()
                assert any(arr_dir.glob("*.aaf"))
                assert (arr_dir / "audio_files").exists()
                
        except Exception as e:
            pytest.fail(f"Workflow failed: {str(e)}")

    def test_complete_workflow_output_matches_expected(self, sample_project_path, temp_dir, expected_aaf_path):
        """Test that complete workflow produces expected AAF structure."""
        # Set up output directories
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        try:
            # Parse FL Studio project
            parser = FLProjectParser(str(sample_project_path))
            project = parser.parse_project()
            
            # Process audio files
            audio_processor = AudioProcessor(str(temp_dir / "audio"))
            clip_map = {}
            
            for arrangement in project.arrangements:
                processed_clips = audio_processor.export_audio_clips(arrangement.clips)
                clip_map[arrangement] = processed_clips
            
            # Generate AAF files
            file_manager = FileManager(str(output_dir))
            arrangement_dirs = file_manager.create_directory_structure(project)
            
            for arrangement in project.arrangements:
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, clip_map[arrangement])
                generator.generate_aaf(str(aaf_path))
                
                # Compare with expected AAF
                assert compare_aaf_metadata(aaf_path, expected_aaf_path)
                
        except Exception as e:
            pytest.fail(f"Workflow failed: {str(e)}")

    def test_large_project_handling(self, temp_dir, sample_wav_file):
        """Test handling of large projects with multiple arrangements and clips."""
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        # Create test project structure
        project_path = temp_dir / "large_project.flp"
        shutil.copy2(sample_wav_file, project_path)
        
        # Create test project with multiple arrangements
        project = FLProjectParser(str(project_path)).parse_project()
        
        # Add test arrangements
        for i in range(5):  # 5 arrangements
            arrangement = project.arrangements[i]
            for j in range(200):  # 200 clips each
                clip = arrangement.clips[j]
                clip.source_path = sample_wav_file
        
        try:
            # Process project
            audio_processor = AudioProcessor(str(temp_dir / "audio"))
            file_manager = FileManager(str(output_dir))
            
            # Export audio and generate AAFs
            arrangement_dirs = file_manager.create_directory_structure(project)
            
            for arrangement in project.arrangements:
                processed_clips = audio_processor.export_audio_clips(
                    arrangement.clips,
                    max_workers=4  # Use parallel processing
                )
                
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, processed_clips)
                generator.generate_aaf(str(aaf_path))
                
                # Verify output
                assert aaf_path.exists()
                assert aaf_path.stat().st_size > 0
                
            assert len(list(output_dir.rglob("*.aaf"))) == len(project.arrangements)
            
        except Exception as e:
            pytest.fail(f"Large project handling failed: {str(e)}")
            
    def test_error_recovery(self, temp_dir, sample_project_path):
        """Test system recovery from various error conditions."""
        output_dir = temp_dir / "output"
        output_dir.mkdir(parents=True)
        
        parser = FLProjectParser(str(sample_project_path))
        project = parser.parse_project()
        
        # Test recovery from missing audio files
        audio_processor = AudioProcessor(str(temp_dir / "audio"))
        processed_clips = audio_processor.export_audio_clips(
            [clip for arr in project.arrangements for clip in arr.clips]
        )
        
        # Should continue with available files
        assert len(processed_clips) > 0
        
        # Test recovery from AAF generation errors
        file_manager = FileManager(str(output_dir))
        arrangement_dirs = file_manager.create_directory_structure(project)
        
        for arrangement in project.arrangements:
            try:
                aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
                generator = AAFGenerator(arrangement, processed_clips)
                generator.generate_aaf(str(aaf_path))
            except Exception as e:
                # Should log error and continue with next arrangement
                continue
                
        # Verify at least some AAFs were generated
        assert any(output_dir.rglob("*.aaf"))

    def test_metadata_preservation_workflow(self, temp_dir, sample_wav_file):
        """Test preservation of metadata through the complete workflow."""
        # Create test project with specific metadata
        project_path = temp_dir / "metadata_test.flp"
        shutil.copy2(sample_wav_file, project_path)
        
        parser = FLProjectParser(str(project_path))
        project = parser.parse_project()
        
        # Add test data with specific metadata
        arrangement = project.arrangements[0]
        test_clip = arrangement.clips[0]
        test_clip.color = "#FF0000"
        test_clip.volume = 0.8
        test_clip.muted = True
        
        # Process through workflow
        output_dir = temp_dir / "output"
        audio_processor = AudioProcessor(str(temp_dir / "audio"))
        processed_clips = audio_processor.export_audio_clips([test_clip])
        
        file_manager = FileManager(str(output_dir))
        arrangement_dirs = file_manager.create_directory_structure(project)
        
        aaf_path = arrangement_dirs[arrangement] / f"{arrangement.name}.aaf"
        generator = AAFGenerator(arrangement, processed_clips)
        generator.generate_aaf(str(aaf_path))
        
        # Verify metadata in AAF
        with aaf2.open(str(aaf_path), 'r') as f:
            composition = next(f.content.toplevel())
            for mob in f.content.mobs:
                if hasattr(mob, 'user_comments'):
                    comments = mob.user_comments
                    if comments.get('Name') == test_clip.name:
                        assert comments.get('Color') == "#FF0000"
                        assert comments.get('Muted') == 'true'
                        if hasattr(mob, 'volume'):
                            assert abs(mob.volume - 0.8) < 0.01