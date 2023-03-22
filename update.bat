timeout /t 3
taskkill /IM /F "Jade Launcher.exe"
del /F "Jade Launcher.exe"
ren "Jade Launcher.exe.download" "Jade Launcher.exe"
"Jade Launcher.exe"