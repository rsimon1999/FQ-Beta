"""Audio and session preset metadata export utilities."""

import os
import json
from typing import Dict, Any


def export_preset_metadata(preset_data: Dict[str, Any], filepath: str) -> str:
    """Exports session configuration parameters to a JSON metadata file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(preset_data, f, indent=4)
    return filepath
