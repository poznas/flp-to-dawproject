import wave
import numpy as np
from pathlib import Path

def generate_test_audio_files(fixtures_dir: Path) -> None:
    """Generate test audio files for testing."""
    audio_dir = fixtures_dir / "audio_clips"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate 1-second sine wave at 440Hz (A4 note)
    sample_rate = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    sine_wave = np.sin(2 * np.pi * 440 * t)
    
    # Create test WAV files
    for i in range(1, 5):
        wav_path = audio_dir / f"clip{i}.wav"
        with wave.open(str(wav_path), 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_data = (sine_wave * 32767).astype(np.int16)
            wav_file.writeframes(wav_data.tobytes())

def generate_sample_flp(fixtures_dir: Path) -> None:
    """Generate a sample FL Studio project file for testing."""
    import pyflp
    
    project = pyflp.Project()
    project.tempo = 140
    
    # Add a few channels with samples
    for i in range(3):
        channel = project.channels.samplers.add()
        channel.name = f"Test Channel {i+1}"
        channel.sample_path = str(fixtures_dir / "audio_clips" / f"clip{i+1}.wav")
        channel.start_offset = i * 100  # stagger the clips
        channel.length = 100
        channel.volume = 1.0
        channel.color = 0xFF0000  # red
    
    # Save the project
    with open(fixtures_dir / "sample_project.flp", "wb") as f:
        f.write(project.save())

if __name__ == "__main__":
    # Get the fixtures directory relative to this file
    fixtures_dir = Path(__file__).parent / "fixtures"
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate test files
    generate_test_audio_files(fixtures_dir)
    generate_sample_flp(fixtures_dir)
    print(f"Test fixtures generated in {fixtures_dir}")