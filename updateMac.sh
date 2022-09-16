echo Starting Updater...
sleep 3
echo $1 >> output.txt
cd "$1"
rm -rf "Jade Launcher.app"
mv "Jade Launcher.app.download/Jade Launcher.app" "Jade Launcher.app"
cd "./Jade Launcher.app/Contents/MacOS"
chmod 775 certifi "Jade Launcher" Python QtBluetooth QtConcurrent QtCore QtDBus QtGui QtLocation QtMultimedia QtNetwork QtNfc QtPositioning
chmod 775 QtPositioningQuick QtPrintSupport QtQml QtQuick QtQuickControls2 QtQuickParticles QtQuickShapes QtQuickTemplates2 QtQuickTest
chmod 775 QtQuickWidgets QtRemoteObjects QtSensors QtSerialPort QtSql QtSvg QtTest QtWebChannel QtWebEngine qtwebengine_locales
chmod 775 QtWebEngineWidgets QtWebSockets QtWidgets QtXmlPatterns tcl tcl8 tk
cd "$1"
xattr -cr "Jade Launcher.app"
open "Jade Launcher.app"
echo Done!