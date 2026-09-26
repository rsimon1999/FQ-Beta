import numpy as np
from scipy.io import wavfile

def generate_pink_noise(num_samples):
    """
    Generates pink noise (1/f) using the Paul Kellet filter method.
    """
    # White noise baseline
    white = np.random.randn(num_samples)
    
    # Filter coefficients for pink noise synthesis
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
        
    # Scale to range -1.0 to 1.0
    pink /= np.max(np.abs(pink))
    return pink

def build_binaural_track(
    file_name, 
    duration_sec, 
    carrier_freq, 
    beat_start_freq, 
    beat_end_freq=None, 
    pink_noise_level=0.15, 
    sample_rate=44100
):
    """
    Generates a stereo binaural beat track (static or progressive ramp) 
    blended with subtle background pink noise.
    """
    if beat_end_freq is None:
        beat_end_freq = beat_start_freq
        
    num_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    
    # Linearly interpolate target beat frequency over duration (enables smooth ramping)
    beat_freq_curve = np.linspace(beat_start_freq, beat_end_freq, num_samples)
    
    # Calculate continuous phase for left and right channels
    freq_left = carrier_freq - (beat_freq_curve / 2.0)
    freq_right = carrier_freq + (beat_freq_curve / 2.0)
    
    phase_left = 2 * np.pi * np.cumsum(freq_left) / sample_rate
    phase_right = 2 * np.pi * np.cumsum(freq_right) / sample_rate
    
    # Synthesize pure sine waves
    left_channel = np.sin(phase_left)
    right_channel = np.sin(phase_right)
    
    # Add subtle background pink noise (identical across both ears for acoustic masking)
    if pink_noise_level > 0:
        noise = generate_pink_noise(num_samples) * pink_noise_level
        left_channel += noise
        right_channel += noise

    # Apply 5-second logarithmic fade-in and 10-second fade-out
    fade_in_len = int(sample_rate * 5)
    fade_out_len = int(sample_rate * 10)
    
    fade_in = np.linspace(0, 1, fade_in_len)
    fade_out = np.linspace(1, 0, fade_out_len)
    
    left_channel[:fade_in_len] *= fade_in
    left_channel[-fade_out_len:] *= fade_out
    right_channel[:fade_in_len] *= fade_in
    right_channel[-fade_out_len:] *= fade_out

    # Combine into stereo matrix
    stereo_signal = np.vstack((left_channel, right_channel)).T
    
    # Peak normalization to prevent digital clipping (-3 dB digital headroom)
    max_val = np.max(np.abs(stereo_signal))
    if max_val > 0:
        stereo_signal = (stereo_signal / max_val) * 0.707

    # Convert to 16-bit PCM WAV format
    audio_data = (stereo_signal * 32767).astype(np.int16)
    wavfile.write(file_name, sample_rate, audio_data)
    print(f"Successfully generated: {file_name}")

# =====================================================================
# TRACK BATCH GENERATION
# =====================================================================

print("Generating binaural audio files...")

# 1. Standard Alpha Relax Track (10 Hz) - 20 Minutes
build_binaural_track(
    file_name="01_Alpha_Relaxation_10Hz.wav",
    duration_sec=1200,
    carrier_freq=250.0,
    beat_start_freq=10.0,
    pink_noise_level=0.12
)

# 2. Standard Beta Focus Track (15 Hz) - 20 Minutes
build_binaural_track(
    file_name="02_Beta_Focus_15Hz.wav",
    duration_sec=1200,
    carrier_freq=250.0,
    beat_start_freq=15.0,
    pink_noise_level=0.12
)

# 3. Standard Pre-Sleep Theta Track (6 Hz) - 30 Minutes
build_binaural_track(
    file_name="03_Theta_Sleep_6Hz.wav",
    duration_sec=1800,
    carrier_freq=200.0,
    beat_start_freq=6.0,
    pink_noise_level=0.15
)

# 4. Gamma Peak Focus Track (40 Hz) - 20 Minutes
build_binaural_track(
    file_name="04_Gamma_PeakFocus_40Hz.wav",
    duration_sec=1200,
    carrier_freq=300.0,
    beat_start_freq=40.0,
    pink_noise_level=0.10
)

# 5. Dynamic Motivation Ramp (10 Hz Alpha -> 20 Hz High Beta) - 20 Minutes
# Starts at 10 Hz to clear brain fog, smoothly accelerating up to 20 Hz to build project momentum
build_binaural_track(
    file_name="05_Motivation_Ramp_10Hz_to_20Hz.wav",
    duration_sec=1200,
    carrier_freq=250.0,
    beat_start_freq=10.0,
    beat_end_freq=20.0,
    pink_noise_level=0.12
)

print("\nAll files created successfully!")