# NeuroAcoustic Sound Studio — Project Plan

## Phase 1: Modularization & Architecture Refactor
- [x] Establish formal directory hierarchy.
- [x] Isolate audio engine, presets, and DSP math from GUI.
- [x] Standardize entry point via `main.py`.

## Phase 2: UI Modernization
- [x] Migrate Tkinter UI to **CustomTkinter** for native macOS dark-mode styling.
- [x] Implement preset dropdown selectors for instant state selection.
- [x] Add real-time frequency ramp canvas visualization (Hz over time).

## Phase 3: DSP & Acoustic Upgrades
- [x] Add dynamic low-pass swept filters for brown and pink noise (wave emulation).
- [x] Implement harmonic carrier overtones (e.g., 432 Hz + 5th harmonic).
- [x] Add Isochronic Pulse overlay option for non-headphone listening.

## Phase 4: Multi-Stage Session Planner (Current Focus)
- [ ] Build multi-phase sequence manager (e.g., 15m Focus → 5m Rest → 10m Re-energize).
- [ ] Add batch export options (WAV / MP3).
