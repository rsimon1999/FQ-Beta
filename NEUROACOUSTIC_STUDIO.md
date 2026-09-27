# NeuroAcoustic Sound Studio — AI Agent Reference & Architectural Specification

> **Target Audience:** AI Coding Agents, Pair Programmers, and Core Developers.  
> **Purpose:** Single source of truth documenting application architecture, DSP mathematics, codebase structure, data models, execution pipelines, and engineering best practices.

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

---

## 2. System Architecture & Component Hierarchy

```mermaid
graph TD
    Entry[main.py] --> MainApp[src.ui.app.MainApp (CustomTkinter)]
    
    subgraph UI_Layer ["UI Layer (src/ui/)"]
        MainApp --> EasyTab[EasyControlFrame (src/ui/frames.py)]
        MainApp --> AdvTab[AdvancedControlFrame (src/ui/frames.py)]
        EasyTab --> UIConst[src.ui.constants (ATMOSPHERE_CHOICES, ATMOSPHERE_MAP)]
        AdvTab --> UIConst
    end

    subgraph Config_Layer ["Configuration & Presets (src/config/ & presets/)"]
        UI_Presets[src.config.presets (PRESETS, SCENARIOS, SEQUENCE_TEMPLATES)]
        Catalog_Presets[presets.easy_mode (EASY_MODE_PRESETS)]
    end

    subgraph Engine_Layer ["DSP & Soundscape Engine (src/audio/)"]
        MainApp --> Engine[SoundscapeEngine (src/audio/engine.py)]
        Engine --> AssetLoader[Asset Loader & Crossfader (_load_and_loop_asset)]
        Engine --> NoiseGen[Noise Generator & Fallback Filters (generate_noise)]
        Engine --> BinauralGen[Binaural & Isochronic Synthesizer (generate_binaural_stage)]
        
        DSP_Ops[src.audio.dsp] -.-> Engine
        DSP_Gen[src.audio.generators] -.-> Engine
    end

    subgraph Storage_Layer ["Assets & Output"]
        AssetLoader --> Assets[(assets/*.mp3)]
        Engine --> OutputFile[(output/Session_*.wav)]
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
├── data/                      # Data persistence and preset configuration storage
├── engine/                    # Background batch processing engines
│   ├── __init__.py
│   └── batch_runner.py        # Threaded batch rendering executor for queued presets
├── gui/                       # Standard Tkinter / ttk alternative panel components
│   ├── __init__.py
│   ├── advanced_panel.py      # Spinbox/combobox based manual frequency panel
│   ├── batch_panel.py         # Multi-preset queue selector and batch export UI
│   └── easy_panel.py          # Categorized treeview preset explorer with stage table
├── output/                    # Destination directory for generated .wav files
├── presets/                   # Standalone preset catalogs
│   ├── __init__.py
│   └── easy_mode.py           # Deep catalog of multi-stage categorized presets
├── src/                       # Primary modular application package
│   ├── __init__.py
│   ├── audio/                 # Signal processing, math, and engine core
│   │   ├── __init__.py
│   │   ├── dsp.py             # Advanced vectorized DSP math (filters, overtones, LFOs)
│   │   ├── engine.py          # Core SoundscapeEngine class (render sessions & stages)
│   │   ├── generators.py      # Elementary sine & noise array generators
│   │   └── presets.py         # Audio layer preset stubs
│   ├── config/                # Central application configurations
│   │   ├── __init__.py
│   │   └── presets.py         # Rich single-stage and 3-stage sequence templates
│   ├── ui/                    # Active modern UI (CustomTkinter)
│   │   ├── __init__.py
│   │   ├── app.py             # MainApp window, layout, and generation orchestration
│   │   ├── constants.py       # Atmosphere dropdown labels and key mappings
│   │   └── frames.py          # EasyControlFrame and AdvancedControlFrame
│   └── utils/                 # Utility helpers
│       ├── __init__.py
│       ├── config.py
│       └── export.py
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_audio.py          # Audio engine test suite
│   └── test_presets.py        # Validation sanity checks for preset catalogs
├── main.py                    # Root application entry point
├── requirements.txt           # Python package dependencies (numpy, scipy, soundfile, customtkinter)
├── PROJECT_PLAN.md            # Roadmap, phase progress, and planned features
├── repairplan.md              # Historical bugfix and hardening audit plan
└── NEUROACOUSTIC_STUDIO.md    # This master reference document
```

