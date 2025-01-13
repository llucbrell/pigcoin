# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

# Incluir los archivos de configuración de bitcoinlib
bitcoinlib_data = collect_data_files('bitcoinlib')

a = Analysis(
    ['pigcoin.py'],
    pathex=[],
    binaries=[],
    datas=bitcoinlib_data,  # Agregar archivos de configuración
    hiddenimports=['bitcoinlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pigcoin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['sources\\pigcoin_logo.ico'],
)
