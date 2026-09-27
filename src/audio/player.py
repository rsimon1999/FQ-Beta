"""Audio Player and Live Preview Engine for real-time streaming and file playback."""

import os
import subprocess
import threading
import numpy as np
from typing import Optional, Callable, Dict, Any

try:
    import sounddevice as sd
    HAS_SOUNDDEVICE = True
except (ImportError, OSError):
    sd = None
    HAS_SOUNDDEVICE = False

try:
    import soundfile as sf
except ImportError:
    sf = None


class AudioPlayer:
    """Manages asynchronous real-time preview streaming and audio file playback."""

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self._is_playing = False
        self._current_source = None
        self._lock = threading.Lock()
        self._completion_callback: Optional[Callable[[], None]] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._subprocess_proc: Optional[subprocess.Popen] = None

    @property
    def is_playing(self) -> bool:
        return self._is_playing

    @property
    def current_source(self) -> Optional[str]:
        return self._current_source

    def play_array(
        self,
        audio_data: np.ndarray,
        sample_rate: Optional[int] = None,
        source_name: str = "Live Preview",
        on_finished: Optional[Callable[[], None]] = None,
    ):
        """Plays an in-memory numpy audio array asynchronously without disk I/O."""
        self.stop()

        if not HAS_SOUNDDEVICE or sd is None:
            raise RuntimeError(
                "Real-time live preview requires 'sounddevice'. "
                "Please run: pip install sounddevice"
            )

        sr = sample_rate or self.sample_rate
        with self._lock:
            self._is_playing = True
            self._current_source = source_name
            self._completion_callback = on_finished

            # Play asynchronously using sounddevice
            sd.play(audio_data, sr)

            duration_sec = len(audio_data) / float(sr)
            self._monitor_thread = threading.Thread(
                target=self._wait_for_completion,
                args=(duration_sec,),
                daemon=True,
            )
            self._monitor_thread.start()

    def play_preview(
        self,
        engine,
        params: Dict[str, Any],
        duration_sec: float = 8.0,
        on_finished: Optional[Callable[[], None]] = None,
    ):
        """Generates an in-memory preview stage and plays it immediately."""
        # Support both multi-stage parameters and flat parameters
        if "stages" in params and params["stages"]:
            first_stage = params["stages"][0]
            start_beat = first_stage.get("start_beat", 10.0)
            target_beat = first_stage.get("target_beat", start_beat)
            carrier_freq = first_stage.get("carrier_freq", 200.0)
            noise_type = first_stage.get("noise_type", params.get("noise_type", "ocean"))
            tone_volume = first_stage.get("tone_volume", params.get("tone_volume", 0.10))
            noise_level = first_stage.get("noise_level", params.get("noise_level", 0.80))
            isochronic_mode = first_stage.get("isochronic_mode", params.get("isochronic_mode", False))
            harmonic_richness = first_stage.get("harmonic_richness", params.get("harmonic_richness", 0.0))
        else:
            start_beat = params.get("start_beat", 10.0)
            target_beat = params.get("target_beat", 10.0)
            carrier_freq = params.get("carrier_freq", 200.0)
            noise_type = params.get("noise_type", "ocean")
            tone_volume = params.get("tone_volume", 0.10)
            noise_level = params.get("noise_level", 0.80)
            isochronic_mode = params.get("isochronic_mode", False)
            harmonic_richness = params.get("harmonic_richness", 0.0)

        preview_audio = engine.generate_binaural_stage(
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
        self.play_array(
            preview_audio,
            sample_rate=engine.sample_rate,
            source_name=f"Preview ({duration_sec:.0f}s)",
            on_finished=on_finished,
        )

    def play_file(
        self,
        filepath: str,
        on_finished: Optional[Callable[[], None]] = None,
    ):
        """Reads and plays a rendered audio file from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file not found: {filepath}")

        self.stop()
        filename = os.path.basename(filepath)

        # 1. Primary path: sounddevice + soundfile
        if HAS_SOUNDDEVICE and sf is not None:
            try:
                data, sr = sf.read(filepath, dtype="float32")
                self.play_array(
                    data,
                    sample_rate=sr,
                    source_name=filename,
                    on_finished=on_finished,
                )
                return
            except Exception as e:
                print(f"sounddevice playback failed ({e}), falling back to native player...")

        # 2. Fallback path for macOS (afplay)
        with self._lock:
            self._is_playing = True
            self._current_source = filename
            self._completion_callback = on_finished

            def _run_afplay():
                try:
                    self._subprocess_proc = subprocess.Popen(["afplay", filepath])
                    self._subprocess_proc.wait()
                except Exception as ex:
                    print(f"afplay error: {ex}")
                finally:
                    with self._lock:
                        self._is_playing = False
                        self._current_source = None
                        self._subprocess_proc = None
                        if self._completion_callback:
                            cb = self._completion_callback
                            self._completion_callback = None
                            try:
                                cb()
                            except Exception:
                                pass

            self._monitor_thread = threading.Thread(target=_run_afplay, daemon=True)
            self._monitor_thread.start()

    def stop(self):
        """Stops any active audio playback immediately."""
        with self._lock:
            if self._is_playing:
                if HAS_SOUNDDEVICE and sd is not None:
                    try:
                        sd.stop()
                    except Exception as e:
                        print(f"Warning during sounddevice stop: {e}")
                if self._subprocess_proc:
                    try:
                        self._subprocess_proc.terminate()
                    except Exception:
                        pass
                    self._subprocess_proc = None

                self._is_playing = False
                self._current_source = None
                if self._completion_callback:
                    cb = self._completion_callback
                    self._completion_callback = None
                    try:
                        cb()
                    except Exception as e:
                        print(f"Error in playback completion callback: {e}")

    def _wait_for_completion(self, duration_sec: float):
        """Monitors playback duration and resets state upon completion."""
        try:
            elapsed = 0.0
            slice_time = 0.1
            while elapsed < duration_sec:
                if not self._is_playing:
                    return
                if HAS_SOUNDDEVICE and sd is not None:
                    sd.sleep(int(slice_time * 1000))
                elapsed += slice_time
        except Exception:
            pass
        finally:
            with self._lock:
                if self._is_playing:
                    self._is_playing = False
                    self._current_source = None
                    if self._completion_callback:
                        cb = self._completion_callback
                        self._completion_callback = None
                        try:
                            cb()
                        except Exception as e:
                            print(f"Error in playback completion callback: {e}")
