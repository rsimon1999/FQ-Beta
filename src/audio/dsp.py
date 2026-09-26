"""DSP mathematical operations and signal generation functions."""

import numpy as np
from scipy.signal import butter, sosfilt


def generate_time_array(duration_sec: float, sample_rate: int = 44100) -> np.ndarray:
    """Generates time array vector for signal calculation."""
    return np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)


def generate_frequency_ramp(
    time_array: np.ndarray, start_hz: float, target_hz: float
) -> np.ndarray:
    """Calculates linear frequency transition across session duration."""
    return np.linspace(start_hz, target_hz, len(time_array))


def generate_binaural_signals(
    t: np.ndarray,
    carrier_freq: float,
    freq_ramp: np.ndarray,
    harmonic_richness: float = 0.3,
) -> tuple[np.ndarray, np.ndarray]:
    """Generates left and right audio channels for binaural entrainment with harmonic overtones."""
    phase_diff = np.cumsum(freq_ramp) / 44100.0

    left_fundamental = np.sin(2 * np.pi * carrier_freq * t)
    right_fundamental = np.sin(2 * np.pi * carrier_freq * t + 2 * np.pi * phase_diff)

    if harmonic_richness <= 0.0:
        return left_fundamental, right_fundamental

    h2_weight = 0.5 * harmonic_richness
    h3_weight = 0.3 * harmonic_richness
    h5_weight = 0.15 * harmonic_richness

    left_h2 = h2_weight * np.sin(2 * np.pi * (carrier_freq * 2) * t)
    left_h3 = h3_weight * np.sin(2 * np.pi * (carrier_freq * 3) * t)
    left_h5 = h5_weight * np.sin(2 * np.pi * (carrier_freq * 5) * t)

    right_h2 = h2_weight * np.sin(2 * np.pi * (carrier_freq * 2) * t + 2 * np.pi * phase_diff)
    right_h3 = h3_weight * np.sin(2 * np.pi * (carrier_freq * 3) * t + 2 * np.pi * phase_diff)
    right_h5 = h5_weight * np.sin(2 * np.pi * (carrier_freq * 5) * t + 2 * np.pi * phase_diff)

    left_total = left_fundamental + left_h2 + left_h3 + left_h5
    right_total = right_fundamental + right_h2 + right_h3 + right_h5

    return left_total, right_total


def generate_isochronic_pulse(
    t: np.ndarray,
    freq_ramp: np.ndarray,
    pulse_depth: float = 0.8,
) -> np.ndarray:
    """Generates volume modulation envelope for speaker-friendly pulsing."""
    phase = np.cumsum(freq_ramp) / 44100.0
    envelope = (1.0 - pulse_depth) + pulse_depth * (0.5 * (1.0 + np.sin(2 * np.pi * phase)))
    return envelope


def generate_colored_noise(
    t: np.ndarray, noise_type: str = "none", sample_rate: int = 44100
) -> np.ndarray:
    """Generates dynamic swept background noise floor (white, pink, brown)."""
    num_samples = len(t)
    if noise_type == "none":
        return np.zeros(num_samples)

    white = np.random.normal(0, 1, num_samples)
    if noise_type == "white":
        return white * 0.05

    # Base noise generation
    if noise_type == "pink":
        b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        a = [1.0, -2.494956002, 2.017265875, -0.522189400]
        from scipy.signal import lfilter
        raw_noise = lfilter(b, a, white)
        base_gain = 0.08
        sweep_period = 6.0  # 6-second rainfall/breeze swell
        min_cutoff, max_cutoff = 400.0, 2500.0
    elif noise_type == "brown":
        brown = np.cumsum(white)
        brown = brown - np.mean(brown)
        max_val = np.max(np.abs(brown))
        raw_noise = (brown / max_val) if max_val > 0 else brown
        base_gain = 0.12
        sweep_period = 10.0  # 10-second ocean wave surf cycle
        min_cutoff, max_cutoff = 120.0, 850.0
    else:
        return np.zeros(num_samples)

    # Dynamic low-pass filter modulation (simulating waves/breeze)
    # Block processing for smooth time-varying filter calculation
    block_size = int(sample_rate * 0.1)  # 100ms processing chunks
    num_blocks = num_samples // block_size
    filtered_noise = np.zeros(num_samples)

    # Low-pass LFO oscillating cutoff frequency
    lfo = 0.5 * (1.0 + np.sin(2 * np.pi * (1.0 / sweep_period) * t))
    cutoff_freqs = min_cutoff + (max_cutoff - min_cutoff) * lfo

    for i in range(num_blocks):
        start_idx = i * block_size
        end_idx = start_idx + block_size

        chunk = raw_noise[start_idx:end_idx]
        current_cutoff = cutoff_freqs[start_idx]

        # 2nd order Butterworth low-pass filter block
        sos = butter(2, current_cutoff, btype="low", fs=sample_rate, output="sos")
        filtered_noise[start_idx:end_idx] = sosfilt(sos, chunk)

    # Handle remaining tail samples if any
    if num_samples > num_blocks * block_size:
        tail_start = num_blocks * block_size
        sos = butter(2, cutoff_freqs[tail_start], btype="low", fs=sample_rate, output="sos")
        filtered_noise[tail_start:] = sosfilt(sos, raw_noise[tail_start:])

    return filtered_noise * base_gain
