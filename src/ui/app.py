"""Main CustomTkinter window application supporting Easy Mode, Advanced DSP Studio, in-app Audio Playback, and Live Preview."""

import os
import customtkinter as ctk
from tkinter import messagebox, filedialog

from src.audio.engine import SoundscapeEngine
from src.audio.player import AudioPlayer
from src.ui.frames import EasyControlFrame, AdvancedControlFrame
from src.utils.config import load_user_settings, save_user_settings

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NeuroAcoustic Sound Studio")
        self.geometry("580x790")
        self.resizable(False, False)

        self.engine = SoundscapeEngine()
        self.player = AudioPlayer(sample_rate=self.engine.sample_rate)
        self.user_settings = load_user_settings()
        self.last_generated_file = None

        self._setup_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)

    def _setup_ui(self):
        # Header
        title_lbl = ctk.CTkLabel(
            self,
            text="NeuroAcoustic Studio",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_lbl.pack(anchor="w", padx=20, pady=(15, 2))

        subtitle_lbl = ctk.CTkLabel(
            self,
            text="Brainwave Entrainment & Soundscape Generator",
            text_color="gray",
        )
        subtitle_lbl.pack(anchor="w", padx=20, pady=(0, 6))

        # Main Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 5))

        self.tab_easy = self.tabview.add("Easy Mode")
        self.tab_advanced = self.tabview.add("Advanced DSP Studio")

        self.easy_frame = EasyControlFrame(
            self.tab_easy,
            generate_callback=self.run_generation,
            preview_callback=self.run_preview,
            stop_callback=self.stop_audio,
            save_defaults_callback=self.save_defaults,
            user_settings=self.user_settings,
        )
        self.easy_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.advanced_frame = AdvancedControlFrame(
            self.tab_advanced,
            generate_callback=self.run_generation,
            preview_callback=self.run_preview,
            stop_callback=self.stop_audio,
            save_defaults_callback=self.save_defaults,
            user_settings=self.user_settings,
        )
        self.advanced_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # In-App Audio Playback Bar
        self.playback_frame = ctk.CTkFrame(self, fg_color=("gray85", "gray17"), corner_radius=6)
        self.playback_frame.pack(fill="x", padx=15, pady=(2, 5))

        self.play_file_btn = ctk.CTkButton(
            self.playback_frame,
            text="▶ Play Generated File",
            fg_color="#1E88E5",
            hover_color="#1565C0",
            state="disabled",
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_play_last_file,
        )
        self.play_file_btn.pack(side="left", padx=10, pady=6)

        self.playback_status_lbl = ctk.CTkLabel(
            self.playback_frame,
            text="No audio file loaded",
            text_color="gray",
            font=ctk.CTkFont(size=11),
            anchor="w",
        )
        self.playback_status_lbl.pack(side="left", fill="x", expand=True, padx=5, pady=6)

        # Bottom Status Bar
        self.status_var = ctk.StringVar(
            value="Ready. Preview your acoustic balance or generate a session."
        )
        self.status_bar = ctk.CTkLabel(
            self,
            textvariable=self.status_var,
            text_color="gray",
            anchor="w",
            font=ctk.CTkFont(size=12),
        )
        self.status_bar.pack(fill="x", side="bottom", padx=20, pady=(0, 8))

    def run_preview(self, params):
        """Generates and streams an 8-second real-time acoustic preview."""
        self.status_var.set("🔊 Playing live preview (8s)... [Press Stop to cancel]")
        self.playback_status_lbl.configure(text="Streaming live preview...")
        self.update_idletasks()

        try:
            self.player.play_preview(
                engine=self.engine,
                params=params,
                duration_sec=8.0,
                on_finished=self._on_playback_finished,
            )
        except Exception as e:
            self.status_var.set(f"❌ Preview error: {e}")
            messagebox.showerror("Preview Error", str(e))

    def stop_audio(self):
        """Stops any active preview or file playback."""
        self.player.stop()
        self.status_var.set("⏹ Audio playback stopped.")
        self.play_file_btn.configure(text="▶ Play Generated File")
        if self.last_generated_file:
            self.playback_status_lbl.configure(text=f"Ready: {os.path.basename(self.last_generated_file)}")
        else:
            self.playback_status_lbl.configure(text="No audio file loaded")

    def _on_playback_finished(self):
        """Callback triggered when audio finishes playing naturally."""
        def _update():
            self.status_var.set("Ready.")
            self.play_file_btn.configure(text="▶ Play Generated File")
            if self.last_generated_file:
                self.playback_status_lbl.configure(text=f"Ready: {os.path.basename(self.last_generated_file)}")
            else:
                self.playback_status_lbl.configure(text="Idle")
        self.after(0, _update)

    def toggle_play_last_file(self):
        """Toggles playback of the last generated session audio file."""
        if not self.last_generated_file or not os.path.exists(self.last_generated_file):
            messagebox.showwarning("No File", "No rendered sound file available to play.")
            return

        if self.player.is_playing and self.player.current_source == os.path.basename(self.last_generated_file):
            self.stop_audio()
        else:
            try:
                self.status_var.set(f"🔊 Playing {os.path.basename(self.last_generated_file)}...")
                self.playback_status_lbl.configure(text=f"Playing: {os.path.basename(self.last_generated_file)}")
                self.play_file_btn.configure(text="⏹ Stop Playback")
                self.player.play_file(
                    self.last_generated_file,
                    on_finished=self._on_playback_finished,
                )
            except Exception as e:
                self.status_var.set("❌ Playback error.")
                messagebox.showerror("Playback Error", str(e))

    def run_generation(self, params):
        mins = int(params.get("duration_sec", 600) // 60)
        preset_tag = params.get("preset_name")

        # Set default output filename base
        if preset_tag:
            clean_name = "".join(c if c.isalnum() else "_" for c in preset_tag).strip("_")
            default_filename = f"{clean_name}_{mins}min.mp3"
        else:
            default_filename = f"Session_{params.get('target_beat', 10)}Hz_{mins}min.mp3"

        os.makedirs("output", exist_ok=True)

        # Native OS Save File Dialog with format selection
        filename = filedialog.asksaveasfilename(
            initialdir="output",
            initialfile=default_filename,
            defaultextension=".mp3",
            filetypes=[
                ("MP3 Audio (*.mp3)", "*.mp3"),
                ("Waveform Audio (*.wav)", "*.wav"),
                ("FLAC Audio (*.flac)", "*.flac"),
                ("Ogg Vorbis Audio (*.ogg)", "*.ogg"),
                ("All Files (*.*)", "*.*")
            ],
            title="Save Rendered Audio Session"
        )

        if not filename:
            self.status_var.set("Generation canceled.")
            return

        self.status_var.set("⏳ Generating sound file... Please wait.")
        self.update_idletasks()

        try:
            stages = params.get("stages")
            if stages and len(stages) > 1:
                output_path = self.engine.render_sequence_session(
                    stages=stages,
                    output_filepath=filename,
                )
            else:
                output_path = self.engine.render_binaural_session(
                    start_beat=params["start_beat"],
                    target_beat=params["target_beat"],
                    carrier_freq=params["carrier_freq"],
                    duration_sec=params["duration_sec"],
                    noise_type=params["noise_type"],
                    isochronic_mode=params.get("isochronic_mode", False),
                    harmonic_richness=params.get("harmonic_richness", 0.0),
                    tone_volume=params.get("tone_volume", 0.10),
                    noise_level=params.get("noise_level", 0.80),
                    output_filepath=filename,
                )
            self.last_generated_file = output_path
            self.play_file_btn.configure(state="normal", text="▶ Play Generated File")
            self.playback_status_lbl.configure(text=f"Ready: {os.path.basename(output_path)}")
            self.status_var.set(f"✅ Saved: {output_path}")

            res = messagebox.askyesno(
                "Sound File Ready!",
                f"Your sound file is ready:\n\n{output_path}\n\nWould you like to play it now inside the app?",
            )
            if res:
                self.toggle_play_last_file()
        except Exception as e:
            self.status_var.set("❌ Error generating audio.")
            messagebox.showerror("Error", str(e))

    def save_defaults(self, params):
        """Saves current frame parameters as user defaults."""
        settings_to_save = {
            "tone_volume": params.get("tone_volume", 0.10),
            "noise_level": params.get("noise_level", 0.80),
            "default_atmosphere": params.get("default_atmosphere", "Ocean Waves"),
            "default_duration_min": params.get("default_duration_min", "10"),
            "isochronic_mode": params.get("isochronic_mode", False),
            "harmonic_richness": params.get("harmonic_richness", 0.0),
            "start_beat": params.get("start_beat", 10.0),
            "target_beat": params.get("target_beat", 10.0),
            "carrier_freq": params.get("carrier_freq", 200.0),
        }
        success = save_user_settings(settings_to_save)
        if success:
            self.user_settings.update(settings_to_save)
            self.status_var.set(
                f"💾 Defaults saved! Tone: {int(settings_to_save['tone_volume']*100)}% | Atmosphere: {int(settings_to_save['noise_level']*100)}%"
            )
            messagebox.showinfo("Defaults Saved", "Your volume levels, atmosphere choice, and preferences have been saved as startup defaults.")
        else:
            self.status_var.set("❌ Failed to save default settings.")
            messagebox.showerror("Error", "Could not save default settings.")

    def _on_window_close(self):
        """Clean shutdown handler stopping any active audio stream."""
        self.player.stop()
        self.destroy()


MainApplication = MainApp
