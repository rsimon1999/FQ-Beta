Markdown
# NeuroAcoustic Sound Studio

A modular Python-based binaural beat and acoustic soundscape generator engineered for brainwave entrainment, focus, deep sleep, and state shifting.

## Features
* **Dynamic Entrainment Ramps:** Smoothly transition brainwave states from baseline to target Hz over customizable durations.
* **Brainwave Presets:** Built-in targets for Delta, Theta, Alpha, Beta, Gamma, and Schumann Resonance.
* **Stereo Binaural Generation:** High-precision carrier tone generation built with NumPy and SciPy.
* **Modular DSP Architecture:** Easily extensible for custom waveforms, pink/brown noise filters, and multi-channel audio tracks.

## Directory Structure
├── data/              # Preset configurations and dynamic profiles
├── output/            # Generated audio files (.wav)
├── src/
│   ├── audio/         # Signal processing, generators, and engine logic
│   ├── ui/            # GUI components and interface layouts
│   └── utils/         # File exports, configuration management
├── tests/             # PyTest test suite
├── main.py            # Primary application launcher
├── requirements.txt   # Dependencies (numpy, scipy)
└── PROJECT_PLAN.md    # Development roadmap


## Quick Start

1. **Activate Virtual Environment:**
   ```bash
   source .venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
Launch Application:

Bash
python main.py