"""
This file parses a json struct for creating folders and organizing based on tags.
"""

import json
from pathlib import Path
from typing import Any


def mold(data: Any):
    return isinstance(data, list) and all([isinstance(x, str) for x in data])


def load_json(filename: str) -> list[str]:
    file = Path(filename)
    if not file.exists():
        raise FileNotFoundError("tags.json file not found")
    data = json.loads(file.read_text())
    if not mold(data):
        raise Exception("Invalid format, expected list[str] only")
    return data
