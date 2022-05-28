'''
Jade Launcher (NEW)
The Jade Launcher is what launches apps like Jade Assistant, where you can buy apps from the Jade Store,
and where you can manage your Jade Account.
'''

# ----------
# Imports
# ----------

# Python Standard Library Imports
import string
import subprocess
import sys
import datetime
from time import sleep
import random
from pathlib import PurePath, Path
import os
import platform
import webbrowser
import threading



# Third Party Imports
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import *
import requests
import pwnedpasswords


# Local Imports
import assets

# ----------
# Set up variables
# ----------

Version_MAJOR = 0
Version_MINOR = 0
Version_PATCH = 7
SignedIn = False
expanded = "0"
developmental = False

downloadJadeAssistantVar = False
updateJadeAssistantVar = False
guiLoopList = []
killThreads = False


# ----------
# Set up the resource manager
# ----------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ----------
# Classes
# ----------
class Account:
    '''A class to contain the user's account data.'''

    
    def __init__(self, plus, suspended, username):
        self.plus = plus
        self.suspended = suspended
        self.username = username

    def writeAccountFile(self, usernameIN, passwordIN):
        '''Code for writing account file so we can remember you'''

        print("Writing account file...")
        accountFile = open("account.txt", "w")
        accountFile.write(usernameIN + "\n" + passwordIN)
        accountFile.close()
        print("Done writing account file.")

    def Authenticate(self):
        '''Code for authentication at startup'''

        global SignedIn
        print("MAINFuncs/readAccountFile: Reading account file...")
        try:
            try:
                accountFile = open("account.txt", "r")
            
            except FileNotFoundError:
                accountFile = open("account.txt", "w")
                accountFile.close()
                accountFile = open("account.txt", "r")

            accountFileLines = accountFile.readlines()
            accountFile.close()
            if len(accountFileLines) == 0:
                print("MAINFuncs/readAccountFile: Account file is empty!")
                SignedIn = False

            elif len(accountFileLines) == 2:
                print("MAINFuncs/readAccountFile: Account file has data! Will try to sign in.")

            else:
                print("MAINFuncs/readAccountFile: There's a problem with the account file.")

        except Exception as e:
            print(f"MAINFuncs/readAccountFile: There was a problem signing you in. {e}")
            UTILITYFuncs.error(f"There was a problem signing you in. {e}")

        try:
            USERNAME = accountFileLines[0]
            PASSWORD = accountFileLines[1]
            print(f"Authenticating with username: {USERNAME} and password: {PASSWORD}")
            try:
                authenticateRequest = requests.get(f"https://nfoert.pythonanywhere.com/jade/get?user={USERNAME},password={PASSWORD}&")
                authenticateRequest.raise_for_status()
            
            except:
                print("PROBLEM")

            if "user=" in authenticateRequest.text:

                try:
                    art = authenticateRequest.text
                    print(art)
                    art_email = UTILITYFuncs.substring(art, ",email=", ",name")
                    art_name = UTILITYFuncs.substring(art, ",name=", ",plus")
                    art_plus = UTILITYFuncs.substring(art, "plus=", ",suspended")
                    art_suspended = UTILITYFuncs.substring(art, "suspended=", "&")

                    if art_suspended == "no":
                        print("Your account isn't suspended!")

                    else:
                        print(f"Your account is suspended for {art_suspended}")
                        dialog_accountSuspended.MAINLABEL.setText(art_suspended)
                        dialog_accountSuspended.MAINLABEL.setFont(QFont("Calibri", 10))
                        
                    


                    SignedIn = True
                    print(f"ALL SIGNED IN: email={art_email},name={art_name},jadeAssistant={art_plus}")
                    window_accountDetails.usernameBox_username.setText(USERNAME)
                    window_accountDetails.usernameBox_username.setFont(QFont("Calibri", 12))

                    window_accountDetails.nameBox_name.setText(art_name)
                    window_accountDetails.nameBox_name.setFont(QFont("Calibri", 12))

                    window_accountDetails.emailBox_email.setText(art_email)
                    window_accountDetails.emailBox_email.setFont(QFont("Calibri", 12))

                    window_main.leftBox_accountLabel.setText(f"Hello, {USERNAME}")
                    window_main.leftBox_accountLabel.setFont(QFont("Calibri Bold", 9))
                    window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
                    window_main.leftBox_accountLabel.setStyleSheet("color: green")

                    self.username = USERNAME
                    self.password = PASSWORD
                    self.email = art_email
                    self.name = art_name
                    self.plus = art_plus
                    self.suspended = art_suspended
                    plus = art_plus
                    suspended = art_suspended

                    return True

                except Exception as e:
                    print(f"There was a problem doing a bunch of essential stuff when Authenticating. {e}")
                    UTILITYFuncs.log("FATAL", f"There was a problem doing a bunch of essential stuff when Authenticating. {e}")
                    UTILITYFuncs.error(f"There was a problem doing a bunch of essential stuff when Authenticating. {e}")

                

            elif "not" in authenticateRequest.text:
                print("Failed to sign in. Incorrect credentials.")
                dialog_signInFailure.show()
                SignedIn = False
                return False

        except:
            print("Account file has no content! Cancel everything!")
            SignedIn = False

        

   

    def signIn(self):
        '''Code for signing in'''

        global SignedIn
        usernameInput = window_signIn.usernameBox_edit.text()
        passwordInput = window_signIn.passwordBox_edit.text()
        
        try:
            signInRequest = requests.get(f"https://nfoert.pythonanywhere.com/jade/get?user={usernameInput},password={passwordInput}&")
            signInRequest.raise_for_status()
            
            if "user=" in signInRequest.text:
                print("All signed in!")
                SignedIn = True
                self.writeAccountFile(usernameInput, passwordInput)
            
                sir = signInRequest.text
                sir_email = UTILITYFuncs.substring(sir, ",email=", ",name")
                sir_name = UTILITYFuncs.substring(sir, ",name=", ",plus")
                sir_plus = UTILITYFuncs.substring(sir, "plus=", ",suspended")
                sir_suspended = UTILITYFuncs.substring(sir, ",suspended=", "&")

                window_accountDetails.usernameBox_username.setText(usernameInput)
                window_accountDetails.usernameBox_username.setFont(QFont("Calibri", 12))

                window_accountDetails.nameBox_name.setText(sir_name)
                window_accountDetails.nameBox_name.setFont(QFont("Calibri", 12))

                window_accountDetails.emailBox_email.setText(sir_email)
                window_accountDetails.emailBox_email.setFont(QFont("Calibri", 12))

                window_main.leftBox_accountLabel.setText(f"Hello, {usernameInput}")
                window_main.leftBox_accountLabel.setFont(QFont("Calibri Bold", 9))
                window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
                window_main.leftBox_accountLabel.setStyleSheet("color: green")

                if sir_suspended == "no":
                    window_signIn.hide()
                    window_accountDetails.show()

                else:
                    window_signIn.hide()
                    window_main.hide()
                    dialog_accountSuspended.MAINLABEL.setText(sir_suspended)
                    dialog_accountSuspended.MAINLABEL.setFont(QFont("Calibri", 10))
                    dialog_accountSuspended.show()

            else:
                print(f"There was a problem signing you in: incorrect credentials. |{usernameInput}|, |{passwordInput}|, |{signInRequest.text}|")
                SignedIn = False
                dialog_signInFailure.show()
        
        except Exception as e:
            print(f"There was a problem signing you in. {e}")
            UTILITYFuncs.log("WARN", "There was a problem signing you in. {e}")
            

        
    def signOut(self):
        '''Code for signing out'''

        global SignedIn
        SignedIn = False
        self.writeAccountFile("","")
        
        window_signIn.usernameBox_edit.clear()
        window_signIn.passwordBox_edit.clear()

        window_main.leftBox_accountLabel.setText(f"Not signed in.")
        window_main.leftBox_accountLabel.setFont(QFont("Calibri", 8))
        window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
        window_main.leftBox_accountLabel.setStyleSheet("color: red")

        window_accountDetails.hide()
        window_signIn.show()

    def createAccount(self):
        '''Code for creating an account'''

        usernameInput = window_createAccount.usernameBox_edit.text()
        passwordInput = window_createAccount.passwordBox_edit.text()
        emailInput = window_createAccount.emailBox_edit.text()
        nameInput = window_createAccount.nameBox_edit.text()

        gc = UTILITYFuncs.getConnection("Account/createAccount")
        if gc == True:
            if len(passwordInput) >= 8:
                
                try:
                    passwordCheck = pwnedpasswords.check(passwordInput)

                except:
                    passwordCheck = 0
                
                if passwordCheck == 0:
                    
                    try:
                        createAccountRequest = requests.get(f"https://nfoert.pythonanywhere.com/jade/create?user={usernameInput},password={passwordInput},email={emailInput},name={nameInput}&")
                        createAccountRequest.raise_for_status()

                        if createAccountRequest.text == "Account sucsessfully created.":
                            print("Account sucsessfully created.")

                            window_createAccount.MESSAGE.setText("Account successfully created. Now authenticating.")
                            window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                            window_createAccount.MESSAGE.setStyleSheet("color: green")
                            window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

                            self.writeAccountFile(usernameInput, passwordInput)
                            self.Authenticate()

                            window_createAccount.hide()
                            window_accountDetails.show()

                        elif createAccountRequest.text == "That account already exists.":
                            print("That account already exists!")
                            window_createAccount.MESSAGE.setText("That account already exists!")
                            window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                            window_createAccount.MESSAGE.setStyleSheet("color: red")
                            window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

                        else:
                            print("There was a problem.")
                            window_createAccount.MESSAGE.setText("There was a problem.")
                            window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                            window_createAccount.MESSAGE.setStyleSheet("color: red")
                            window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

                    except Exception as e:
                        print(f"There was a problem creating an account. {e} @ {e.__traceback__.tb_lineno}")
                        UTILITYFuncs.log("WARN", f"There was a problem creating an account. {e}")
                        window_createAccount.MESSAGE.setText("There was a problem creating an account.t")
                        window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                        window_createAccount.MESSAGE.setStyleSheet("color: red")
                        window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

            

                elif passwordCheck >= 1:
                    print("Password is not safe!")
                    window_createAccount.MESSAGE.setText(f"Password has been leaked {passwordCheck} times! Please select a new password.")
                    window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                    window_createAccount.MESSAGE.setStyleSheet("color: red")
                    window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

                else:
                    print("There was a problem checking password safety.")
                    window_createAccount.MESSAGE.setText(f"There was a problem checking password safety.")
                    window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                    window_createAccount.MESSAGE.setStyleSheet("color: red")
                    window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)
            else:
                print("Please select a password with more than 8 characters.")
                window_createAccount.MESSAGE.setText("Please select a password with more than 8 characters.")
                window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
                window_createAccount.MESSAGE.setStyleSheet("color: red")
                window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

        elif gc == False:
            window_createAccount.MESSAGE.setText(f"You're not connected!")
            window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
            window_createAccount.MESSAGE.setStyleSheet("color: red")
            window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)

        else:
            window_createAccount.MESSAGE.setText(f"There was a problem getting connection.")
            window_createAccount.MESSAGE.setFont(QFont("Calibri", 8))
            window_createAccount.MESSAGE.setStyleSheet("color: red")
            window_createAccount.MESSAGE.setAlignment(QtCore.Qt.AlignCenter)
        
