"""
Advanced Mode Panel GUI Component
Provides fine-grained manual frequency controls, custom stage building, and wave parameters.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class AdvancedModePanel(ttk.Frame):
    def __init__(self, parent, on_apply_custom_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.on_apply_custom_callback = on_apply_custom_callback
        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Signal Generator Parameters
        param_frame = ttk.LabelFrame(self, text=" Custom Signal Parameters ", padding=15)
        param_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        param_frame.columnconfigure(1, weight=1)

        ttk.Label(param_frame, text="Base Frequency (Hz):").grid(row=0, column=0, sticky="w", pady=5)
        self.base_freq_spin = ttk.Spinbox(param_frame, from_=20.0, to=1000.0, increment=1.0)
        self.base_freq_spin.set(200.0)
        self.base_freq_spin.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(param_frame, text="Binaural Beat Freq (Hz):").grid(row=1, column=0, sticky="w", pady=5)
        self.beat_freq_spin = ttk.Spinbox(param_frame, from_=0.1, to=50.0, increment=0.1)
        self.beat_freq_spin.set(10.0)
        self.beat_freq_spin.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(param_frame, text="Duration (Minutes):").grid(row=2, column=0, sticky="w", pady=5)
        self.dur_spin = ttk.Spinbox(param_frame, from_=1, to=120, increment=1)
        self.dur_spin.set(15)
        self.dur_spin.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(param_frame, text="Waveform Shape:").grid(row=3, column=0, sticky="w", pady=5)
        self.wave_combo = ttk.Combobox(param_frame, values=["sine", "triangle", "square", "sawtooth"], state="readonly")
        self.wave_combo.set("sine")
        self.wave_combo.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Action Trigger
        apply_btn = ttk.Button(param_frame, text="Generate & Load Custom Session", command=self._on_apply)
        apply_btn.grid(row=4, column=0, columnspan=2, sticky="e", pady=(15, 0))

    def _on_apply(self):
        try:
            custom_data = {
                "name": "Custom Session",
                "description": "User-defined custom frequency generator curve.",
                "category": "Custom",
                "stages": [
                    {
                        "name": "Manual Stage",
                        "duration_min": float(self.dur_spin.get()),
                        "start_freq": float(self.beat_freq_spin.get()),
                        "end_freq": float(self.beat_freq_spin.get()),
                        "base_freq": float(self.base_freq_spin.get()),
                        "wave_type": self.wave_combo.get()
                    }
                ]
            }
            if self.on_apply_custom_callback:
                self.on_apply_custom_callback(custom_data)
            else:
                messagebox.showinfo("Custom Stage Created", "Loaded custom signal parameters into audio engine.")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please check input values: {e}")