---

## 4. Detailed Component Specifications

### 4.1 `main.py`
* **Role:** Entry point launcher.
* **Key Function:** Guarantees `PROJECT_ROOT` is at `sys.path[0]`, handles resilient imports of `MainApp` / `MainApplication`, and instantiates `app.mainloop()`.

### 4.2 `src/ui/app.py` (`MainApp`)
* **Framework:** `customtkinter` (`Dark` mode, `blue` theme).
* **Dimensions:** Fixed $580 \times 740\,\text{px}$.
* **Structure:**
  * Header: Title & Subtitle.
  * Tabview: `"Easy Mode"` and `"Advanced DSP Studio"`.
  * Status Bar: Live status indicator (`self.status_var`).
* **Generation Handler (`run_generation`):**
  * Receives normalized parameter dictionary from active frame.
  * Formats output path: `output/Session_<target_beat>Hz_<mins>min.wav`.
  * Calls `self.engine.render_binaural_session(...)`.
  * Displays GUI notification (`messagebox.showinfo` or `messagebox.showerror`).

### 4.3 `src/ui/frames.py` & `src/ui/constants.py`
* **`EasyControlFrame`:**
  * Built-in 4 key quick-presets: Deep Focus (Alpha - 10 Hz), Deep Sleep (Delta - 2.5 Hz), Meditation (Theta - 6.0 Hz), Relaxation (Alpha - 8.5 Hz).
  * Duration selector: 5, 10, 15, 20, 30, 45, 60 minutes.
  * Atmosphere selector from `ATMOSPHERE_CHOICES`.
  * Sliders: Binaural Tone Volume (0–100%) and Atmosphere Volume (0–100%).
* **`AdvancedControlFrame`:**
  * Exact numeric entries: `Start Beat (Hz)`, `Target Beat (Hz)`, `Carrier (Hz)`, `Duration (min)`.
  * Atmosphere selector dropdown.
  * Volume sliders: Tone Volume and Atmosphere Volume.
  * Isochronic toggle: `CTkSwitch` (`Enable Isochronic Pulses`).
  * Harmonic richness: `CTkSlider` ($0.0 - 1.0$).
* **`src/ui/constants.py`:**
  * Maps 14 human-readable UI names (`"Ocean Waves"`, `"Light Thunderstorm"`, `"Forest"`, etc.) to engine keys (`"ocean"`, `"thunder"`, `"forest"`, etc.).

### 4.4 `src/audio/engine.py` (`SoundscapeEngine`)
The flagship DSP audio synthesis engine.

#### Asset Registry & Gain Trimming
```python
ASSET_REGISTRY = {
    "rain": ("rain.mp3", 1.0),
    "pink": ("rain.mp3", 1.0),
    "wave": ("ocean.mp3", 1.0),
    "ocean": ("ocean.mp3", 1.0),
    "brown": ("ocean.mp3", 1.0),
    "white": ("white.mp3", 0.75),
    "wind": ("wind.mp3", 0.90),
    "forest": ("forest.mp3", 1.0),
    "forrest": ("forest.mp3", 1.0),
    "pond": ("pond.mp3", 1.0),
    "river": ("river.mp3", 0.45),      # Attenuated to prevent loud mix drowning
    "camping": ("camping.mp3", 0.90),
    "thunder": ("thunder.mp3", 1.0),
    "storm": ("thunder.mp3", 1.0),
    "wildlife": ("wildlife.mp3", 0.85),
    "urban": ("urban.mp3", 0.80),
}
```

