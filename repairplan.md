# Binaural Audio Generator — Codebase Repair Plan

## Overview & Scope
This repair plan addresses critical architecture, thread safety, import resolution, and DSP audio continuity issues identified during the system audit.

---

## Task Matrix & Severity

| ID | Module | Issue | Impact | Severity | Status |
|:---|:---|:---|:---|:---|:---|
| **BUG-01** | `batch_panel.py` | Cross-thread Tkinter GUI mutation | UI freeze / hard crash on X11/Cocoa | **CRITICAL** | Pending |
| **BUG-02** | Multi-Module | Inconsistent module import paths | `ModuleNotFoundError` outside `src/` | **HIGH** | Pending |
| **DSP-01** | `engine.py` / `generators.py` | Discontinuous phase across stage ramps | Transient clicks/pops at stage bounds | **MEDIUM** | Pending |
| **TST-01** | Test Suite | Missing automated batch rendering sanity test | Regressions in background exports | **LOW** | Pending |

---

## Implementation Steps

### Step 1: Fix Tkinter Thread-Safety Violations (`batch_panel.py`)
Dispatch all UI progress and completion updates back to the main GUI event loop using `self.after()`.

### Step 2: Unify Package Import Resolution
Add robust fallback imports to `batch_runner.py`, `batch_panel.py`, and `easy_panel.py` so modules execute cleanly whether launched from standard execution, package installation, or nested directories.

### Step 3: Phase Continuity Audit in DSP Pipeline
Ensure frequency ramp calculations integrate instantaneous phase ($\phi_n = \phi_{n-1} + 2\pi \cdot f_n / f_s$) rather than re-indexing $t=0$ at each stage boundary.

---

## Execution Scripts

Run the scripts below from your project root to apply the fixes automatically.

