import wave
import numpy as np
import pytest
import aaf2
from pathlib import Path
import shutil
import pyflp


def generate_sine_wave(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
    """Generate a sine wave array."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * frequency * t)

def save_wav(filename: Path, audio_data: np.ndarray, channels: int = 1, sample_rate: int = 44100) -> None:
    """Save audio data as WAV file."""
    scaled = np.int16(audio_data * 32767)
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(scaled.tobytes())

@pytest.fixture(scope="session")
def fixtures_dir(tmp_path_factory) -> Path:
    """Create and return a temporary fixtures directory."""
    return tmp_path_factory.mktemp("fixtures")

@pytest.fixture(scope="session")
def sample_audio_dir(fixtures_dir) -> Path:
    """Generate test audio files and return their directory."""
    audio_dir = fixtures_dir / "audio_clips"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate audio files with different characteristics
    audio_files = [
        # clip1.wav - mono, 2 seconds, 440Hz
        ("clip1.wav", generate_sine_wave(440, 2.0), 1),
        # clip2.wav - stereo, 3 seconds, 880Hz
        ("clip2.wav", np.vstack((
            generate_sine_wave(880, 3.0),
            generate_sine_wave(880, 3.0) * 0.5
        )).T, 2),
        # clip3.wav - mono, 1 second, 330Hz
        ("clip3.wav", generate_sine_wave(330, 1.0), 1),
        # clip4.wav - stereo, 2 seconds, combined frequencies
        ("clip4.wav", np.vstack((
            generate_sine_wave(440, 2.0),
            generate_sine_wave(880, 2.0)
        )).T, 2)
    ]
    
    for filename, data, channels in audio_files:
        save_wav(audio_dir / filename, data, channels)
    
    return audio_dir

@pytest.fixture(scope="session")
def sample_project_path(fixtures_dir, sample_audio_dir) -> Path:
    """Generate sample FL Studio project file."""
    project_path = fixtures_dir / "sample_project.flp"
    
    project = pyflp.Project()
    project.tempo = 140
    
    # Add channels with different arrangements
    arrangements = {
        "MAIN": [(0, "clip1.wav"), (100, "clip2.wav")],
        "VERSE": [(200, "clip3.wav")],
        "CHORUS": [(300, "clip4.wav"), (400, "clip1.wav")]
    }
    
    for arr_name, clips in arrangements.items():
        for offset, wav_name in clips:
            channel = project.channels.samplers.add()
            channel.name = f"{arr_name}_{wav_name}"
            channel.sample_path = str(sample_audio_dir / wav_name)
            channel.start_offset = offset
            channel.length = 100
            channel.volume = 1.0
            channel.color = 0xFF0000  # red
            channel.group = arr_name
    
    with open(project_path, "wb") as f:
        f.write(project.save())
    
    return project_path

@pytest.fixture(scope="session")
def expected_aaf_path(fixtures_dir, sample_audio_dir) -> Path:
    """Generate expected AAF output file that matches our AAF generator output."""
    aaf_path = fixtures_dir / "expected_output" / "expected_arrangement.aaf"
    aaf_path.parent.mkdir(parents=True, exist_ok=True)
    
    with aaf2.open(str(aaf_path), 'w') as f:
        # Create main composition
        main_composition = f.create.MasterMob("TEST_ARRANGEMENT")
        f.content.mobs.append(main_composition)
        
        # Set basic project properties
        edit_rate = 25  # Standard frame rate
        timecode_rate = 25
        start_time = 0
        
        # Create tape source (for timecode)
        tape_mob = f.create.SourceMob()
        f.content.mobs.append(tape_mob)
        
        # Add tape slots
        tape_mob.create_tape_slots(
            "Master",
            edit_rate,
            timecode_rate,
            media_kind='picture'
        )
        
        # Create source clip that references timecode
        tape_clip = tape_mob.create_source_clip(1, start_time)
        
        # Add test clips with different properties
        test_clips = [
            {
                "name": "clip1",
                "position": 0.0,
                "duration": 2.0,
                "color": "#FF0000",
                "volume": 1.0,
                "file": "clip1.wav"
            },
            {
                "name": "clip2",
                "position": 3.0,
                "duration": 3.0,
                "color": "#00FF00",
                "volume": 0.8,
                "file": "clip2.wav"
            },
            {
                "name": "clip3",
                "position": 7.0,
                "duration": 1.0,
                "color": "#0000FF",
                "volume": 0.5,
                "file": "clip3.wav"
            }
        ]
        
        # Process each test clip
        for clip_data in test_clips:
            # Create source mob for the audio file
            source_mob = f.create.SourceMob()
            f.content.mobs.append(source_mob)
            
            # Import the audio essence
            audio_path = sample_audio_dir / clip_data["file"]
            source_mob.import_audio_essence(str(audio_path), edit_rate)
            
            # Calculate position and length in edit rate units
            position_frames = int(clip_data["position"] * edit_rate)
            length_frames = int(clip_data["duration"] * edit_rate)
            
            # Create the clip reference
            clip_slot = source_mob.create_source_clip(1, position_frames)
            clip_slot.length = length_frames
            
            # Set clip metadata
            if hasattr(clip_slot, 'user_comments'):
                clip_slot.user_comments['Name'] = clip_data["name"]
                clip_slot.user_comments['Color'] = clip_data["color"]
            
            # Apply volume
            if clip_data["volume"] != 1.0:
                try:
                    clip_slot.volume = clip_data["volume"]
                except Exception:
                    pass  # Some AAF versions might not support volume
    
    return aaf_path

@pytest.fixture
def temp_dir(tmp_path) -> Path:
    """Get temporary directory for test outputs."""
    test_dir = tmp_path / "test_output"
    test_dir.mkdir(exist_ok=True)
    return test_dir

@pytest.fixture
def sample_wav_file(temp_dir) -> Path:
    """Create a simple test WAV file."""
    wav_path = temp_dir / "test.wav"
    duration = 1.0  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
    
    # Ensure directory exists
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save as WAV
    scaled = np.int16(audio_data * 32767)
    with wave.open(str(wav_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(scaled.tobytes())
    
    return wav_path

@pytest.fixture
def sample_clip(sample_wav_file):
    """Create a sample clip instance."""
    from src.models.clip import Clip
    return Clip(
        name="test_clip",
        position=0.0,
        duration=1.0,
        color="#FF0000",
        source_path=sample_wav_file,
        volume=1.0
    )

@pytest.fixture
def sample_arrangement(sample_clip):
    """Create a sample arrangement instance."""
    from src.models.arrangement import Arrangement
    arrangement = Arrangement(name="TEST_ARRANGEMENT")
    arrangement.add_clip(sample_clip)
    return arrangement

@pytest.fixture
def sample_project(sample_arrangement, temp_dir):
    """Create a sample project instance."""
    from src.models.project import Project
    project = Project(
        name="test_project",
        source_path=temp_dir / "test.flp",
        output_dir=temp_dir / "output"
    )
    project.add_arrangement(sample_arrangement)
    return project