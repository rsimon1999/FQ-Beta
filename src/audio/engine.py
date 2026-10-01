"""Core Soundscape Engine handling DSP synthesis, dynamic asset management, per-track volume trimming, and multi-stage session rendering."""

import os
import numpy as np
import scipy.signal as signal
import soundfile as sf

from src.utils.config import DEFAULT_ASSETS_DIR


class SoundscapeEngine:

    # Registry mapping query keys -> (filename, default_gain_trim)
    ASSET_REGISTRY = {
        "rain": ("rain.mp3", 1.0),
        "pink": ("rain.mp3", 1.0),
        "wave": ("ocean.mp3", 1.0),
        "ocean": ("ocean.mp3", 1.0),
        "brown": ("ocean.mp3", 1.0),
        "white": ("white.mp3", 0.75),
        "wind": ("wind.mp3", 0.90),
        "forest": ("forest.mp3", 1.0),
        "forrest": ("forest.mp3", 1.0),
        "pond": ("pond.mp3", 1.0),
        "river": ("river.mp3", 0.45),  # Attenuated to fix loud mix balance
        "camping": ("camping.mp3", 0.90),
        "thunder": ("thunder.mp3", 1.0),
        "storm": ("thunder.mp3", 1.0),
        "wildlife": ("wildlife.mp3", 0.85),
        "urban": ("urban.mp3", 0.80),
    }

    def __init__(self, sample_rate=44100, assets_dir=None):
        self.sample_rate = sample_rate
        self.assets_dir = assets_dir or DEFAULT_ASSETS_DIR

    def _load_and_loop_asset(self, filename, duration_samples, level=0.65, trim=1.0):
        """Loads an audio asset, resamples to engine sample rate, applies gain trim, and loops seamlessly with crossfades."""
        filepath = os.path.join(self.assets_dir, filename)
        if not os.path.exists(filepath):
            return None

        try:
            data, sr = sf.read(filepath, dtype='float32')
        except Exception as e:
            print(f"Warning: Could not read asset file {filepath}: {e}")
            return None

        # Resample if asset sample rate differs
        if sr != self.sample_rate:
            num_target_samples = int(len(data) * (self.sample_rate / float(sr)))
            data = signal.resample(data, num_target_samples, axis=0)

        # Force 2-channel stereo
        if data.ndim == 1:
            data = np.column_stack((data, data))
        elif data.shape[1] == 1:
            data = np.repeat(data, 2, axis=1)

        # Equal-power crossfade looping across boundaries
        asset_len = len(data)
        if asset_len >= duration_samples:
            looped_audio = data[:duration_samples]
        else:
            fade_samples = min(int(0.35 * self.sample_rate), asset_len // 4)
            if fade_samples > 0:
                fade_out = np.linspace(1.0, 0.0, fade_samples)[:, np.newaxis]
                fade_in = np.linspace(0.0, 1.0, fade_samples)[:, np.newaxis]

                head = data[:-fade_samples]
                tail = data[-fade_samples:]
                start = data[:fade_samples]

                crossfaded_boundary = (tail * fade_out) + (start * fade_in)
                loop_unit = np.vstack((head, crossfaded_boundary))
            else:
                loop_unit = data

            repeats = int(np.ceil(duration_samples / len(loop_unit))) + 1
            full_stream = np.tile(loop_unit, (repeats, 1))
            looped_audio = full_stream[:duration_samples]

        # Peak normalization and apply master level + trim
        max_val = np.max(np.abs(looped_audio))
        if max_val > 0:
            looped_audio = (looped_audio / max_val) * (level * trim)

        return looped_audio.astype(np.float32)

    def generate_noise(self, noise_type, duration_samples, level=0.65):
        """Generates stereo soundscapes using registered sample assets with DSP mathematical fallbacks."""
        noise_str = str(noise_type).lower().strip()

        if "none" in noise_str or not noise_str:
            return np.zeros((duration_samples, 2), dtype=np.float32)

        nyquist = self.sample_rate / 2.0
        white = np.random.uniform(-1.0, 1.0, (duration_samples, 2)).astype(np.float32)

        # 1. Check registry for matching audio file asset
        for key, (filename, trim) in self.ASSET_REGISTRY.items():
            if key in noise_str:
                asset_audio = self._load_and_loop_asset(filename, duration_samples, level=level, trim=trim)
                if asset_audio is not None:
                    return asset_audio

        # 2. DSP Fallbacks if assets are missing
        if "white" in noise_str:
            b, a = signal.butter(2, 8000.0 / nyquist, btype='low')
            soft_white = signal.lfilter(b, a, white, axis=0)
            max_v = np.max(np.abs(soft_white))
            if max_v > 0:
                soft_white = (soft_white / max_v) * level
            return soft_white.astype(np.float32)

        if "pink" in noise_str or "rain" in noise_str:
            t = np.linspace(0, duration_samples / self.sample_rate, duration_samples, endpoint=False)
            b_pink = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
            a_pink = [1.0, -2.494956002, 2.017265875, -0.522189400]
            pink_base = signal.lfilter(b_pink, a_pink, white, axis=0)

            b_lp, a_lp = signal.butter(2, 1800.0 / nyquist, btype='low')
            rain_bed = signal.lfilter(b_lp, a_lp, pink_base, axis=0)

            wind_lfo = 0.70 + 0.30 * np.sin(2 * np.pi * 0.04 * t)
            rain_bed *= wind_lfo[:, np.newaxis]

            max_bed = np.max(np.abs(rain_bed))
            if max_bed > 0:
                rain_bed = (rain_bed / max_bed) * level
            return rain_bed.astype(np.float32)

        if "brown" in noise_str or "wave" in noise_str or "ocean" in noise_str:
            b_br = [0.10]
            a_br = [1.0, -0.985]
            brown_base = signal.lfilter(b_br, a_br, white, axis=0)
            max_b = np.max(np.abs(brown_base))
            if max_b > 0:
                brown_base = (brown_base / max_b) * level
            return brown_base.astype(np.float32)

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

    def _save_audio_file(self, output_filepath, audio_data):
        """Saves rendered audio array to WAV, FLAC, OGG, or MP3 based on extension."""
        ext = os.path.splitext(output_filepath)[1].lower()
        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)

        if ext in [".wav", ".flac", ".ogg"]:
            sf.write(output_filepath, audio_data, self.sample_rate)
            return output_filepath
        elif ext == ".mp3":
            temp_wav = output_filepath + ".tmp.wav"
            sf.write(temp_wav, audio_data, self.sample_rate)
            try:
                from pydub import AudioSegment
                sound = AudioSegment.from_wav(temp_wav)
                sound.export(output_filepath, format="mp3", bitrate="192k")
            except Exception as e:
                # Fallback to WAV if MP3 conversion fails
                fallback_wav = os.path.splitext(output_filepath)[0] + ".wav"
                sf.write(fallback_wav, audio_data, self.sample_rate)
                raise RuntimeError(
                    f"MP3 export failed ({e}). Saved as WAV instead: {fallback_wav}"
                )
            finally:
                if os.path.exists(temp_wav):
                    os.remove(temp_wav)
            return output_filepath
        else:
            sf.write(output_filepath, audio_data, self.sample_rate)
            return output_filepath

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
        output_filepath="output/session.mp3",
    ):
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
        return self._save_audio_file(output_filepath, audio_data)

    def render_sequence_session(self, stages, output_filepath="output/sequence_session.mp3", crossfade_sec=0.5):
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

        return self._save_audio_file(output_filepath, final_audio)