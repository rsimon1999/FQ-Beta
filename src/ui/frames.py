"""UI Frames for Easy Mode and Advanced DSP Studio controls with Live Preview, Category Pills & Settings persistence."""

import customtkinter as ctk
from src.ui.constants import ATMOSPHERE_CHOICES, ATMOSPHERE_MAP
from presets.easy_mode import (
    EASY_MODE_PRESETS,
    CATEGORY_ORDER,
)


class EasyControlFrame(ctk.CTkFrame):
    PILL_MAP = {
        "Focus": "Focus & Attention",
        "Sleep": "Sleep & Recovery",
        "Calm": "Calm & Relaxation",
        "Flow": "Creativity & Flow",
        "Mindful": "Meditation & Mindfulness",
        "Energy": "Energy & Arousal",
        "Peak": "Peak Cognition",
    }

    def __init__(
        self,
        parent,
        generate_callback,
        preview_callback=None,
        stop_callback=None,
        save_defaults_callback=None,
        user_settings=None,
    ):
        super().__init__(parent)
        self.generate_callback = generate_callback
        self.preview_callback = preview_callback
        self.stop_callback = stop_callback
        self.save_defaults_callback = save_defaults_callback
        self.user_settings = user_settings or {}
        self.presets = EASY_MODE_PRESETS
        self._setup_ui()

    def _setup_ui(self):
        # 1. Category Pill Selector
        ctk.CTkLabel(self, text="Target State / Category:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(6, 2))
        self.pill_menu = ctk.CTkSegmentedButton(
            self,
            values=list(self.PILL_MAP.keys()),
            command=self._on_pill_changed,
            height=30,
            font=ctk.CTkFont(size=11, weight="bold"),
            selected_color="#1E88E5",
            selected_hover_color="#1565C0",
        )
        self.pill_menu.pack(fill="x", padx=15, pady=(0, 6))

        # 2. Preset Protocol Dropdown (Cascaded from active Pill)
        ctk.CTkLabel(self, text="Preset Protocol:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.preset_option = ctk.CTkOptionMenu(
            self,
            values=[],
            command=self._on_preset_selected,
            dynamic_resizing=False,
            height=30,
            font=ctk.CTkFont(size=13),
        )
        self.preset_option.pack(fill="x", padx=15, pady=(0, 4))

        # Preset Description Box
        self.desc_lbl = ctk.CTkLabel(
            self,
            text="",
            text_color="gray75",
            font=ctk.CTkFont(size=11),
            wraplength=500,
            justify="left",
            anchor="w",
        )
        self.desc_lbl.pack(fill="x", padx=15, pady=(0, 4))

        # Duration selector
        dur_row = ctk.CTkFrame(self, fg_color="transparent")
        dur_row.pack(fill="x", padx=15, pady=(2, 2))
        dur_row.columnconfigure(0, weight=1)
        dur_row.columnconfigure(1, weight=1)

        ctk.CTkLabel(dur_row, text="Duration (minutes):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w")
        self.duration_option = ctk.CTkOptionMenu(
            dur_row,
            values=["5", "10", "15", "20", "25", "30", "45", "60"],
            height=28,
        )
        default_dur = self.user_settings.get("default_duration_min", "10")
        self.duration_option.set(default_dur if default_dur in ["5", "10", "15", "20", "25", "30", "45", "60"] else "10")
        self.duration_option.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # Background Atmosphere selector
        ctk.CTkLabel(self, text="Atmosphere / Soundscape:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(2, 2))
        self.noise_option = ctk.CTkOptionMenu(self, values=ATMOSPHERE_CHOICES, height=28)
        default_atmo = self.user_settings.get("default_atmosphere", "Ocean Waves")
        self.noise_option.set(default_atmo if default_atmo in ATMOSPHERE_CHOICES else "Ocean Waves")
        self.noise_option.pack(fill="x", padx=15, pady=(0, 6))

        # Tone Volume Slider (Default: 10%)
        initial_tone = int(self.user_settings.get("tone_volume", 0.10) * 100)
        self.tone_lbl = ctk.CTkLabel(self, text=f"Binaural Tone Volume: {initial_tone}%", font=ctk.CTkFont(weight="bold"))
        self.tone_lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.tone_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_tone_lbl)
        self.tone_slider.set(initial_tone)
        self.tone_slider.pack(fill="x", padx=15, pady=(0, 6))

        # Atmosphere Volume Slider (Default: 80%)
        initial_noise = int(self.user_settings.get("noise_level", 0.80) * 100)
        self.noise_vol_lbl = ctk.CTkLabel(self, text=f"Atmosphere Volume: {initial_noise}%", font=ctk.CTkFont(weight="bold"))
        self.noise_vol_lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.noise_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_noise_lbl)
        self.noise_slider.set(initial_noise)
        self.noise_slider.pack(fill="x", padx=15, pady=(0, 8))

        # Live Preview & Audio Control Row
        preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        preview_frame.pack(fill="x", padx=15, pady=(0, 6))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)

        self.preview_btn = ctk.CTkButton(
            preview_frame,
            text="▶ Live Preview (8s)",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_preview,
        )
        self.preview_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.stop_btn = ctk.CTkButton(
            preview_frame,
            text="⏹ Stop Audio",
            fg_color="#C62828",
            hover_color="#8E0000",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_stop,
        )
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # Generate Button
        self.gen_btn = ctk.CTkButton(
            self,
            text="Generate Sound File",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            command=self._on_generate,
        )
        self.gen_btn.pack(fill="x", padx=15, pady=(2, 5))

        # Save Defaults Button
        self.save_def_btn = ctk.CTkButton(
            self,
            text="💾 Save Current Settings as Default",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray85"),
            font=ctk.CTkFont(size=11),
            command=self._on_save_defaults,
        )
        self.save_def_btn.pack(fill="x", padx=15, pady=(0, 6))

        # Initialize with first category pill
        initial_pill = "Focus"
        self.pill_menu.set(initial_pill)
        self._on_pill_changed(initial_pill)

    def _get_presets_for_category(self, category_name):
        presets = [
            name for name, data in self.presets.items()
            if data.get("category") == category_name
        ]
        presets.sort(key=str.lower)
        return presets

    def _on_pill_changed(self, pill_label):
        category_name = self.PILL_MAP.get(pill_label, "Focus & Attention")
        presets = self._get_presets_for_category(category_name)
        if presets:
            self.preset_option.configure(values=presets)
            self.preset_option.set(presets[0])
            self._on_preset_selected(presets[0])

    def _on_preset_selected(self, preset_name):
        preset_data = self.presets.get(preset_name, {})
        cat = preset_data.get("category", "")
        desc = preset_data.get("description", "")
        stages = preset_data.get("stages", [])
        total_m = sum(s.get("duration_min", 0) for s in stages)
        stage_names = " ➔ ".join(s.get("name", "") for s in stages)
        self.desc_lbl.configure(text=f"[{cat}] {desc}\nStages ({len(stages)}): {stage_names}")
        if str(total_m) in ["5", "10", "15", "20", "25", "30", "45", "60"]:
            self.duration_option.set(str(total_m))

    def _update_tone_lbl(self, val):
        self.tone_lbl.configure(text=f"Binaural Tone Volume: {int(val)}%")

    def _update_noise_lbl(self, val):
        self.noise_vol_lbl.configure(text=f"Atmosphere Volume: {int(val)}%")

    def _get_current_params(self):
        preset_name = self.preset_option.get()
        preset_data = self.presets.get(preset_name, {})
        selected_atmosphere = self.noise_option.get()
        noise_key = ATMOSPHERE_MAP.get(selected_atmosphere, selected_atmosphere.lower())
        tone_vol = self.tone_slider.get() / 100.0
        noise_vol = self.noise_slider.get() / 100.0
        total_custom_min = float(self.duration_option.get())

        stages_spec = preset_data.get("stages", [])
        orig_total_min = sum(s.get("duration_min", 10) for s in stages_spec) or 10.0
        scale = total_custom_min / float(orig_total_min)

        computed_stages = []
        for s in stages_spec:
            stage_dur_sec = max(1.0, float(s.get("duration_min", 10)) * scale * 60.0)
            computed_stages.append({
                "name": s.get("name", "Stage"),
                "start_beat": float(s.get("start_freq", 10.0)),
                "target_beat": float(s.get("end_freq", 10.0)),
                "carrier_freq": float(s.get("base_freq", 200.0)),
                "duration_sec": stage_dur_sec,
                "noise_type": noise_key,
                "tone_volume": tone_vol,
                "noise_level": noise_vol,
                "isochronic_mode": False,
                "harmonic_richness": 0.0,
            })

        first_stage = computed_stages[0] if computed_stages else {}
        return {
            "preset_name": preset_name,
            "category": preset_data.get("category", ""),
            "start_beat": first_stage.get("start_beat", 10.0),
            "target_beat": computed_stages[-1].get("target_beat", 10.0) if computed_stages else 10.0,
            "carrier_freq": first_stage.get("carrier_freq", 200.0),
            "duration_sec": total_custom_min * 60.0,
            "noise_type": noise_key,
            "tone_volume": tone_vol,
            "noise_level": noise_vol,
            "isochronic_mode": False,
            "harmonic_richness": 0.0,
            "stages": computed_stages,
            "default_atmosphere": selected_atmosphere,
            "default_duration_min": self.duration_option.get(),
        }

    def _on_preview(self):
        if self.preview_callback:
            self.preview_callback(self._get_current_params())

    def _on_stop(self):
        if self.stop_callback:
            self.stop_callback()

    def _on_generate(self):
        self.generate_callback(self._get_current_params())

    def _on_save_defaults(self):
        if self.save_defaults_callback:
            self.save_defaults_callback(self._get_current_params())


class AdvancedControlFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        generate_callback,
        preview_callback=None,
        stop_callback=None,
        save_defaults_callback=None,
        user_settings=None,
    ):
        super().__init__(parent)
        self.generate_callback = generate_callback
        self.preview_callback = preview_callback
        self.stop_callback = stop_callback
        self.save_defaults_callback = save_defaults_callback
        self.user_settings = user_settings or {}
        self._setup_ui()

    def _setup_ui(self):
        # Start & Target Beat Hz
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        start_b = str(self.user_settings.get("start_beat", 10.0))
        target_b = str(self.user_settings.get("target_beat", 10.0))
        carrier_b = str(self.user_settings.get("carrier_freq", 200.0))
        dur_b = str(self.user_settings.get("default_duration_min", "10"))

        ctk.CTkLabel(grid_frame, text="Start Beat (Hz):").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.start_beat_entry = ctk.CTkEntry(grid_frame, width=80)
        self.start_beat_entry.insert(0, start_b)
        self.start_beat_entry.grid(row=0, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_frame, text="Target Beat (Hz):").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.target_beat_entry = ctk.CTkEntry(grid_frame, width=80)
        self.target_beat_entry.insert(0, target_b)
        self.target_beat_entry.grid(row=0, column=3, padx=5, pady=4)

        # Carrier Freq & Duration
        ctk.CTkLabel(grid_frame, text="Carrier (Hz):").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.carrier_entry = ctk.CTkEntry(grid_frame, width=80)
        self.carrier_entry.insert(0, carrier_b)
        self.carrier_entry.grid(row=1, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_frame, text="Duration (min):").grid(row=1, column=2, sticky="w", padx=5, pady=4)
        self.duration_entry = ctk.CTkEntry(grid_frame, width=80)
        self.duration_entry.insert(0, dur_b)
        self.duration_entry.grid(row=1, column=3, padx=5, pady=4)

        # Atmosphere
        ctk.CTkLabel(self, text="Atmosphere / Soundscape:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(6, 2))
        self.noise_option = ctk.CTkOptionMenu(self, values=ATMOSPHERE_CHOICES, height=28)
        default_atmo = self.user_settings.get("default_atmosphere", "Ocean Waves")
        self.noise_option.set(default_atmo if default_atmo in ATMOSPHERE_CHOICES else "Ocean Waves")
        self.noise_option.pack(fill="x", padx=15, pady=(0, 6))

        # Tone Volume Slider (Default: 10%)
        initial_tone = int(self.user_settings.get("tone_volume", 0.10) * 100)
        self.tone_lbl = ctk.CTkLabel(self, text=f"Binaural Tone Volume: {initial_tone}%", font=ctk.CTkFont(weight="bold"))
        self.tone_lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.tone_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_tone_lbl)
        self.tone_slider.set(initial_tone)
        self.tone_slider.pack(fill="x", padx=15, pady=(0, 6))

        # Atmosphere Volume Slider (Default: 80%)
        initial_noise = int(self.user_settings.get("noise_level", 0.80) * 100)
        self.noise_vol_lbl = ctk.CTkLabel(self, text=f"Atmosphere Volume: {initial_noise}%", font=ctk.CTkFont(weight="bold"))
        self.noise_vol_lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.noise_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_noise_lbl)
        self.noise_slider.set(initial_noise)
        self.noise_slider.pack(fill="x", padx=15, pady=(0, 6))

        # Isochronic & Harmonics
        iso_val = bool(self.user_settings.get("isochronic_mode", False))
        self.isochronic_switch = ctk.CTkSwitch(self, text="Enable Isochronic Pulses")
        if iso_val:
            self.isochronic_switch.select()
        self.isochronic_switch.pack(anchor="w", padx=15, pady=3)

        harm_val = float(self.user_settings.get("harmonic_richness", 0.0))
        self.harmonic_lbl = ctk.CTkLabel(self, text=f"Harmonic Richness: {harm_val:.2f}")
        self.harmonic_lbl.pack(anchor="w", padx=15, pady=(2, 2))
        self.harmonic_slider = ctk.CTkSlider(self, from_=0.0, to=100, number_of_steps=20, command=self._update_harmonic_lbl)
        self.harmonic_slider.set(harm_val)
        self.harmonic_slider.pack(fill="x", padx=15, pady=(0, 8))

        # Live Preview & Audio Control Row
        preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        preview_frame.pack(fill="x", padx=15, pady=(0, 8))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(1, weight=1)

        self.preview_btn = ctk.CTkButton(
            preview_frame,
            text="▶ Live Preview (8s)",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_preview,
        )
        self.preview_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.stop_btn = ctk.CTkButton(
            preview_frame,
            text="⏹ Stop Audio",
            fg_color="#C62828",
            hover_color="#8E0000",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_stop,
        )
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # Generate Button
        self.gen_btn = ctk.CTkButton(
            self,
            text="Generate DSP Sound File",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            command=self._on_generate,
        )
        self.gen_btn.pack(fill="x", padx=15, pady=(2, 6))

        # Save Defaults Button
        self.save_def_btn = ctk.CTkButton(
            self,
            text="💾 Save Current Settings as Default",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray85"),
            font=ctk.CTkFont(size=11),
            command=self._on_save_defaults,
        )
        self.save_def_btn.pack(fill="x", padx=15, pady=(0, 8))

    def _update_tone_lbl(self, val):
        self.tone_lbl.configure(text=f"Binaural Tone Volume: {int(val)}%")

    def _update_noise_lbl(self, val):
        self.noise_vol_lbl.configure(text=f"Atmosphere Volume: {int(val)}%")

    def _update_harmonic_lbl(self, val):
        self.harmonic_lbl.configure(text=f"Harmonic Richness: {val:.2f}")

    def _get_current_params(self):
        selected_atmosphere = self.noise_option.get()
        noise_key = ATMOSPHERE_MAP.get(selected_atmosphere, selected_atmosphere.lower())
        return {
            "start_beat": float(self.start_beat_entry.get()),
            "target_beat": float(self.target_beat_entry.get()),
            "carrier_freq": float(self.carrier_entry.get()),
            "duration_sec": float(self.duration_entry.get()) * 60,
            "noise_type": noise_key,
            "tone_volume": self.tone_slider.get() / 100.0,
            "noise_level": self.noise_slider.get() / 100.0,
            "isochronic_mode": bool(self.isochronic_switch.get()),
            "harmonic_richness": float(self.harmonic_slider.get()),
            "default_atmosphere": selected_atmosphere,
            "default_duration_min": self.duration_entry.get(),
        }

    def _on_preview(self):
        if self.preview_callback:
            self.preview_callback(self._get_current_params())

    def _on_stop(self):
        if self.stop_callback:
            self.stop_callback()

    def _on_generate(self):
        self.generate_callback(self._get_current_params())

    def _on_save_defaults(self):
        if self.save_defaults_callback:
            self.save_defaults_callback(self._get_current_params())
