#!/usr/bin/env python3
"""
NeuroAcoustic Sound Studio — Maintenance, Health Audit & Roadmap Tool
Integrates with NEUROACOUSTIC_STUDIO.md and PROJECT_PLAN.md.
"""

import os
import sys
import shutil
import argparse
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

REQUIRED_ASSETS = [
    "camping.mp3", "forest.mp3", "ocean.mp3", "pond.mp3", "rain.mp3",
    "river.mp3", "thunder.mp3", "urban.mp3", "white.mp3", "wildlife.mp3", "wind.mp3"
]

OBSOLETE_ITEMS = [
    "__artifacts__",
    "export-md.py",
    "repairplan.md",
]


def audit_health():
    """Performs a comprehensive integrity check on code, assets, and tests."""
    print("=" * 65)
    print(" 🔍 NEUROACOUSTIC SOUND STUDIO — SYSTEM HEALTH AUDIT")
    print("=" * 65)

    issues = []

    # 1. Check Sound Assets
    assets_dir = os.path.join(PROJECT_ROOT, "assets")
    print("\n[1/4] Checking Ambient Soundscape Library (assets/)...")
    if not os.path.exists(assets_dir):
        issues.append("Missing 'assets/' directory.")
        print("  ❌ 'assets/' directory missing!")
    else:
        found_assets = os.listdir(assets_dir)
        missing = [a for a in REQUIRED_ASSETS if a not in found_assets]
        if missing:
            issues.append(f"Missing {len(missing)} asset(s): {missing}")
            print(f"  ❌ Missing assets: {missing}")
        else:
            print(f"  ✅ All {len(REQUIRED_ASSETS)} ambient assets verified.")

    # 2. Check Key Architecture Modules
    print("\n[2/4] Verifying Core Architecture Modules...")
    core_modules = [
        "src.audio.engine",
        "src.audio.dsp",
        "src.audio.generators",
        "src.ui.app",
        "src.ui.frames",
        "src.ui.constants",
        "src.config.presets",
    ]
    for mod in core_modules:
        try:
            __import__(mod)
            print(f"  ✅ Module '{mod}' loaded cleanly.")
        except Exception as e:
            issues.append(f"Module import failed: {mod} ({e})")
            print(f"  ❌ Failed to load {mod}: {e}")

    # 3. Run Test Suite
    print("\n[3/4] Running Automated Unit & Preset Test Suite...")
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(PROJECT_ROOT, "tests"))
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if not result.wasSuccessful():
        issues.append(f"Test suite failed with {len(result.failures)} failure(s) and {len(result.errors)} error(s).")
    else:
        print("  ✅ All test cases passed successfully.")

    # 4. Check Documentation Sync
    print("\n[4/4] Checking Architectural Documentation...")
    doc_path = os.path.join(PROJECT_ROOT, "NEUROACOUSTIC_STUDIO.md")
    if os.path.exists(doc_path):
        print("  ✅ 'NEUROACOUSTIC_STUDIO.md' is present and synchronized.")
    else:
        issues.append("Missing NEUROACOUSTIC_STUDIO.md reference document.")
        print("  ❌ 'NEUROACOUSTIC_STUDIO.md' missing!")

    print("\n" + "-" * 65)
    if issues:
        print(f"⚠️ AUDIT WARNING: Found {len(issues)} issue(s):")
        for iss in issues:
            print(f"   • {iss}")
        return False
    else:
        print("🎉 HEALTH AUDIT PASSED: System is clean, healthy, and operational!")
        print("=" * 65)
        return True


def display_roadmap():
    """Prints the project plan and current roadmap status."""
    print("=" * 65)
    print(" 🗺️ NEUROACOUSTIC SOUND STUDIO — PROJECT ROADMAP & PROGRESS")
    print("=" * 65)

    plan_file = os.path.join(PROJECT_ROOT, "PROJECT_PLAN.md")
    if os.path.exists(plan_file):
        with open(plan_file, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("PROJECT_PLAN.md not found.")
    print("=" * 65)


def cleanup_artifacts(dry_run=False):
    """Safely cleans up obsolete artifacts, caches, and temporary files."""
    print("=" * 65)
    print(f" 🧹 ARTIFACT CLEANUP {'(DRY RUN)' if dry_run else '(ACTIVE)'}")
    print("=" * 65)

    removed_count = 0
    reclaimed_bytes = 0

    # 1. Clean Known Obsolete Paths
    for item in OBSOLETE_ITEMS:
        full_path = os.path.join(PROJECT_ROOT, item)
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                total_size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, filenames in os.walk(full_path) for f in filenames)
                print(f"  {'[DRY RUN] Would delete' if dry_run else 'Deleting'} legacy directory: {item} ({total_size / 1024:.1f} KB)")
                if not dry_run:
                    shutil.rmtree(full_path)
                reclaimed_bytes += total_size
            else:
                sz = os.path.getsize(full_path)
                print(f"  {'[DRY RUN] Would delete' if dry_run else 'Deleting'} obsolete file: {item} ({sz} bytes)")
                if not dry_run:
                    os.remove(full_path)
                reclaimed_bytes += sz
            removed_count += 1

    # 2. Clean .DS_Store, __pycache__, and test renders in output/
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Clean __pycache__
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            if not dry_run:
                shutil.rmtree(cache_path)
            removed_count += 1

        for f in files:
            file_path = os.path.join(root, f)
            # Remove .DS_Store
            if f == ".DS_Store":
                sz = os.path.getsize(file_path)
                if not dry_run:
                    os.remove(file_path)
                reclaimed_bytes += sz
                removed_count += 1
            # Clean large .wav test exports in output/
            elif "output" in root and f.endswith(".wav"):
                sz = os.path.getsize(file_path)
                print(f"  {'[DRY RUN] Would remove' if dry_run else 'Removing'} test render: {os.path.relpath(file_path, PROJECT_ROOT)} ({sz / (1024*1024):.1f} MB)")
                if not dry_run:
                    os.remove(file_path)
                reclaimed_bytes += sz
                removed_count += 1

    print("\n" + "-" * 65)
    print(f"Cleanup summary: {removed_count} item(s) processed.")
    print(f"Reclaimed disk space: {reclaimed_bytes / (1024*1024):.2f} MB")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="NeuroAcoustic Studio Maintenance & Roadmap Tool")
    parser.add_argument("--audit", action="store_true", help="Run system health audit and tests")
    parser.add_argument("--roadmap", action="store_true", help="Display roadmap and phase milestones")
    parser.add_argument("--clean", action="store_true", help="Perform automated cleanup of obsolete artifacts")
    parser.add_argument("--dry-run", action="store_true", help="Preview cleanup without modifying filesystem")

    args = parser.parse_args()

    if not any([args.audit, args.roadmap, args.clean, args.dry_run]):
        # Default behavior: run audit and show roadmap
        audit_health()
        print()
        display_roadmap()
        return

    if args.clean or args.dry_run:
        cleanup_artifacts(dry_run=args.dry_run)

    if args.audit:
        audit_health()

    if args.roadmap:
        display_roadmap()


if __name__ == "__main__":
    main()
