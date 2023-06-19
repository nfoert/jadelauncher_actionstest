import shelve
from pathlib import Path
import platform

UTILITYFuncs = ""

def init(UTILITYFuncsImport):
    global UTILITYFuncs
    UTILITYFuncs = UTILITYFuncsImport
    if platform.system() == "Windows":
        datFile = Path("jadeLauncherConfig.dat")
        dirFile = Path("jadeLauncherConfig.dir")
        bakFile = Path("jadeLauncherConfig.bak")
        if datFile.exists() == True and dirFile.exists() == True and bakFile.exists() == True:
            UTILITYFuncs.logAndPrint("INFO", "[Jade Config] Config file already exists!")

        else:
            UTILITYFuncs.logAndPrint("INFO", "[Jade Config] Config file does not exist.")
            configFile = shelve.open("jadeLauncherConfig")
            configFile.close()
            configFile = shelve.open("jadeLauncherConfig") # Do it twice because value was not setting correctly
            
            # Set default values
            setValue("intro", "true")
            setValue("new", "true")
            
            configFile.close()

    elif platform.system() == "Darwin":
        dbFile = Path("jadeLauncherConfig.db")
        if dbFile.exists() == True:
            UTILITYFuncs.logAndPrint("INFO", "[Jade Config] Config file already exists!")

        else:
            UTILITYFuncs.logAndPrint("INFO", "[Jade Config] Config file does not exist.")
            configFile = shelve.open("jadeLauncherConfig")
            configFile.close()
            configFile = shelve.open("jadeLauncherConfig") # Do it twice because value was not setting correctly

            # Set default values
            setValue("intro", "true")
            setValue("new", "true")

            configFile.close()

    else:
        UTILITYFuncs.error("[Jade Config] Your OS isn't supported! Please use Windows or Mac.")
    
    UTILITYFuncs.logAndPrint("INFO", "[Jade Config] Jade Config has been initiated")

def getValue(key):
    global UTILITYFuncs
    configFile = shelve.open("jadeLauncherConfig")
    try:
        data = configFile[key]
        configFile.close()
        UTILITYFuncs.logAndPrint("INFO", f"[Jade Config] Found '{data}' for key '{key}'")
        return data

    except KeyError:
        configFile.close()
        UTILITYFuncs.logAndPrint("INFO", f"[Jade Config] Key '{key}' not found!")

def setValue(key, value):
    global UTILITYFuncs
    configFile = shelve.open("jadeLauncherConfig")
    configFile[key] = value
    configFile.close()
    UTILITYFuncs.logAndPrint("INFO", f"[Jade Config] Saved '{key}' as '{value}'")

def removeValue(key):
    global UTILITYFuncs
    configFile = shelve.open("jadeLauncherConfig")
    try:
        del configFile[key]
        configFile.close()
        UTILITYFuncs.logAndPrint("INFO", f"[Jade Config] Removed key '{key}'")

    except KeyError:
        UTILITYFuncs.logAndPrint("INFO", f"[Jade Config] Key '{key}' not found!")
        configFile.close()

def listValues():
    configFile = shelve.open("jadeLauncherConfig")
    if len(configFile) != 0:
        print("Values ----------")
        for key, value in configFile.items():
            print(f"    - '{key}' with value '{value}'")

        print(f"({len(configFile)} results)")

    else:
        print("No values have been set.")
