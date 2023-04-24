from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtGui import QMovie
from pathlib import PurePath

window_main = ""
developmental = ""
resource_path = ""

def init(window_mainImport, developmentalImport, resource_pathImport):
    global window_main
    global developmental
    global resource_path
    window_main = window_mainImport
    developmental = developmentalImport
    resource_path = resource_pathImport

    print("Jade Status: INIT")


    

def setStatus(status):
    # ok
    # load
    # offline

    global window_main
    global resource_path
    if status == "ok":
        if developmental == False:
            pixmap = QtGui.QPixmap(str(resource_path("status_ok.png")))

        elif developmental == True:
            pixmap = QtGui.QPixmap(str(PurePath("assets/icons/status_ok.png")))

        window_main.status.setPixmap(pixmap)

    elif status == "load":
        if developmental == False:
            movie = QMovie(str(resource_path("status_load.gif")))

        elif developmental == True:
            movie = QMovie(str(PurePath("assets/animations/status_load.gif")))

        window_main.status.setMovie(movie)
        movie.start()
        window_main.status.show()

    elif status == "offline":
        if developmental == False:
            pixmap = QtGui.QPixmap(str(resource_path("status_offline.png")))

        elif developmental == True:
            pixmap = QtGui.QPixmap(str(PurePath("assets/icons/status_offline.png")))

        window_main.status.setPixmap(pixmap)
        

    else:
        print("Status not recognized.")
