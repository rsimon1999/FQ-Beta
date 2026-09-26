"""
Batch Render Panel GUI Component
Allows queuing multiple presets or custom sequences for sequential background rendering to disk.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from presets.easy_mode import EASY_MODE_PRESETS
except ImportError:
    from src.presets.easy_mode import EASY_MODE_PRESETS


class BatchRenderPanel(ttk.Frame):
    def __init__(self, parent, batch_runner=None, available_presets=None, on_render_batch_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.batch_runner = batch_runner
        self.available_presets = available_presets or EASY_MODE_PRESETS
        self.on_render_batch_callback = on_render_batch_callback
        self.output_directory = os.path.expanduser("~/Music")

        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        dir_frame = ttk.LabelFrame(self, text=" Export Directory ", padding=10)
        dir_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        dir_frame.columnconfigure(0, weight=1)

        self.dir_entry = ttk.Entry(dir_frame)
        self.dir_entry.insert(0, self.output_directory)
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        browse_btn = ttk.Button(dir_frame, text="Browse...", command=self._browse_directory)
        browse_btn.grid(row=0, column=1)

        left_frame = ttk.LabelFrame(self, text=" Available Presets ", padding=10)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.available_box = tk.Listbox(left_frame, selectmode=tk.MULTIPLE)
        self.available_box.pack(fill="both", expand=True, side="left")

        avail_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.available_box.yview)
        avail_scroll.pack(side="right", fill="y")
        self.available_box.configure(yscrollcommand=avail_scroll.set)

        for preset_name in self.available_presets.keys():
            self.available_box.insert(tk.END, preset_name)

        mid_frame = ttk.Frame(self, padding=5)
        mid_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        mid_frame.columnconfigure(0, weight=1)
        mid_frame.rowconfigure(1, weight=1)

        btn_box = ttk.Frame(mid_frame)
        btn_box.grid(row=1, column=0)

        add_btn = ttk.Button(btn_box, text="Add Selected >>", command=self._add_selected)
        add_btn.pack(fill="x", pady=5)

        remove_btn = ttk.Button(btn_box, text="<< Remove", command=self._remove_selected)
        remove_btn.pack(fill="x", pady=5)

        clear_btn = ttk.Button(btn_box, text="Clear Queue", command=self._clear_queue)
        clear_btn.pack(fill="x", pady=5)

        right_frame = ttk.LabelFrame(mid_frame, text=" Render Queue ", padding=10)
        right_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")

        self.queue_box = tk.Listbox(right_frame, selectmode=tk.SINGLE)
        self.queue_box.pack(fill="both", expand=True, side="left")

        queue_scroll = ttk.Scrollbar(right_frame, orient="vertical", command=self.queue_box.yview)
        queue_scroll.pack(side="right", fill="y")
        self.queue_box.configure(yscrollcommand=queue_scroll.set)

        bottom_frame = ttk.Frame(self, padding=5)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.render_btn = ttk.Button(bottom_frame, text="Start Batch Export", command=self._start_batch_render)
        self.render_btn.pack(side="right")

    def _browse_directory(self):
        selected = filedialog.askdirectory(initialdir=self.output_directory)
        if selected:
            self.output_directory = selected
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, selected)

    def _add_selected(self):
        indices = self.available_box.curselection()
        for idx in indices:
            preset_name = self.available_box.get(idx)
            self.queue_box.insert(tk.END, preset_name)

    def _remove_selected(self):
        selected = self.queue_box.curselection()
        if selected:
            self.queue_box.delete(selected[0])

    def _clear_queue(self):
        self.queue_box.delete(0, tk.END)

    def _start_batch_render(self):
        queue = list(self.queue_box.get(0, tk.END))
        if not queue:
            messagebox.showwarning("Empty Queue", "Please add at least one preset to the render queue.")
            return

        out_dir = self.dir_entry.get().strip()
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Export Error", f"Could not create export directory: {e}")
                return

        if self.batch_runner:
            self.render_btn.configure(state="disabled")

            def on_progress(preset_name, idx, total, status):
                self.after(0, lambda: self.render_btn.configure(text=f"Rendering {idx}/{total}..."))

            def on_complete(success):
                def _update_ui():
                    self.render_btn.configure(state="normal", text="Start Batch Export")
                    if success:
                        messagebox.showinfo("Export Complete", f"Successfully exported {len(queue)} items to:\n{out_dir}")
                    else:
                        messagebox.showwarning("Export Interrupted", "Batch export was cancelled or stopped.")
                self.after(0, _update_ui)

            self.batch_runner.run_batch(queue, out_dir, progress_callback=on_progress, completion_callback=on_complete)
        elif self.on_render_batch_callback:
            self.on_render_batch_callback(queue, out_dir)
        else:
            messagebox.showinfo("Batch Queued", f"Queued {len(queue)} items for export to:\n{out_dir}")
