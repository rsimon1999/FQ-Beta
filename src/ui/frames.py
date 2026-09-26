"""UI Frames for Easy Mode and Advanced DSP Studio controls."""

import customtkinter as ctk


class EasyControlFrame(ctk.CTkFrame):
    PRESETS = {
        "Deep Focus (Alpha - 10 Hz)": {"start_beat": 10.0, "target_beat": 10.0, "carrier_freq": 200.0},
        "Deep Sleep (Delta - 2.5 Hz)": {"start_beat": 6.0, "target_beat": 2.5, "carrier_freq": 150.0},
        "Meditation (Theta - 6.0 Hz)": {"start_beat": 10.0, "target_beat": 6.0, "carrier_freq": 180.0},
        "Relaxation (Alpha - 8.5 Hz)": {"start_beat": 12.0, "target_beat": 8.5, "carrier_freq": 210.0},
    }

    def __init__(self, parent, generate_callback):
        super().__init__(parent)
        self.generate_callback = generate_callback
        self._setup_ui()

    def _setup_ui(self):
        # Preset selection
        ctk.CTkLabel(self, text="Session Preset:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(15, 2))
        self.preset_option = ctk.CTkOptionMenu(self, values=list(self.PRESETS.keys()))
        self.preset_option.pack(fill="x", padx=15, pady=(0, 10))

        # Duration selector
        ctk.CTkLabel(self, text="Duration (minutes):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(5, 2))
        self.duration_option = ctk.CTkOptionMenu(self, values=["5", "10", "15", "20", "30", "45", "60"])
        self.duration_option.set("10")
        self.duration_option.pack(fill="x", padx=15, pady=(0, 10))

        # Background Atmosphere selector
        ctk.CTkLabel(self, text="Atmosphere / Noise:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(5, 2))
        self.noise_option = ctk.CTkOptionMenu(self, values=["Brown Noise (Ocean Waves)", "Pink Noise (Rain)", "White Noise", "None"])
        self.noise_option.set("Brown Noise (Ocean Waves)")
        self.noise_option.pack(fill="x", padx=15, pady=(0, 15))

        # Tone Volume Slider
        self.tone_lbl = ctk.CTkLabel(self, text="Binaural Tone Volume: 10%", font=ctk.CTkFont(weight="bold"))
        self.tone_lbl.pack(anchor="w", padx=15, pady=(5, 2))
        self.tone_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_tone_lbl)
        self.tone_slider.set(10)
        self.tone_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Noise Volume Slider
        self.noise_vol_lbl = ctk.CTkLabel(self, text="Atmosphere Volume: 65%", font=ctk.CTkFont(weight="bold"))
        self.noise_vol_lbl.pack(anchor="w", padx=15, pady=(5, 2))
        self.noise_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_noise_lbl)
        self.noise_slider.set(65)
        self.noise_slider.pack(fill="x", padx=15, pady=(0, 15))

        # Generate Button
        self.gen_btn = ctk.CTkButton(
            self,
            text="Generate Sound File",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self._on_generate,
        )
        self.gen_btn.pack(fill="x", padx=15, pady=(10, 15))

    def _update_tone_lbl(self, val):
        self.tone_lbl.configure(text=f"Binaural Tone Volume: {int(val)}%")

    def _update_noise_lbl(self, val):
        self.noise_vol_lbl.configure(text=f"Atmosphere Volume: {int(val)}%")

    def _on_generate(self):
        preset_data = self.PRESETS[self.preset_option.get()]
        params = {
            "start_beat": preset_data["start_beat"],
            "target_beat": preset_data["target_beat"],
            "carrier_freq": preset_data["carrier_freq"],
            "duration_sec": float(self.duration_option.get()) * 60,
            "noise_type": self.noise_option.get(),
            "tone_volume": self.tone_slider.get() / 100.0,
            "noise_level": self.noise_slider.get() / 100.0,
            "isochronic_mode": False,
            "harmonic_richness": 0.0,
        }
        self.generate_callback(params)


class AdvancedControlFrame(ctk.CTkFrame):
    def __init__(self, parent, generate_callback):
        super().__init__(parent)
        self.generate_callback = generate_callback
        self._setup_ui()

    def _setup_ui(self):
        # Start & Target Beat Hz
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(grid_frame, text="Start Beat (Hz):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.start_beat_entry = ctk.CTkEntry(grid_frame, width=80)
        self.start_beat_entry.insert(0, "10.0")
        self.start_beat_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(grid_frame, text="Target Beat (Hz):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.target_beat_entry = ctk.CTkEntry(grid_frame, width=80)
        self.target_beat_entry.insert(0, "10.0")
        self.target_beat_entry.grid(row=0, column=3, padx=5, pady=5)

        # Carrier Freq & Duration
        ctk.CTkLabel(grid_frame, text="Carrier (Hz):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.carrier_entry = ctk.CTkEntry(grid_frame, width=80)
        self.carrier_entry.insert(0, "200.0")
        self.carrier_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(grid_frame, text="Duration (min):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.duration_entry = ctk.CTkEntry(grid_frame, width=80)
        self.duration_entry.insert(0, "10")
        self.duration_entry.grid(row=1, column=3, padx=5, pady=5)

        # Atmosphere
        ctk.CTkLabel(self, text="Atmosphere / Noise:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.noise_option = ctk.CTkOptionMenu(self, values=["Brown Noise (Ocean Waves)", "Pink Noise (Rain)", "White Noise", "None"])
        self.noise_option.set("Brown Noise (Ocean Waves)")
        self.noise_option.pack(fill="x", padx=15, pady=(0, 10))

        # Tone Volume Slider
        self.tone_lbl = ctk.CTkLabel(self, text="Binaural Tone Volume: 10%", font=ctk.CTkFont(weight="bold"))
        self.tone_lbl.pack(anchor="w", padx=15, pady=(5, 2))
        self.tone_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_tone_lbl)
        self.tone_slider.set(10)
        self.tone_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Noise Volume Slider
        self.noise_vol_lbl = ctk.CTkLabel(self, text="Atmosphere Volume: 65%", font=ctk.CTkFont(weight="bold"))
        self.noise_vol_lbl.pack(anchor="w", padx=15, pady=(5, 2))
        self.noise_slider = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, command=self._update_noise_lbl)
        self.noise_slider.set(65)
        self.noise_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Isochronic & Harmonics
        self.isochronic_switch = ctk.CTkSwitch(self, text="Enable Isochronic Pulses")
        self.isochronic_switch.pack(anchor="w", padx=15, pady=5)

        self.harmonic_lbl = ctk.CTkLabel(self, text="Harmonic Richness: 0.0")
        self.harmonic_lbl.pack(anchor="w", padx=15, pady=(5, 2))
        self.harmonic_slider = ctk.CTkSlider(self, from_=0.0, to=1.0, number_of_steps=20, command=self._update_harmonic_lbl)
        self.harmonic_slider.set(0.0)
        self.harmonic_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Generate Button
        self.gen_btn = ctk.CTkButton(
            self,
            text="Generate DSP Sound File",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self._on_generate,
        )
        self.gen_btn.pack(fill="x", padx=15, pady=(10, 15))

    def _update_tone_lbl(self, val):
        self.tone_lbl.configure(text=f"Binaural Tone Volume: {int(val)}%")

    def _update_noise_lbl(self, val):
        self.noise_vol_lbl.configure(text=f"Atmosphere Volume: {int(val)}%")

    def _update_harmonic_lbl(self, val):
        self.harmonic_lbl.configure(text=f"Harmonic Richness: {val:.2f}")

    def _on_generate(self):
        params = {
            "start_beat": float(self.start_beat_entry.get()),
            "target_beat": float(self.target_beat_entry.get()),
            "carrier_freq": float(self.carrier_entry.get()),
            "duration_sec": float(self.duration_entry.get()) * 60,
            "noise_type": self.noise_option.get(),
            "tone_volume": self.tone_slider.get() / 100.0,
            "noise_level": self.noise_slider.get() / 100.0,
            "isochronic_mode": bool(self.isochronic_switch.get()),
            "harmonic_richness": float(self.harmonic_slider.get()),
        }
        self.generate_callback(params)
