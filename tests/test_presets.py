import sys
import os

# Guarantee project root is at top of search path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from presets.easy_mode import EASY_MODE_PRESETS, get_presets_by_category

REQUIRED_PRESET_KEYS = {"description", "category", "stages"}
REQUIRED_STAGE_KEYS = {"name", "duration_min", "start_freq", "end_freq", "base_freq", "wave_type"}

def run_preset_sanity_check():
    print("=" * 60)
    print(" Running Sanity Check on Easy Mode Presets Catalog")
    print("=" * 60)

    total_presets = len(EASY_MODE_PRESETS)
    print(f"Total Presets Found: {total_presets}\n")

    errors = []

    for name, data in EASY_MODE_PRESETS.items():
        missing_top = REQUIRED_PRESET_KEYS - set(data.keys())
        if missing_top:
            errors.append(f"[{name}] Missing top-level keys: {missing_top}")

        category = data.get("category", "")
        if not category:
            errors.append(f"[{name}] Missing category specification.")

        stages = data.get("stages", [])
        if not isinstance(stages, list) or len(stages) == 0:
            errors.append(f"[{name}] 'stages' must be a non-empty list.")
            continue

        for i, stage in enumerate(stages):
            missing_stage = REQUIRED_STAGE_KEYS - set(stage.keys())
            if missing_stage:
                errors.append(f"[{name} -> Stage {i+1}] Missing stage keys: {missing_stage}")

            if not isinstance(stage.get("duration_min", 0), (int, float)) or stage.get("duration_min", 0) <= 0:
                errors.append(f"[{name} -> Stage {i+1}] Invalid 'duration_min': {stage.get('duration_min')}")
            
            if not isinstance(stage.get("start_freq", 0), (int, float)) or stage.get("start_freq", 0) <= 0:
                errors.append(f"[{name} -> Stage {i+1}] Invalid 'start_freq': {stage.get('start_freq')}")

            if not isinstance(stage.get("end_freq", 0), (int, float)) or stage.get("end_freq", 0) <= 0:
                errors.append(f"[{name} -> Stage {i+1}] Invalid 'end_freq': {stage.get('end_freq')}")

            if not isinstance(stage.get("base_freq", 0), (int, float)) or stage.get("base_freq", 0) <= 0:
                errors.append(f"[{name} -> Stage {i+1}] Invalid 'base_freq': {stage.get('base_freq')}")

    categorized = get_presets_by_category()
    print("Presets grouped by category:")
    for cat, items in categorized.items():
        print(f"  - {cat}: {len(items)} scenario(s)")
        for preset_name, _ in items:
            print(f"      • {preset_name}")

    print("\n" + "-" * 60)
    if errors:
        print(f"FAILED: Found {len(errors)} error(s):")
        for err in errors:
            print(f"  ❌ {err}")
        sys.exit(1)
    else:
        print("PASSED: All preset schemas, keys, and values are valid!")
        print("=" * 60)

if __name__ == "__main__":
    run_preset_sanity_check()
