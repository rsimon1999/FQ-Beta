"""Unit tests for the SoundscapeEngine DSP audio pipeline, AudioPlayer, and Settings."""

import os
import sys
import unittest
import numpy as np

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.audio.engine import SoundscapeEngine
from src.audio.player import AudioPlayer
from src.utils.config import load_user_settings, save_user_settings


class TestSoundscapeEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SoundscapeEngine(sample_rate=44100, assets_dir="assets")

    def test_noise_generation_none(self):
        """Test 'none' noise returns zeros."""
        samples = 44100
        noise = self.engine.generate_noise("none", samples)
        self.assertEqual(noise.shape, (samples, 2))
        self.assertTrue(np.all(noise == 0.0))

    def test_noise_generation_white_fallback(self):
        """Test white noise fallback."""
        samples = 22050
        noise = self.engine.generate_noise("white", samples, level=0.5)
        self.assertEqual(noise.shape, (samples, 2))
        self.assertLessEqual(np.max(np.abs(noise)), 0.55)

    def test_binaural_stage_stereo_shape(self):
        """Test binaural stage generation yields proper shape and normalization."""
        duration = 1.0  # 1 second test
        audio = self.engine.generate_binaural_stage(
            start_beat=10.0,
            target_beat=10.0,
            carrier_freq=200.0,
            duration_sec=duration,
            noise_type="none",
            tone_volume=0.10,
        )
        expected_samples = int(self.engine.sample_rate * duration)
        self.assertEqual(audio.shape, (expected_samples, 2))
        self.assertLessEqual(np.max(np.abs(audio)), 1.0)

    def test_binaural_stage_with_harmonics_and_isochronic(self):
        """Test generation with harmonic richness and isochronic pulsing."""
        duration = 0.5
        audio = self.engine.generate_binaural_stage(
            start_beat=12.0,
            target_beat=8.0,
            carrier_freq=216.0,
            duration_sec=duration,
            noise_type="rain",
            isochronic_mode=True,
            harmonic_richness=0.5,
            tone_volume=0.10,
            noise_level=0.80,
        )
        expected_samples = int(self.engine.sample_rate * duration)
        self.assertEqual(audio.shape, (expected_samples, 2))
        self.assertLessEqual(np.max(np.abs(audio)), 1.0)

    def test_render_session_wav_export(self):
        """Test rendering full binaural session to WAV file."""
        os.makedirs("output", exist_ok=True)
        test_file = "output/test_quick_session.wav"
        try:
            out_path = self.engine.render_binaural_session(
                start_beat=10.0,
                target_beat=10.0,
                carrier_freq=200.0,
                duration_sec=0.5,
                noise_type="none",
                output_filepath=test_file,
            )
            self.assertTrue(os.path.exists(out_path))
            self.assertGreater(os.path.getsize(out_path), 1000)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_user_settings_persistence(self):
        """Test loading and saving default settings."""
        settings = load_user_settings()
        self.assertIn("tone_volume", settings)
        self.assertIn("noise_level", settings)
        self.assertEqual(settings["tone_volume"], 0.10)
        self.assertEqual(settings["noise_level"], 0.80)

        # Test save and reload
        save_user_settings({"default_atmosphere": "Ocean Waves", "tone_volume": 0.10, "noise_level": 0.80})
        reloaded = load_user_settings()
        self.assertEqual(reloaded["noise_level"], 0.80)
        self.assertEqual(reloaded["tone_volume"], 0.10)

    def test_audio_player_instantiation_and_stop(self):
        """Test AudioPlayer lifecycle and stopping."""
        player = AudioPlayer()
        self.assertFalse(player.is_playing)
        player.stop()
        self.assertFalse(player.is_playing)


if __name__ == "__main__":
    unittest.main()
