import pytest
import numpy as np
import wave
import shutil
from pathlib import Path

from src.models.clip import Clip
from src.models.arrangement import Arrangement
from src.models.project import Project

def generate_sine_wave(frequency: float = 440, duration: float = 1.0, sample_rate: int = 44100) -> np.ndarray:
    """Generate a sine wave array."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * frequency * t)

def save_wav(filename: Path, audio_data: np.ndarray, channels: int = 1, sample_rate: int = 44100) -> None:
    """Save audio data as WAV file."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    scaled = np.int16(audio_data * 32767)
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(scaled.tobytes())

@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Get fixtures directory."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory) -> Path:
    """Create temporary directory for test outputs."""
    test_dir = tmp_path_factory.mktemp("test_output")
    return test_dir

@pytest.fixture
def sample_wav_file(temp_dir: Path) -> Path:
    """Create a simple test WAV file."""
    wav_path = temp_dir / "test.wav"
    audio_data = generate_sine_wave(440, 1.0)
    save_wav(wav_path, audio_data)
    return wav_path

@pytest.fixture
def sample_clip(sample_wav_file: Path) -> Clip:
    """Create a sample clip instance."""
    return Clip(
        name="test_clip",
        position=0.0,
        duration=2.0,  # Fixed duration to match test expectations
        color="#FF0000",
        source_path=sample_wav_file,
        volume=1.0,
        muted=False
    )

@pytest.fixture
def sample_arrangement(sample_clip: Clip) -> Arrangement:
    """Create a sample arrangement instance."""
    arrangement = Arrangement(name="TEST_ARRANGEMENT")
    arrangement.add_clip(sample_clip)
    return arrangement

@pytest.fixture
def sample_project(sample_arrangement: Arrangement, temp_dir: Path) -> Project:
    """Create a sample project instance."""
    project = Project(
        name="test_project",
        source_path=temp_dir / "test.flp",
        output_dir=temp_dir / "output"
    )
    project.add_arrangement(sample_arrangement)
    return project

@pytest.fixture
def expected_aaf_path(fixtures_dir: Path) -> Path:
    """Get path to expected AAF file."""
    return fixtures_dir / "expected_output" / "expected_arrangement.aaf"

@pytest.fixture(autouse=True)
def cleanup_temp_files(temp_dir: Path):
    """Clean up temporary files after each test."""
    yield
    if temp_dir.exists():
        shutil.rmtree(temp_dir)