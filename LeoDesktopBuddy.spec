# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

project = Path(SPECPATH)

a = Analysis(
    [str(project / "leo_pet.py")],
    pathex=[str(project)],
    binaries=[],
    datas=[
        (str(project / "assets" / "sprites" / "leo-walk-v2.png"), "assets/sprites"),
        (str(project / "assets" / "sprites" / "leo-fight.png"), "assets/sprites"),
    ],
    hiddenimports=["PIL._tkinter_finder"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="LeoDesktopBuddy",
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
