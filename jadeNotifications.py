from PyQt5 import QtCore, QtGui, uic, QtWidgets
import sys
import assets
from time import sleep
import threading
import playsound
from pathlib import PurePath

title = "Loading..."
text = "Loading..."
notification = False
more = 0
guiLoopList = []
window_notification = ""
window_main = ""
developmental = ""
resource_path = ""

extraHeight = 121

killThreads = False

def notificationThread():
    print("==================== Notification thread is going. ==========================")
    global title
    global text
    global notification
    global window_main
    global extraHeight
    global developmental

    global killThreads
    while killThreads == False:
        print("=============== notification loop =================")
        if notification == True:
            try:
                # Thanks to https://notificationsounds.com/ via https://notificationsounds.com/notification-sounds/ill-make-it-possible-notification
                guiLoopList.append("window_notification.title.hide()")
                guiLoopList.append("window_notification.text.hide()")
                if developmental == True:
                    audioPath = PurePath("assets/audio/notification.mp3")

                elif developmental == False:
                    audioPath = PurePath(resource_path("notification.mp3"))
                
                playsound.playsound("assets/audio/ill-make-it-possible-notification.mp3", block=False) #This may have been the only reason notifications stopped working. (The audio path was wrong) FIXME: Investigate, maybe re-implement later.
                #                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  Should be audioPath as set above depending on the developmental status
                print("SHOWY")
                guiLoopList.append("window_notification.show()")
                guiLoopList.append(f"window_notification.title.setText('{title}')")
                guiLoopList.append('window_notification.title.setFont(QtGui.QFont("Calibri", 16))')

                guiLoopList.append(f"window_notification.text.setText('{text}')")
                guiLoopList.append('window_notification.title.setFont(QtGui.QFont("Calibri", 12))')

                opaqueness = 0.0
                step = 0.01
                guiLoopList.append(f'window_notification.setWindowOpacity({opaqueness})')
                guiLoopList.append('window_notification.show()')
                while opaqueness < 1:
                    guiLoopList.append(f'window_notification.setWindowOpacity({opaqueness})')
                    sleep(0.001)
                    opaqueness += step

                sleep(3)
                guiLoopList.append(f'window_notification.title.resize(0, 61)')
                guiLoopList.append(f"window_notification.title.show()")

                for i in range(230):
                    guiLoopList.append(f'window_notification.frame.resize({i + 101}, {extraHeight})')
                    guiLoopList.append(f'window_notification.title.resize({i}, 61)')
                    sleep(0.00001)
                
                sleep(2)
                guiLoopList.append(f'window_notification.text.resize(271, 0)')
                guiLoopList.append(f"window_notification.text.show()")

                for i in range(70):
                    guiLoopList.append(f'window_notification.frame.resize(332, {i + 121})')
                    guiLoopList.append(f'window_notification.text.resize(271, {i})')
                    sleep(0.0001)

                sleep(5)

                opaqueness = 1.0
                step = 0.001
                guiLoopList.append(f'window_notification.setWindowOpacity({opaqueness})')
                guiLoopList.append('window_notification.show()')
                while opaqueness > 0:
                    guiLoopList.append(f'window_notification.setWindowOpacity({opaqueness})')
                    sleep(0.001)
                    opaqueness -= step

                guiLoopList.append('window_notification.hide()')
                guiLoopList.append('window_notification.setWindowOpacity(1)')

                notification = False

                sleep(2)
            except Exception as e:
                print(f"ACK IG {e}")

        elif window_main.isVisible() == False:
            return False


def init(guiLoopListImport, window_notificationImport, window_mainImport, developmentalImport, resource_pathimport):
    global notification
    global guiLoopList
    global window_notification
    global window_main
    global more
    global developmental
    global resource_path

    window_notification = window_notificationImport
    window_main = window_mainImport
    developmental = developmentalImport
    resource_path = resource_pathimport

    guiLoopList = guiLoopListImport
    print("Starting Jade Notifications...")

    window_notification.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    window_notification.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    window_notification.move(10, 10)
    window_notification.title.hide()
    window_notification.text.hide()
    window_notification.hide()
    window_notification.setWindowOpacity(0)

    window_notification.more.resize(21, 0)

    thread = threading.Thread(target=notificationThread, daemon=True)
    thread.start()

    print("Jade Notifications ready!")

def showNotification(titleImport, textImport):
    global title
    global text
    global notification
    global more
    global extraHeight

    if notification == False:
        print("Notification false")
        guiLoopList.append("window_notification.more.hide()")
        window_notification.frame.resize(101, 101)
        extraHeight = 101
        title = titleImport
        text = textImport
        notification = True

    elif notification == True:
        print("Notification true")
        print("There's already a notification shown!")
        guiLoopList.append("window_notification.more.show()")
        window_notification.frame.resize(101, 121)
        extraHeight = 121
        if more == 0:
            more = 1

        elif more > 1:
            more = more + 1

        for i in range(10):
            guiLoopList.append(f"window_notification.more.setText(' +{more} More')")
            guiLoopList.append(f"window_notification.more.resize({i * 10}, 21)")
            sleep(0.01)


    print("Showing notification!")

def kill():
    global killThreads
    killThreads = True

