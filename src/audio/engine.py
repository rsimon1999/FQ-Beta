"""Core Soundscape Engine handling DSP synthesis for binaural beats, dynamic ocean swells, organic rain patter, and multi-stage sequencing."""

import numpy as np
import scipy.signal as signal
import soundfile as sf


class SoundscapeEngine:

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, noise_type, duration_samples, level=0.65):
        """Generates realistic 2-channel (stereo) soundscapes (Ocean Waves, Rain Patter, Soft White)."""
        noise_str = str(noise_type).lower().strip()

        if "none" in noise_str or not noise_str:
            return np.zeros((duration_samples, 2), dtype=np.float32)

        # Independent stereo white noise streams
        white = np.random.uniform(-1.0, 1.0, (duration_samples, 2)).astype(np.float32)
        nyquist = self.sample_rate / 2.0

        if "white" in noise_str:
            # Softened white noise (gentle roll-off above 8kHz to remove ear fatigue)
            b, a = signal.butter(2, 8000.0 / nyquist, btype='low')
            soft_white = signal.lfilter(b, a, white, axis=0)
            max_v = np.max(np.abs(soft_white))
            if max_v > 0:
                soft_white = (soft_white / max_v) * level
            return soft_white.astype(np.float32)

        if "pink" in noise_str:
            # --- ORGANIC RAIN ENGINE ---
            # 1. Base Pink Noise generation (Voss-McCartney filter)
            b_pink = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
            a_pink = [1.0, -2.494956002, 2.017265875, -0.522189400]
            pink_base = signal.lfilter(b_pink, a_pink, white, axis=0)

            # Dampen static hiss with a 5kHz low-pass filter
            b_lp, a_lp = signal.butter(2, 5000.0 / nyquist, btype='low')
            rain_bed = signal.lfilter(b_lp, a_lp, pink_base, axis=0)

            # 2. Wind/Gust Modulation (slow LFOs for shifting rain intensity)
            t = np.linspace(0, duration_samples / self.sample_rate, duration_samples, endpoint=False)
            wind_lfo_l = 0.75 + 0.25 * np.sin(2 * np.pi * 0.12 * t)
            wind_lfo_r = 0.75 + 0.25 * np.sin(2 * np.pi * 0.09 * t + 0.8)
            rain_bed[:, 0] *= wind_lfo_l
            rain_bed[:, 1] *= wind_lfo_r

            # 3. Raindrop Impact Layer (Granular splatter patter)
            drop_impulses = (np.random.uniform(0, 1, (duration_samples, 2)) > 0.9975).astype(np.float32)
            drop_impulses *= np.random.uniform(0.2, 1.0, (duration_samples, 2))
            
            # Bandpass filter drop impacts (1.2kHz - 4.5kHz) for natural droplet acoustics
            b_bp, a_bp = signal.butter(2, [1200.0 / nyquist, 4500.0 / nyquist], btype='bandpass')
            droplets = signal.lfilter(b_bp, a_bp, drop_impulses, axis=0)

            # Balance bed (80%) + droplet patter (20%)
            max_bed = np.max(np.abs(rain_bed))
            if max_bed > 0:
                rain_bed /= max_bed
            max_drop = np.max(np.abs(droplets))
            if max_drop > 0:
                droplets /= max_drop

            rain_mix = (0.80 * rain_bed) + (0.20 * droplets)
            rain_mix *= level
            return rain_mix.astype(np.float32)

        if "brown" in noise_str:
            # --- DYNAMIC OCEAN WAVE SURF ENGINE ---
            # 1. Brownian noise base
            b_br = [0.10]
            a_br = [1.0, -0.985]
            brown_base = signal.lfilter(b_br, a_br, white, axis=0)

            # 2. Dual-band spectrums (Deep Rumble vs. Foam/Surf Crash)
            b_deep, a_deep = signal.butter(2, 220.0 / nyquist, btype='low')
            b_surf, a_surf = signal.butter(2, 1400.0 / nyquist, btype='low')
            
            deep_layer = signal.lfilter(b_deep, a_deep, brown_base, axis=0)
            surf_layer = signal.lfilter(b_surf, a_surf, brown_base, axis=0)

            max_d = np.max(np.abs(deep_layer))
            if max_d > 0: deep_layer /= max_d
            max_s = np.max(np.abs(surf_layer))
            if max_s > 0: surf_layer /= max_s

            # 3. Time-varying Stereo Wave Swell LFOs
            t = np.linspace(0, duration_samples / self.sample_rate, duration_samples, endpoint=False)
            
            lfo_l = 0.5 * (1.0 + np.sin(2 * np.pi * 0.08 * t))
            lfo_r = 0.5 * (1.0 + np.sin(2 * np.pi * 0.065 * t + 1.2))
            
            swell_l = 0.15 + 0.85 * lfo_l
            swell_r = 0.15 + 0.85 * lfo_r

            # Dynamic Spectral Crossfade:
            # Trough -> Deep underwater rumble dominates
            # Crest -> Bright crashing surf washes in
            left_wave = (deep_layer[:, 0] * (0.8 - 0.4 * swell_l)) + (surf_layer[:, 0] * (swell_l ** 1.6))
            right_wave = (deep_layer[:, 1] * (0.8 - 0.4 * swell_r)) + (surf_layer[:, 1] * (swell_r ** 1.6))

            ocean_stereo = np.column_stack((left_wave * swell_l, right_wave * swell_r))
            max_ocean = np.max(np.abs(ocean_stereo))
            if max_ocean > 0:
                ocean_stereo = (ocean_stereo / max_ocean) * level

            return ocean_stereo.astype(np.float32)

        return np.zeros((duration_samples, 2), dtype=np.float32)

    def generate_binaural_stage(
        self,
        start_beat,
        target_beat,
        carrier_freq,
        duration_sec,
        noise_type="none",
        isochronic_mode=False,
        harmonic_richness=0.0,
        tone_volume=0.10,
        noise_level=0.65,
    ):
        """Generates a raw 2-channel numpy array for a single entrainment stage."""
        num_samples = int(self.sample_rate * duration_sec)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)

        beat_freqs = np.linspace(start_beat, target_beat, num_samples)
        phase_diff = 2 * np.pi * np.cumsum(beat_freqs) / self.sample_rate

        carrier_phase = 2 * np.pi * carrier_freq * t
        
        left_channel = tone_volume * np.sin(carrier_phase)
        right_channel = tone_volume * np.sin(carrier_phase + phase_diff)

        if harmonic_richness > 0:
            left_channel += tone_volume * harmonic_richness * 0.5 * np.sin(2 * carrier_phase)
            right_channel += tone_volume * harmonic_richness * 0.5 * np.sin(2 * (carrier_phase + phase_diff))

        if isochronic_mode:
            pulse_hz = beat_freqs
            pulse_phase = 2 * np.pi * np.cumsum(pulse_hz) / self.sample_rate
            envelope = 0.5 * (1.0 + np.sin(pulse_phase))
            left_channel *= envelope
            right_channel *= envelope

        # Add 2-channel stereo noise layer
        stereo_noise = self.generate_noise(noise_type, num_samples, level=noise_level)
        left_channel += stereo_noise[:, 0]
        right_channel += stereo_noise[:, 1]

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
        tone_volume=0.10,
        noise_level=0.65,
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
            tone_volume=tone_volume,
            noise_level=noise_level,
        )
        sf.write(output_filepath, audio_data, self.sample_rate)
        return output_filepath

    def render_sequence_session(self, stages, output_filepath="output/sequence_session.wav", crossfade_sec=0.5):
        """Renders a multi-stage sequence into a single continuous WAV file."""
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
                tone_volume=stage.get("tone_volume", 0.10),
                noise_level=stage.get("noise_level", 0.65),
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
