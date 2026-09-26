"""Core Soundscape Engine handling DSP synthesis for binaural beats, dynamic ocean swells, acoustic rain patter, and multi-stage sequencing."""

import numpy as np
import scipy.signal as signal
import soundfile as sf


class SoundscapeEngine:

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, noise_type, duration_samples, level=0.65):
        """Generates realistic 2-channel soundscapes (Ocean Waves, Heavy Rain Drops, Soft White)."""
        noise_str = str(noise_type).lower().strip()

        if "none" in noise_str or not noise_str:
            return np.zeros((duration_samples, 2), dtype=np.float32)

        nyquist = self.sample_rate / 2.0
        white = np.random.uniform(-1.0, 1.0, (duration_samples, 2)).astype(np.float32)

        if "white" in noise_str:
            b, a = signal.butter(2, 8000.0 / nyquist, btype='low')
            soft_white = signal.lfilter(b, a, white, axis=0)
            max_v = np.max(np.abs(soft_white))
            if max_v > 0:
                soft_white = (soft_white / max_v) * level
            return soft_white.astype(np.float32)

        if "pink" in noise_str:
            # --- HEAVY DROPLET & SOFT AMBIENT RAIN ENGINE ---
            t = np.linspace(0, duration_samples / self.sample_rate, duration_samples, endpoint=False)

            # 1. Base Pink Bed (Voss-McCartney filter)
            b_pink = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
            a_pink = [1.0, -2.494956002, 2.017265875, -0.522189400]
            pink_base = signal.lfilter(b_pink, a_pink, white, axis=0)

            # Soften static bed with a warm 1.8kHz low-pass roll-off
            b_lp, a_lp = signal.butter(2, 1800.0 / nyquist, btype='low')
            rain_bed = signal.lfilter(b_lp, a_lp, pink_base, axis=0)

            # 2. Wind Gust Modulation (Gentle intensity waves)
            wind_lfo = 0.70 + 0.30 * (
                0.5 * np.sin(2 * np.pi * 0.04 * t) +
                0.3 * np.sin(2 * np.pi * 0.09 * t + 1.1) +
                0.2 * np.sin(2 * np.pi * 0.015 * t + 2.5)
            )
            rain_bed[:, 0] *= wind_lfo
            rain_bed[:, 1] *= wind_lfo

            # 3. Heavy Droplet Impact Layer (Low frequency, spaced further apart)
            impulse_threshold = 0.9995  # Sparse threshold for well-separated drops
            impulses_l = (np.random.uniform(0, 1, duration_samples) > impulse_threshold).astype(np.float32)
            impulses_r = (np.random.uniform(0, 1, duration_samples) > impulse_threshold).astype(np.float32)

            impulses_l *= np.random.uniform(0.3, 1.0, duration_samples)
            impulses_r *= np.random.uniform(0.3, 1.0, duration_samples)

            # Low-frequency peak filters for heavy drop body and puddle impact
            # Deep puddle plop (420 Hz)
            b_pop1, a_pop1 = signal.iirpeak(420.0 / nyquist, Q=5.0)
            pops_low_l = signal.lfilter(b_pop1, a_pop1, impulses_l)
            pops_low_r = signal.lfilter(b_pop1, a_pop1, impulses_r)

            # Mid drop body (780 Hz)
            b_pop2, a_pop2 = signal.iirpeak(780.0 / nyquist, Q=7.0)
            pops_mid_l = signal.lfilter(b_pop2, a_pop2, impulses_l)
            pops_mid_r = signal.lfilter(b_pop2, a_pop2, impulses_r)

            # Upper drop tone (1250 Hz)
            b_pop3, a_pop3 = signal.iirpeak(1250.0 / nyquist, Q=9.0)
            pops_high_l = signal.lfilter(b_pop3, a_pop3, impulses_l)
            pops_high_r = signal.lfilter(b_pop3, a_pop3, impulses_r)

            droplets_l = (1.2 * pops_low_l) + pops_mid_l + (0.7 * pops_high_l)
            droplets_r = (1.2 * pops_low_r) + pops_mid_r + (0.7 * pops_high_r)

            # Normalize layers
            max_bed = np.max(np.abs(rain_bed))
            if max_bed > 0:
                rain_bed /= max_bed
            
            droplet_stereo = np.column_stack((droplets_l, droplets_r))
            max_drop = np.max(np.abs(droplet_stereo))
            if max_drop > 0:
                droplet_stereo /= max_drop

            # Mix: 45% warm background bed + 55% heavy resonant drop impacts
            rain_mix = (0.45 * rain_bed) + (0.55 * droplet_stereo)
            rain_mix *= level
            return rain_mix.astype(np.float32)

        if "brown" in noise_str:
            # --- DYNAMIC OCEAN WAVE SURF ENGINE ---
            b_br = [0.10]
            a_br = [1.0, -0.985]
            brown_base = signal.lfilter(b_br, a_br, white, axis=0)

            b_deep, a_deep = signal.butter(2, 220.0 / nyquist, btype='low')
            b_surf, a_surf = signal.butter(2, 1400.0 / nyquist, btype='low')
            
            deep_layer = signal.lfilter(b_deep, a_deep, brown_base, axis=0)
            surf_layer = signal.lfilter(b_surf, a_surf, brown_base, axis=0)

            max_d = np.max(np.abs(deep_layer))
            if max_d > 0: deep_layer /= max_d
            max_s = np.max(np.abs(surf_layer))
            if max_s > 0: surf_layer /= max_s

            t = np.linspace(0, duration_samples / self.sample_rate, duration_samples, endpoint=False)
            
            lfo_l = 0.5 * (1.0 + np.sin(2 * np.pi * 0.08 * t))
            lfo_r = 0.5 * (1.0 + np.sin(2 * np.pi * 0.065 * t + 1.2))
            
            swell_l = 0.15 + 0.85 * lfo_l
            swell_r = 0.15 + 0.85 * lfo_r

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