class News:
    def __init__(self, header, date, text, url, number):
        self.header = header
        self.date = date
        self.text = text
        self.url = url
        self.number = number

    def expand(self):
        print(f"Expanding news {self.number}")
        window_expandedNews.header.setText(self.header)
        window_expandedNews.header.setFont(QFont("Calibri", 16))
        window_expandedNews.header.setAlignment(QtCore.Qt.AlignCenter)

        window_expandedNews.body.setText(self.text)
        window_expandedNews.body.setFont(QFont("Calibri", 11))

        window_expandedNews.date.setText(self.date)
        window_expandedNews.date.setFont(QFont("Calibri Italic", 8))
        window_expandedNews.date.setAlignment(QtCore.Qt.AlignCenter)

        window_expandedNews.number.setText(f"[ {self.number} ]")
        window_expandedNews.number.setFont(QFont("Calibri Bold", 12))
        window_expandedNews.number.setAlignment(QtCore.Qt.AlignCenter)

        window_expandedNews.url.setText(self.url)
        window_expandedNews.url.setFont(QFont("Calibri", 8))
        window_expandedNews.url.setAlignment(QtCore.Qt.AlignCenter)

        # Check for 'none' url
        if self.url == "none":
            window_expandedNews.url.hide()
            window_expandedNews.openUrl.hide()
            window_expandedNews.show()

        else:
            WEBVIEW.openWebView(self.url)

        
        
        print("Done expanding.")

    def openUrl(self):
        print("Attempting to open url:")
        WEBVIEW.openWebView(self.url)


class LauncherId:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def getId(self):
        print("Getting Launcher Id...")
        gc = UTILITYFuncs.getConnection("LauncherId/getId")
        if gc == True:
            try:
                IdFile = open("id.txt", "r")
                readfile = IdFile.read()
                IdFile.close()
                self.id = readfile
                return readfile
            
            except OSError:
                print("This launcher does not have an id. Creating one...")
                IdFile = open("id.txt", "w")
                letters = string.ascii_lowercase
                randomId = ""
                randomIdFound = False
                
                while randomIdFound == False:
                    for i in range(10):
                        choose = random.choice(letters)
                        randomId = randomId + choose

                    print(f"Random string is {randomId} Checking...")

                    try:
                        randomIdCheck = requests.get(f"https://nfoert.pythonanywhere.com/jade/checkForExistingLauncherId?{randomId}&")

                    except Exception as e:
                        print("There was a problem checking the id.")
                        UTILITYFuncs.error(f"When checking if the newly randomized Id for this launcher is valid, there was a problem. {e}")

                    if randomIdCheck.text == "SAFE TO USE":
                        IdFile.write(randomId)
                        print("Id checked and ready to go.")
                        self.id = randomId
                        randomIdFound = True
                        return randomId

                    else:
                        print("There was a problem checking the Id. Maybe it already existed?")
                        randomIdFound == False
                        continue
                        return False

        elif gc == False:
            print("You're not connected!")

    def updateStatus(self):
        print("Updating launcher status.")
        gc = UTILITYFuncs.getConnection("LauncherId/updateStatus")
        if gc == True:
            version = f"{Version_MAJOR}.{Version_MINOR}.{Version_PATCH}"
            if SignedIn == True:
                USERNAMEINPUT = self.username

            elif SignedIn == False:
                USERNAMEINPUT = "notSignedIn"

            else:
                print("There was a problem determining signed in status.")
                USERNAMEINPUT = "notSignedIn"
            
            try:
                updateStatusRequest = requests.get(f"https://nfoert.pythonanywhere.com/jade/updateLauncherId?id={self.id},username={USERNAMEINPUT},version={version}&")

            except:
                print("There was a problem getting the update status request.")

            if updateStatusRequest.text == "DONE":
                print("Done.")

            else:
                print("There was a problem updating Launcher Id.")
                

        elif gc == False:
            print("You're not conected!")

        else:
            print("Couldn't determine if you're connected or not.")
            UTILITYFuncs.error("Couldn't determine if you're connected or not when updating Launcher status.")
            UTILITYFuncs.log("WARN", "Couldn't detmine if you're connected or not when updating Launcher status.")


class WebView:
    '''A group of functions for the window_webView'''
    def __init__(self):
        pass

    def reload():
        window_webView.web.reload()

    def back():
        window_webView.web.back()

    def forward():
        window_webView.web.forward()
    
    def startLoading():
        window_webView.statusbar.showMessage("Loading page...")

    def doneLoading():
        try:
            window_webView.statusbar.clearMessage()
            window_webView.title.setText(str(window_webView.web.title()))
            window_webView.title.setAlignment(QtCore.Qt.AlignLeft)
            window_webView.title.setFont(QFont("Calibri", 16))

            url = window_webView.web.url().toString()
            window_webView.url.setText(url)
            window_webView.title.setAlignment(QtCore.Qt.AlignLeft)
            window_webView.title.setFont(QFont("Calibri", 8))

        except Exception as e:
            UTILITYFuncs.error(f"There was a problem done loading! {e}")
    
    def openWebView(urlInput):
        gc = UTILITYFuncs.getConnection("WebView/openWebView")
        if gc == True:
            if platform.system() == "Windows":
                window_webView.web.setUrl(QUrl(urlInput))
                window_webView.show()

            elif platform.system() == "Darwin":
                print("You're on mac! Will just open in default webbrowser instead.")
                webbrowser.open(str(urlInput))

        elif gc == False:
            print("You're offline!")

        else:
            print("There was a problem getting connection status.")

