"""Application configuration, default paths, and user preference persistence."""

import os
import json
from typing import Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
DEFAULT_ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
DEFAULT_DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DEFAULT_SAMPLE_RATE = 44100
SETTINGS_FILE = os.path.join(DEFAULT_DATA_DIR, "user_settings.json")

DEFAULT_USER_SETTINGS: Dict[str, Any] = {
    "tone_volume": 0.10,        # 10% binaural tone volume
    "noise_level": 0.80,        # 80% atmosphere volume
    "default_atmosphere": "Ocean Waves",
    "default_duration_min": "10",
    "isochronic_mode": False,
    "harmonic_richness": 0.0,
    "start_beat": 10.0,
    "target_beat": 10.0,
    "carrier_freq": 200.0,
}


def load_user_settings() -> Dict[str, Any]:
    """Loads saved user preferences from JSON, falling back to defaults."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                merged = dict(DEFAULT_USER_SETTINGS)
                merged.update(saved)
                return merged
        except Exception as e:
            print(f"Warning: Could not read settings file ({e}). Using defaults.")
    return dict(DEFAULT_USER_SETTINGS)


def save_user_settings(settings: Dict[str, Any]) -> bool:
    """Saves user preferences to JSON file."""
    os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)
    try:
        current = load_user_settings()
        current.update(settings)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False
