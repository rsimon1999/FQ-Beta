"""DSP math and audio signal generators."""

import numpy as np


def generate_tone(
    freq: float, duration: float, sample_rate: int = 44100
) -> np.ndarray:
    """Generate a clean sine wave array."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t)


def generate_binaural_beat(
    base_carrier: float,
    beat_freq: float,
    duration: float,
    sample_rate: int = 44100,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate stereo left/right channels for a binaural beat."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    left_channel = np.sin(2 * np.pi * base_carrier * t)
    right_channel = np.sin(2 * np.pi * (base_carrier + beat_freq) * t)
    return left_channel, right_channel


def generate_noise(noise_type: str, num_samples: int) -> np.ndarray:
    """Generate basic audio noise backgrounds."""
    white_noise = np.random.uniform(-1.0, 1.0, num_samples)

    if noise_type.lower() == "white":
        return white_noise
    elif noise_type.lower() == "pink":
        b = [0.04992203, -0.09599353, 0.05061269, -0.00440878]
        a = [1.0, -2.49495600, 2.01726587, -0.52218940]
        from scipy.signal import lfilter

        return lfilter(b, a, white_noise)
    elif noise_type.lower() == "brown":
        return np.cumsum(white_noise) / 50.0

    return white_noise
