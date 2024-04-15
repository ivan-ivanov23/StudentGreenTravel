# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['calculator.py'],
    pathex=[],
    binaries=[(r'C:\Users\Ivan_PC\AppData\Local\Programs\Python\Python312\python312.dll', '.')],
    datas=[('data', 'data'), ('icons', 'icons'), ('pictures', 'pictures')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='StudentGreenTravel',
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
    icon=['eco.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StudentGreenTravel',
)
