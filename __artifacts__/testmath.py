import numpy as np

# Test frequency ramping math
sample_rate = 44100
duration = 10 # 10 seconds test
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Instantaneous phase for ramping frequency from f_start to f_end
f_start = 10.0
f_end = 20.0
# Phase for linear sweep: phi(t) = 2 * pi * (f_start * t + (f_end - f_start) / (2 * duration) * t^2)
phase = 2 * np.pi * (f_start * t + (f_end - f_start) / (2 * duration) * (t ** 2))
signal_left = np.sin(2 * np.pi * 250 * t - phase / 2)
signal_right = np.sin(2 * np.pi * 250 * t + phase / 2)

print("Signal min/max:", np.min(signal_left), np.max(signal_left))
print("Phase shape:", phase.shape)