# NeuroAcoustic Sound Studio

A modular Python-based binaural beat and acoustic soundscape workstation engineered for brainwave entrainment, focus, deep sleep, meditation, and cognitive state shifting.

---

## Features

* **Segmented Category Pill Selector:** Quick-access pills for **Focus**, **Sleep**, **Calm**, **Flow**, **Mindful**, **Energy**, and **Peak** mental states with 27 scientifically mapped protocols.
* **Real-Time Live Preview:** Audition your binaural tone and atmosphere balance instantly (8s in-memory stream) before rendering long files to disk.
* **In-App Audio Player:** Listen to generated session files immediately inside the application.
* **High-Fidelity Ambient Soundscapes:** 11 real-world audio atmospheres (Ocean Waves, Rain, River, Forest, Wind, Thunderstorm, Pond, Camping, Wildlife, Urban, White Noise) with seamless equal-power crossfade looping and per-track gain trimming.
* **Advanced DSP Studio:** Fine-grained carrier frequency control, start/target Hz frequency sweeps, 2nd/3rd/5th harmonic overtone enrichment, and speaker-friendly isochronic pulse modulation.
* **Preference Persistence:** Save your preferred startup volume levels (default: 80% atmosphere / 10% tone) and default atmosphere with one click.
* **Resilient Architecture:** Automatic fallback to algorithmic mathematical noise filters (Butterworth low-pass swept pink/brown/white noise) and native macOS `afplay` playback fallback.

---

## Directory Structure

```
├── assets/                    # MP3 ambient soundscape field recording loops
├── data/                      # Preset schemas and persisted user_settings.json
├── output/                    # Generated session audio files (.wav)
├── presets/                   # Comprehensive 27-preset catalog (easy_mode.py)
├── scripts/                   # System health audit, cleanup, and maintenance tool
├── src/
│   ├── audio/                 # DSP engine, real-time player, and signal generators
│   ├── config/                # Preset templates and scenario configurations
│   ├── ui/                    # CustomTkinter modern dark-mode interface and frames
│   └── utils/                 # Path helpers, configuration persistence, and exporters
├── tests/                     # Unit test suite for DSP engine and preset sanity checks
├── main.py                    # Root application entry point
├── requirements.txt           # Python package dependencies
├── PROJECT_PLAN.md            # Development roadmap and phase tracking
├── AGENTS.md                  # Quick pointer to master AI documentation
└── NEUROACOUSTIC_STUDIO.md    # Master architectural specification
```

---

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Application:**
   ```bash
   python3 main.py
   ```

3. **Run System Health Audit & Tests:**
   ```bash
   python3 scripts/maintenance.py --audit
   ```