"""Test suite for FL Studio to Cubase migration tool."""

from pathlib import Path
from typing import Iterator

def get_fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"

def get_test_data_path(filename: str) -> Path:
    """Get path to a test data file."""
    return get_fixtures_dir() / filename

def iter_test_files(pattern: str) -> Iterator[Path]:
    """Iterate over test files matching glob pattern."""
    return get_fixtures_dir().glob(pattern)

__all__ = [
    'get_fixtures_dir',
    'get_test_data_path',
    'iter_test_files'
]