#### Audio Loading & Looping (`_load_and_loop_asset`)
1. Reads MP3 via `soundfile.read(filepath, dtype='float32')`.
2. Resamples on-the-fly with `scipy.signal.resample` if native rate $\neq 44.1\,\text{kHz}$.
3. Forces dual-channel stereo formatting.
4. Performs **equal-power crossfade looping**:
   $$\text{fade\_out} = \text{linspace}(1.0, 0.0, N), \quad \text{fade\_in} = \text{linspace}(0.0, 1.0, N)$$
   $$\text{crossfaded\_boundary} = (\text{tail} \cdot \text{fade\_out}) + (\text{start} \cdot \text{fade\_in})$$
5. Applies peak normalization followed by master level and asset-specific trim.

#### Binaural Synthesis Math (`generate_binaural_stage`)
* **Phase Accumulation (Linear Ramp):**
  To prevent click/pop artifacts during frequency sweeps, instantaneous phase is computed via discrete integration:
  $$\phi_{\text{beat}}(n) = \frac{2\pi}{f_s} \sum_{k=0}^{n} f_{\text{beat}}(k)$$
  $$\phi_{\text{carrier}}(n) = 2\pi \cdot f_{\text{carrier}} \cdot t(n)$$
* **Stereo Channel Formulation:**
  $$\text{Left}(n) = V_{\text{tone}} \cdot \sin(\phi_{\text{carrier}}(n))$$
  $$\text{Right}(n) = V_{\text{tone}} \cdot \sin(\phi_{\text{carrier}}(n) + \phi_{\text{beat}}(n))$$
* **Harmonic Overtones:**
  When $\text{harmonic\_richness} = H > 0$:
  $$\text{Left}(n) \mathrel{+}= V_{\text{tone}} \cdot H \cdot 0.5 \cdot \sin(2 \cdot \phi_{\text{carrier}}(n))$$
  $$\text{Right}(n) \mathrel{+}= V_{\text{tone}} \cdot H \cdot 0.5 \cdot \sin(2 \cdot (\phi_{\text{carrier}}(n) + \phi_{\text{beat}}(n)))$$
* **Isochronic Modulation:**
  When enabled:
  $$\phi_{\text{pulse}}(n) = \frac{2\pi}{f_s} \sum_{k=0}^{n} f_{\text{beat}}(k)$$
  $$E(n) = 0.5 \cdot (1.0 + \sin(\phi_{\text{pulse}}(n)))$$
  $$\text{Left}(n) \leftarrow \text{Left}(n) \cdot E(n), \quad \text{Right}(n) \leftarrow \text{Right}(n) \cdot E(n)$$
* **Mixing & Normalization:**
  Left/Right channels sum tone arrays + stereo atmosphere arrays, with global safety clipping prevention ($\max(|\text{audio}|) > 1.0 \implies \text{audio} \leftarrow \text{audio} / \max$).

#### Multi-Stage Sequence Sessions (`render_sequence_session`)
* Renders discrete stages sequentially.
* Overlaps successive stages using a $0.5\,\text{s}$ crossfade window to ensure continuous acoustic transition without phase jumps.

---

## 5. Preset Catalogs & Data Schemas

### 5.1 Single-Stage Preset Schema (`src/config/presets.py` & `src/ui/frames.py`)
```python
{
    "start_beat": 10.0,          # float: Initial beat delta (Hz)
    "target_beat": 16.0,         # float: Final beat delta (Hz)
    "carrier_freq": 216.0,       # float: Base carrier frequency (Hz)
    "duration_sec": 300,         # int/float: Stage duration in seconds
    "harmonic_richness": 0.3,    # float: [0.0 - 1.0] overtone blend weight
    "noise_type": "pink",        # str: Key matching ATMOSPHERE_MAP / ASSET_REGISTRY
    "isochronic_mode": False,    # bool: Enable amplitude modulation pulsing
    "tone_volume": 0.10,         # float: [0.0 - 1.0] Tone mix gain
    "noise_level": 0.65          # float: [0.0 - 1.0] Atmosphere mix gain
}
```

