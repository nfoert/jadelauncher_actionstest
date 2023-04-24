from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
import assets
from time import sleep
import threading
from pathlib import PurePath
from time import sleep
from PyQt5.QtGui import QFont

guiLoopList = []
dot_jadeAssistantDownload = ""
dot_jadeAppsDownload = ""
showDotVar = ""
killThreads = False


def showDotThread():
    global guiLoopList
    global showDotVar
    global killThreads
    while killThreads == False:
        if showDotVar == "jadeAssistantDownload":
            print(f"Showing dot 'jadeAssistantDownload'")
            opaqueness = 0.0
            step = 0.05
            guiLoopList.append(f'dot_jadeAssistantDownload.setWindowOpacity({opaqueness})')
            guiLoopList.append('dot_jadeAssistantDownload.show()')
            while opaqueness < 1:
                guiLoopList.append(f'dot_jadeAssistantDownload.setWindowOpacity({opaqueness})')
                sleep(0.001)
                opaqueness += step

            showDotVar = False

        elif showDotVar == "jadeAppsDownload":
            print("Showing dot 'jadeAppsDownload'")
            opaqueness = 0.0
            step = 0.05
            guiLoopList.append(f'dot_jadeAppsDownload.setWindowOpacity({opaqueness})')
            guiLoopList.append('dot_jadeAppsDownload.show()')
            while opaqueness < 1:
                guiLoopList.append(f'dot_jadeAppsDownload.setWindowOpacity({opaqueness})')
                sleep(0.001)
                opaqueness += step

            showDotVar = False

        else:
            sleep(0.1)
        
        


def init(guiLoopListImport, window_mainImport, developmental, screen, dot_jadeAssistantDownloadImport, dot_jadeAppsDownloadImport):
    global guiLoopList
    global dot_jadeAssistantDownload
    global dot_jadeAppsDownload
    
    guiLoopList = guiLoopListImport
    dot_jadeAssistantDownload = dot_jadeAssistantDownloadImport
    dot_jadeAppsDownload = dot_jadeAppsDownloadImport

    screenSize = screen.size()
    moveHeight = screenSize.height() - 150
    moveWidth = screenSize.width() - 110

    showDotThreadManager = threading.Thread(target=showDotThread, daemon=True)
    showDotThreadManager.start()

    #Jade Assistant
    dot_jadeAssistantDownload.setFont(QFont("Calibri", 16))
    dot_jadeAssistantDownload.showMessage("\nLoading...", alignment=QtCore.Qt.AlignCenter)

    dot_jadeAssistantDownload.move(moveWidth, moveHeight)

    #Jade Apps
    dot_jadeAppsDownload.setFont(QFont("Calibri", 16))
    dot_jadeAppsDownload.showMessage("\nLoading...", alignment=QtCore.Qt.AlignCenter)

    dot_jadeAppsDownload.move(moveWidth, moveHeight)

    

def showDot(dot):
    global guiLoopList
    global dot_jadeAssistantDownload
    global dot_jadeAppsDownload
    global showDotVar
    if dot == "jadeAssistantDownload":
        showDotVar = "jadeAssistantDownload"

    elif dot == "jadeAppsDownload":
        showDotVar = "jadeAppsDownload"

    else:
        print(f"Dot not found! '{dot}'")

def hideDot(dot):
    global guiLoopList
    global dot_jadeAssistantDownload
    global showDot
    if dot == "jadeAssistantDownload":
        dot_jadeAssistantDownload.hide()

    elif dot == "jadeAppsDownload":
        dot_jadeAppsDownload.hide()

    else:
        print(f"Dot not found! '{dot}'")

def setDotPercent(dot, percent):
    if dot == "jadeAssistantDownload":
        dot_jadeAssistantDownload.setFont(QFont("Calibri", 16))
        dot_jadeAssistantDownload.showMessage(f"\n{percent}", alignment=QtCore.Qt.AlignCenter)

    elif dot == "jadeAppsDownload":
        dot_jadeAppsDownload.setFont(QFont("Calibri", 16))
        dot_jadeAppsDownload.showMessage(f"\n{percent}", alignment=QtCore.Qt.AlignCenter)


    else:
        print(f"Dot not found! '{dot}'")

def kill():
    global killThreads
    killThreads = True
    