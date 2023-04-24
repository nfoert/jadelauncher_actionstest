# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['newJadeLauncher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["PyQtWebEngine"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas += [('accountDetails.ui','./ui/accountDetails.ui', "DATA"),
	('accountSuspended.ui','./ui/accountSuspended.ui', "DATA"),
	('createAccount.ui','./ui/createAccount.ui', "DATA"),
	('main.ui','./ui/main.ui', "DATA"),
	('offline.ui','./ui/offline.ui', "DATA"),
	('signIn.ui','./ui/signIn.ui', "DATA"),
	('signInFailure.ui','./ui/signInFailure.ui', "DATA"),
	("error.ui", "./ui/error.ui", "DATA"),
	('webView.ui','./ui/webView.ui', "DATA"),
    ('about.ui','./ui/about.ui', "DATA"),
    ('update.ui','./ui/update.ui', "DATA"),
    ('changePassword.ui','./ui/changePassword.ui', "DATA"),
    ('appStatus.ui','./ui/appStatus.ui', "DATA"),
    ('notification.ui','./ui/notification.ui', "DATA"),
	("JadeLauncherSplash.png", "./assets/other/JadeLauncherSplash.png", "DATA"),
    ("jadeAssistantDownloadDot.png", "./assets/dots/jadeAssistantDownloadDot.png", "DATA"),
    ("intro.png", "./assets/other/intro.png", "DATA"),
    ("status_ok.png", "./assets/icons/status_ok.png", "DATA"),
    ("status_offline.png", "./assets/icons/status_offline.png", "DATA"),
    ("status_load.gif", "./assets/animations/status_load.gif", "DATA"),
    ("notification.mp3", "./assets/audio/notification.mp3", "DATA")
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Jade Launcher',
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
    name='newJadeLauncher',
)
app = BUNDLE(
    coll,
    name='Jade Launcher.app',
    icon="jadeLauncher.icns",
    bundle_identifier=None,
)