### 5.2 Multi-Stage Sequence Schema (`presets/easy_mode.py`)
```python
"Deep Sleep & Insomnia Relief": {
    "description": "Gradual ramp from High Alpha down to Deep Delta for restorative sleep.",
    "category": "Sleep & Recovery",
    "stages": [
        {
            "name": "Wind Down",
            "duration_min": 10,
            "start_freq": 10.0,
            "end_freq": 6.0,
            "base_freq": 210.0,
            "wave_type": "sine"
        },
        ...
    ]
}
```

---

## 6. Execution Flow & Pipeline

```
[User Interaction]
       │
       ▼
[Easy/Advanced Frame] ──(Collects & Normalizes Inputs)──> [Dictionary Parameters]
                                                                  │
                                                                  ▼
                                                      [SoundscapeEngine Method]
                                                                  │
                     ┌────────────────────────────────────────────┴───────────────────────────┐
                     ▼                                                                        ▼
         [Tone & Carrier Array]                                                    [Atmosphere Loader]
   - Cumulative Phase Integration                                            - Lookup in ASSET_REGISTRY
   - Left/Right Channel Sinusoids                                            - Resample to 44.1 kHz
   - Harmonic Overtones (2x)                                                 - Equal-power crossfade loop
   - Isochronic Pulse Modulation                                             - Gain trimming & fallback DSP
                     │                                                                        │
                     └────────────────────────────┬───────────────────────────────────────────┘
                                                  ▼
                                       [Sum Channels (Stereo)]
                                                  │
                                                  ▼
                                       [Peak Range Normalizer]
                                                  │
                                                  ▼
                                      [soundfile.write (.wav)]
                                                  │
                                                  ▼
                                         [GUI Status Feedback]
```

---

## 7. Developer Guidelines & Architectural Invariants

### 7.1 Thread Safety & UI Responsiveness
* **Rule:** Audio rendering is compute-intensive (especially $30 - 60\,\text{minute}$ sessions with millions of samples).
* **Best Practice:** When rendering long sessions or batch queues, execute DSP rendering in a worker `threading.Thread` and dispatch GUI updates back to Tkinter via `self.after(0, callback)` to prevent freezing Cocoa/X11 main event loops.

### 7.2 Phase Continuity Across Stages
* **Invariant:** Never re-index $t=0$ or discretize phase with naive $2\pi f t$ during frequency ramping.
* **Correct:** Always use cumulative summation ($\phi(n) = \frac{2\pi}{f_s}\sum f(k)$) to avoid phase discontinuity clicks.

### 7.3 Resilient Import Patterns
* To ensure modules work whether invoked from `python main.py`, test runners, or subpackages:
  ```python
  import os, sys
  PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
  if PROJECT_ROOT not in sys.path:
      sys.path.insert(0, PROJECT_ROOT)
  ```

### 7.4 Audio Safety & Volume Dynamics
* Binaural beats are psychoacoustic tones requiring low amplitude ($0.05 - 0.20$) relative to background soundscapes ($0.50 - 0.80$).
* Total summed signal must always be checked and normalized before writing to disk to prevent integer overflow and audio clipping distortion.

---

## 8. Verification & Test Suite

Run the full preset catalog sanity check:
```bash
python tests/test_presets.py
```
This tests all presets in `presets/easy_mode.py` for:
1. Top-level required keys (`description`, `category`, `stages`).
2. Stage-level required keys (`name`, `duration_min`, `start_freq`, `end_freq`, `base_freq`, `wave_type`).
3. Positive numerical boundaries and valid types.

---

## 9. Future Roadmap & Addon Integration Points

1. **Multi-Stage Sequence Builder UI:** Dynamic stage editor tab in CustomTkinter allowing users to build and reorder customizable $N$-stage sound journeys.
2. **Background Batch Rendering:** Wiring `BatchRunner` with `SoundscapeEngine` for queue-based multi-file export.
3. **Lossless / Compressed Export Options:** Adding MP3/FLAC encoding via `pydub` or `ffmpeg`.
4. **Realtime Audio Preview Streamer:** Real-time low-latency audio playback buffer (e.g., via `sounddevice` or `miniaudio`) before exporting to disk.
5. **Dynamic Canvas Wave Visualizer:** Live waveform / frequency envelope preview plotting.
