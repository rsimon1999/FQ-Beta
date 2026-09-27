# NeuroAcoustic Sound Studio — Project Plan & Roadmap

## Phase 1: Modularization & Architecture Refactor
- [x] Establish formal directory hierarchy (`src/audio/`, `src/ui/`, `src/config/`, `src/utils/`).
- [x] Isolate audio engine, presets, and DSP math from GUI.
- [x] Standardize entry point via `main.py` with resilient import resolution.
- [x] Implement automated preset validation test suite (`tests/test_presets.py`).

## Phase 2: UI Modernization & UX Refinement
- [x] Migrate Tkinter UI to **CustomTkinter** for native macOS dark-mode styling.
- [x] Implement Category Pill Selector (`Focus`, `Sleep`, `Calm`, `Flow`, `Mindful`, `Energy`, `Peak`).
- [x] Build comprehensive 27-preset catalog mapped across 7 functional categories.
- [x] Add live preset description box and multi-stage sequence progression display.
- [x] Implement user preference persistence (`data/user_settings.json`) with calibrated defaults (80% Atmosphere, 10% Tone).

## Phase 3: DSP & Acoustic Upgrades
- [x] Integrate 11 ambient soundscape field recording loops with seamless equal-power crossfade looping.
- [x] Implement asset-specific gain trimming (e.g. river mix balancing).
- [x] Add dynamic low-pass swept filters for brown, pink, and white noise fallbacks.
- [x] Implement harmonic carrier overtone synthesis (2nd, 3rd, 5th harmonics).
- [x] Add Isochronic Pulse amplitude modulation option for non-headphone listening.
- [x] Ensure continuous instantaneous phase integration ($\phi(n) = \frac{2\pi}{f_s}\sum f(k)$) to eliminate clicks.

## Phase 4: Audio Playback & Live Auditioning
- [x] Implement `AudioPlayer` engine with asynchronous `sounddevice` streaming.
- [x] Add **Real-Time Live Preview (8s)** button to test acoustic balance directly from RAM without disk I/O.
- [x] Add integrated in-app audio player toolbar with instant post-render playback prompt.
- [x] Add native macOS `afplay` fallback for maximum system compatibility.

## Phase 5: Multi-Stage Sequence Planner & Advanced Exporters (Current Roadmap)
- [ ] Interactive custom sequence journey builder GUI (create, reorder, and save custom $N$-stage protocols).
- [ ] Background batch rendering queue executor.
- [ ] Lossless and compressed export formats (WAV / MP3 / FLAC).
- [ ] Canvas frequency ramp & waveform envelope visualizer.
