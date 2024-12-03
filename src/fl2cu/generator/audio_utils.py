import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

class AudioAnalyzer:
    """Handles audio file analysis and metadata extraction."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_audio_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get audio file metadata using ffprobe."""
        if not file_path.exists():
            self.logger.error(f"Audio file not found: {file_path}")
            return None
            
        try:
            result = subprocess.run([
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(file_path)
            ], capture_output=True, text=True, check=True)
            
            data = json.loads(result.stdout)
            
            # Extract relevant metadata
            audio_stream = next(
                (s for s in data.get('streams', []) if s.get('codec_type') == 'audio'),
                None
            )
            
            if not audio_stream:
                self.logger.error(f"No audio stream found in {file_path}")
                return None
                
            return {
                'channels': int(audio_stream.get('channels', 2)),
                'sample_rate': int(audio_stream.get('sample_rate', 44100)),
                'duration': float(audio_stream.get('duration', 0.0)),
                'bit_depth': int(audio_stream.get('bits_per_sample', 16)),
                'codec': audio_stream.get('codec_name', 'pcm_s16le')
            }
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"ffprobe failed for {file_path}: {e.stderr}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse ffprobe output: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error analyzing audio file {file_path}: {e}")
            return None

class AudioProcessor:
    """Handles audio file processing and conversion."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analyzer = AudioAnalyzer()

    def process_audio_file(
        self,
        source_path: Path,
        dest_path: Path,
        target_sample_rate: int = 44100,
        target_bit_depth: int = 24
    ) -> bool:
        """Process audio file ensuring consistent format."""
        try:
            # Get source metadata
            metadata = self.analyzer.get_audio_metadata(source_path)
            if not metadata:
                return False

            # Check if conversion is needed
            if (metadata['sample_rate'] == target_sample_rate and 
                metadata['bit_depth'] == target_bit_depth):
                # Just copy file if no conversion needed
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                dest_path.write_bytes(source_path.read_bytes())
                return True

            # Convert audio
            result = subprocess.run([
                'ffmpeg',
                '-i', str(source_path),
                '-ar', str(target_sample_rate),
                '-c:a', f'pcm_s{target_bit_depth}le',
                '-y',  # Overwrite output file
                str(dest_path)
            ], capture_output=True, text=True, check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Audio processing failed for {source_path}: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Error processing audio file {source_path}: {e}")
            return False