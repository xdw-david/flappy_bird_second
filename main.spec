# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/pythontest/flappy_bird/music/start_music.mp3', 'music'), ('D:/pythontest/flappy_bird/music/game_music.mp3', 'music'), ('D:/pythontest/flappy_bird/sound/jump.mp3', 'sound'), ('D:/pythontest/flappy_bird/sound/coin.mp3', 'sound'), ('D:/pythontest/flappy_bird/sound/game_over.mp3', 'sound'), ('D:/pythontest/flappy_bird/pic/bird.png', 'pic'), ('D:/pythontest/flappy_bird/pic/tube_up.png', 'pic'), ('D:/pythontest/flappy_bird/pic/tube_down.png', 'pic'), ('D:/pythontest/flappy_bird/pic/coin.png', 'pic'), ('D:/pythontest/flappy_bird/pic/restart_button.png', 'pic'), ('D:/pythontest/flappy_bird/pic/background.png', 'pic'), ('D:/pythontest/flappy_bird/pic/frame1.png', 'pic'), ('D:/pythontest/flappy_bird/pic/frame2.png', 'pic'), ('D:/pythontest/flappy_bird/pic/frame3.png', 'pic'), ('D:/pythontest/flappy_bird/pic/start_button.png', 'pic')],
    hiddenimports=['pygame'],
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
    name='main',
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
)
