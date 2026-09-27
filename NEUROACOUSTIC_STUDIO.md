# NeuroAcoustic Sound Studio — AI Agent Reference & Architectural Specification

> **Target Audience:** AI Coding Agents, Pair Programmers, and Core Developers.  
> **Purpose:** Single source of truth documenting application architecture, DSP mathematics, codebase structure, audio playback & preview engine, preset catalog, execution pipelines, and engineering best practices.

---

## 1. Executive Summary & Core Domain

**NeuroAcoustic Sound Studio** is a Python-based digital signal processing (DSP) acoustic workstation designed for brainwave entrainment, cognitive optimization, deep meditation, sleep induction, and state-shifting audio creation.

### 1.1 Scientific & DSP Principles
* **Binaural Beat Synthesis:** Presenting two slightly differing sine frequencies independently to each ear (e.g., Left: $200\,\text{Hz}$, Right: $210\,\text{Hz}$) causes the brain's superior olivary complex to perceive a phantom third modulation tone equal to the frequency delta ($\Delta f = 10\,\text{Hz}$).
* **Dynamic Entrainment Ramps:** Smooth linear transitions from an initial brainwave state ($\text{start\_beat}$) to a target brainwave state ($\text{target\_beat}$) over a configured session duration.
* **Brainwave Frequency Bands:**
  | State | Frequency Range | Target Mental State |
  | :--- | :--- | :--- |
  | **Delta** | $0.5 - 4.0\,\text{Hz}$ | Deep restorative sleep, cellular recovery, unconscious healing |
  | **Theta** | $4.0 - 8.0\,\text{Hz}$ | Deep meditation, REM sleep, dream state, hypnagogia, creativity |
  | **Schumann** | $7.83\,\text{Hz}$ | Earth geomagnetic harmonic, grounded relaxation |
  | **Alpha** | $8.0 - 13.0\,\text{Hz}$ | Relaxed alertness, calm focus, stress reduction, flow state |
  | **Beta** | $13.0 - 30.0\,\text{Hz}$ | Active concentration, linear logic, analytical thinking |
  | **Gamma** | $30.0 - 100.0\,\text{Hz}$| High cognition, information synthesis, peak memory recall |
* **Harmonic Overtones:** Incorporates weighted upper harmonics (2nd, 3rd, 5th harmonics) atop the base carrier to enrich acoustic warmth and prevent auditory fatigue.
* **Isochronic Pulses:** Amplitude modulation envelopes applied evenly to both stereo channels for rhythmic brain entrainment audible through standard loudspeakers without headphones.
* **Acoustic Atmosphere & Dynamic Soundscapes:** Real-world field recordings (ocean, rain, river, forest, etc.) with equal-power crossfade seamless looping, per-asset gain balancing, and algorithmic fallback DSP noise filters (Butterworth low-pass swept pink/brown/white noise).
* **Calibrated Default Mix:** Default soundscape balance is configured at **80% Atmosphere Volume** and **10% Binaural Tone Volume** for optimal psychoacoustic immersion.

---

## 2. System Architecture & Component Hierarchy

```mermaid
graph TD
    Entry[main.py] --> MainApp[src.ui.app.MainApp (CustomTkinter)]
    
    subgraph UI_Layer ["UI Layer (src/ui/)"]
        MainApp --> EasyTab[EasyControlFrame (src/ui/frames.py)]
        MainApp --> AdvTab[AdvancedControlFrame (src/ui/frames.py)]
        MainApp --> PlaybackBar[In-App Playback Toolbar]
        
        EasyTab --> CategoryPills[Category Pill Bar (Focus, Sleep, Calm, Flow, Mindful, Energy, Peak)]
        EasyTab --> PresetDropdown[Preset Protocol Dropdown (presets.easy_mode)]
        EasyTab --> UIConst[src.ui.constants (ATMOSPHERE_CHOICES, ATMOSPHERE_MAP)]
        AdvTab --> UIConst
    end

    subgraph Config_Layer ["Configuration & Defaults (src/utils/ & presets/)"]
        ConfigUtil[src.utils.config (load_user_settings, save_user_settings)]
        Catalog_Presets[presets.easy_mode (EASY_MODE_PRESETS: 27 Protocols)]
        UI_Presets[src.config.presets (PRESETS, SCENARIOS, SEQUENCE_TEMPLATES)]
    end

    subgraph Engine_Layer ["DSP & Soundscape Engine (src/audio/)"]
        MainApp --> Engine[SoundscapeEngine (src/audio/engine.py)]
        MainApp --> Player[AudioPlayer (src/audio/player.py)]
        
        Player -->|Async Stream / Live Preview| SysAudio[sounddevice (Speaker Output)]
        Player -->|File Playback / Native Fallback| SoundFile[soundfile / afplay (.wav)]
        
        Engine --> AssetLoader[Asset Loader & Crossfader (_load_and_loop_asset)]
        Engine --> NoiseGen[Noise Generator & Fallback Filters (generate_noise)]
        Engine --> BinauralGen[Binaural & Isochronic Synthesizer (generate_binaural_stage)]
        
        DSP_Ops[src.audio.dsp] -.-> Engine
        DSP_Gen[src.audio.generators] -.-> Engine
    end

    subgraph Storage_Layer ["Assets & Output"]
        AssetLoader --> Assets[(assets/*.mp3)]
        Engine --> OutputFile[(output/Session_*.wav)]
        ConfigUtil --> UserConfig[(data/user_settings.json)]
    end
```

