import os
import numpy as np
from scipy.io import wavfile


def generate_pink_noise(num_samples):
    """
    Generates pink noise (1/f power spectrum) for acoustic masking.
    """
    # Generate white noise in frequency domain
    white = np.random.normal(0, 1, num_samples)
    fourier = np.fft.rfft(white)
    
    # Scale amplitudes by 1/sqrt(f)
    scales = 1.0 / np.sqrt(np.arange(1, len(fourier) + 1))
    fourier *= scales
    
    # Transform back to time domain
    pink = np.fft.irfft(fourier, n=num_samples)
    return pink / np.max(np.abs(pink))


def create_binaural_track(
    file_name,
    duration_sec,
    carrier_freq,
    start_beat_freq,
    end_beat_freq=None,
    add_pink_noise=True,
    pink_noise_level=0.15,
    sample_rate=44100
):
    """
    Generates a stereo binaural beat track with optional frequency ramping and pink noise.
    """
    if end_beat_freq is None:
        end_beat_freq = start_beat_freq

    total_samples = int(sample_rate * duration_sec)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)

    # Calculate instantaneous phase difference for steady or ramping beat frequencies
    if start_beat_freq == end_beat_freq:
        phase_diff = 2 * np.pi * start_beat_freq * t
    else:
        # Linear sweep: integral of (f_start + slope * t)
        slope = (end_beat_freq - start_beat_freq) / duration_sec
        phase_diff = 2 * np.pi * (start_beat_freq * t + 0.5 * slope * (t ** 2))

    # Base carrier phase
    carrier_phase = 2 * np.pi * carrier_freq * t

    # Left and Right stereo channels
    left_channel = np.sin(carrier_phase - (phase_diff / 2.0))
    right_channel = np.sin(carrier_phase + (phase_diff / 2.0))

    # Add background Pink Noise if requested
    if add_pink_noise:
        noise = generate_pink_noise(total_samples) * pink_noise_level
        left_channel += noise
        right_channel += noise

    # Smooth 3-second fade-in and 5-second fade-out to eliminate clicks/pops
    fade_in_len = int(sample_rate * 3)
    fade_out_len = int(sample_rate * 5)
    
    fade_in = np.linspace(0, 1, fade_in_len)
    fade_out = np.linspace(1, 0, fade_out_len)

    left_channel[:fade_in_len] *= fade_in
    left_channel[-fade_out_len:] *= fade_out
    right_channel[:fade_in_len] *= fade_in
    right_channel[-fade_out_len:] *= fade_out

    # Combine into stereo array and normalize to -3 dB headroom (approx 0.707 max amplitude)
    stereo = np.vstack((left_channel, right_channel)).T
    max_val = np.max(np.abs(stereo))
    if max_val > 0:
        stereo = (stereo / max_val) * 0.707

    # Convert to 16-bit PCM integer WAV format
    audio_data = (stereo * 32767).astype(np.int16)
    wavfile.write(file_name, sample_rate, audio_data)
    print(f"✔ Successfully generated: {file_name}")


def create_multi_stage_sequence(file_name, stages, carrier_freq=250.0, sample_rate=44100):
    """
    Concatenates multiple distinct frequency stages into one seamless audio file.
    """
    combined_left = np.array([], dtype=np.float64)
    combined_right = np.array([], dtype=np.float64)

    for stage in stages:
        dur = stage["duration_sec"]
        f_start = stage["start_beat"]
        f_end = stage.get("end_beat", f_start)
        
        num_samples = int(sample_rate * dur)
        t = np.linspace(0, dur, num_samples, endpoint=False)

        if f_start == f_end:
            phase_diff = 2 * np.pi * f_start * t
        else:
            slope = (f_end - f_start) / dur
            phase_diff = 2 * np.pi * (f_start * t + 0.5 * slope * (t ** 2))

        carrier_phase = 2 * np.pi * carrier_freq * t
        left = np.sin(carrier_phase - (phase_diff / 2.0))
        right = np.sin(carrier_phase + (phase_diff / 2.0))

        # Add pink noise layer
        noise = generate_pink_noise(num_samples) * 0.12
        left += noise
        right += noise

        combined_left = np.concatenate((combined_left, left))
        combined_right = np.concatenate((combined_right, right))

    # Apply overall master fade-in (3s) and fade-out (10s to total silence)
    total_samples = len(combined_left)
    fade_in_len = int(sample_rate * 3)
    fade_out_len = int(sample_rate * 10)

    combined_left[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    combined_left[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)
    combined_right[:fade_in_len] *= np.linspace(0, 1, fade_in_len)
    combined_right[-fade_out_len:] *= np.linspace(1, 0, fade_out_len)

    # Normalize
    stereo = np.vstack((combined_left, combined_right)).T
    stereo = (stereo / np.max(np.abs(stereo))) * 0.707

    # Export
    audio_data = (stereo * 32767).astype(np.int16)
    wavfile.write(file_name, sample_rate, audio_data)
    print(f"✔ Successfully generated multi-stage sequence: {file_name}")


# ==========================================================
# EXECUTION: BUILD ALL TRACKS
# ==========================================================
if __name__ == "__main__":
    print("Generating custom brainwave suite...\n")

    # 1. Get Moving Sequence (30 min: Alpha clearing -> Beta ramp -> Gamma peak)
    get_moving_stages = [
        {"duration_sec": 300,  "start_beat": 10.0, "end_beat": 10.0},  # 5 min Alpha (10 Hz)
        {"duration_sec": 900,  "start_beat": 10.0, "end_beat": 20.0},  # 15 min Beta ramp (10 -> 20 Hz)
        {"duration_sec": 600,  "start_beat": 40.0, "end_beat": 40.0}   # 10 min Gamma hold (40 Hz)
    ]
    create_multi_stage_sequence("01_Get_Moving_Progression_30min.wav", get_moving_stages)

    # 2. Creative Problem-Solving & Flow State (30 min steady Schumann 7.83 Hz)
    create_binaural_track(
        file_name="02_Creative_Flow_Schumann_7.83Hz_30min.wav",
        duration_sec=1800,
        carrier_freq=250.0,
        start_beat_freq=7.83,
        add_pink_noise=True
    )

    # 3. Peak Gamma Working Memory & Focus (20 min steady 40 Hz)
    create_binaural_track(
        file_name="03_Gamma_Intense_Focus_40Hz_20min.wav",
        duration_sec=1200,
        carrier_freq=250.0,
        start_beat_freq=40.0,
        add_pink_noise=True
    )

    # 4. Sensorimotor Rhythm Calm Alertness (20 min steady 14 Hz SMR)
    create_binaural_track(
        file_name="04_SMR_Calm_Alertness_14Hz_20min.wav",
        duration_sec=1200,
        carrier_freq=250.0,
        start_beat_freq=14.0,
        add_pink_noise=True
    )

    # 5. Pre-Bedtime Wind-Down Sequence (30 min: Alpha -> Theta -> Silent Fade)
    bedtime_stages = [
        {"duration_sec": 600,  "start_beat": 10.0, "end_beat": 10.0},  # 10 min Alpha (10 Hz)
        {"duration_sec": 900,  "start_beat": 10.0, "end_beat": 6.0},   # 15 min Theta ramp down (10 -> 6 Hz)
        {"duration_sec": 300,  "start_beat": 6.0,  "end_beat": 4.0}    # 5 min Deep Theta/Delta transition
    ]
    create_multi_stage_sequence("05_Bedtime_WindDown_Sequence_30min.wav", bedtime_stages, carrier_freq=200.0)

    print("\nAll WAV files created successfully in your current working directory!")