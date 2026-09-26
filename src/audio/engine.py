"""Core Soundscape Engine handling DSP synthesis for binaural beats, noise generation, and multi-stage sequencing."""

import numpy as np
import scipy.signal as signal
import soundfile as sf


class SoundscapeEngine:

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, noise_type, duration_samples, level=0.25):
        """Generates normalized noise scaled to a specific peak level relative to 1.0 sine carrier."""
        noise_str = str(noise_type).lower().strip()

        if "none" in noise_str or not noise_str:
            return np.zeros(duration_samples, dtype=np.float32)

        # Base white noise uniform distribution [-1, 1]
        white = np.random.uniform(-1.0, 1.0, duration_samples)

        if "white" in noise_str:
            return (white * level).astype(np.float32)

        if "pink" in noise_str:
            # Voss-McCartney / Paul Kellet pinking filter
            b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
            a = [1.0, -2.494956002, 2.017265875, -0.522189400]
            pink = signal.lfilter(b, a, white)
            max_p = np.max(np.abs(pink))
            if max_p > 0:
                pink = (pink / max_p) * level
            return pink.astype(np.float32)

        if "brown" in noise_str:
            # Leaky Integrator filter for Brownian noise (prevents long-term DC drift)
            b = [0.10]
            a = [1.0, -0.985]
            brown = signal.lfilter(b, a, white)
            max_b = np.max(np.abs(brown))
            if max_b > 0:
                brown = (brown / max_b) * level
            return brown.astype(np.float32)

        return np.zeros(duration_samples, dtype=np.float32)

    def generate_binaural_stage(
        self,
        start_beat,
        target_beat,
        carrier_freq,
        duration_sec,
        noise_type="none",
        isochronic_mode=False,
        harmonic_richness=0.0,
    ):
        """Generates a raw 2-channel numpy array for a single entrainment stage."""
        num_samples = int(self.sample_rate * duration_sec)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)

        beat_freqs = np.linspace(start_beat, target_beat, num_samples)
        phase_diff = 2 * np.pi * np.cumsum(beat_freqs) / self.sample_rate

        carrier_phase = 2 * np.pi * carrier_freq * t
        left_channel = np.sin(carrier_phase)
        right_channel = np.sin(carrier_phase + phase_diff)

        if harmonic_richness > 0:
            left_channel += harmonic_richness * 0.5 * np.sin(2 * carrier_phase)
            right_channel += harmonic_richness * 0.5 * np.sin(2 * (carrier_phase + phase_diff))

        if isochronic_mode:
            pulse_hz = beat_freqs
            pulse_phase = 2 * np.pi * np.cumsum(pulse_hz) / self.sample_rate
            envelope = 0.5 * (1.0 + np.sin(pulse_phase))
            left_channel *= envelope
            right_channel *= envelope

        # Generate noise (scaled to 25% of sine amplitude)
        noise = self.generate_noise(noise_type, num_samples, level=0.25)
        left_channel += noise
        right_channel += noise

        # Peak normalization across both channels
        max_val = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)))
        if max_val > 1.0:
            left_channel /= max_val
            right_channel /= max_val

        return np.column_stack((left_channel, right_channel)).astype(np.float32)

    def render_binaural_session(
        self,
        start_beat,
        target_beat,
        carrier_freq,
        duration_sec,
        noise_type="none",
        isochronic_mode=False,
        harmonic_richness=0.0,
        output_filepath="output/session.wav",
    ):
        """Single-stage render wrapper."""
        audio_data = self.generate_binaural_stage(
            start_beat=start_beat,
            target_beat=target_beat,
            carrier_freq=carrier_freq,
            duration_sec=duration_sec,
            noise_type=noise_type,
            isochronic_mode=isochronic_mode,
            harmonic_richness=harmonic_richness,
        )
        sf.write(output_filepath, audio_data, self.sample_rate)
        return output_filepath

    def render_sequence_session(self, stages, output_filepath="output/sequence_session.wav", crossfade_sec=0.5):
        """
        Renders a multi-stage sequence into a single continuous WAV file.
        `stages` is a list of stage dictionaries.
        """
        if not stages:
            raise ValueError("No stages provided for sequence generation.")

        rendered_blocks = []

        for stage in stages:
            block = self.generate_binaural_stage(
                start_beat=stage["start_beat"],
                target_beat=stage["target_beat"],
                carrier_freq=stage["carrier_freq"],
                duration_sec=stage["duration_sec"],
                noise_type=stage.get("noise_type", "none"),
                isochronic_mode=stage.get("isochronic_mode", False),
                harmonic_richness=stage.get("harmonic_richness", 0.0),
            )
            rendered_blocks.append(block)

        crossfade_samples = int(self.sample_rate * crossfade_sec)
        full_audio = [rendered_blocks[0]]

        for i in range(1, len(rendered_blocks)):
            prev_block = full_audio[-1]
            next_block = rendered_blocks[i]

            if len(prev_block) > crossfade_samples and len(next_block) > crossfade_samples:
                fade_out = np.linspace(1.0, 0.0, crossfade_samples)[:, np.newaxis]
                fade_in = np.linspace(0.0, 1.0, crossfade_samples)[:, np.newaxis]

                overlap = (prev_block[-crossfade_samples:] * fade_out) + (next_block[:crossfade_samples] * fade_in)

                full_audio[-1] = prev_block[:-crossfade_samples]
                full_audio.append(overlap)
                full_audio.append(next_block[crossfade_samples:])
            else:
                full_audio.append(next_block)

        final_audio = np.concatenate(full_audio, axis=0)

        max_val = np.max(np.abs(final_audio))
        if max_val > 1.0:
            final_audio /= max_val

        sf.write(output_filepath, final_audio, self.sample_rate)
        return output_filepath
