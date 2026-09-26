"""
Batch Runner Engine
Executes sequential audio rendering jobs for queued binaural presets.
"""

import os
import threading
import time
import wave
import numpy as np

try:
    from presets.easy_mode import EASY_MODE_PRESETS
except ImportError:
    from src.presets.easy_mode import EASY_MODE_PRESETS


class BatchRunner:
    def __init__(self, engine_render_func=None, audio_engine=None):
        self.engine_render_func = engine_render_func
        self.audio_engine = audio_engine
        self.is_running = False
        self._cancel_requested = False

    def run_batch(self, queue, output_dir, progress_callback=None, completion_callback=None):
        """Runs a list of preset names sequentially in a background thread."""
        thread = threading.Thread(
            target=self._execute_batch,
            args=(queue, output_dir, progress_callback, completion_callback),
            daemon=True
        )
        thread.start()

    def _execute_batch(self, queue, output_dir, progress_callback, completion_callback):
        self.is_running = True
        self._cancel_requested = False
        total = len(queue)

        for idx, preset_name in enumerate(queue, start=1):
            if self._cancel_requested:
                break

            preset_data = EASY_MODE_PRESETS.get(preset_name)
            if not preset_data:
                continue

            if progress_callback:
                progress_callback(preset_name, idx, total, "Rendering...")

            clean_name = "".join(c if c.isalnum() else "_" for c in preset_name.lower())
            output_file = os.path.join(output_dir, f"{clean_name}.wav")

            if self.engine_render_func:
                try:
                    res = self.engine_render_func(preset_data)
                    if isinstance(res, tuple) and len(res) == 2:
                        audio_data, sample_rate = res
                        self._save_wav(output_file, audio_data, sample_rate)
                except Exception as e:
                    print(f"Error rendering {preset_name}: {e}")
            elif self.audio_engine and hasattr(self.audio_engine, "export_preset"):
                self.audio_engine.export_preset(preset_data, output_file)
            else:
                time.sleep(0.5)

        self.is_running = False
        if completion_callback:
            completion_callback(not self._cancel_requested)

    def _save_wav(self, filepath, audio_data, sample_rate):
        audio_data = np.clip(audio_data, -1.0, 1.0)
        int_data = (audio_data * 32767).astype(np.int16)
        channels = 1 if int_data.ndim == 1 else int_data.shape[1]

        with wave.open(filepath, "w") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(int_data.tobytes())

    def cancel(self):
        self._cancel_requested = True
