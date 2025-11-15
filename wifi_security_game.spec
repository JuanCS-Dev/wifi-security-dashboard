# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for WiFi Security Education Game

Builds standalone executable for Windows, Linux, and macOS.

Author: Juan-Dev + AI Architect - Soli Deo Gloria ✝️
Date: 2025-11-15
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all data files
datas = []
datas += collect_data_files('pygame')

# Collect all submodules
hiddenimports = []
hiddenimports += collect_submodules('pygame')
hiddenimports += collect_submodules('src.gamification')
hiddenimports += collect_submodules('src.presentation')
hiddenimports += collect_submodules('src.plugins')

# Add explicit imports
hiddenimports += [
    'pygame',
    'pygame.locals',
    'pygame.font',
    'pygame.mixer',
    'scapy.all',
    'pyric',
    'dotenv',
]

a = Analysis(
    ['wifi_security_game.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='wifi-security-game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Show console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # TODO: Add icon file
)

# macOS bundle (only created on macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='WiFi Security Game.app',
        icon=None,
        bundle_identifier='com.juandev.wifisecuritygame',
        info_plist={
            'CFBundleName': 'WiFi Security Game',
            'CFBundleDisplayName': 'WiFi Security Education',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHumanReadableCopyright': 'Copyright © 2025 Juan-Dev. Soli Deo Gloria ✝️',
            'NSHighResolutionCapable': True,
        },
    )
