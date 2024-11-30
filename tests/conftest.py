# File: tests/conftest.py
"""
PyTest configuration and shared fixtures.

Filepath: tests/conftest.py
"""
import pytest
from pathlib import Path

@pytest.fixture
def sample_project_path():
    """Fixture providing path to sample FL Studio project"""
    return Path("tests/fixtures/sample_project.flp")

@pytest.fixture
def sample_arrangement_data():
    """Fixture providing sample arrangement data"""
    return {
        "name": "NAGRYWKI_MAIN",
        "clips": [
            {
                "name": "vocal_01",
                "position": 0.0,
                "duration": 4.0,
                "color": "#FF0000"
            }
        ]
    }