---

## 3. Directory & File Catalog

```
/Users/rian/FQ/
├── assets/                    # MP3 field recording loops for ambient soundscapes
│   ├── camping.mp3
│   ├── forest.mp3
│   ├── ocean.mp3
│   ├── pond.mp3
│   ├── rain.mp3
│   ├── river.mp3
│   ├── thunder.mp3
│   ├── urban.mp3
│   ├── white.mp3
│   ├── wildlife.mp3
│   └── wind.mp3
├── data/                      # Data persistence and user settings
│   ├── presets.json           # Catalog structure definition
│   └── user_settings.json     # Persisted user startup volume & atmosphere preferences
├── engine/                    # Background batch processing engines
│   ├── __init__.py
│   └── batch_runner.py        # Threaded batch rendering executor for queued presets
├── gui/                       # Standard Tkinter / ttk alternative panel components
│   ├── __init__.py
│   ├── advanced_panel.py      # Spinbox/combobox based manual frequency panel
│   ├── batch_panel.py         # Multi-preset queue selector and batch export UI
│   └── easy_panel.py          # Categorized treeview preset explorer with stage table
├── output/                    # Destination directory for generated .wav files
├── presets/                   # Primary categorized preset catalog
│   ├── __init__.py
│   └── easy_mode.py           # 27 multi-stage presets mapped across 7 functional categories
├── scripts/                   # System automation & maintenance
│   └── maintenance.py         # Health audit, roadmap tracker, and cleanup tool
├── src/                       # Primary modular application package
│   ├── __init__.py
│   ├── audio/                 # Signal processing, math, and engine core
│   │   ├── __init__.py
│   │   ├── dsp.py             # Advanced vectorized DSP math (filters, overtones, LFOs)
│   │   ├── engine.py          # Core SoundscapeEngine class (render sessions & stages)
│   │   ├── generators.py      # Elementary sine & noise array generators
│   │   ├── player.py          # Real-time live preview & async audio file player
│   │   └── presets.py         # Audio layer preset stubs
│   ├── config/                # Central application configurations
│   │   ├── __init__.py
│   │   └── presets.py         # Rich single-stage and 3-stage sequence templates
│   ├── ui/                    # Active modern UI (CustomTkinter)
│   │   ├── __init__.py
│   │   ├── app.py             # MainApp window, layout, and playback orchestration
│   │   ├── constants.py       # Atmosphere dropdown labels and key mappings
│   │   └── frames.py          # EasyControlFrame (Pill Selector) and AdvancedControlFrame
│   └── utils/                 # Utility helpers
│       ├── __init__.py
│       ├── config.py          # Path constants & user settings persistence (load/save)
│       └── export.py          # Preset metadata and JSON exporters
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_audio.py          # Audio engine, player, & settings unit tests
│   └── test_presets.py        # Validation sanity checks for preset catalogs
├── main.py                    # Root application entry point
├── requirements.txt           # Python package dependencies (customtkinter, numpy, scipy, soundfile, sounddevice)
├── PROJECT_PLAN.md            # Roadmap, phase progress, and planned features
├── AGENTS.md                  # Quick pointer to master AI documentation
└── NEUROACOUSTIC_STUDIO.md    # This master reference document
```

---

## 4. UI Layer & Category Pill Selector (`src/ui/frames.py`)

### 4.1 Category Pill Navigation (`EasyControlFrame`)
* **Widget:** `ctk.CTkSegmentedButton` with 7 target state pills:
  * `[ Focus ]` -> *Focus & Attention (6 presets)*
  * `[ Sleep ]` -> *Sleep & Recovery (5 presets)*
  * `[ Calm ]` -> *Calm & Relaxation (4 presets)*
  * `[ Flow ]` -> *Creativity & Flow (5 presets)*
  * `[ Mindful ]` -> *Meditation & Mindfulness (2 presets)*
  * `[ Energy ]` -> *Energy & Arousal (3 presets)*
  * `[ Peak ]` -> *Peak Cognition (2 presets)*
* **Cascade Behavior:** Clicking any pill instantly filters the `Preset Protocol` dropdown to the clean, alphabetically sorted protocols for that specific goal.
* **Live Insight Display:** Displays the category name, full descriptive summary, and sequential stage transition route (`Stages (N): Stage 1 ➔ Stage 2 ➔ Stage 3`).
* **Duration Auto-Sync:** Automatically defaults the session duration selector to the sum of the preset's stage minutes.

---

## 5. Audio Playback & Live Preview Engine (`src/audio/player.py`)

### 5.1 Real-Time In-Memory Preview (`play_preview`)
* Synthesizes an $8\text{-second}$ stereo buffer using `SoundscapeEngine.generate_binaural_stage(...)`.
* Streams non-blocking audio directly to the default audio device via `sounddevice.play(array, 44100)` without creating disk files.

### 5.2 In-App File Playback (`play_file`)
* Reads rendered `.wav` files via `soundfile.read(...)` and streams asynchronously in a background monitor thread.
* Features native macOS `afplay` fallback if `sounddevice` encounters system backend issues.
* Clean window closing protocol ensuring audio stops on application exit.

---

## 6. Verification & Health Audit

Run the system health audit at any time:
```bash
python3 scripts/maintenance.py --audit
```
Run automated unit tests:
```bash
python3 -m unittest discover tests
```
Run preset catalog verification:
```bash
python3 tests/test_presets.py
```
