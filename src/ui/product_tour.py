"""
Product Tour — Speech-bubble callout overlay for Easy Mode.

Each step renders as a compact, chrome-free tooltip "callout" that floats
beside the target widget.  The bubble has a triangular pointer that
automatically flips direction based on available screen space.

Design goals
------------
* Non-modal: the user can still interact with the app during the tour.
* Chrome-free: overrideredirect(True) removes the OS title-bar.
* Compact: short body text, no scroll boxes.
* Comic-book feel: coloured border, bold title, triangular speech-bubble arrow.
* Persistent flag: completion stored in user_settings.json so the tour never
  auto-starts again after the first run.
"""

import customtkinter as ctk
import tkinter as tk
from src.utils.config import save_user_settings

# ---------------------------------------------------------------------------
# Colour palette for the callout bubble
# ---------------------------------------------------------------------------
BUBBLE_BG      = "#1A1A2E"   # dark navy body
BUBBLE_BORDER  = "#1E88E5"   # bright blue border
TITLE_COLOR    = "#90CAF9"   # light-blue title text
BODY_COLOR     = "#E0E0E0"   # near-white body text
BTN_NEXT_BG    = "#1E88E5"
BTN_NEXT_HVR   = "#1565C0"
BTN_BACK_BG    = "#2A2A3E"
BTN_SKIP_COLOR = "#555577"

BUBBLE_W = 300   # callout width  (px)
ARROW_H  = 12    # height of the triangular pointer

# ---------------------------------------------------------------------------
# Tour step definitions — keep body text SHORT (2-3 lines)
# ---------------------------------------------------------------------------
TOUR_STEPS = [
    {
        "title": "👋 Welcome!",
        "body": (
            "Quick tour: 10 steps to walk you through Easy Mode.\n"
            "We encourage you to follow along in the main UI while this is open.\n"
            "Click Next or Skip Tour anytime."
        ),
        "anchor_attr": None,
    },
    {
        "title": "Step 1 — Choose a Preset",
        "body": (
            "Pick a category pill (Focus, Sleep, Calm…) then select a\n"
            "Preset Protocol — this sets your brainwave 'goal'.\n"
            "The description below updates with stage details."
        ),
        "anchor_attr": "preset_option",
    },
    {
        "title": "Step 2 — Duration",
        "body": (
            "Choose how long your session will run.\n"
            "Start with 10–15 min — files stay small and it's a\n"
            "great way to audition a preset before a long render."
        ),
        "anchor_attr": "duration_option",
    },
    {
        "title": "Step 3 — Atmosphere",
        "body": (
            "Layer a real-world soundscape (ocean, rain, thunder…)\n"
            "behind the binaural tone, or leave it as None for a\n"
            "clean tone-only session.\n"
            "Try Calm and Light Thunder.  It's my personal favorite!"
        ),
        "anchor_attr": "noise_option",
    },
    {
        "title": "Step 4a — Binaural Tone Volume",
        "body": (
            "This is the 'wa-wa-wa' pulsing sound in each ear.\n"
            "Start around 10% — it works even at low levels.\n"
            "Headphones required for the binaural effect."
        ),
        "anchor_attr": "tone_slider",
    },
    {
        "title": "Step 4b — Atmosphere Volume",
        "body": (
            "Controls the level of your chosen soundscape.\n"
            "If you picked Thunder or Ocean, try starting around\n"
            "60% so it doesn't overpower the binaural tone."
        ),
        "anchor_attr": "noise_slider",
    },
    {
        "title": "Step 5 — Live Preview",
        "body": (
            "▶ Live Preview streams an 8-second sample in real\n"
            "time — no file written. Great for checking your mix.\n"
            "⏹ Stop Audio halts any active playback instantly."
        ),
        "anchor_attr": "preview_btn",
    },
    {
        "title": "Step 6 — Generate File",
        "body": (
            "Renders the full session to MP3 / WAV / FLAC / OGG.\n"
            "A save dialog lets you pick the location — save it\n"
            "somewhere easy to find (Music folder, Desktop, etc.)."
        ),
        "anchor_attr": "gen_btn",
    },
    {
        "title": "Step 7 — Save as Default",
        "body": (
            "Writes your current volumes, atmosphere, and duration\n"
            "to disk. The app will load these settings every launch\n"
            "so you won't need to adjust sliders each time."
        ),
        "anchor_attr": "save_def_btn",
    },
    {
        "title": "Step 8 — Play Generated File",
        "body": (
            "Enabled after a successful generation. Plays the most\n"
            "recently created file directly inside the app.\n"
            "That's it — enjoy your sessions! 🎧\n"
            "Make sure to use stereo headphones!"
        ),
        "anchor_attr": None,
    },
]