# ----------
# Functions
# ----------
'''
Note: I understand this is maybe not the best way to group functions,
but I feel this will help my code workflow. The old Jade Launcher
had a mess of functions, so I hope this will help
with organization.
'''
class UTILITYFuncs:
    '''A Group of functions for various utility purposes.'''
    
    def __init__(self):
        pass

    def log(tag, text):
        now = datetime.datetime.now()
        try:
            logFile = open("JadeLauncherLog.txt", "a")
            logFile.write(f"\n[{now.month}/{now.day}/{now.year}] [{now.hour}:{now.minute}:{now.second}] |{tag}| >>> {text}")
        
        except Exception as e:
            print(f"There was a problem logging messgages to the log file! {e}")
            sys.exit()
        
        logFile.close()

    def getConnection(fromWhat):
        print(f"UTILITYFuncs/getConnection: Getting Connection Status from: {fromWhat}")
        try:
            gcRequest = requests.get("https://google.com")
            
            try:
                gcRequest.raise_for_status()

            except:
                print(f"UTILITYFuncs:/getConnection: You're not connected! From: {fromWhat}")
                UTILITYFuncs.log("GetConnection", f"You're not connected! From: {fromWhat}")
                window_offline.show()
                return(False)

        except:
            print(f"UTILITYFuncs:/getConnection: You're not connected! From: {fromWhat}")
            UTILITYFuncs.log("GetConnection", f"You're not connected! From: {fromWhat}")
            window_offline.show()
            return(False)

        
        print("UTILITYFuncs:/getConnection: You're connected!")
        UTILITYFuncs.log("GetConnection", f"You're connected! From: {fromWhat}")
        return(True)

    def substring(inputString, one, two):
        try:
            start = inputString.find(one) + len(one)

            try:
                end = inputString.find(two)
                
                try:
                    result = inputString[start:end]
        
                    if len(inputString) >= 100:
                        print("Input string output will be converted to a shortened version.")
                        inputString = inputString[:100] + "..."

                    else:
                        print("Input string does not need to be shortened.")
                
                    UTILITYFuncs.log("INFO", f"Just substringed '{inputString}' with result '{inputString}'")
                    return result

                except:
                    print(f"UTILITYFuncs/substring: There was a problem finishing substringing with input '{inputString}'")
                    UTILITYFuncs.log("WARN", f"There was a problem finishing substringing with input '{inputString}'")
                    raise Exception("Could not finish substringing.")

            except:
                print(f"UTILITYFuncs/substring: Unable to find the second string with input '{inputString}'")
                UTILITYFuncs.log("WARN", f"Unable to find the second string with input '{inputString}'")
                raise Exception("Could not find the second string.")
        
        except:
            print(f"UTILITYFuncs/substring: Unable to find the first string with input '{inputString}'")
            UTILITYFuncs.log("WARN", f"Unable to find the first string with input '{inputString}'")
            raise Exception("Could not find the first string.")

    def error(Error):
        window_main.hide()
        window_jadeAssistantMenu.hide()
        dialog_error.ERROR.setText(Error)
        dialog_error.ERROR.setFont(QFont("Calibri", 14))
        dialog_error.show()
        print("-----")
        print("[ A Fatal Exception Occured ]")
        print("-----")
        print(Error)
        print("-----")
        UTILITYFuncs.log("FATAL", f"A fatal exception occured: {Error}")

        app.exec()
        dialog_error.show()




