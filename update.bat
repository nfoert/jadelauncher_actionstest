timeout /t 3
taskkill /IM "Jade Launcher.exe" /F
del /F "Jade Launcher.exe"
ren "Jade Launcher.exe.download" "Jade Launcher.exe"
"Jade Launcher.exe"