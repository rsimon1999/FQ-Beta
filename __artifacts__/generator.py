import numpy as np
from scipy.io import wavfile

def generate_binaural_beat(file_name, duration_sec, carrier_freq, beat_freq, sample_rate=44100):
    """
    Generates a stereo WAV file with a binaural beat.
    """
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    
    # Calculate left and right frequencies around carrier
    freq_left = carrier_freq - (beat_freq / 2.0)
    freq_right = carrier_freq + (beat_freq / 2.0)
    
    # Generate pure sine waves
    left_channel = np.sin(2 * np.pi * freq_left * t)
    right_channel = np.sin(2 * np.pi * freq_right * t)
    
    # Apply soft 3-second fade-in and fade-out to prevent abrupt auditory pops
    fade_len = int(sample_rate * 3)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    
    left_channel[:fade_len] *= fade_in
    left_channel[-fade_len:] *= fade_out
    right_channel[:fade_len] *= fade_in
    right_channel[-fade_len:] *= fade_out
    
    # Combine into stereo matrix and normalize to -6 dB (0.5 amplitude) for digital headroom
    stereo_signal = np.vstack((left_channel, right_channel)).T * 0.5
    
    # Export as 16-bit PCM WAV
    audio_data = (stereo_signal * 32767).astype(np.int16)
    wavfile.write(file_name, sample_rate, audio_data)
    print(f"Generated: {file_name}")

# --- Generate files for 3 primary brainwave targets ---
# 1. Focus / Working Memory (15 Hz Beta) | Carrier: 250 Hz | 20 mins
generate_binaural_beat("Beta_Focus_15Hz.wav", duration_sec=1200, carrier_freq=250.0, beat_freq=15.0)

# 2. Relaxed Flow State (10 Hz Alpha) | Carrier: 250 Hz | 20 mins
generate_binaural_beat("Alpha_Relax_10Hz.wav", duration_sec=1200, carrier_freq=250.0, beat_freq=10.0)

# 3. Deep Memory / Pre-Sleep (6 Hz Theta) | Carrier: 200 Hz | 20 mins
generate_binaural_beat("Theta_Sleep_6Hz.wav", duration_sec=1200, carrier_freq=200.0, beat_freq=6.0)