class MAINFuncs:
    '''A Group of functions integral to the Launcher.'''
    global SignedIn
    global myAccount
    
    def __init__(self):
        pass

    def mainCode():
        '''The most important code of the Jade Launcher. Will check for updates, sign you in, and fetch news.'''
        
        global Version_MAJOR
        global Version_MINOR
        global Version_PATCH

        global myAccount

        global news1
        global news2
        global news3

        global Launcher

        CONFIG_CheckForUpdates = True
        CONFIG_Authenticate = True
        CONFIG_FetchNews = True


        print("MAINFuncs/mainCode: Main code thread started!")
        # Thanks to Liam on StackOverflow
        # https://stackoverflow.com/questions/58661539/create-splash-screen-in-pyqt5
        splash_pix = QtGui.QPixmap(str(resource_path("JadeLauncherSplash.png")))
        window_splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        # add fade to splashscreen 
        opaqueness = 0.0
        step = 0.01
        window_splash.setWindowOpacity(opaqueness)
        window_splash.show()
        while opaqueness < 1:
            window_splash.setWindowOpacity(opaqueness)
            sleep(step) # Gradually appears
            opaqueness+=step


        # Check for updates
        print("MAINFuncs/mainCode/checkForUpdates: Checking for updates...")
        

        if CONFIG_CheckForUpdates == True:
            gc = UTILITYFuncs.getConnection("mainCode/Check For Updates")
            if gc == True:
                try:
                    versionRequest = requests.get("https://nfoert.pythonanywhere.com/jade/jadeLauncherVersion")
                    versionRequest.raise_for_status()

                except Exception as e:
                    print(f"MAINFuncs/mainCode/checkForUpdates: There was a problem checking for updates. {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem checking for updates. {e}")

                vrt = versionRequest.text
                requestMajor = UTILITYFuncs.substring(vrt, "major=", ",minor")
                requestMinor = UTILITYFuncs.substring(vrt, ",minor=", ",patch")
                requestPatch = UTILITYFuncs.substring(vrt, "patch=", "&")

                if versionRequest.ok == True:
                    print("Version requests are ok!")

                    requestMajor = int(requestMajor)
                    requestMinor = int(requestMinor)
                    requestPatch = int(requestPatch)

                    if Version_MAJOR < requestMajor:
                        print("Updates are required.")
                        update = "yes"

                    elif Version_MINOR < requestMinor:
                        print("Updates are required.")
                        update = "yes"

                    elif Version_PATCH < requestPatch:
                        print("Updates are required.")
                        update = "yes"

                    else:
                        print("Updates not required.")
                        update = "no"

                else:
                    print("Version requests are not ok!")
                    update = "no"
                    window_splash.hide()
                    UTILITYFuncs.error("It looks like my web server is down. Wait a bit and see if it fixes, otherwise please send me an email and I'll take a look at it. You could also check PythonAnywhere's twitter page to see if it's down. (That's who hosts the web server for me.)")
                    return(False)
                
                if update == "yes":
                    print("Now updating... First going to remove the updater - if it exists")
                    try:
                        if platform.system() == "Windows":
                            os.remove("Jade Launcher Updater.exe")

                        elif platform.system() == "Darwin":
                            os.remove("Jade Launcher Updater")

                        else:
                            print("Your OS isn't supported.")
                            UTILITYFuncs.error("Hey there! Your OS isn't supported. Please install the Launcher for Windows or Mac from my website, 'https://nofoert.wixsite.com/jade/download'")

                    except OSError as e:
                        print(f"The updater dosen't seem to exist. {e}")

                    except Exception as e:
                        print("There was a problem removing the Updater.")
                        UTILITYFuncs.log("WARN", f"There was a problem removing the Updater: {e}")
                        
                        

                    print("Now going to download and run the installer.")
                    try:
                        if platform.system() == "Windows":
                            print("Going to update for windows.")
                            try:
                                jadeLauncherUpdaterRequest = requests.get("https://raw.githubusercontent.com/nfoert/jadelauncher/main/Jade%20Launcher%20Updater.exe")
                                jadeLauncherUpdaterRequest.raise_for_status()
                                print("Saving...")
                                jadeLauncherUpdater = open("jadeLauncherUpdater.exe", "wb")
                                for chunk in jadeLauncherUpdaterRequest.iter_content(100000):
                                    jadeLauncherUpdater.write(chunk)

                                jadeLauncherUpdater.close()

                                print("Done. Now opening.")
                                try:
                                    subprocess.Popen("jadeLauncherUpdater.exe")
                                    sys.exit()

                                except Exception as e:
                                    print(f"There was a problem starting the updater. {e}")
                                    UTILITYFuncs.log("WARN", f"There was a problem starting the updater: {e}")
                                    UTILITYFuncs.error(f"There was a problem starting the updater. This may be nothing. Please restart. {e}")


                            except Exception as e:
                                print(f"There was a problem installing the updater for windows. {e}")
                                UTILITYFuncs.log("WARN", f"There was a problem installing the updater for windows. {e}")

                        elif platform.system() == "Darwin":
                            print("Going to update for Mac.")
                            try:
                                jadeLauncherUpdaterRequest = requests.get("https://raw.githubusercontent.com/nfoert/jadelauncher/main/jadeLauncherUpdater")
                                jadeLauncherUpdaterRequest.raise_for_status()
                                print("Saving...")
                                jadeLauncherUpdater = open("jadeLauncherUpdater", "wb")
                                for chunk in jadeLauncherUpdaterRequest.iter_content(100000):
                                    jadeLauncherUpdater.write(chunk)

                                print("Done. Now opening.")
                                try:
                                    subprocess.Popen("jadeLauncherUpdater")
                                    sys.exit()

                                except Exception as e:
                                    print("There was a problem starting the updater.")
                                    UTILITYFuncs.log("WARN", f"There was a problem starting the updater: {e}")
                                    UTILITYFuncs.error(f"There was a problem starting the updater. This may be nothing. Please restart. {e}")

                            except Exception as e:
                                print(f"There was a problem installing the updater for windows. {e}")
                                UTILITYFuncs.log("WARN", f"There was a problem installing the updater for windows. {e}")

                        else:
                            print("Your OS is not supported.")

                    except Exception as e:
                        print(f"There was a problem when updating. {e}")
                        UTILITYFuncs.log("WARN", f"There was a problem when updating: {e}")
                        UTILITYFuncs.error(f"There was a problem when updating. {e}")


                
                elif update == "no":
                    print("Not updating. Going to try to remove the updater - just in case it exists.")
                    try:
                        if platform.system() == "Windows":
                            os.remove("jadeLauncherUpdater.exe")

                        elif platform.system() == "Darwin":
                            os.remove("jadeLauncherUpdater")

                        else:
                            print("Your OS isn't supported.")

                    except OSError as e:
                        print(f"The updater dosen't seem to exist. {e}")

                    except Exception as e:
                        print("There was a problem removing the Updater.")
                        UTILITYFuncs.log("WARN", f"There was a problem removing the Updater: {e}")
                        UTILITYFuncs.error("There was a problem removing the updater. This will cause problems when updating in the future. Please restart.")


                else:
                    print("Not updating. Couldn't figure out if we're supposed to or not, so let's say no.")
                    UTILITYFuncs.log("WARN", "Couldn't tell if we should have updated or not.")


            elif gc == False:
                print("MAINFuncs/mainCode/checkForUpdates: You're not connected! Skipping checking for updates.")
                window_main.show()
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()

        elif CONFIG_CheckForUpdates == False:
            print("MAINFuncs/mainCode/checkForUpdates: Skipping checking for updates, as it's turned off.")

        else:
            print(f"MAINFuncs/mainCode/checkForUpdates: Skipping checking for updates, as we can't tell if it's turned off or on. '{CONFIG_CheckForUpdates}'")


        # Sign in
        print("MAINFuncs/mainCode/authenticate: Signing in...")

        if CONFIG_Authenticate == True:
            gc = UTILITYFuncs.getConnection("mainCode/Authenticate")
            if gc == True:
                print("MAINFuncs/mainCode/authenticate: Signing in.")
                myAccount.Authenticate()

            elif gc == False:
                print("MAINFuncs/mainCode/authenticate: Skipping signing in as you're not connected.")
                window_main.show()
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()

            else:
                print("MAINFuncs/mainCode/authenticate: Skipping signing in as we can't tell if you're connected or not.")

        elif CONFIG_Authenticate == False:
            print("MAINFuncs/mainCode/authenticate: Skipping signing in as it's turned off.")

        else:
            print(f"MAINFuncs/mainCode/authenticate: Skipping signing in as we can't tell if it's turned off or on. '{CONFIG_Authenticate}'")

        
        # Fetch news
        print("THREADFuncs/mainCode/fetchNews: Fetching news...")
        
        if CONFIG_FetchNews == True:
            gc = UTILITYFuncs.getConnection("mainCode/fetchNews")
            if gc == True:
                print("THREADFuncs/mainCode/fetchNews: Fetching news...")
                UTILITYFuncs.log("INFO", "Fetching news...")
                try:
                    newsCodeRequest = requests.get("https://nfoert.pythonanywhere.com/jade/returnNews")
                    newsCodeRequest.raise_for_status

                except Exception as e:
                    print(f"THREADFuncs/mainCode/fetchNews: There was a problem fetching news. AT: Get news codes {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem fetching news. AT: Get news codes. {e}")
                    window_main.newsBox1.hide()
                    window_main.newsBox2.hide()
                    window_main.newsBox3.hide()

                ncrText = newsCodeRequest.text
                try:
                    newsCode1 = UTILITYFuncs.substring(ncrText, "1=", ",2=")
                    newsCode2 = UTILITYFuncs.substring(ncrText, "2=", ",3=")
                    newsCode3 = UTILITYFuncs.substring(ncrText, "3=", "&")

                except Exception as e:
                    print(f"THREADFuncs/mainCode/fetchNews: There was a problem substringing the codes out of the news code request. {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem substringing the codes out of the news code request. {e}")
                    window_main.newsBox1.hide()
                    window_main.newsBox2.hide()
                    window_main.newsBox3.hide()

                try:
                    print("THREADFuncs/mainCode/fetchNews: Getting news requests...")
                    newsRequest1 = requests.get(f"https://nfoert.pythonanywhere.com/jade/news?{newsCode1}&")
                    newsRequest2 = requests.get(f"https://nfoert.pythonanywhere.com/jade/news?{newsCode2}&")
                    newsRequest3 = requests.get(f"https://nfoert.pythonanywhere.com/jade/news?{newsCode3}&")
                    print("THREADFuncs/mainCode/fetchNews: Done.")

                except Exception as e:
                    print(f"THREADFuncs/mainCode/fetchNews: There was a problem getting the news requests. {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem getting the news requests. {e}")
                    window_main.newsBox1.hide()
                    window_main.newsBox2.hide()
                    window_main.newsBox3.hide()

                if newsRequest1.ok == True:
                    pass
                else:
                    print("THREADFuncs/mainCode/fetchNews: NEWS 1 FAIL")
                    window_main.newsBox1.hide()

                if newsRequest2.ok == True:
                    pass
                else:
                    print("THREADFuncs/mainCode/fetchNews: NEWS 2 FAIL")
                    window_main.newsBox2.hide()

                if newsRequest3.ok == True:
                    pass
                else:
                    print("THREADFuncs/mainCode/fetchNews: NEWS 3 FAIL")
                    window_main.newsBox3.hide()
                    
                
                # News 1
                nr1Text = newsRequest1.text
                if "header=" in nr1Text:
                    print("THREADFuncs/mainCode/fetchNews: News 1 is good!")
                    news1Header = UTILITYFuncs.substring(nr1Text, "header=", ",text")
                    news1Text = UTILITYFuncs.substring(nr1Text, ",text=", ",date")
                    news1Date = UTILITYFuncs.substring(nr1Text, ",date=", ",url")
                    news1Url = UTILITYFuncs.substring(nr1Text, ",url=", "&")

                    window_main.header1.setText(f"{news1Header[:15]}...")
                    window_main.header1.setFont(QFont('Calibri Bold', 12))
                    window_main.header1.setAlignment(QtCore.Qt.AlignCenter)

                    try:
                        window_main.text1.setText(f"{news1Text[:150]}...")
                    except:
                        window_main.text1.setText(news3Text)

                    window_main.text1.setFont(QFont("Calibri", 10))

                    window_main.date1.setText(news1Date)
                    window_main.date1.setFont(QFont("Calibri Italic", 8))
                    window_main.date1.setAlignment(QtCore.Qt.AlignCenter)


                elif "There is no news article that matches that code." in nr1Text:
                    print(f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 1. Code is '{newsCode1}'")
                    window_main.newsBox1.hide()

                else:
                    print("THREADFuncs/mainCode/fetchNews: There was a problem validating the first news request.")
                    window_main.newsBox1.hide()

                # News 2
                nr2Text = newsRequest2.text
                if "header=" in nr2Text:
                    print("THREADFuncs/mainCode/fetchNews: News 2 is good!")
                    news2Header = UTILITYFuncs.substring(nr2Text, "header=", ",text")
                    news2Text = UTILITYFuncs.substring(nr2Text, ",text=", ",date")
                    news2Date = UTILITYFuncs.substring(nr2Text, ",date=", ",url")
                    news2Url = UTILITYFuncs.substring(nr2Text, "url=", "&")

                    window_main.header2.setText(f"{news2Header[:15]}...")
                    window_main.header2.setFont(QFont('Calibri Bold', 12))
                    window_main.header2.setAlignment(QtCore.Qt.AlignCenter)
                    
                    try:
                        window_main.text2.setText(f"{news2Text[:150]}...")
                    except:
                        window_main.text2.setText(news2Text)

                    window_main.text2.setFont(QFont("Calibri", 10))

                    window_main.date2.setText(news2Date)
                    window_main.date2.setFont(QFont("Calibri Italic", 8))
                    window_main.date2.setAlignment(QtCore.Qt.AlignCenter)

                elif "There is no news article that matches that code." in nr2Text:
                    print(f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 2. Code is '{newsCode2}'")
                    window_main.newsBox2.hide()

                else:
                    print("THREADFuncs/mainCode/fetchNews: There was a problem validating the second news request.")
                    window_main.newsBox2.hide()

                # News 3
                nr3Text = newsRequest3.text
                if "header=" in nr3Text:
                    print("THREADFuncs/mainCode/fetchNews: News 3 is good!")
                    news3Header = UTILITYFuncs.substring(nr3Text, "header=", ",text")
                    news3Text = UTILITYFuncs.substring(nr3Text, ",text=", ",date")
                    news3Date = UTILITYFuncs.substring(nr3Text, ",date=", ",url")
                    news3Url = UTILITYFuncs.substring(nr3Text, ",url=", "&")

                    window_main.header3.setText(f"{news3Header[:15]}...")
                    window_main.header3.setFont(QFont('Calibri Bold', 12))
                    window_main.header3.setAlignment(QtCore.Qt.AlignCenter)

                    try:
                        window_main.text3.setText(f"{news3Text[:150]}...")
                    except:
                        window_main.text3.setText(news3Text)

                    window_main.text3.setFont(QFont("Calibri", 10))

                    window_main.date3.setText(news3Date)
                    window_main.date3.setFont(QFont("Calibri Italic", 8))
                    window_main.date3.setAlignment(QtCore.Qt.AlignCenter)


                

                elif "There is no news article that matches that code." in nr3Text:
                    print(f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 3. Code is '{newsCode3}'")
                    window_main.newsBox3.hide()

                else:
                    print("THREADFuncs/mainCode/fetchNews: There was a problem validating the third news request.")
                    window_main.newsBox3.hide()


                # Check for emptiness deep inside themselves
                if newsCode1 == "000":
                    print("THREADFuncs/mainCode/fetchNews: Hiding news 1 as the code is 000.")
                    window_main.newsBox1.hide()

                else:
                    pass

                if newsCode2 == "000":
                    print("THREADFuncs/mainCode/fetchNews: Hiding news 2 as the code is 000.")
                    window_main.newsBox2.hide()

                else:
                    pass

                if newsCode3 == "000":
                    print("THREADFuncs/mainCode/fetchNews: Hiding news 3 as the code is 000.")
                    window_main.newsBox3.hide()

                else:
                    pass


                # Set news classes
                try:
                    news1.header = news1Header
                    news1.text = news1Text
                    news1.date = news1Date
                    news1.url = news1Url
                except Exception as e:
                    print(f"There was a problem setting up news1 Class. {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem setting up news 1 class. {e}")
                    window_main.newsBox1.hide()
                
                try:
                    news2.header = news2Header
                    news2.text = news2Text
                    news2.date = news2Date
                    news2.url = news2Url
                
                except Exception as e:
                    print(f"There was a problem setting up news2 Class. {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem setting up news 2 class. {e}")
                    window_main.newsBox2.hide()

                try:
                    news3.header = news3Header
                    news3.text = news3Text
                    news3.date = news3Date
                    news3.url = news3Url

                except Exception as e:
                    print(f"There was a problem setting up news3 Class. {e}")
                    UTILITYFuncs.log("WARN", f"There was a problem setting up news 3 class. {e}")
                    window_main.newsBox3.hide()


            elif gc == False:
                print("THREADFuncs/mainCode/fetchNews: Skipping fetching of news as you're not conected.")
                UTILITYFuncs.log("INFO", "Skipping fetching of news as you're not connected.")
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()
                window_main.show()

            else:
                print("THREADFuncs/mainCode/fetchNews: Skipping fetching of news as we can't decide if you're connected or not.")
                UTILITYFuncs.log("INFO", "Skipping fetching of news as we can't decide if you're connected or not.")
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()


        elif CONFIG_FetchNews == False:
            print("THREADFuncs/mainCode/fetchNews: Skipping fetching of news as it's not allowed.")
            UTILITYFuncs.log("INFO", "Skipping fetching of news as it's not allowed.")
            window_main.newsBox1.hide()
            window_main.newsBox2.hide()
            window_main.newsBox3.hide()
        else:
            print("THREADFuncs/mainCode/fetchNews: Skipping news fetch as we can't determine if it's allowed or not.")
            UTILITYFuncs.log("INFO", "Skipping news fetch as we can't determine if it's allowed or not.")

        # Update Id
        getId = Launcher.getId()
        Launcher.username = myAccount.username
        Launcher.updateStatus()

        if myAccount.suspended == "no":
            print("Main code check: not suspended")
            window_main.show()


        else:
            print("Main code check: suspended.")
            window_splash.hide()
            dialog_accountSuspended.show()

        # Set greeting
        now = datetime.datetime.now().hour
        if now == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9 or 10 or 11:
            #Good morning
            window_main.welcomeBox_text.setText("Good morning.")

        elif now == 12 or 13 or 14 or 15 or 14 or 15:
            #Good afternoon
            window_main.welcomeBox_text.setText("Good afternoon.")

        elif now == 16 or 17 or 18 or 19 or 20 or 21 or 22 or 23:
            # Good evening
            window_main.welcomeBox_text.setText("Good evening.")

        else:
            # Welcome back
            window_main.welcomeBox_text.setText("Welcome back to the")

        window_main.welcomeBox_text.setFont(QFont("Calibri Bold", 16))
        window_main.welcomeBox_text.setAlignment(QtCore.Qt.AlignCenter)

        # Check if Jade Assistant exists, or needs an update.

        jadeAssistantWindows = Path("Jade Assistant.exe").exists()
        jadeAssistantMac = Path("Jade Assistant").exists()
        if jadeAssistantWindows == True or jadeAssistantMac == True:
            print("Jade Assistant exists!")
            # It exists! Now check for existance of version file
            jadeAssistantVersionFileExists = Path("jadeAssistantVersion.txt").exists()
            if jadeAssistantVersionFileExists == True:
                #It exists! Now check for updates
                jadeAssistantVersionFile = open("jadeAssistantVersion.txt", "r")
                jadeAssistantVersionFileContents = jadeAssistantVersionFile.readlines()
                jadeAssistantVersion_MAJOR = jadeAssistantVersionFileContents[0]
                jadeAssistantVersion_MINOR = jadeAssistantVersionFileContents[1]
                jadeAssistantVersion_PATCH = jadeAssistantVersionFileContents[2]

                try:
                    jadeAssistantVersionFromServer = requests.get("https://nfoert.pythonanywhere.com/jade/jadeAssistantVersion")
                    jadeAssistantVersionFromServer.raise_for_status()

                except:
                    print("There was a problem checking Jade Assistant for updates!")
                    window_jadeAssistantMenu.launchButton.show()
                    window_jadeAssistantMenu.updateButton.hide()
                    window_jadeAssistantMenu.downloadButton.hide()
                    window_jadeAssistantMenu.removeButton.show()

                javfsMAJOR = UTILITYFuncs.substring(jadeAssistantVersionFromServer.text, "major=", ",minor")
                javfsMINOR = UTILITYFuncs.substring(jadeAssistantVersionFromServer.text, "minor=", ",patch")
                javfsPATCH = UTILITYFuncs.substring(jadeAssistantVersionFromServer.text, "patch=", "&")

                

                if jadeAssistantVersion_MAJOR < javfsMAJOR:
                    # Updates required
                    window_jadeAssistantMenu.launchButton.hide()
                    window_jadeAssistantMenu.updateButton.show()
                    window_jadeAssistantMenu.downloadButton.hide()
                    window_jadeAssistantMenu.removeButton.show()
                    print(f"Updates required. {jadeAssistantVersion_MAJOR} < {javfsMAJOR}")
                    window_jadeAssistantMenu.version.setText(f"Update to version {javfsMAJOR}.{javfsMINOR}.{javfsPATCH}")

                elif jadeAssistantVersion_MINOR < javfsMINOR:
                    # Updates required
                    window_jadeAssistantMenu.launchButton.hide()
                    window_jadeAssistantMenu.updateButton.show()
                    window_jadeAssistantMenu.downloadButton.hide()
                    window_jadeAssistantMenu.removeButton.show()
                    print(f"Updates required. {jadeAssistantVersion_MINOR} < {javfsMINOR}")
                    window_jadeAssistantMenu.version.setText(f"Update to version {javfsMAJOR}.{javfsMINOR}.{javfsPATCH}")

                elif jadeAssistantVersion_PATCH < javfsPATCH:
                    # Updates required
                    window_jadeAssistantMenu.launchButton.hide()
                    window_jadeAssistantMenu.updateButton.show()
                    window_jadeAssistantMenu.downloadButton.hide()
                    window_jadeAssistantMenu.removeButton.show()
                    print(f"Updates required. {jadeAssistantVersion_PATCH} < {javfsPATCH}")
                    window_jadeAssistantMenu.version.setText(f"Update to version {javfsMAJOR}.{javfsMINOR}.{javfsPATCH}")

                else:
                    # Updates not required
                    window_jadeAssistantMenu.launchButton.show()
                    window_jadeAssistantMenu.updateButton.hide()
                    window_jadeAssistantMenu.downloadButton.hide()
                    window_jadeAssistantMenu.removeButton.show()
                    print("Updates not required.")
                    window_jadeAssistantMenu.version.setText(f"Version {javfsMAJOR}.{javfsMINOR}.{javfsPATCH}")
                        

        elif jadeAssistantWindows == False or jadeAssistantMac == False:
            # It dosen't exist! Show button for downloading.
            print("Jade Assistant dosen't exist!")
            window_jadeAssistantMenu.launchButton.hide()
            window_jadeAssistantMenu.updateButton.hide()
            window_jadeAssistantMenu.downloadButton.show()
            window_jadeAssistantMenu.removeButton.hide()
            window_jadeAssistantMenu.version.setText(f"Download version {javfsMAJOR}.{javfsMINOR}.{javfsPATCH}")

        else:
            #Unable to tell if it exists or not
            UTILITYFuncs.error("Unable to tell if Jade Assistant exists or not!")

        window_jadeAssistantMenu.version.setAlignment(QtCore.Qt.AlignCenter)

        print("=================================")
        print("THREADFuncs/mainCode/: Finished! ")
        print("=================================")
            

class THREADFuncs:
    def __init__(self):
        pass

    def downloadJadeAssistant():
        global downloadJadeAssistantVar
        global guiLoopList
        global killThreads
        while True:
            if downloadJadeAssistantVar == True:
                guiLoopList.append('window_jadeAssistantMenu.launchButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.downloadButton.show()')
                guiLoopList.append('window_jadeAssistantMenu.removeButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.downloadButton.setEnabled(False)')
                guiLoopList.append('window_jadeAssistantMenu.downloadButton.setText("Downloading...")')
                if platform.system() == "Windows":
                    try:
                        print("Downloading Jade Assistant!")
                        jadeAssistantDownload = requests.get("https://github.com/nfoert/jadeassistant/raw/main/Jade%20Assistant.exe")
                        jadeAssistantDownload.raise_for_status()
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.setText("Saving...")')
                        jadeAssistant = open("Jade Assistant.exe", "wb")
                        for chunk in jadeAssistantDownload.iter_content(100000):
                            jadeAssistant.write(chunk)

                        jadeAssistant.close()
                        downloadJadeAssistantVar = False
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')
                        print("Done downloading Jade Assistant!")

                    except Exception as e:
                        print(f"There was a problem downloading Jade Assistant! {e}")
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setEnabled(False)')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setText("There was a problem.")')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')

                elif platform.system() == "Darwin":
                    try:
                        jadeAssistantDownload = requests.get("https://github.com/nfoert/jadeassistant/raw/main/Jade%20Assistant")
                        jadeAssistantDownload.raise_for_status()
                        guiLoopList.append('window_main.updateButton.setText("Saving...")')
                        jadeAssistant = open("Jade Assistant", "wb")
                        for chunk in jadeAssistantDownload.iter_content(100000):
                            jadeAssistant.write(chunk)

                        jadeAssistant.close()
                        downloadJadeAssistantVar = False
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')

                    except Exception as e:
                        print(f"There was a problem downloading Jade Assistant! {e}")
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setEnabled(False)')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setText("There was a problem.")')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')

                else:
                    print("Your OS isn't supported!")
                    UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac or Windows.")

            elif killThreads == True:
                return False

            else:
                sleep(1)
                continue

    def updateJadeAssistant():
        global updateJadeAssistantVar
        global guiLoopList
        global killThreads
        while True:
            if updateJadeAssistantVar == True:
                print("Updating Jade Assistant...")
                guiLoopList.append('window_jadeAssistantMenu.launchButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.updateButton.show()')
                guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')
                guiLoopList.append('window_jadeAssistantMenu.updateButton.setEnabled(False)')
                guiLoopList.append('window_jadeAssistantMenu.updateButton.setText("Downloading...")')
                if platform.system() == "Windows":
                    try:
                        os.remove("Jade Assistant.exe")
                        jadeAssistantDownload = requests.get("https://github.com/nfoert/jadeassistant/raw/main/Jade%20Assistant.exe")
                        jadeAssistantDownload.raise_for_status()
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.setText("Saving...")')
                        jadeAssistant = open("Jade Assistant.exe", "wb")
                        for chunk in jadeAssistantDownload.iter_content(100000):
                            jadeAssistant.write(chunk)

                        jadeAssistant.close()
                        updateJadeAssistantVar = False
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')
                        print("Done updating Jade Assistant.")

                    except Exception as e:
                        print(f"There was a problem updating Jade Assistant! {e}")
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setEnabled(False)')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setText("There was a problem.")')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')

                elif platform.system() == "Darwin":
                    try:
                        os.remove("Jade Assistant")
                        jadeAssistantDownload = requests.get("https://github.com/nfoert/jadeassistant/raw/main/Jade%20Assistant")
                        jadeAssistantDownload.raise_for_status()
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.setText("Saving...")')
                        jadeAssistant = open("Jade Assistant", "wb")
                        for chunk in jadeAssistantDownload.iter_content(100000):
                            jadeAssistant.write(chunk)

                        jadeAssistant.close()
                        updateJadeAssistantVar = False
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')
                        print("Done updating Jade Assistant.")

                    except Exception as e:
                        print(f"There was a problem updating Jade Assistant! {e}")
                        guiLoopList.append('window_jadeAssistantMenu.launchButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.updateButton.show()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.hide()')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setEnabled(False)')
                        guiLoopList.append('window_jadeAssistantMenu.downloadButton.setText("There was a problem.")')
                        guiLoopList.append('window_jadeAssistantMenu.removeButton.show()')

                else:
                    print("Your OS isn't supported!")
                    UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac or Windows.")

            elif killThreads == True:
                return False

            else:
                sleep(1)
                continue

