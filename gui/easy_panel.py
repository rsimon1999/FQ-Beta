"""
Easy Mode Panel GUI Component
Provides preset selection, stage overview, and execution triggers for Easy Mode presets.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from presets.easy_mode import EASY_MODE_PRESETS, get_presets_by_category


class EasyModePanel(ttk.Frame):
    def __init__(self, parent, on_select_preset_callback=None, on_run_preset_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.on_select_preset_callback = on_select_preset_callback or on_run_preset_callback
        self.on_run_preset_callback = on_run_preset_callback or on_select_preset_callback

        self.categorized_presets = get_presets_by_category()
        self.selected_preset_name = None

        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        left_frame = ttk.LabelFrame(self, text=" Preset Catalog ", padding=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.tree = ttk.Treeview(left_frame, selectmode="browse", show="tree")
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self._populate_tree()
        self.tree.bind("<<TreeviewSelect>>", self._on_preset_selected)

        right_frame = ttk.LabelFrame(self, text=" Preset Details & Stages ", padding=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(right_frame, text="Select a preset from the left catalog", font=("Helvetica", 12, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.desc_label = ttk.Label(right_frame, text="", wraplength=400, justify="left")
        self.desc_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        columns = ("stage", "duration", "start_freq", "end_freq", "base_freq", "wave")
        self.stage_table = ttk.Treeview(right_frame, columns=columns, show="headings", height=6)
        self.stage_table.grid(row=2, column=0, sticky="nsew", pady=5)

        self.stage_table.heading("stage", text="Stage Name")
        self.stage_table.heading("duration", text="Duration (min)")
        self.stage_table.heading("start_freq", text="Start (Hz)")
        self.stage_table.heading("end_freq", text="End (Hz)")
        self.stage_table.heading("base_freq", text="Base (Hz)")
        self.stage_table.heading("wave", text="Waveform")

        self.stage_table.column("stage", width=120)
        self.stage_table.column("duration", width=80, anchor="center")
        self.stage_table.column("start_freq", width=70, anchor="center")
        self.stage_table.column("end_freq", width=70, anchor="center")
        self.stage_table.column("base_freq", width=70, anchor="center")
        self.stage_table.column("wave", width=80, anchor="center")

        self.run_button = ttk.Button(right_frame, text="Load & Run Preset", state="disabled", command=self._on_run_click)
        self.run_button.grid(row=3, column=0, sticky="e", pady=(10, 0))

    def _populate_tree(self):
        for category, presets in self.categorized_presets.items():
            cat_id = self.tree.insert("", "end", text=category, open=True)
            for name, _ in presets:
                self.tree.insert(cat_id, "end", text=name, values=(name,))

    def _on_preset_selected(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item.get("values")

        if not values:
            self.run_button.configure(state="disabled")
            return

        preset_name = values[0]
        self.selected_preset_name = preset_name
        preset_data = EASY_MODE_PRESETS.get(preset_name)

        if preset_data:
            self.title_label.configure(text=preset_name)
            self.desc_label.configure(text=preset_data.get("description", ""))

            for row in self.stage_table.get_children():
                self.stage_table.delete(row)

            for stage in preset_data.get("stages", []):
                dur = stage.get('duration_min')
                sf = stage.get('start_freq')
                ef = stage.get('end_freq')
                bf = stage.get('base_freq')
                wave = stage.get('wave_type', 'sine')
                self.stage_table.insert("", "end", values=(
                    stage.get("name"),
                    f"{dur} min",
                    f"{sf} Hz",
                    f"{ef} Hz",
                    f"{bf} Hz",
                    wave
                ))

            self.run_button.configure(state="normal")
            if self.on_select_preset_callback:
                self.on_select_preset_callback(preset_data)

    def _on_run_click(self):
        if self.selected_preset_name and self.on_run_preset_callback:
            preset_data = EASY_MODE_PRESETS.get(self.selected_preset_name)
            self.on_run_preset_callback(preset_data)
