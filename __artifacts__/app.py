import os
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy.io import wavfile

# --- DSP ENGINE ---

def generate_noise(num_samples, noise_type="pink"):
    white = np.random.randn(num_samples)
    if noise_type == "brown":
        brown = np.cumsum(white)
        max_b = np.max(np.abs(brown))
        return brown / max_b if max_b > 0 else brown
    elif noise_type == "pink":
        b0 = b1 = b2 = b3 = b4 = b5 = b6 = 0.0
        pink = np.zeros(num_samples)
        for i in range(num_samples):
            w = white[i]
            b0 = 0.99886 * b0 + w * 0.0555179
            b1 = 0.99332 * b1 + w * 0.0750759
            b2 = 0.96900 * b2 + w * 0.1538520
            b3 = 0.86650 * b3 + w * 0.3104856
            b4 = 0.55000 * b4 + w * 0.5329522
            b5 = -0.7616 * b5 - w * 0.0168980
            pink[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + w * 0.5362
            b6 = w * 0.115926
        max_p = np.max(np.abs(pink))
        return pink / max_p if max_p > 0 else pink
    else:
        return np.zeros(num_samples)

def synthesize_audio(file_name, duration_min, carrier_freq, beat_start, beat_end, 
                     is_isochronic=False, noise_type="pink", noise_lvl=0.12, 
                     fade_in_sec=5, fade_out_sec=10, sample_rate=44100):
    
    duration_sec = duration_min * 60
    num_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    
    beat_curve = np.linspace(beat_start, beat_end, num_samples)
    
    if is_isochronic:
        # Isochronic: Single carrier frequency modulated by sharp volume pulse
        carrier_phase = 2 * np.pi * carrier_freq * t
        carrier = np.sin(carrier_phase)
        
        pulse_phase = 2 * np.pi * np.cumsum(beat_curve) / sample_rate
        # Square-like pulse modulation envelope
        modulation = 0.5 * (1.0 + np.sin(pulse_phase))
        modulation = modulation ** 2  # Sharpen the pulse transition
        
        left = carrier * modulation
        right = carrier * modulation
    else:
        # Binaural: Phase-shifted frequencies per ear
        freq_l = carrier_freq - (beat_curve / 2.0)
        freq_r = carrier_freq + (beat_curve / 2.0)
        
        phase_l = 2 * np.pi * np.cumsum(freq_l) / sample_rate
        phase_r = 2 * np.pi * np.cumsum(freq_r) / sample_rate
        
        left = np.sin(phase_l)
        right = np.sin(phase_r)
    
    # Add Background Masking
    if noise_type != "none" and noise_lvl > 0:
        bg_noise = generate_noise(num_samples, noise_type) * noise_lvl
        left += bg_noise
        right += bg_noise
        
    # Apply Custom Fade Ramps
    fade_in_samples = int(sample_rate * fade_in_sec)
    fade_out_samples = int(sample_rate * fade_out_sec)
    
    if fade_in_samples > 0:
        fade_in = np.linspace(0, 1, fade_in_samples)
        left[:fade_in_samples] *= fade_in
        right[:fade_in_samples] *= fade_in
        
    if fade_out_samples > 0:
        fade_out = np.linspace(1, 0, fade_out_samples)
        left[-fade_out_samples:] *= fade_out
        right[-fade_out_samples:] *= fade_out
        
    # Combine & Normalize to -3 dBFS
    stereo = np.vstack((left, right)).T
    max_val = np.max(np.abs(stereo))
    if max_val > 0:
        stereo = (stereo / max_val) * 0.707
        
    audio_data = (stereo * 32767).astype(np.int16)
    wavfile.write(file_name, sample_rate, audio_data)
    return file_name

# --- MATRIX LOOKUP ---

MOOD_PRESETS = {
    "Stressed / Anxious": {"start": 18.0, "carrier": 200.0, "noise": "brown"},
    "Overstimulated / Fidgety": {"start": 16.0, "carrier": 180.0, "noise": "brown"},
    "Sluggish / Lethargic": {"start": 8.0, "carrier": 260.0, "noise": "pink"},
    "Depressed / Low Energy": {"start": 6.0, "carrier": 250.0, "noise": "pink"},
    "Neutral / Normal": {"start": 10.0, "carrier": 220.0, "noise": "pink"},
}

GOAL_PRESETS = {
    "Bedtime / Sleep": {"end": 4.0, "carrier_mod": -20},
    "Deep Relaxation": {"end": 7.83, "carrier_mod": -10},
    "Calm / Peaceful Rationality (Budget)": {"end": 12.0, "carrier_mod": 0},
    "Work / Sharp Focus": {"end": 15.0, "carrier_mod": 10},
    "Amped Up / High Drive": {"end": 20.0, "carrier_mod": 20},
    "Sexy Time / Hyper-Arousal": {"end": 40.0, "carrier_mod": -10},
}

# --- TKINTER GRAPHICAL INTERFACE ---

class NeuroAcousticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neuro-Acoustic Generator Studio")
        self.root.geometry("540x680")
        self.root.resizable(False, False)
        
        style = ttk.Style()
        style.theme_use("clam")
        
        # Header
        lbl_header = ttk.Label(root, text="Neuro-Acoustic State Generator", font=("Helvetica", 16, "bold"))
        lbl_header.pack(pady=12)
        
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill="both", expand=True)
        
        # 1. Current State
        ttk.Label(main_frame, text="1. Select Current Baseline State:", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        self.combo_mood = ttk.Combobox(main_frame, values=list(MOOD_PRESETS.keys()), state="readonly", width=35)
        self.combo_mood.current(0)
        self.combo_mood.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Intensity Slider
        ttk.Label(main_frame, text="Current State Intensity (1 = Mild, 10 = Severe):").grid(row=2, column=0, sticky="w")
        self.slider_intensity = ttk.Scale(main_frame, from_=1, to=10, orient="horizontal")
        self.slider_intensity.set(5)
        self.slider_intensity.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # 2. Target Goal
        ttk.Label(main_frame, text="2. Select Desired Goal State:", font=("Helvetica", 10, "bold")).grid(row=4, column=0, sticky="w", pady=4)
        self.combo_goal = ttk.Combobox(main_frame, values=list(GOAL_PRESETS.keys()), state="readonly", width=35)
        self.combo_goal.current(3)
        self.combo_goal.grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # 3. Delivery Hardware Selection
        ttk.Label(main_frame, text="3. Output Delivery Mode:", font=("Helvetica", 10, "bold")).grid(row=6, column=0, sticky="w", pady=4)
        self.mode_var = tk.StringVar(value="binaural")
        r_bin = ttk.Radiobutton(main_frame, text="Binaural Beats (Headphones Required)", variable=self.mode_var, value="binaural")
        r_iso = ttk.Radiobutton(main_frame, text="Isochronic Tones (Room Speakers / Soundbar)", variable=self.mode_var, value="isochronic")
        r_bin.grid(row=7, column=0, sticky="w")
        r_iso.grid(row=8, column=0, sticky="w", pady=(0, 15))
        
        # 4. Session Controls
        ttk.Label(main_frame, text="4. Session Configuration:", font=("Helvetica", 10, "bold")).grid(row=9, column=0, sticky="w", pady=4)
        
        f_controls = ttk.Frame(main_frame)
        f_controls.grid(row=10, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        ttk.Label(f_controls, text="Duration (Mins):").grid(row=0, column=0, padx=5)
        self.spin_duration = ttk.Spinbox(f_controls, from_=5, to=60, width=5)
        self.spin_duration.set(20)
        self.spin_duration.grid(row=0, column=1, padx=5)
        
        ttk.Label(f_controls, text="Fade Out (Secs):").grid(row=0, column=2, padx=5)
        self.spin_fade = ttk.Spinbox(f_controls, from_=2, to=30, width=5)
        self.spin_fade.set(10)
        self.spin_fade.grid(row=0, column=3, padx=5)
        
        # Generate Button
        btn_generate = ttk.Button(main_frame, text="Generate Custom Audio File", command=self.run_generation)
        btn_generate.grid(row=11, column=0, columnspan=2, pady=15, ipady=8, sticky="ew")
        
        # Status Output
        self.lbl_status = ttk.Label(main_frame, text="Status: Ready", font=("Helvetica", 9, "italic"), foreground="gray")
        self.lbl_status.grid(row=12, column=0, columnspan=2)

    def run_generation(self):
        mood = self.combo_mood.get()
        goal = self.combo_goal.get()
        intensity = self.slider_intensity.get()
        is_iso = (self.mode_var.get() == "isochronic")
        duration = int(self.spin_duration.get())
        fade_out = int(self.spin_fade.get())
        
        mood_cfg = MOOD_PRESETS[mood]
        goal_cfg = GOAL_PRESETS[goal]
        
        # Calculate dynamic start frequency based on intensity scale (1-10)
        beat_start = mood_cfg["start"] + ((intensity - 5) * 0.5)
        beat_end = goal_cfg["end"]
        carrier = mood_cfg["carrier"] + goal_cfg["carrier_mod"]
        noise_type = mood_cfg["noise"]
        
        mode_suffix = "Isochronic_Speakers" if is_iso else "Binaural_Headphones"
        clean_goal = goal.split('/')[0].strip().replace(' ', '_')
        file_name = f"{clean_goal}_{duration}min_{mode_suffix}.wav"
        
        self.lbl_status.config(text=f"Status: Generating {file_name}...", foreground="blue")
        self.root.update()
        
        try:
            out_path = synthesize_audio(
                file_name=file_name,
                duration_min=duration,
                carrier_freq=carrier,
                beat_start=beat_start,
                beat_end=beat_end,
                is_isochronic=is_iso,
                noise_type=noise_type,
                fade_out_sec=fade_out
            )
            self.lbl_status.config(text=f"Status: Success! Saved as {out_path}", foreground="green")
            messagebox.showinfo("Generation Complete", f"Successfully synthesized custom track:\n\nFile: {out_path}\nRamp: {beat_start:.1f} Hz -> {beat_end:.1f} Hz\nMode: {'Isochronic' if is_iso else 'Binaural'}")
        except Exception as e:
            self.lbl_status.config(text="Status: Generation Failed", foreground="red")
            messagebox.showerror("Error", f"Failed to generate audio: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroAcousticApp(root)
    root.mainloop()