# -----
# Setup threads
# ----
downloadJadeAssistantThread = threading.Thread(target=THREADFuncs.downloadJadeAssistant)
updateJadeAssistantThread = threading.Thread(target=THREADFuncs.updateJadeAssistant)

downloadJadeAssistantThread.start()
updateJadeAssistantThread.start()
                    


class UIFuncs:
    '''A group of functions that the UI uses.'''
    global SignedIn
    
    def __init__(self):
        pass

    # Offline Screen
    def closeOffline():
        window_offline.hide()
        window_main.show()
        window_main.show()
        window_main.newsBox1.hide()
        window_main.newsBox2.hide()
        window_main.newsBox3.hide()
        window_main.offlineLabel.show()
        window_main.newsLabel.hide()
        window_main.line.hide()
        

    # Main Screen
    def openAccountScreen():
        gc = UTILITYFuncs.getConnection("openAccountScreen")
        if gc == True:
            if SignedIn == True:
                window_accountDetails.show()

            elif SignedIn == False:
                window_signIn.show()

            else:
                print("There was a problem checking if you're signed in or not to open the Account screen.")

        elif gc == False:
            print("You're not connected!")

        else:
            print("Unable to determine connectivity.")

    def openPlus():
        global myAccount

        if myAccount.plus == "True":
            window_plusOwned.show()

        elif myAccount.plus == "False":
            window_plus.show()

        else:
            print("There was a problem checking if you have Jade Plus or not.")

    def openJadeBar():
        window_jadeBar.show()

    def stopAll():
        global killThreads
        killThreads = True
        sys.exit()

    def signInButton():
        myAccount.signIn()

    def signOutButton():
        myAccount.signOut()

    def jadeAssistantButton():
        window_jadeAssistantMenu.show()

    def switchToCreateAccount():
        window_signIn.usernameBox_edit.clear()
        window_signIn.passwordBox_edit.clear()

        window_signIn.hide()
        window_createAccount.show()

    def switchToSignIn():
        window_createAccount.hide()
        window_signIn.show()

    def passwordToggle():
        state = window_signIn.passwordBox_show.checkState()
        if state == 2:
            #checked
            window_signIn.passwordBox_edit.setEchoMode(0)


        elif state == 0:
            #not checked
            window_signIn.passwordBox_edit.setEchoMode(2)

        else:
            print("There was a problem setting show/hide password.")
            UTILITYFuncs.log("WARN", "There was a problem setting show/hide password.")

    def createAccountButton():
        global myAccount
        myAccount.createAccount()

    def suspendedQuit():
        global killThreads
        killThreads = True
        sys.exit()

    def suspendedLogOut():
        global myAccount
        myAccount.signOut()
        window_main.show()
        dialog_accountSuspended.hide()

    def expandNews1():
        global news1
        global expanded
        expanded = "1"
        news1.expand()

    def expandNews2():
        global news2
        global expanded
        expanded = "2"
        news2.expand()

    def expandNews3():
        global news3
        global expanded
        expanded = "3"
        news3.expand()

    def openChangelog():
        WEBVIEW.openWebView("https://nofoert.wixsite.com/jade/changelog")

    #Expanded news
    def openUrlButton():
        global expanded
        global news1
        global news2
        global news3

        if expanded == "0":
            print("There was a problem expanding news. Nothing is actually expanded?")
            UTILITYFuncs.log("WARN", "There was a problem expanding news. Nothing is actually expanded?")

        elif expanded == "1":
            news1.openUrl()

        elif expanded == "2":
            news2.openUrl()

        elif expanded == "3":
            news3.openUrl()

        else:
            print("There was a problem determining what news article to open a url for.")
            UTILITYFuncs.log("WARN", "There was a problem determinign what news article to open a url for.")

    def quitErrorDialog():
        global killThreads
        killThreads = True
        dialog_error.hide()
        sys.exit()

    def restartAction():
        if platform.system() == "Windows":
            try:
                subprocess.Popen("Jade Launcher.exe")
                sys.exit()
            
            except Exception as e:
                print("There was a problem restarting.")
                UTILITYFuncs.error(f"There was a problem restarting. {e}")

        elif platform.system == "Darwin":
            try:
                subprocess.Popen("Jade Launcher")
                sys.exit()

            except Exception as e:
                print("There was a problem restarting.")
                UTILITYFuncs.error(f"There was a problem restarting. {e}")

    def downloadJadeAssistant():
        print("Download button pressed for Jade Assistant!")
        global downloadJadeAssistantVar
        downloadJadeAssistantVar = True

    def updateJadeAssistant():
        print("Update button pressed for Jade Assistant!")
        global updateJadeAssistantVar
        updateJadeAssistantVar = True

    def launchJadeAssistant():
        global killThreads
        try:
            if platform.system() == "Windows":
                subprocess.Popen("Jade Assistant.exe")
                killThreads = True
                sys.exit()
                
            elif platform.system() == "Darwin":
                subprocess.Popen("Jade Assistant")
                killThreads = True
                sys.exit()
                
            else:
                print("Your OS isn't supported!")
                UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac OS or Windows.")

        except Exception as e:
            UTILITYFuncs.error(f"There was a problem launching Jade Assistant! {e}")

    def removeJadeAssistant():
        try:
            if platform.system() == "Windows":
                os.system('taskkill /F /IM "Jade Assistant.exe"')
                os.remove("Jade Assistant.exe")
                guiLoopList.append('window_jadeAssistantMenu.launchButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.downloadButton.show()')
                guiLoopList.append('window_jadeAssistantMenu.removeButton.hide()')

            elif platform.system() == "Darwin":
                os.system('killall "Jade Assistant.exe"')
                os.remove("Jade Assistant")
                guiLoopList.append('window_jadeAssistantMenu.launchButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.updateButton.hide()')
                guiLoopList.append('window_jadeAssistantMenu.downloadButton.show()')
                guiLoopList.append('window_jadeAssistantMenu.removeButton.hide()')

            else:
                print("Your OS isn't supported!")
                UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac OS or Windows.")

        except Exception as e:
            UTILITYFuncs.error(f"There was a problem removing Jade Assistant! {e}")

    

