"""
Easy Mode Presets Catalog
Contains pre-configured multi-stage binaural sequences mapped to functional target states.
"""

EASY_MODE_PRESETS = {
    # --- SLEEP & RECOVERY ---
    "Deep Sleep & Insomnia Relief": {
        "description": "Gradual ramp from High Alpha down to Deep Delta (0.5 Hz) for restorative sleep.",
        "category": "Sleep & Recovery",
        "stages": [
            {"name": "Wind Down", "duration_min": 10, "start_freq": 10.0, "end_freq": 6.0, "base_freq": 210.0, "wave_type": "sine"},
            {"name": "Light Sleep Entry", "duration_min": 15, "start_freq": 6.0, "end_freq": 3.0, "base_freq": 180.0, "wave_type": "sine"},
            {"name": "Deep Delta Sleep", "duration_min": 35, "start_freq": 3.0, "end_freq": 0.5, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },
    "Power Nap Recovery": {
        "description": "20-minute rapid restorative cycle with a waking Gamma ramp at the end.",
        "category": "Sleep & Recovery",
        "stages": [
            {"name": "Quick Induction", "duration_min": 5, "start_freq": 12.0, "end_freq": 4.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Theta Rest", "duration_min": 12, "start_freq": 4.0, "end_freq": 4.0, "base_freq": 150.0, "wave_type": "sine"},
            {"name": "Wake Up Booster", "duration_min": 3, "start_freq": 4.0, "end_freq": 16.0, "base_freq": 250.0, "wave_type": "sine"}
        ]
    },
    "REM Dream Induction": {
        "description": "Targeted Theta (5.5 Hz) oscillation designed to stimulate vivid dream cycles.",
        "category": "Sleep & Recovery",
        "stages": [
            {"name": "Relaxation", "duration_min": 10, "start_freq": 10.0, "end_freq": 6.0, "base_freq": 190.0, "wave_type": "sine"},
            {"name": "REM Theta Sync", "duration_min": 30, "start_freq": 6.0, "end_freq": 5.5, "base_freq": 144.0, "wave_type": "sine"}
        ]
    },

    # --- FOCUS & PRODUCTIVITY ---
    "Deep Focus & Flow State": {
        "description": "Sustained Mid-Alpha and Low-Beta entrainment for deep work and coding.",
        "category": "Focus & Productivity",
        "stages": [
            {"name": "Alpha Settling", "duration_min": 5, "start_freq": 14.0, "end_freq": 10.0, "base_freq": 210.0, "wave_type": "sine"},
            {"name": "SMR / Low Beta Focus", "duration_min": 25, "start_freq": 10.0, "end_freq": 14.0, "base_freq": 220.0, "wave_type": "sine"},
            {"name": "Flow Maintenance", "duration_min": 30, "start_freq": 14.0, "end_freq": 14.0, "base_freq": 220.0, "wave_type": "sine"}
        ]
    },
    "ADHD Attention Anchor": {
        "description": "Sensory-Motor Rhythm (12–15 Hz) entrainment to reduce brain fog and distraction.",
        "category": "Focus & Productivity",
        "stages": [
            {"name": "Stabilization", "duration_min": 5, "start_freq": 10.0, "end_freq": 13.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "SMR Focus Anchor", "duration_min": 35, "start_freq": 13.0, "end_freq": 15.0, "base_freq": 210.0, "wave_type": "sine"}
        ]
    },
    "Creative Ideation": {
        "description": "Alpha/Theta crossover (7.83 Hz) tuned to Schumann resonance for creative synthesis.",
        "category": "Focus & Productivity",
        "stages": [
            {"name": "Mind Clearing", "duration_min": 5, "start_freq": 12.0, "end_freq": 8.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Schumann Flow", "duration_min": 25, "start_freq": 8.0, "end_freq": 7.83, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },

    # --- STRESS & RELAXATION ---
    "Anxiety Release": {
        "description": "Calm Alpha wave stabilization to lower nervous system arousal and quiet overthinking.",
        "category": "Stress & Relaxation",
        "stages": [
            {"name": "Decompression", "duration_min": 10, "start_freq": 16.0, "end_freq": 10.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Alpha Coherence", "duration_min": 20, "start_freq": 10.0, "end_freq": 8.0, "base_freq": 180.0, "wave_type": "sine"}
        ]
    },
    "Post-Work Decompression": {
        "description": "Smooth transition from intense Beta work state down to relaxing Alpha.",
        "category": "Stress & Relaxation",
        "stages": [
            {"name": "Beta Downshift", "duration_min": 10, "start_freq": 20.0, "end_freq": 12.0, "base_freq": 220.0, "wave_type": "sine"},
            {"name": "Alpha Unwind", "duration_min": 15, "start_freq": 12.0, "end_freq": 9.0, "base_freq": 190.0, "wave_type": "sine"}
        ]
    },

    # --- MEDITATION & CONSCIOUSNESS ---
    "Zen Meditation & Mindfulness": {
        "description": "Deep Theta dive (5.5 Hz) tuned to Earths resonance harmonic.",
        "category": "Meditation & Consciousness",
        "stages": [
            {"name": "Centering", "duration_min": 5, "start_freq": 12.0, "end_freq": 7.83, "base_freq": 136.1, "wave_type": "sine"},
            {"name": "Deep Theta Meditation", "duration_min": 20, "start_freq": 7.83, "end_freq": 5.5, "base_freq": 136.1, "wave_type": "sine"},
            {"name": "Return to Awareness", "duration_min": 5, "start_freq": 5.5, "end_freq": 10.0, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },
    "Transcendental Deep Theta": {
        "description": "Low-Theta entrainment (4.5 Hz) for deep meditative introspection.",
        "category": "Meditation & Consciousness",
        "stages": [
            {"name": "Introductory Relaxation", "duration_min": 8, "start_freq": 10.0, "end_freq": 6.0, "base_freq": 150.0, "wave_type": "sine"},
            {"name": "Deep Theta Hold", "duration_min": 30, "start_freq": 6.0, "end_freq": 4.5, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },

    # --- COGNITIVE PERFORMANCE ---
    "High Cognition & Memory Recall": {
        "description": "Gamma frequency stimulation (40 Hz) designed for complex problem solving.",
        "category": "Cognitive Performance",
        "stages": [
            {"name": "Preparation", "duration_min": 5, "start_freq": 10.0, "end_freq": 18.0, "base_freq": 220.0, "wave_type": "sine"},
            {"name": "40 Hz Gamma Focus", "duration_min": 25, "start_freq": 40.0, "end_freq": 40.0, "base_freq": 240.0, "wave_type": "sine"},
            {"name": "Cool Down", "duration_min": 5, "start_freq": 18.0, "end_freq": 10.0, "base_freq": 210.0, "wave_type": "sine"}
        ]
    },

    # --- ENERGY & VITALITY ---
    "Morning Energy Kickstart": {
        "description": "Ramps from relaxed wakefulness up to energizing High Beta (20 Hz).",
        "category": "Energy & Vitality",
        "stages": [
            {"name": "Awakening", "duration_min": 3, "start_freq": 8.0, "end_freq": 12.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Beta Activation", "duration_min": 12, "start_freq": 12.0, "end_freq": 20.0, "base_freq": 250.0, "wave_type": "sine"}
        ]
    }
}

def get_presets_by_category():
    """Returns scenarios grouped by category for GUI populating."""
    categorized = {}
    for name, data in EASY_MODE_PRESETS.items():
        cat = data.get("category", "General")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append((name, data))
    return categorized
