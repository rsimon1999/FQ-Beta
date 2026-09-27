# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Specification for NeuroAcoustic Sound Studio.
Bundles CustomTkinter, NumPy, SciPy, SoundDevice, SoundFile, and ambient assets into a standalone binary / app bundle.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Project root directory
SPEC_DIR = os.path.dirname(os.path.abspath(SPEC)) if 'SPEC' in locals() else os.getcwd()
PROJECT_ROOT = os.path.abspath(os.path.join(SPEC_DIR, "..")) if os.path.basename(SPEC_DIR) == "build_scripts" else SPEC_DIR

# Collect CustomTkinter assets, themes, and fonts
customtkinter_datas = collect_data_files('customtkinter')

# Data files to bundle: assets, presets, and data
datas = [
    (os.path.join(PROJECT_ROOT, 'assets'), 'assets'),
    (os.path.join(PROJECT_ROOT, 'presets'), 'presets'),
    (os.path.join(PROJECT_ROOT, 'data'), 'data'),
] + customtkinter_datas

# Hidden imports required by DSP and UI libraries
hiddenimports = [
    'customtkinter',
    'darkdetect',
    'sounddevice',
    'soundfile',
    'scipy',
    'scipy.signal',
    'scipy.signal.windows',
    'numpy',
    'cffi',
    'PIL',
    'PIL._tkinter_finder',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'src.audio.engine',
    'src.audio.player',
    'src.audio.dsp',
    'src.audio.generators',
    'src.ui.app',
    'src.ui.frames',
    'src.ui.constants',
    'src.utils.config',
    'src.utils.export',
    'presets.easy_mode',
]

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'main.py')],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'IPython', 'jupyter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable specification
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='NeuroAcousticStudio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NeuroAcousticStudio',
)

# macOS App Bundle (only active on macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='NeuroAcoustic Studio.app',
        icon=None,
        bundle_identifier='com.neuroacoustic.soundstudio',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSRequiresAquaSystemAppearance': 'False',
            'NSHumanReadableCopyright': 'Copyright © 2026 NeuroAcoustic Sound Studio',
        },
    )