# ----------
# Starting prints & logs
# ----------

print("----------")
print("Jade Launcher")
print(f"Version: {Version_MAJOR}.{Version_MAJOR}.{Version_PATCH}")
print("----------")

UTILITYFuncs.log("INFO", " ")
UTILITYFuncs.log("INFO", "-----")
UTILITYFuncs.log("INFO", f"| Jade Launcher | Version: {Version_MAJOR}.{Version_MAJOR}.{Version_PATCH}")
UTILITYFuncs.log("INFO", "-----")

# ----------
# PyQt5
# ----------

# Create Windows
app = QtWidgets.QApplication(sys.argv)

if developmental == False:
    print("Loading like it's an executable.")
    # Load like an exe
    try:
        window_accountDetails = uic.loadUi(str(PurePath(resource_path("accountDetails.ui"))))
        window_alreadyOwn = uic.loadUi(str(PurePath(resource_path("alreadyOwn.ui"))))
        window_createAccount = uic.loadUi(str(PurePath(resource_path("createAccount.ui"))))
        window_jadeBar = uic.loadUi(str(PurePath(resource_path("jadeBar.ui"))))
        window_main = uic.loadUi(str(PurePath(resource_path("main.ui"))))
        window_notification = uic.loadUi(str(PurePath(resource_path("notification.ui"))))
        window_offline = uic.loadUi(str(PurePath(resource_path("offline.ui"))))
        window_signIn = uic.loadUi(str(PurePath(resource_path("signIn.ui"))))
        window_plus = uic.loadUi(str(PurePath(resource_path("plus.ui"))))
        window_plusOwned = uic.loadUi(str(PurePath(resource_path("plusOwned.ui"))))
        window_storeDetails = uic.loadUi(str(PurePath(resource_path("storeDetails.ui"))))
        window_storeNotSignedIn = uic.loadUi(str(PurePath(resource_path("storeNotSignedIn.ui"))))
        window_jadeAssistantMenu = uic.loadUi(str(PurePath(resource_path("jadeAssistantMenu.ui"))))
        window_expandedNews = uic.loadUi(str(PurePath(resource_path("expandedNews.ui"))))
        window_changelog = uic.loadUi(str(PurePath(resource_path("changelog.ui"))))
        window_webView = uic.loadUi(str(PurePath(resource_path("webView.ui"))))
        dialog_signInFailure = uic.loadUi(str(PurePath(resource_path("signInFailure.ui"))))
        dialog_accountSuspended = uic.loadUi(str(PurePath(resource_path("accountSuspended.ui"))))
        dialog_error = uic.loadUi(str(PurePath(resource_path("error.ui"))))

    except Exception as e:
        print(f"There was a problem creating windows! (During a non-developmental run) {e}")
        UTILITYFuncs.log("FATAL", f"There was a problem creating windows! {e}")
        UTILITYFuncs.error(f"There was a problem creating windows! (During a non-developmental run {e}")

