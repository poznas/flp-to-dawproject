# File: src/models/clip.py
"""
Data structures for audio clip representation.

Filepath: src/models/clip.py
"""
from dataclasses import dataclass

@dataclass
class Clip:
    name: str
    position: float
    duration: float
    color: str
    # TODO: Add additional clip attributes
