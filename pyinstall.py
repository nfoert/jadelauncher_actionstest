from colorama import Fore, Style
import platform
import sys
from time import sleep
import os
import subprocess
import playsound

# Enter the name of your spec file here:
specfile_windows = "newJadeLauncherWINDOWS.spec"
specfile_mac = "newJadeLauncherMAC.spec"
# -------------------------------------

print(f"{Fore.YELLOW}--------------------------------------------------------------------------")
print(f"{Fore.MAGENTA}                _          _____       _           _        _ _            ")
print(f"{Fore.MAGENTA}     /\        | |        |  __ \     (_)         | |      | | |           ")
print(f"{Fore.MAGENTA}    /  \  _   _| |_ ___   | |__) |   _ _ _ __  ___| |_ __ _| | | ___ _ __  ")
print(f"{Fore.MAGENTA}   / /\ \| | | | __/ _ \  |  ___/ | | | | '_ \/ __| __/ _` | | |/ _ \ '__| ")
print(f"{Fore.MAGENTA}  / ____ \ |_| | || (_) | | |   | |_| | | | | \__ \ || (_| | | |  __/ |    ") 
print(f"{Fore.MAGENTA} /_/    \_\__,_|\__\___/  |_|    \__, |_|_| |_|___/\__\__,_|_|_|\___|_|    ")
print(f"{Fore.MAGENTA}                                  __/ |                                    ")
print(f"{Fore.MAGENTA}                                |___/                                      ")
print(f"{Fore.MAGENTA}         (Now with audio!)                                                 ")
print(f"{Fore.YELLOW}--------------------------------------------------------------------------")

if platform.system() == "Windows":
    print(f"{Fore.YELLOW}Selected OS: Windows")

elif platform.system() == "Darwin":
    print(f"{Fore.YELLOW}Selected OS: Mac")

else:
    print(f"{Fore.RED}OS NOT DETECTED OR SUPPORTED")
    print(f"{Fore.YELLOW}--------------------------------------------------------------------------")
    print(Style.RESET_ALL)
    sys.exit()

print(f"{Fore.GREEN}PREPARE FOR PYINSTALLING")
print(f"{Fore.YELLOW}--------------------------------------------------------------------------")
sleep(1)
print(f"{Fore.GREEN}Starting in 3")
sleep(1)
print("\033[A                             \033[A")
print(f"{Fore.GREEN}Starting in 2")
sleep(1)
print("\033[A                             \033[A")
print(f"{Fore.GREEN}Starting in 1")
sleep(1)
print("\033[A                             \033[A")
print(f"{Fore.GREEN}Starting!")
print(f"{Fore.YELLOW}--------------------------------------------------------------------------")

print(Style.RESET_ALL)

if platform.system() == "Darwin":
    cmd = subprocess.call("pyinstaller --noconfirm newJadeLauncherMAC.spec", shell=True, stdout=subprocess.PIPE)

else:
    cmd = subprocess.call("pyinstaller --noconfirm newJadeLauncherWINDOWS.spec", shell=True, stdout=subprocess.PIPE)


if platform.system() == "Darwin":
    print(f"{Fore.YELLOW}--------------------------------------------------------------------------")
    print(f"{Fore.BLUE} Finishing up...")
    os.remove("./dist/Jade Launcher.app/Contents/MacOS/QtWebEngineCore")
    os.system("rm -rf '/Users/noahfoertmeyer/Programming/Jade/Jade Launcher/SYNC SPOT/dist/Jade Launcher.app/Contents/MacOS/PyQt5/Qt/lib/QtWebEngineCore.framework'")
    print(f"{Fore.GREEN} Done!")
    print(f"{Fore.YELLOW}--------------------------------------------------------------------------")

else:
    print(f"{Fore.GREEN} Done!")
    print(f"{Fore.YELLOW}--------------------------------------------------------------------------")
    # thanks to https://notificationsounds.com/free-jingles-and-logos/message-ringtone-magic
    playsound.playsound("magic.mp3")


print(Style.RESET_ALL)