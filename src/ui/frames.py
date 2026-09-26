"""User interface input controls with simplified terminology and visualizer."""

import customtkinter as ctk
from src.audio.presets import BRAINWAVE_PRESETS


class ControlFrame(ctk.CTkFrame):

    def __init__(self, parent, generate_callback):
        super().__init__(parent)
        self.generate_callback = generate_callback

        self._create_widgets()

    def _create_widgets(self):
        # --- Quick Presets Dropdown ---
        preset_lbl = ctk.CTkLabel(
            self,
            text="1. Choose a Goal (Preset):",
            font=ctk.CTkFont(weight="bold"),
        )
        preset_lbl.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))

        self.preset_options = list(BRAINWAVE_PRESETS.keys())
        self.preset_var = ctk.StringVar(value=self.preset_options[0])
        self.preset_dropdown = ctk.CTkOptionMenu(
            self,
            values=self.preset_options,
            variable=self.preset_var,
            command=self._on_preset_select,
        )
        self.preset_dropdown.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5)
        )

        # Preset Description Box
        self.desc_lbl = ctk.CTkLabel(
            self, text="", text_color="gray", wraplength=450, justify="left"
        )
        self.desc_lbl.grid(
            row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10)
        )

        # --- Listening Mode (Headphones vs Speakers) ---
        mode_lbl = ctk.CTkLabel(
            self, text="Listening Setup:", font=ctk.CTkFont(weight="bold")
        )
        mode_lbl.grid(row=3, column=0, sticky="w", padx=10, pady=(2, 2))

        self.mode_var = ctk.StringVar(value="Headphones")
        self.mode_switch = ctk.CTkSegmentedButton(
            self,
            values=["Headphones", "Speakers"],
            variable=self.mode_var,
        )
        self.mode_switch.grid(
            row=3, column=1, sticky="ew", padx=10, pady=(2, 5)
        )

        # --- Visualizer Canvas ---
        viz_title = ctk.CTkLabel(
            self,
            text="Mind State Ramp Preview:",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        viz_title.grid(row=4, column=0, sticky="w", padx=10, pady=(5, 2))

        self.canvas = ctk.CTkCanvas(
            self,
            height=65,
            bg="#1e1e1e",
            highlightthickness=1,
            highlightbackground="#333333",
        )
        self.canvas.grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10)
        )

        # --- Custom Adjustments ---
        custom_lbl = ctk.CTkLabel(
            self, text="2. Fine-Tune Sound:", font=ctk.CTkFont(weight="bold")
        )
        custom_lbl.grid(row=6, column=0, sticky="w", padx=10, pady=(5, 5))

        # Pitch (Carrier)
        self.pitch_lbl = ctk.CTkLabel(self, text="Base Tone Pitch:")
        self.pitch_lbl.grid(row=7, column=0, sticky="w", padx=10)
        self.pitch_slider = ctk.CTkSlider(
            self,
            from_=60,
            to=432,
            number_of_steps=372,
            command=self._update_labels_and_viz,
        )
        self.pitch_slider.set(216)
        self.pitch_slider.grid(row=7, column=1, sticky="ew", padx=10, pady=4)

        # Tone Warmth / Harmonics
        self.warmth_lbl = ctk.CTkLabel(self, text="Tone Warmth (Harmonics):")
        self.warmth_lbl.grid(row=8, column=0, sticky="w", padx=10)
        self.warmth_slider = ctk.CTkSlider(
            self,
            from_=0.0,
            to=0.6,
            number_of_steps=30,
            command=self._update_labels_and_viz,
        )
        self.warmth_slider.set(0.3)
        self.warmth_slider.grid(row=8, column=1, sticky="ew", padx=10, pady=4)

        # Mind State Shift (Start -> Target Beat)
        self.start_lbl = ctk.CTkLabel(self, text="Starting State (Hz):")
        self.start_lbl.grid(row=9, column=0, sticky="w", padx=10)
        self.start_slider = ctk.CTkSlider(
            self,
            from_=1,
            to=30,
            number_of_steps=29,
            command=self._update_labels_and_viz,
        )
        self.start_slider.set(15)
        self.start_slider.grid(row=9, column=1, sticky="ew", padx=10, pady=4)

        self.target_lbl = ctk.CTkLabel(self, text="Target State (Hz):")
        self.target_lbl.grid(row=10, column=0, sticky="w", padx=10)
        self.target_slider = ctk.CTkSlider(
            self,
            from_=1,
            to=40,
            number_of_steps=39,
            command=self._update_labels_and_viz,
        )
        self.target_slider.set(10)
        self.target_slider.grid(row=10, column=1, sticky="ew", padx=10, pady=4)

        # Session Duration
        self.dur_lbl = ctk.CTkLabel(self, text="Duration (Minutes):")
        self.dur_lbl.grid(row=11, column=0, sticky="w", padx=10)
        self.dur_slider = ctk.CTkSlider(
            self,
            from_=5,
            to=60,
            number_of_steps=55,
            command=self._update_labels_and_viz,
        )
        self.dur_slider.set(20)
        self.dur_slider.grid(row=11, column=1, sticky="ew", padx=10, pady=4)

        # Background Atmosphere (Noise)
        bg_lbl = ctk.CTkLabel(self, text="Background Sound:")
        bg_lbl.grid(row=12, column=0, sticky="w", padx=10, pady=(4, 5))
        self.noise_var = ctk.StringVar(value="None")
        self.noise_dropdown = ctk.CTkOptionMenu(
            self,
            values=[
                "None",
                "Brown (Ocean Waves)",
                "Pink (Steady Rain)",
                "White (Soft Static)",
            ],
            variable=self.noise_var,
        )
        self.noise_dropdown.grid(
            row=12, column=1, sticky="ew", padx=10, pady=(4, 5)
        )

        # Generate Button
        self.gen_btn = ctk.CTkButton(
            self,
            text="🎧 Create Sound File",
            fg_color="#1f538d",
            hover_color="#14375e",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_generate,
        )
        self.gen_btn.grid(
            row=13, column=0, columnspan=2, sticky="ew", padx=10, pady=(12, 10)
        )

        self._on_preset_select(self.preset_var.get())

    def _on_preset_select(self, choice):
        preset = BRAINWAVE_PRESETS.get(choice, {})
        if preset:
            self.target_slider.set(preset["target_hz"])
            self.pitch_slider.set(preset["carrier_hz"])
            self.desc_lbl.configure(text=f"💡 {preset['description']}")
            self._update_labels_and_viz()

    def _update_labels_and_viz(self, _=None):
        pitch = int(self.pitch_slider.get())
        warmth = int(self.warmth_slider.get() * 100)
        start = round(self.start_slider.get(), 1)
        target = round(self.target_slider.get(), 1)
        dur = int(self.dur_slider.get())

        self.pitch_lbl.configure(text=f"Base Tone Pitch: {pitch} Hz")
        self.warmth_lbl.configure(
            text=f"Tone Warmth: {warmth}% ({'Pure Flute' if warmth < 15 else 'Rich Acoustic' if warmth < 40 else 'Deep Warm Resonance'})"
        )
        self.start_lbl.configure(
            text=f"Starting State: {start} Hz ({self._hz_to_label(start)})"
        )
        self.target_lbl.configure(
            text=f"Target State: {target} Hz ({self._hz_to_label(target)})"
        )
        self.dur_lbl.configure(text=f"Duration: {dur} Minutes")

        self._draw_ramp_visualization(start, target, dur)

    def _draw_ramp_visualization(self, start_hz, target_hz, duration_min):
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        if w <= 1:
            w = 460
        h = 65

        padding = 15
        max_hz = 40.0

        y_start = (h - padding) - ((start_hz / max_hz) * (h - 2 * padding))
        y_target = (h - padding) - ((target_hz / max_hz) * (h - 2 * padding))

        self.canvas.create_line(
            padding, h - padding, w - padding, h - padding, fill="#333333"
        )

        self.canvas.create_line(
            padding,
            y_start,
            w - padding,
            y_target,
            fill="#3b82f6",
            width=3,
            smooth=True,
        )

        self.canvas.create_oval(
            padding - 4, y_start - 4, padding + 4, y_start + 4, fill="#60a5fa", outline=""
        )
        self.canvas.create_oval(
            w - padding - 4, y_target - 4, w - padding + 4, y_target + 4, fill="#60a5fa", outline=""
        )

        self.canvas.create_text(
            padding, y_start - 8, text=f"Start: {start_hz}Hz", fill="#a1a1aa", font=("Arial", 9), anchor="w"
        )
        self.canvas.create_text(
            w - padding, y_target - 8, text=f"End: {target_hz}Hz ({duration_min}m)", fill="#a1a1aa", font=("Arial", 9), anchor="e"
        )

    def _hz_to_label(self, hz):
        if hz < 4:
            return "Deep Sleep"
        elif hz < 8:
            return "Relax & Dream"
        elif hz < 13:
            return "Calm Focus"
        elif hz < 30:
            return "Active Thinking"
        else:
            return "Peak Brain Power"

    def _on_generate(self):
        noise_choice = self.noise_var.get().split()[0].lower()
        is_isochronic = self.mode_var.get() == "Speakers"
        params = {
            "start_beat": self.start_slider.get(),
            "target_beat": self.target_slider.get(),
            "carrier_freq": self.pitch_slider.get(),
            "harmonic_richness": self.warmth_slider.get(),
            "duration_sec": self.dur_slider.get() * 60,
            "noise_type": noise_choice if noise_choice != "none" else "none",
            "isochronic_mode": is_isochronic,
        }
        self.generate_callback(params)
