# File: src/models/arrangement.py
"""
Data structures for arrangement representation.

Filepath: src/models/arrangement.py
"""
from dataclasses import dataclass
from typing import List

@dataclass
class Arrangement:
    name: str
    clips: List['Clip']
    # TODO: Add additional arrangement attributes
