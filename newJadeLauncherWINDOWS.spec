# -*- mode: python -*-

block_cipher = None


a = Analysis(['newJadeLauncher.py'],
             pathex=['newJadeLauncher.py'],
             binaries=[],
             datas=[],
             hiddenimports=["jade_config"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

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
    ('settings.ui','./ui/settings.ui', "DATA"),
    ('alert.ui','./ui/alert.ui', "DATA"),
    ('new.ui','./ui/new.ui', "DATA"),
	("JadeLauncherSplash.png", "./assets/other/JadeLauncherSplash.png", "DATA"),
    ("jadeAssistantDownloadDot.png", "./assets/dots/jadeAssistantDownloadDot.png", "DATA"),
    ("jadeAppsDownloadDot.png", "./assets/dots/jadeAppsDownloadDot.png", "DATA"),
    ("intro.png", "./assets/other/intro.png", "DATA"),
    ("status_ok.png", "./assets/icons/status_ok.png", "DATA"),
    ("status_offline.png", "./assets/icons/status_offline.png", "DATA"),
    ("status_load.gif", "./assets/animations/status_load.gif", "DATA"),
    ("notification.mp3", "./assets/audio/notification.mp3", "DATA")
]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Jade Launcher',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='favicon.ico')
