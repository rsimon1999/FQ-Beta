# Brainwave Entrainment Audio Generator

A collection of Python scripts designed to generate precise, phase-locked binaural audio tracks and progressive frequency ramps layered with acoustic masking (pink noise) for cognitive state optimization.

---

## Script Overview

### 1. Master Audio Generator (`generator.py`)
Generates 5 distinct binaural beat WAV files tailored for focus, relaxation, sleep onset, high-level problem solving, and task initiation:
* **`01_Alpha_Relaxation_10Hz.wav`**: 20-minute track for light relaxation and stress reduction.
* **`02_Beta_Focus_15Hz.wav`**: 20-minute track for sustained analytical focus and working memory.
* **`03_Theta_Sleep_6Hz.wav`**: 30-minute pre-sleep transition track ending in complete silence.
* **`04_Gamma_PeakFocus_40Hz.wav`**: 20-minute track for intense problem solving and complex cognition.
* **`05_Motivation_Ramp_10Hz_to_20Hz.wav`**: 20-minute progressive frequency ramp designed to clear brain fog (10 Hz) and accelerate into high alertness (20 Hz) to overcome task aversion.

### 2. Standalone Binaural Generator (`Tones.py`)
A lightweight utility script used to produce simple, single-frequency binaural WAV files without additional background noise or progressive frequency shifts.

---

## Environment Setup & Execution Commands

Run these terminal commands from your root project directory to install dependencies and execute the scripts using your local virtual environment:

### Step 1: Install Dependencies
```bash
"/Users/rian/Desktop/untitled folder/.venv/bin/python" -m pip install numpy scipy
```

### Step 2: Execute Scripts

#### Option A: Run the Master Audio Generator (`generator.py`)
```bash
"/Users/rian/Desktop/untitled folder/.venv/bin/python" "/Users/rian/Desktop/untitled folder/generator.py"
```

#### Option B: Run the Simple Tones Generator (`Tones.py`)
```bash
"/Users/rian/Desktop/untitled folder/.venv/bin/python" "/Users/rian/Desktop/untitled folder/Tones.py"
```

---

## Playback Best Practices

* **Headphones Required:** Binaural entrainment relies on stereo isolation (Left/Right channel separation). Always use stereo headphones or earbuds (e.g., Bose QuietComfort).
* **Volume Levels:**
  * **Quiet Mode (Active Noise Cancellation):** Set device volume between **20% – 35%**.
  * **Aware / Transparency Mode:** Set device volume between **35% – 50%**.
* **Safety:** Keep volume levels comfortable ($\approx 55 \text{--} 65 \text{ dB SPL}$). High volume does not increase neural entrainment and can cause auditory fatigue.