elif developmental == True:
    print("Loading like it's a .py")
    # Load normally
    try:
        window_accountDetails = uic.loadUi(str(PurePath("ui/accountDetails.ui")))
        window_alreadyOwn = uic.loadUi(str(PurePath("ui/alreadyOwn.ui")))
        window_createAccount = uic.loadUi(str(PurePath("ui/createAccount.ui")))
        window_jadeBar = uic.loadUi(str(PurePath("ui/jadeBar.ui")))
        window_main = uic.loadUi(str(PurePath("ui/main.ui")))
        window_notification = uic.loadUi(str(PurePath("ui/notification.ui")))
        window_offline = uic.loadUi(str(PurePath("ui/offline.ui")))
        window_signIn = uic.loadUi(str(PurePath("ui/signIn.ui")))
        window_plus = uic.loadUi(str(PurePath("ui/plus.ui")))
        window_plusOwned = uic.loadUi(str(PurePath("ui/plusOwned.ui")))
        window_storeDetails = uic.loadUi(str(PurePath("ui/storeDetails.ui")))
        window_storeNotSignedIn = uic.loadUi(str(PurePath("ui/storeNotSignedIn.ui")))
        window_jadeAssistantMenu = uic.loadUi(str(PurePath("ui/jadeAssistantMenu.ui")))
        window_expandedNews = uic.loadUi(str(PurePath("ui/expandedNews.ui")))
        window_changelog = uic.loadUi(str(PurePath("ui/changelog.ui")))
        window_webView = uic.loadUi(str(PurePath("ui/webView.ui")))
        dialog_signInFailure = uic.loadUi(str(PurePath("ui/signInFailure.ui")))
        dialog_accountSuspended = uic.loadUi(str(PurePath("ui/accountSuspended.ui")))
        dialog_error = uic.loadUi(str(PurePath("ui/error.ui")))

    except Exception as e:
        print(f"There was a problem creating windows! (During a developental run) {e}")
        UTILITYFuncs.log("FATAL", f"There was a problem creating windows! {e}")
        UTILITYFuncs.error(f"There was a problem creating windows! (During a developmental run {e}")
        

