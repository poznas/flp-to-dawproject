# File: src/models/project.py
"""
Data structures for FL Studio project representation.

Filepath: src/models/project.py
"""
from dataclasses import dataclass
from typing import List

@dataclass
class Project:
    name: str
    arrangements: List['Arrangement']
    # TODO: Add additional project attributes