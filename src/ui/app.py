"""Main CustomTkinter window application supporting Tabview controls."""
import os
import customtkinter as ctk
from tkinter import messagebox

from src.audio.engine import SoundscapeEngine
from src.ui.frames import ControlFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NeuroAcoustic Sound Studio")
        self.geometry("560x680")
        self.resizable(False, False)
        self.engine = SoundscapeEngine()
        self._setup_ui()

    def _setup_ui(self):
        # Header Title
        title_lbl = ctk.CTkLabel(
            self,
            text="NeuroAcoustic Studio",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_lbl.pack(anchor="w", padx=20, pady=(15, 2))

        subtitle_lbl = ctk.CTkLabel(
            self,
            text="Custom Brainwave & Soundscape Generator",
            text_color="gray",
        )
        subtitle_lbl.pack(anchor="w", padx=20, pady=(0, 10))

        # Main Tabview Interface
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        self.tab_easy = self.tabview.add("Easy Mode")
        self.tab_advanced = self.tabview.add("Advanced DSP Studio")

        # Easy Mode Controls
        self.control_frame = ControlFrame(
            self.tab_easy, generate_callback=self.run_generation
        )
        self.control_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Advanced DSP Studio Placeholder Label
        dsp_label = ctk.CTkLabel(
            self.tab_advanced,
            text="Advanced DSP Controls & Multi-Phase Routing",
            text_color="gray",
        )
        dsp_label.pack(expand=True)

        # Status Bar
        self.status_var = ctk.StringVar(
            value="Ready. Select a goal or adjust sliders."
        )
        self.status_bar = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            text_color="gray",
            anchor="w",
        )
        self.status_bar.pack(fill="x", side="bottom", padx=20, pady=(0, 10))

    def run_generation(self, params):
        self.status_var.set("Generating sound file... Please wait.")
        self.update_idletasks()
        os.makedirs("output", exist_ok=True)
        mins = int(params.get("duration_sec", 600) // 60)
        filename = f"output/Session_{params.get('target_beat', 10)}Hz_{mins}min.wav"

        try:
            output_path = self.engine.render_binaural_session(
                start_beat=params["start_beat"],
                target_beat=params["target_beat"],
                carrier_freq=params["carrier_freq"],
                duration_sec=params["duration_sec"],
                noise_type=params["noise_type"],
                output_filepath=filename,
            )
            self.status_var.set(f" Saved: {output_path}")
            messagebox.showinfo(
                "Success!", f"Your sound file is ready:\n\n{output_path}"
            )
        except Exception as e:
            self.status_var.set(" Error generating audio.")
            messagebox.showerror("Error", str(e))

# Backward compatibility alias
MainApplication = MainApp