else:
    print("There was a terrible problem when opening windows. It it developental? We dont know.")
    UTILITYFuncs.log("FATAL", "There was a problem determining if it's developmental or not.")
    UTILITYFuncs.error(f"There was a problem determining if we're running as developental or not. Variable is '{developmental}'")
    sys.exit()

# Connect buttons to functions

# Offline
window_offline.button.clicked.connect(UIFuncs.closeOffline)

# Main Screen
window_main.leftBox_jadeAccountButton.clicked.connect(UIFuncs.openAccountScreen)
#window_main.leftBox_jadeBarButton.clicked.connect(UIFuncs.openJadeBar)
#window_main.leftBox_plusButton.clicked.connect(UIFuncs.openPlus)
window_main.leftBox_powerButton.clicked.connect(UIFuncs.stopAll)
window_main.leftBox_jadeAssistantButton.clicked.connect(UIFuncs.jadeAssistantButton)
window_main.button1.clicked.connect(UIFuncs.expandNews1)
window_main.button2.clicked.connect(UIFuncs.expandNews2)
window_main.button3.clicked.connect(UIFuncs.expandNews3)
window_main.changelogButton.clicked.connect(UIFuncs.openChangelog)
window_main.actionQuit_Jade_Launcher.triggered.connect(UIFuncs.stopAll)
window_main.actionRestart_Jade_Launcher.triggered.connect(UIFuncs.restartAction)

# Sign In Screen
window_signIn.signInBox_button.clicked.connect(UIFuncs.signInButton)
window_signIn.switchWindowBox_button.clicked.connect(UIFuncs.switchToCreateAccount)
window_signIn.passwordBox_show.stateChanged.connect(UIFuncs.passwordToggle)

# Account details
window_accountDetails.buttonsBox_signOut.clicked.connect(UIFuncs.signOutButton)
window_accountDetails.buttonsBox_changePassword.hide()

# Create Account
window_createAccount.switchWindowBox_button.clicked.connect(UIFuncs.switchToSignIn)
window_createAccount.mainBox_button.clicked.connect(UIFuncs.createAccountButton)

# Account suspended dialog
dialog_accountSuspended.logOut.clicked.connect(UIFuncs.suspendedLogOut)
dialog_accountSuspended.quit.clicked.connect(UIFuncs.suspendedQuit)

# Expanded news screen
window_expandedNews.openUrl.clicked.connect(UIFuncs.openUrlButton)

# Error dialog
dialog_error.QUIT.clicked.connect(UIFuncs.quitErrorDialog)

# Web view
WEBVIEW = WebView
window_webView.back.clicked.connect(WEBVIEW.back)
window_webView.forward.clicked.connect(WEBVIEW.forward)
window_webView.reload.clicked.connect(WEBVIEW.reload)
window_webView.web.loadFinished.connect(WEBVIEW.doneLoading)
window_webView.web.loadStarted.connect(WEBVIEW.startLoading)

# Jade Assistant menu
window_jadeAssistantMenu.launchButton.clicked.connect(UIFuncs.launchJadeAssistant)
window_jadeAssistantMenu.downloadButton.clicked.connect(UIFuncs.downloadJadeAssistant)
window_jadeAssistantMenu.updateButton.clicked.connect(UIFuncs.updateJadeAssistant)
window_jadeAssistantMenu.removeButton.clicked.connect(UIFuncs.removeJadeAssistant)

# -----
# Set properties of windows
window_jadeBar.move(10, 10)
window_main.VERSION.setText(f"Version BETA {Version_MAJOR}.{Version_MINOR}.{Version_PATCH}")
window_main.VERSION.setFont(QFont("Calibri", 10))

# Splash Text
splashTexts = ["It's nice to see you!", "Hey there!", "This is some splash text!"]
splashTextChoice = random.choice(splashTexts)
print(f"Selected splash text: '{splashTextChoice}'")
window_main.splash.setText(f"[ {splashTextChoice} ]")
window_main.splash.setFont(QFont("Calibri", 18))

window_main.splash.hide()
#Yes, I removed it. Not needed right now.

window_main.offlineLabel.hide()


# ----------
# Start App
# ----------
myAccount = Account("False", "no", "loading...")

news1 = News("loading", "loading", "loading", "loading", "1")
news2 = News("loading", "loading", "loading", "loading", "2")
news3 = News("loading", "loading", "loading", "loading", "3")

Launcher = LauncherId("loading", "loading") 

def guiLoop():
    global guiLoopList
    if len(guiLoopList) >= 1:
        try:
            print(f"Running code '{guiLoopList[0]}'")
            exec(guiLoopList[0])
            guiLoopList.remove(guiLoopList[0])

        except Exception as e:
            print(f"There was a problem running some code! {e}")
            guiLoopList.remove(guiLoopList[0])
            UTILITYFuncs.error(f"The gui loop had a problem running some code! '{e}'")

guiLoopTimer = QTimer()
guiLoopTimer.timeout.connect(guiLoop)
guiLoopTimer.start(100)

firstGC = UTILITYFuncs.getConnection("main")
if firstGC == True:
    MAINFuncs.mainCode()

app.exec()

