"""
Easy Mode Presets Catalog
Contains pre-configured multi-stage binaural sequences mapped to functional target states.
"""

CATEGORY_ORDER = [
    "Focus & Attention",
    "Sleep & Recovery",
    "Calm & Relaxation",
    "Creativity & Flow",
    "Meditation & Mindfulness",
    "Energy & Arousal",
    "Peak Cognition",
]

CATEGORY_TAGS = {
    "Focus & Attention": "Focus",
    "Sleep & Recovery": "Sleep",
    "Calm & Relaxation": "Calm",
    "Creativity & Flow": "Flow",
    "Meditation & Mindfulness": "Meditation",
    "Energy & Arousal": "Energy",
    "Peak Cognition": "Peak",
}

EASY_MODE_PRESETS = {
    # --- 1. FOCUS & ATTENTION ---
    "Active Working Memory": {
        "category": "Focus & Attention",
        "description": "15 Hz Beta focus for rapid information processing, note-taking, and short-term memory execution.",
        "stages": [
            {"name": "Processing Speed", "duration_min": 15, "start_freq": 15.0, "end_freq": 15.0, "base_freq": 220.0, "wave_type": "sine"}
        ]
    },
    "ADHD Attention Anchor": {
        "category": "Focus & Attention",
        "description": "Sensory-Motor Rhythm (12–15 Hz) entrainment to reduce brain fog and physical restlessness.",
        "stages": [
            {"name": "Stabilization", "duration_min": 5, "start_freq": 10.0, "end_freq": 13.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "SMR Focus Anchor", "duration_min": 35, "start_freq": 13.0, "end_freq": 15.0, "base_freq": 210.0, "wave_type": "sine"}
        ]
    },
    "Analytical Problem Solving": {
        "category": "Focus & Attention",
        "description": "18 Hz Mid-Beta stimulation designed for complex math, coding, logic analysis, and decision making.",
        "stages": [
            {"name": "Executive Functioning", "duration_min": 20, "start_freq": 18.0, "end_freq": 18.0, "base_freq": 240.0, "wave_type": "sine"}
        ]
    },
    "Deep Focus & Flow State": {
        "category": "Focus & Attention",
        "description": "Sustained Mid-Alpha and Low-Beta entrainment for deep work and programming.",
        "stages": [
            {"name": "Alpha Settling", "duration_min": 5, "start_freq": 14.0, "end_freq": 10.0, "base_freq": 210.0, "wave_type": "sine"},
            {"name": "SMR / Low Beta Focus", "duration_min": 25, "start_freq": 10.0, "end_freq": 14.0, "base_freq": 220.0, "wave_type": "sine"},
            {"name": "Flow Maintenance", "duration_min": 30, "start_freq": 14.0, "end_freq": 14.0, "base_freq": 220.0, "wave_type": "sine"}
        ]
    },
    "Deep Study & Reading": {
        "category": "Focus & Attention",
        "description": "Sustained 13 Hz Low Beta entrainment for prolonged reading comprehension and minimal cognitive fatigue.",
        "stages": [
            {"name": "Sustained Focus", "duration_min": 25, "start_freq": 13.0, "end_freq": 13.0, "base_freq": 210.0, "wave_type": "sine"}
        ]
    },
    "High-Engagement Sprint": {
        "category": "Focus & Attention",
        "description": "22 Hz High Beta protocol for timed work sprints, tight deadlines, and high-stakes alertness.",
        "stages": [
            {"name": "High Beta Sprint", "duration_min": 15, "start_freq": 22.0, "end_freq": 22.0, "base_freq": 260.0, "wave_type": "sine"}
        ]
    },

    # --- 2. SLEEP & RECOVERY ---
    "Deep Sleep & Insomnia Relief": {
        "category": "Sleep & Recovery",
        "description": "Gradual ramp from High Alpha down to Deep Delta (0.5 Hz) for restorative sleep.",
        "stages": [
            {"name": "Wind Down", "duration_min": 10, "start_freq": 10.0, "end_freq": 6.0, "base_freq": 210.0, "wave_type": "sine"},
            {"name": "Light Sleep Entry", "duration_min": 15, "start_freq": 6.0, "end_freq": 3.0, "base_freq": 180.0, "wave_type": "sine"},
            {"name": "Deep Delta Sleep", "duration_min": 35, "start_freq": 3.0, "end_freq": 0.5, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },
    "Deep Sleep Induction": {
        "category": "Sleep & Recovery",
        "description": "Steep downward transition from 8 Hz Alpha to 2.0 Hz Deep Delta to induce rapid sleep onset.",
        "stages": [
            {"name": "Sleep Ramp", "duration_min": 10, "start_freq": 8.0, "end_freq": 4.0, "base_freq": 150.0, "wave_type": "sine"},
            {"name": "Delta Induction", "duration_min": 20, "start_freq": 4.0, "end_freq": 2.0, "base_freq": 120.0, "wave_type": "sine"}
        ]
    },
    "Physical Recovery & Cellular Repair": {
        "category": "Sleep & Recovery",
        "description": "1.5 Hz Deep Delta frequency targeted at physical rest and cellular regeneration.",
        "stages": [
            {"name": "Anabolic Recovery", "duration_min": 30, "start_freq": 1.5, "end_freq": 1.5, "base_freq": 100.0, "wave_type": "sine"}
        ]
    },
    "Power Nap Recovery": {
        "category": "Sleep & Recovery",
        "description": "20-minute rapid restorative cycle with a waking Gamma ramp at the end.",
        "stages": [
            {"name": "Quick Induction", "duration_min": 5, "start_freq": 12.0, "end_freq": 4.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Theta Rest", "duration_min": 12, "start_freq": 4.0, "end_freq": 4.0, "base_freq": 150.0, "wave_type": "sine"},
            {"name": "Wake Up Booster", "duration_min": 3, "start_freq": 4.0, "end_freq": 16.0, "base_freq": 250.0, "wave_type": "sine"}
        ]
    },
    "REM Dream Induction": {
        "category": "Sleep & Recovery",
        "description": "Targeted Theta (5.5 Hz) oscillation designed to stimulate vivid dream cycles.",
        "stages": [
            {"name": "Relaxation", "duration_min": 10, "start_freq": 10.0, "end_freq": 6.0, "base_freq": 190.0, "wave_type": "sine"},
            {"name": "REM Theta Sync", "duration_min": 30, "start_freq": 6.0, "end_freq": 5.5, "base_freq": 144.0, "wave_type": "sine"}
        ]
    },

    # --- 3. CALM & RELAXATION ---
    "Anxiety Release & Calm": {
        "category": "Calm & Relaxation",
        "description": "8.5 Hz Low Alpha curve designed to damp hyperactive nervous arousal and quiet overthinking.",
        "stages": [
            {"name": "Decompression", "duration_min": 10, "start_freq": 16.0, "end_freq": 10.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Alpha Coherence", "duration_min": 20, "start_freq": 10.0, "end_freq": 8.5, "base_freq": 180.0, "wave_type": "sine"}
        ]
    },
    "Emotional Grounding": {
        "category": "Calm & Relaxation",
        "description": "Ramps from 14 Hz Beta down to 6 Hz Theta to shift emotional overwhelm into grounded processing.",
        "stages": [
            {"name": "De-escalation", "duration_min": 6, "start_freq": 14.0, "end_freq": 9.0, "base_freq": 180.0, "wave_type": "sine"},
            {"name": "Theta Integration", "duration_min": 14, "start_freq": 9.0, "end_freq": 6.0, "base_freq": 160.0, "wave_type": "sine"}
        ]
    },
    "Evening Unwind & Chill": {
        "category": "Calm & Relaxation",
        "description": "Gentle 9.0 Hz Alpha wave for evening relaxation and easing out of the workday.",
        "stages": [
            {"name": "Evening Unwind", "duration_min": 20, "start_freq": 9.0, "end_freq": 9.0, "base_freq": 180.0, "wave_type": "sine"}
        ]
    },
    "Post-Work Decompression": {
        "category": "Calm & Relaxation",
        "description": "Smooth transition from intense Beta work state down to relaxing Alpha.",
        "stages": [
            {"name": "Beta Downshift", "duration_min": 10, "start_freq": 20.0, "end_freq": 12.0, "base_freq": 220.0, "wave_type": "sine"},
            {"name": "Alpha Unwind", "duration_min": 15, "start_freq": 12.0, "end_freq": 9.0, "base_freq": 190.0, "wave_type": "sine"}
        ]
    },

    # --- 4. CREATIVITY & FLOW ---
    "Alpha Flow State": {
        "category": "Creativity & Flow",
        "description": "10 Hz Alpha anchor state balancing relaxed awareness with frictionless creative productivity.",
        "stages": [
            {"name": "Alpha Flow", "duration_min": 20, "start_freq": 10.0, "end_freq": 10.0, "base_freq": 200.0, "wave_type": "sine"}
        ]
    },
    "Creative Breakthrough (Hypnagogic)": {
        "category": "Creativity & Flow",
        "description": "7.5 Hz Theta entrainment encouraging visual imagination, non-linear thinking, and creative insight.",
        "stages": [
            {"name": "Alpha Entry", "duration_min": 5, "start_freq": 10.0, "end_freq": 7.5, "base_freq": 180.0, "wave_type": "sine"},
            {"name": "Theta Insight", "duration_min": 15, "start_freq": 7.5, "end_freq": 7.5, "base_freq": 180.0, "wave_type": "sine"}
        ]
    },
    "Creative Ideation (Schumann)": {
        "category": "Creativity & Flow",
        "description": "Alpha/Theta crossover (7.83 Hz) tuned to Schumann resonance for creative synthesis.",
        "stages": [
            {"name": "Mind Clearing", "duration_min": 5, "start_freq": 12.0, "end_freq": 8.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Schumann Flow", "duration_min": 25, "start_freq": 8.0, "end_freq": 7.83, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },
    "Divergent Brainstorming": {
        "category": "Creativity & Flow",
        "description": "6.0 Hz Deep Theta curve for conceptual ideation, association building, and abstract problem solving.",
        "stages": [
            {"name": "Deep Ideation", "duration_min": 15, "start_freq": 6.0, "end_freq": 6.0, "base_freq": 170.0, "wave_type": "sine"}
        ]
    },
    "Midday Reset / Work Break": {
        "category": "Creativity & Flow",
        "description": "11 Hz High Alpha refresher session to clear mental fatigue between intensive work blocks.",
        "stages": [
            {"name": "Cognitive Wash", "duration_min": 10, "start_freq": 11.0, "end_freq": 11.0, "base_freq": 200.0, "wave_type": "sine"}
        ]
    },

    # --- 5. MEDITATION & MINDFULNESS ---
    "Transcendental Deep Theta": {
        "category": "Meditation & Mindfulness",
        "description": "Low-Theta entrainment (4.5 Hz) for deep meditative introspection.",
        "stages": [
            {"name": "Introductory Relaxation", "duration_min": 8, "start_freq": 10.0, "end_freq": 6.0, "base_freq": 150.0, "wave_type": "sine"},
            {"name": "Deep Theta Hold", "duration_min": 30, "start_freq": 6.0, "end_freq": 4.5, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },
    "Zen Meditation & Mindfulness": {
        "category": "Meditation & Mindfulness",
        "description": "Deep Theta dive (5.5 Hz) tuned to Earth's resonance harmonic.",
        "stages": [
            {"name": "Centering", "duration_min": 5, "start_freq": 12.0, "end_freq": 7.83, "base_freq": 136.1, "wave_type": "sine"},
            {"name": "Deep Theta Meditation", "duration_min": 20, "start_freq": 7.83, "end_freq": 5.5, "base_freq": 136.1, "wave_type": "sine"},
            {"name": "Return to Awareness", "duration_min": 5, "start_freq": 5.5, "end_freq": 10.0, "base_freq": 136.1, "wave_type": "sine"}
        ]
    },

    # --- 6. ENERGY & AROUSAL ---
    "Hyper-Arousal Down-Ramp (De-Agitation)": {
        "category": "Energy & Arousal",
        "description": "Downward sweep from 18 Hz High Beta to 8.5 Hz Low Alpha to soothe over-caffeinated or frantic energy.",
        "stages": [
            {"name": "Catch Speed", "duration_min": 3, "start_freq": 18.0, "end_freq": 14.0, "base_freq": 210.0, "wave_type": "sine"},
            {"name": "Alpha Down-Ramp", "duration_min": 12, "start_freq": 14.0, "end_freq": 8.5, "base_freq": 180.0, "wave_type": "sine"}
        ]
    },
    "Morning Energy Kickstart": {
        "category": "Energy & Arousal",
        "description": "Ramps from relaxed wakefulness up to energizing High Beta (20 Hz).",
        "stages": [
            {"name": "Awakening", "duration_min": 3, "start_freq": 8.0, "end_freq": 12.0, "base_freq": 200.0, "wave_type": "sine"},
            {"name": "Beta Activation", "duration_min": 12, "start_freq": 12.0, "end_freq": 20.0, "base_freq": 250.0, "wave_type": "sine"}
        ]
    },
    "Pre-Workout & Physical Amp-Up": {
        "category": "Energy & Arousal",
        "description": "High-intensity ramp into 35 Hz Beta/Gamma for adrenaline, physical drive, and motor preparation.",
        "stages": [
            {"name": "Activation", "duration_min": 4, "start_freq": 15.0, "end_freq": 25.0, "base_freq": 280.0, "wave_type": "sine"},
            {"name": "Gamma Peak", "duration_min": 6, "start_freq": 25.0, "end_freq": 35.0, "base_freq": 310.0, "wave_type": "sine"}
        ]
    },

    # --- 7. PEAK COGNITION ---
    "40 Hz Gamma Peak Cognition": {
        "category": "Peak Cognition",
        "description": "40 Hz Gamma wave entrainment associated with neural synchronization and memory consolidation.",
        "stages": [
            {"name": "Preparation", "duration_min": 5, "start_freq": 10.0, "end_freq": 18.0, "base_freq": 220.0, "wave_type": "sine"},
            {"name": "40 Hz Gamma Focus", "duration_min": 25, "start_freq": 40.0, "end_freq": 40.0, "base_freq": 240.0, "wave_type": "sine"},
            {"name": "Cool Down", "duration_min": 5, "start_freq": 18.0, "end_freq": 10.0, "base_freq": 210.0, "wave_type": "sine"}
        ]
    },
    "Sensory Binding & Insight (42 Hz Gamma)": {
        "category": "Peak Cognition",
        "description": "42 Hz Gamma frequency for perceptual clarity, holistic problem solving, and sensory integration.",
        "stages": [
            {"name": "High Gamma Processing", "duration_min": 15, "start_freq": 42.0, "end_freq": 42.0, "base_freq": 320.0, "wave_type": "sine"}
        ]
    }
}


def get_formatted_preset_catalog(category_filter: str = "All"):
    """
    Returns (formatted_display_labels, label_to_preset_key_map)
    sorted by defined Category order, then Alphabetically within each category.
    """
    display_labels = []
    label_map = {}

    for cat in CATEGORY_ORDER:
        if category_filter != "All" and category_filter != cat:
            continue

        tag = CATEGORY_TAGS.get(cat, cat)
        # Gather presets under this category and sort alphabetically by name
        cat_presets = [
            (name, data) for name, data in EASY_MODE_PRESETS.items()
            if data.get("category") == cat
        ]
        cat_presets.sort(key=lambda item: item[0].lower())

        for name, data in cat_presets:
            display_label = f"[{tag}] {name}"
            display_labels.append(display_label)
            label_map[display_label] = name

    return display_labels, label_map


def get_presets_by_category():
    """Returns scenarios grouped by category for GUI treeviews and batch runners."""
    categorized = {}
    for name, data in EASY_MODE_PRESETS.items():
        cat = data.get("category", "General")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append((name, data))
    return categorized
