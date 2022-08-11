echo Starting updater...
sleep 3
cd %1
del "Jade Launcher.exe"
move "Jade Launcher.exe.download" "Jade Launcher.exe"
"Jade Launcher.exe"
echo Done!