# ---------------------------------------------------------------------------
# CalloutBubble — a single chrome-free speech-bubble window
# ---------------------------------------------------------------------------

class CalloutBubble(tk.Toplevel):
    """
    A borderless Toplevel that looks like a comic-book speech bubble.

    The window body is drawn on a Canvas; an arrow triangle points toward
    the anchor widget.  Direction is either 'up' (arrow on top) or 'down'
    (arrow on bottom), chosen to keep the bubble on-screen.
    """

    RADIUS   = 12   # corner radius of the rounded rectangle
    PAD      = 16   # inner padding
    BORDER_W = 2    # border stroke width

    def __init__(self, parent, step: dict, step_num: int, total: int,
                 on_next, on_back, on_skip, on_finish, on_dont_show_toggle):
        super().__init__(parent)

        self.overrideredirect(True)          # remove OS chrome
        self.wm_attributes("-topmost", True)
        self.configure(bg=BUBBLE_BG)

        self._step       = step
        self._step_num   = step_num
        self._total      = total
        self._arrow_dir  = "down"            # set before draw()
        self._dont_show  = tk.BooleanVar(value=False)
        self._dont_show.trace_add("write", lambda *_: on_dont_show_toggle(self._dont_show.get()))

        self._on_next    = on_next
        self._on_back    = on_back
        self._on_skip    = on_skip
        self._on_finish  = on_finish

        self._build()

    # ------------------------------------------------------------------
    def _build(self):
        is_last = (self._step_num == self._total)

        # ---- Canvas for speech-bubble background ----
        # We'll set the canvas size after measuring the inner frame.
        self._canvas = tk.Canvas(
            self, bg=BUBBLE_BG, highlightthickness=0, bd=0
        )
        self._canvas.pack(fill="both", expand=True)

        # ---- Inner content frame (lives ON the canvas via create_window) ----
        self._inner = tk.Frame(self._canvas, bg=BUBBLE_BG)

        # Progress dots row
        dot_row = tk.Frame(self._inner, bg=BUBBLE_BG)
        dot_row.pack(fill="x", pady=(0, 4))
        for i in range(self._total):
            color = BUBBLE_BORDER if i == self._step_num - 1 else "#333355"
            tk.Label(dot_row, text="●", fg=color, bg=BUBBLE_BG,
                     font=("Helvetica", 7)).pack(side="left", padx=1)

        # Title
        tk.Label(
            self._inner, text=self._step["title"],
            fg=TITLE_COLOR, bg=BUBBLE_BG,
            font=("Helvetica", 12, "bold"),
            anchor="w", justify="left",
            wraplength=BUBBLE_W - self.PAD * 2 - 6,
        ).pack(fill="x", pady=(0, 6))

        # Body
        tk.Label(
            self._inner, text=self._step["body"],
            fg=BODY_COLOR, bg=BUBBLE_BG,
            font=("Helvetica", 10),
            anchor="w", justify="left",
            wraplength=BUBBLE_W - self.PAD * 2 - 6,
        ).pack(fill="x", pady=(0, 10))

        # Separator
        tk.Frame(self._inner, bg="#333355", height=1).pack(fill="x", pady=(0, 8))

        # Button row
        btn_row = tk.Frame(self._inner, bg=BUBBLE_BG)
        btn_row.pack(fill="x")

        # Don't-show checkbox (left)
        chk = tk.Checkbutton(
            btn_row, text="Don't show again",
            variable=self._dont_show,
            fg="#888899", bg=BUBBLE_BG, selectcolor=BUBBLE_BG,
            activebackground=BUBBLE_BG, activeforeground=TITLE_COLOR,
            font=("Helvetica", 9), bd=0, highlightthickness=0,
            cursor="hand2",
        )
        chk.pack(side="left")

        # Skip (right side, muted)
        skip_btn = tk.Label(
            btn_row, text="Skip",
            fg=BTN_SKIP_COLOR, bg=BUBBLE_BG,
            font=("Helvetica", 9, "underline"),
            cursor="hand2",
        )
        skip_btn.pack(side="right", padx=(4, 0))
        skip_btn.bind("<Button-1>", lambda _: self._on_skip())

        # Finish / Next
        action_label = "Finish ✓" if is_last else "Next →"
        action_cmd   = self._on_finish if is_last else self._on_next
        action_bg    = "#2E7D32" if is_last else BTN_NEXT_BG
        action_hov   = "#1B5E20" if is_last else BTN_NEXT_HVR

        next_btn = tk.Label(
            btn_row, text=action_label,
            fg="white", bg=action_bg,
            font=("Helvetica", 10, "bold"),
            padx=10, pady=3, cursor="hand2",
        )
        next_btn.pack(side="right", padx=(4, 0))
        next_btn.bind("<Button-1>", lambda _: action_cmd())
        next_btn.bind("<Enter>", lambda _: next_btn.config(bg=action_hov))
        next_btn.bind("<Leave>", lambda _: next_btn.config(bg=action_bg))

        # Back (if not first step)
        if self._step_num > 1:
            back_btn = tk.Label(
                btn_row, text="← Back",
                fg="#AAAACC", bg=BUBBLE_BG,
                font=("Helvetica", 9),
                padx=6, pady=3, cursor="hand2",
            )
            back_btn.pack(side="right", padx=(0, 4))
            back_btn.bind("<Button-1>", lambda _: self._on_back())

        # Force geometry update so we can measure the inner frame
        self._inner.update_idletasks()

    def draw_bubble(self, arrow_dir: str = "down"):
        """
        Called after placement: draws the rounded-rect + arrow on the canvas,
        then places the inner frame inside it.
        """
        self._arrow_dir = arrow_dir

        inner_w = self._inner.winfo_reqwidth()
        inner_h = self._inner.winfo_reqheight()

        body_w = max(inner_w + self.PAD * 2, BUBBLE_W)
        body_h = inner_h + self.PAD * 2

        total_h = body_h + ARROW_H

        self.geometry(f"{body_w}x{total_h}")
        self._canvas.config(width=body_w, height=total_h)
        self._canvas.delete("all")
        # Schedule a lift after the event loop processes the geometry
        self.after(50, self._raise_to_top)

        r = self.RADIUS
        bw = self.BORDER_W

        if arrow_dir == "down":
            # Arrow points downward (bubble is above the widget)
            rx0, ry0 = 0, 0
            rx1, ry1 = body_w, body_h
            # Arrow centred at bottom of the body rect
            ax = body_w // 2
            arrow_pts = [ax - 10, body_h, ax, body_h + ARROW_H, ax + 10, body_h]
            frame_y_offset = 0
        else:
            # Arrow points upward (bubble is below the widget)
            rx0, ry0 = 0, ARROW_H
            rx1, ry1 = body_w, ARROW_H + body_h
            ax = body_w // 2
            arrow_pts = [ax - 10, ARROW_H, ax, 0, ax + 10, ARROW_H]
            frame_y_offset = ARROW_H

        # Draw filled rounded rectangle + border
        self._rounded_rect(rx0, ry0, rx1, ry1, r, fill=BUBBLE_BG, outline=BUBBLE_BORDER, width=bw)

        # Draw arrow (filled polygon — same colour as bg, then outlined)
        self._canvas.create_polygon(arrow_pts, fill=BUBBLE_BG, outline=BUBBLE_BORDER,
                                    width=bw, smooth=False)
        # Cover the border between arrow base and rect body
        cover_y = body_h if arrow_dir == "down" else ARROW_H
        self._canvas.create_line(ax - 11, cover_y, ax + 11, cover_y,
                                 fill=BUBBLE_BG, width=bw + 1)

        # Place inner content frame on canvas
        self._canvas.create_window(
            body_w // 2, frame_y_offset + body_h // 2,
            window=self._inner, anchor="center",
            width=body_w - self.PAD * 2,
        )

        self.update_idletasks()

    def _raise_to_top(self):
        """Ensure the bubble is visible above all other windows."""
        try:
            self.lift()
            self.wm_attributes("-topmost", True)
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _rounded_rect(self, x0, y0, x1, y1, r, **kwargs):
        """Draw a rounded rectangle on self._canvas."""
        c = self._canvas
        c.create_arc(x0,     y0,     x0+2*r, y0+2*r, start=90,  extent=90,  style="arc", **kwargs)
        c.create_arc(x1-2*r, y0,     x1,     y0+2*r, start=0,   extent=90,  style="arc", **kwargs)
        c.create_arc(x1-2*r, y1-2*r, x1,     y1,     start=270, extent=90,  style="arc", **kwargs)
        c.create_arc(x0,     y1-2*r, x0+2*r, y1,     start=180, extent=90,  style="arc", **kwargs)

        fill = kwargs.get("fill", BUBBLE_BG)
        out  = kwargs.get("outline", BUBBLE_BORDER)
        w    = kwargs.get("width", 2)

        c.create_rectangle(x0+r, y0,   x1-r, y1,   fill=fill, outline="")
        c.create_rectangle(x0,   y0+r, x1,   y1-r, fill=fill, outline="")

        c.create_line(x0+r, y0,   x1-r, y0,   fill=out, width=w)
        c.create_line(x0+r, y1,   x1-r, y1,   fill=out, width=w)
        c.create_line(x0,   y0+r, x0,   y1-r, fill=out, width=w)
        c.create_line(x1,   y0+r, x1,   y1-r, fill=out, width=w)


# ---------------------------------------------------------------------------
# ProductTour — orchestrates the callout flow
# ---------------------------------------------------------------------------

class ProductTour:
    """
    Manages the sequential speech-bubble callout tour for Easy Mode.

    Usage
    -----
    tour = ProductTour(app_window, easy_frame)
    tour.start()
    """

    def __init__(self, parent: ctk.CTk, easy_frame):
        self.parent      = parent
        self.easy_frame  = easy_frame
        self._step_idx   = 0
        self._bubble     = None
        self._dont_show  = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self):
        self._step_idx = 0
        self._show_step()

    def close(self):
        if self._bubble and self._bubble.winfo_exists():
            try:
                self._bubble.destroy()
            except Exception:
                pass
        self._bubble = None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _show_step(self):
        self.close()

        if self._step_idx >= len(TOUR_STEPS):
            return

        step    = TOUR_STEPS[self._step_idx]
        total   = len(TOUR_STEPS)
        current = self._step_idx + 1

        self._bubble = CalloutBubble(
            parent=self.parent,
            step=step,
            step_num=current,
            total=total,
            on_next=self._on_next,
            on_back=self._on_back,
            on_skip=self._on_skip,
            on_finish=self._on_finish,
            on_dont_show_toggle=self._set_dont_show,
        )

        # Draw + position (needs two passes: measure then place)
        self._bubble.update_idletasks()
        arrow_dir, x, y = self._compute_position(step.get("anchor_attr"))
        self._bubble.draw_bubble(arrow_dir)
        self._bubble.geometry(f"+{x}+{y}")
        self._bubble.update_idletasks()
        # macOS: overrideredirect windows can appear behind — force them up
        self._bubble.lift()
        self._bubble.after(100, self._bubble._raise_to_top)
        self._bubble.after(300, self._bubble._raise_to_top)

    def _set_dont_show(self, value: bool):
        self._dont_show = value

    def _compute_position(self, anchor_attr):
        """
        Returns (arrow_dir, x, y) for the bubble window.
        Tries to place it below the widget (arrow up); falls back to above (arrow down).
        """
        bw = BUBBLE_W
        bh = (self._bubble.winfo_reqheight() if self._bubble else 220) + ARROW_H + 30

        screen_w = self.parent.winfo_screenwidth()
        screen_h = self.parent.winfo_screenheight()

        try:
            if anchor_attr and hasattr(self.easy_frame, anchor_attr):
                widget = getattr(self.easy_frame, anchor_attr)
                widget.update_idletasks()
                wx  = widget.winfo_rootx()
                wy  = widget.winfo_rooty()
                ww  = widget.winfo_width()
                wh  = widget.winfo_height()

                # Centre horizontally on the widget
                x = wx + ww // 2 - bw // 2

                # Prefer below; flip to above if it would go off screen
                y_below = wy + wh + 4
                y_above = wy - bh - 4

                if y_below + bh < screen_h - 20:
                    arrow_dir = "up"
                    y = y_below
                else:
                    arrow_dir = "down"
                    y = max(10, y_above)
            else:
                # Centred over parent window
                px = self.parent.winfo_rootx()
                py = self.parent.winfo_rooty()
                pw = self.parent.winfo_width()
                ph = self.parent.winfo_height()
                x  = px + pw // 2 - bw // 2
                y  = py + ph // 2 - bh // 2
                arrow_dir = "down"

            # Clamp to screen
            x = max(10, min(x, screen_w - bw - 10))
            y = max(10, min(y, screen_h - bh - 10))
            return arrow_dir, x, y

        except Exception:
            return "up", 100, 100

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _on_next(self):
        self._step_idx += 1
        self._show_step()

    def _on_back(self):
        self._step_idx = max(0, self._step_idx - 1)
        self._show_step()

    def _on_skip(self):
        if self._dont_show:
            self._persist_completed()
        self.close()

    def _on_finish(self):
        self._persist_completed()
        self.close()

    def _persist_completed(self):
        save_user_settings({"easy_mode_tour_completed": True})
