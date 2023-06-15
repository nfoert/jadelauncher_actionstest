'''
Jade Launcher (NEW)
The Jade Launcher is what launches, updates and downloads apps like Jade Assistant,
and where you can manage your Jade Account.

The Jade Launcher went through another iteration before this one. The previous one used guizero (https://lawsie.github.io/guizero/about/)
which is an incredible and easy to use GUI library. Guizero treated me well but I began to require more features which made me decide
to switch to PyQt5. (https://pypi.org/project/PyQt5/) Unfortunately, that was such a large change so I decided to start the Launcher over.

Jade Software was built by nfoert over nearly a year and a half.
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
import stat
import platform
import webbrowser
import threading
import sys

# Third Party Imports
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl, QTimer

import requests
import pwnedpasswords

# Thanks to Цзыюнь Янь's answer here https://stackoverflow.com/questions/68531326/what-is-the-error-in-the-code-for-this-playsound-module-even-though-the-syntax-i
import playsound

if platform.system() == "Windows":
    from PyQt5.QtWebEngineWidgets import *

else:
    print("Not importing QtWebEngine because it's not required for mac OS")

import psutil

# Local Imports
import assets #The resources for PyQt
import jadeDots
import jadeStatus
from jade_config import config


# ----------
# Set up variables
# ----------

# Detect if i'm an .exe or a .py
# Thanks to https://pyinstaller.org/en/stable/runtime-information.html
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    developmental = False
else:
    developmental = True

Version_MAJOR = 2
Version_MINOR = 1
Version_PATCH = 0
debug = False
debugOpenAllWindows = False

Version_TOTAL = f"{Version_MAJOR}.{Version_MINOR}.{Version_PATCH}"
SignedIn = False
LauncherIdVar = "Loading..."
expanded = "0"

guiLoopList = []
killThreads = False

selectedApp = False

downloadAppVar = False
updateAppVar = False
jadeAssistantVersion = "Loading..."
downloadUpdateVar = False
installUpdateVar = False
cancelInstallUpdateVar = False

progress_bar = ""

TruePath = ""

update = ""

# ----------
# Set up the resource manager
# ----------

# Thanks to ArmindoFlores's answer on Stack Overflow https://stackoverflow.com/questions/51264169/pyinstaller-add-folder-with-images-in-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ----------
# Get current location of script
# ----------

# Thanks to Soviut's Answer here: https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
if developmental == False:
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)

    elif __file__:
        application_path = os.path.dirname(__file__)

    TruePath = os.path.join(application_path)
    if platform.system() == "Windows":
        TruePath = TruePath + "\\"

    elif platform.system() == "Darwin":
        TruePath = TruePath + "/"
        TruePath = TruePath.replace("Jade Launcher.app/Contents/MacOS/", "")

elif developmental == True:
    TruePath = ""


# ----------
# Classes
# ----------
class Account:
    '''A class to contain the user's account data, and also handles sign in, create acccount, change password, and more.'''
    
    def __init__(self, plus, suspended, username):
        '''Init the class'''
        self.plus = plus
        self.suspended = suspended
        self.username = username

    def writeAccountFile(self, usernameIN, passwordIN):
        '''Code for writing account file so we can remember you'''
        global TruePath

        UTILITYFuncs.logAndPrint("INFO", "Classes/Account/writeAccountFile: Writing account file...")
        accountFile = open(f"{TruePath}account.txt", "w")
        accountFile.write(usernameIN + "\n" + passwordIN)
        accountFile.close()
        UTILITYFuncs.logAndPrint("INFO", "Class/Account/writeAccountFile: Done writing account file.")

    def Authenticate(self):
        '''Code for authentication at startup'''

        global SignedIn
        global TruePath
        UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: Reading account file...")
        try:
            try:
                accountFile = open(f"{TruePath}account.txt", "r")
            
            except FileNotFoundError:
                UTILITYFuncs.logAndPrint("WARN", "Classes/Account/Authenticate: Account file not found! Will create one.")
                accountFile = open(f"{TruePath}account.txt", "w")
                accountFile.close()
                accountFile = open(f"{TruePath}account.txt", "r")

            accountFileLines = accountFile.readlines()
            accountFile.close()
            if len(accountFileLines) == 0:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: Account file is empty! Not signed in.")
                window_main.account_label.setText(f"Not signed in.")
                window_main.account_label.setFont(QFont("Calibri", 8))
                window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
                window_main.account_label.setStyleSheet("color: red")
                window_main.account_letter.setText("")
                SignedIn = False

            elif len(accountFileLines) == 2:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: Account file has data! Will try to sign in.")

            else:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: There's a problem with the account file.")

        except Exception as e:
            UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/Authenticate: There was a problem signing you in. {e}")
            UTILITYFuncs.error(f"There was a problem signing you in. {e}")

        try:
            USERNAME = accountFileLines[0]
            PASSWORD = accountFileLines[1]
            UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/Authenticate: Authenticating with username: {USERNAME} and password: {PASSWORD}")
            try:
                authenticateRequest = requests.get(f"https://nfoert.pythonanywhere.com/jadeCore/get?user={USERNAME},password={PASSWORD}&")
                authenticateRequest.raise_for_status()
            
            except Exception as e:
                UTILITYFuncs.logAndPrint("WARN", "Classes/Account/Authenticate: There was a problem getting authentication requests.")

            if "user=" in authenticateRequest.text:

                try:
                    art = authenticateRequest.text
                    art_email = UTILITYFuncs.substring(art, ",email=", ",name")
                    art_name = UTILITYFuncs.substring(art, ",name=", ",plus")
                    art_plus = UTILITYFuncs.substring(art, "plus=", ",suspended")
                    art_suspended = UTILITYFuncs.substring(art, "suspended=", "&")

                    if art_suspended == "no":
                        UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: Your account isn't suspended!")

                    else:
                        UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/Authenticate: Your account is suspended for {art_suspended}")
                        dialog_accountSuspended.MAINLABEL.setText(art_suspended)
                        dialog_accountSuspended.MAINLABEL.setFont(QFont("Calibri", 10))
                        
                    


                    SignedIn = True
                    UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/Authenticate: SIGNED IN: email={art_email},name={art_name},jadeAssistant={art_plus}")
                    window_accountDetails.usernameBox_username.setText(USERNAME)
                    window_accountDetails.usernameBox_username.setFont(QFont("Calibri", 12))

                    window_accountDetails.nameBox_name.setText(art_name)
                    window_accountDetails.nameBox_name.setFont(QFont("Calibri", 12))

                    window_accountDetails.emailBox_email.setText(art_email)
                    window_accountDetails.emailBox_email.setFont(QFont("Calibri", 12))

                    window_main.account_label.setText(f"Hello, {USERNAME}")
                    window_main.account_label.setFont(QFont("Calibri", 11))
                    window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
                    window_main.account_label.setStyleSheet("color: green")

                    window_main.account_letter.setText(USERNAME[0])
                    window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)

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
                    UTILITYFuncs.logAndPrint("FATAL", f"Classes/Account/Authenticate: There was a problem doing a bunch of essential stuff when Authenticating. {e}")
                    UTILITYFuncs.error(f"There was a problem doing a bunch of essential stuff when Authenticating. {e}")

                

            elif "not" in authenticateRequest.text:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: Failed to sign in. Incorrect credentials.")
                dialog_signInFailure.show()
                window_main.account_label.setText(f"Not signed in.")
                window_main.account_label.setFont(QFont("Calibri", 8))
                window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
                window_main.account_label.setStyleSheet("color: red")
                window_main.account_letter.setText("")
                SignedIn = False
                return False

        except Exception as e:
            UTILITYFuncs.logAndPrint("WARN", f"Classes/Account/Authenticate: There was a problem signing you in. (Account file may have no content.) '{e}'")
            window_main.account_label.setText(f"Not signed in.")
            window_main.account_label.setFont(QFont("Calibri", 8))
            window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
            window_main.account_label.setStyleSheet("color: red")
            window_main.account_letter.setText("")
            SignedIn = False

        
    def signIn(self):
        '''Code for signing in via the sign in window.'''
        
        global SignedIn
        
        usernameInput = window_signIn.usernameBox_edit.text()
        passwordInput = window_signIn.passwordBox_edit.text()
        
        try:
            signInRequest = requests.get(f"https://nfoert.pythonanywhere.com/jadeCore/get?user={usernameInput},password={passwordInput}&")
            signInRequest.raise_for_status()
            
            if "user=" in signInRequest.text:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/signIn: Signed In!")
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

                window_main.account_label.setText(f"Hello, {usernameInput}")
                window_main.account_label.setFont(QFont("Calibri Bold", 9))
                window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
                window_main.account_label.setStyleSheet("color: green")

                window_main.account_letter.setText(usernameInput[0])

                self.password = passwordInput
                self.username = usernameInput
                self.email = sir_email
                self.name = sir_name

                if sir_suspended == "no":
                    UTILITYFuncs.logAndPrint("INFO", "Classes/Account/signIn: You're not suspended!")
                    window_signIn.hide()
                    window_accountDetails.show()

                else:
                    UTILITYFuncs.logAndPrint("INFO", "Classes/Account/signIn: You're suspended!")
                    window_signIn.hide()
                    window_main.hide()
                    dialog_accountSuspended.MAINLABEL.setText(sir_suspended)
                    dialog_accountSuspended.MAINLABEL.setFont(QFont("Calibri", 10))
                    dialog_accountSuspended.show()

            else:
                UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/signIn: There was a problem signing you in: incorrect credentials. |{usernameInput}|, |{passwordInput}|, |{signInRequest.text}|")
                SignedIn = False
                dialog_signInFailure.show()
        
        except Exception as e:
            UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/signIn: There was a problem signing you in. {e}")
            
    
    def signOut(self):
        '''Code for signing out'''

        global SignedIn
        SignedIn = False
        self.writeAccountFile("","")
        
        window_signIn.usernameBox_edit.clear()
        window_signIn.passwordBox_edit.clear()

        window_main.account_label.setText(f"Not signed in.")
        window_main.account_label.setFont(QFont("Calibri", 10))
        window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
        window_main.account_label.setStyleSheet("color: red")
        window_main.account_letter.setText("")

        window_accountDetails.hide()
        window_signIn.show()
        UTILITYFuncs.logAndPrint("INFO", "Classes/Account/signOut: Signed out.")

    def createAccount(self):
        '''Code for creating an account'''

        usernameInput = window_createAccount.usernameBox_edit.text()
        passwordInput = window_createAccount.passwordBox_edit.text()
        emailInput = window_createAccount.emailBox_edit.text()
        nameInput = window_createAccount.nameBox_edit.text()

        gc = UTILITYFuncs.getConnection("Account/createAccount")
        if gc == True:
            window_createAccount.mainBox_button.setEnabled(False)
            window_createAccount.mainBox_button.setText("Checking password...")
            if len(passwordInput) >= 8:
                
                try:
                    passwordCheck = pwnedpasswords.check(passwordInput)

                except:
                    passwordCheck = 0
                    
                if passwordCheck == 0:
                        
                    try:
                        window_createAccount.mainBox_button.setText("Creating Account...")
                        createAccountRequest = requests.get(f"https://nfoert.pythonanywhere.com/jadeCore/create?user={usernameInput},password={passwordInput},email={emailInput},name={nameInput}&")
                        createAccountRequest.raise_for_status()

                        if createAccountRequest.text == "Account successfully created.":
                            UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: Account sucsessfully created.")
                            window_createAccount.mainBox_button.setEnabled(True)
                            window_createAccount.mainBox_button.setText("Create Account")

                            UTILITYFuncs.alert("Account successfully created.", "Your Account has been created.")

                            self.writeAccountFile(usernameInput, passwordInput)
                            self.Authenticate()

                            window_createAccount.usernameBox_edit.clear()
                            window_createAccount.passwordBox_edit.clear()
                            window_createAccount.nameBox_edit.clear()
                            window_createAccount.emailBox_edit.clear()

                            window_createAccount.hide()
                            window_accountDetails.show()

                        elif createAccountRequest.text == "That account already exists.":
                            UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: That account already exists!")
                            UTILITYFuncs.alert("That account already exists!", "That username matches another username in our database. Maybe you created an account, then forgot it existed?")
                            window_createAccount.mainBox_button.setEnabled(True)
                            window_createAccount.mainBox_button.setText("Create Account")

                        else:
                            UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: There was a problem.")
                            UTILITYFuncs.alert("There was a problem creating an Account.", "We couldn't create your account.")
                            window_createAccount.mainBox_button.setEnabled(True)
                            window_createAccount.mainBox_button.setText("Create Account")

                    except Exception as e:
                        UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/createAccount: There was a problem creating an account. {e}")
                        UTILITYFuncs.alert("There was a problem creating an Account.", "We couldn't create your account.")
                        window_createAccount.mainBox_button.setEnabled(True)
                        window_createAccount.mainBox_button.setText("Create Account")
                    
                elif passwordCheck >= 1:
                    UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/createAccount: Password is not safe! Has been leaked {passwordCheck} times.")
                    UTILITYFuncs.alert("That password is not safe!", f"That password has been leaked {passwordCheck} times.")
                    window_createAccount.mainBox_button.setEnabled(True)
                    window_createAccount.mainBox_button.setText("Create Account")

                else:
                    UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: There was a problem checking password safety.")
                    UTILITYFuncs.alert("There was a problem checking password safety.", "We were not able to confirm that your password is safe.")
                    window_createAccount.mainBox_button.setEnabled(True)
                    window_createAccount.mainBox_button.setText("Create Account")    


            else:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: Please select a password with more than 8 characters.")
                UTILITYFuncs.alert("Password is too short!", "Please make sure your password has eight or more characters.")
                window_createAccount.mainBox_button.setEnabled(True)
                window_createAccount.mainBox_button.setText("Create Account")

        elif gc == False:
            UTILITYFuncs.alert("There was a problem creating an Account.", "You're not connected!")

        else:
            UTILITYFuncs.alert("There was a problem creating an Account.", "There was a problem getting connection status.")

    def changePassword(self):
        '''Code for changing the user's password'''
        verificationCode = window_changePassword.verificationCode_edit.text()
        oldPassword = window_changePassword.oldPassword_edit.text()
        newPassword = window_changePassword.passwordBox_edit.text()

        if len(newPassword) >= 8:
            window_changePassword.button.setEnabled(False)
            window_changePassword.button.setText("Checking password...")
            try:
                passwordCheck = pwnedpasswords.check(newPassword)

            except:
                    passwordCheck = 0

            if passwordCheck == 0:

                try:
                    window_changePassword.button.setEnabled(False)
                    window_changePassword.button.setText("Changing password...")
                    changePasswordRequest = requests.get(f"https://nfoert.pythonanywhere.com/jadeCore/changePassword?username={self.username},password={oldPassword},code={verificationCode},new={newPassword}&")
                    changePasswordRequest.raise_for_status()

                    if changePasswordRequest.text == "True":
                        window_changePassword.hide()
                        window_accountDetails.hide()

                        self.password = newPassword

                        window_changePassword.verificationCode_edit.clear()
                        window_changePassword.oldPassword_edit.clear()
                        window_changePassword.passwordBox_edit.clear()

                        UTILITYFuncs.logAndPrint("INFO", "Account/changePassword: You changed your password.")
                        UTILITYFuncs.alert("Password changed", "Your password has been changed.")

                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                        myAccount.writeAccountFile(self.username, newPassword)

                        window_accountDetails.show()

                    elif changePasswordRequest.text == "There was a problem getting Verification Code data.":
                        window_changePassword.passwordBox_edit.clear()
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: Your verification code is not correct. '{changePasswordRequest.text}'")
                        UTILITYFuncs.alert("Your verification code is not correct.", f"Please check your email account {self.email} to view your verification code.")
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                    elif changePasswordRequest.text == "There was a problem getting Account data.":
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: There was a problem getting Account data.. '{changePasswordRequest.text}'")
                        UTILITYFuncs.alert("There was a problem getting Account data.", "It looks like your username is not correct for some reason.")
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                    elif changePasswordRequest.text == "That username and password don't match any Account in the database.":
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: Your old password is not correct. '{changePasswordRequest.text}'")
                        UTILITYFuncs.alert("Your old password is not correct.", "Please confirm that your old password is correct.")
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                    else:
                        window_changePassword.passwordBox_edit.clear()
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: There was a problem changing your password. '{changePasswordRequest.text}'")
                        UTILITYFuncs.alert("There was a problem changing your password.", changePasswordRequest.text)
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                        
                except Exception as e:
                    UTILITYFuncs.logAndPrint("FATAL", f"Account/changePassword: An exception occured when changing your password. '{e}'")
                    UTILITYFuncs.error(f"An exception occured when changing your password. '{e}'")
                    window_changePassword.button.setEnabled(True)
                    window_changePassword.button.setText("Change Password")

            else:
                UTILITYFuncs.alert("That password is not safe!", f"Your new password has been leaked {passwordCheck} times.")
                window_changePassword.passwordBox_edit.clear()
                window_changePassword.button.setEnabled(True)
                window_changePassword.button.setText("Change Password")

        else:
            UTILITYFuncs.alert("That password is not long enough!", "Please make your new password eight or more characters.")
            window_changePassword.passwordBox_edit.clear()
        
class News:
    '''A class to control news expansion and opening url.'''
    def __init__(self, header, date, text, url, number, code):
        self.header = header
        self.date = date
        self.text = text
        self.url = url
        self.number = number
        self.code = code

    def expand(self):
        '''Expand news'''
        UTILITYFuncs.logAndPrint("INFO", f"Classes/News/expand: Expanding news {self.number}")

        if platform.system() == "Windows":
            WEBVIEW.openWebView(f"https://nfoert.pythonanywhere.com/jadesite/post?{self.code}&")

        elif platform.system() == "Darwin":
            webbrowser.open(self.url)

        else:
            UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")

        
        
        print("Done expanding.")

    def openUrl(self):
        '''Opens the news article using the built-in web browser on Windows or by opening the default webbrowser on Mac'''
        UTILITYFuncs.logAndPrint("INFO", "Classes/News/openUrl: Attempting to open url.")
        if platform.system() == "Windows":
            WEBVIEW.openWebView(self.url)

        elif platform.system() == "Darwin":
            webbrowser.open(self.url)

        else:
            UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")



class LauncherId:
    '''A class for managing your Launcher Id'''
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def getId(self):
        '''Obtain the ID'''
        global LauncherIdVar
        global TruePath
        UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/getId: Getting Launcher Id...")
        gc = UTILITYFuncs.getConnection("LauncherId/getId")
        if gc == True:
            try:
                IdFile = open(f"{TruePath}id.txt", "r")
                readfile = IdFile.read()
                IdFile.close()
                self.id = readfile
                return readfile
            
            except OSError:
                UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/getId: This launcher does not have an id. Creating one...")
                IdFile = open(f"{TruePath}id.txt", "w")
                letters = string.ascii_lowercase
                randomId = ""
                randomIdFound = False
                
                while randomIdFound == False:
                    for i in range(10):
                        choose = random.choice(letters)
                        randomId = randomId + choose

                    UTILITYFuncs.logAndPrint("INFO", f"Classes/LauncherId/getId: Random string is {randomId} Checking...")

                    try:
                        randomIdCheck = requests.get(f"https://nfoert.pythonanywhere.com/jadeLauncher/checkForExistingLauncherId?{randomId}&")

                    except Exception as e:
                        UTILITYFuncs.logAndPrint("WARN", f"Classes/LauncherId/getId: There was a problem checking the id. '{e}'")

                    if randomIdCheck.text == "SAFE TO USE":
                        IdFile.write(randomId)
                        UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/getId: Id is safe to use.")
                        self.id = randomId
                        randomIdFound = True
                        LauncherIdVar = self.id
                        return randomId

                    else:
                        UTILITYFuncs.logAndPrint("WARN", "Classes/LauncherId/getId: There was a problem checking the Id. Maybe it already existed?")
                        randomIdFound == False
                        return False

        elif gc == False:
            return False

    def updateStatus(self):
        '''Update this Launcher's status.'''
        global LauncherIdVar
        UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/updateStatus: Updating launcher status.")
        gc = UTILITYFuncs.getConnection("LauncherId/updateStatus")
        if gc == True:
            version = f"{Version_MAJOR}.{Version_MINOR}.{Version_PATCH}"
            if SignedIn == True:
                USERNAMEINPUT = self.username

            elif SignedIn == False:
                USERNAMEINPUT = "notSignedIn"

            else:
                UTILITYFuncs.logAndPrint("WARN", "Classes/LauncherId/updateStatus: There was a problem determining signed in status.")
                USERNAMEINPUT = "notSignedIn"
            
            try:
                updateStatusRequest = requests.get(f"https://nfoert.pythonanywhere.com/jadeLauncher/updateLauncherId?id={self.id},username={USERNAMEINPUT},version={version}&")

            except:
                UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/updateStatus: There was a problem getting the update status request.")

            if updateStatusRequest.text == "DONE":
                UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/updateStatus: Done.")
                dialog_about.id.setText(self.id)
                dialog_about.id.setFont(QFont("Calibri", 11))

            else:
                UTILITYFuncs.logAndPrint("INFO", f"Classes/LauncherId/updateStatus: There was a problem updating Launcher Id. {updateStatusRequest.text}, {self.id}")
                

        elif gc == False:
            return False

        else:
            UTILITYFuncs.logAndPrint("INFO", "Classes/LauncherId/updateStatus: Couldn't determine if you're connected or not.")
            UTILITYFuncs.error("Couldn't determine if you're connected or not when updating Launcher status.")


class WebView:
    '''A group of functions for the window_webView'''
    def __init__(self):
        pass

    def reload():
        '''Reload the page'''
        window_webView.web.reload()
        UTILITYFuncs.logAndPrint("INFO", "Classes/WebView/reload: Reloaded the page.")

    def back():
        '''Go back a page'''
        window_webView.web.back()
        url = window_webView.web.url().toString()
        if url == "about:blank":
            window_webView.web.back()
        UTILITYFuncs.logAndPrint("INFO", "Classes/WebView/back: Went back a page.")

    def forward():
        '''Go forward a page'''
        window_webView.web.forward()
        UTILITYFuncs.logAndPrint("INFO", "Classes/WebView/forward: Went forward a page.")
    
    def startLoading():
        '''When the page begins to load'''
        window_webView.statusbar.showMessage("Loading page...")
        UTILITYFuncs.logAndPrint("INFO", "Classes/WebView/startLoading: Began to load the page.")

    def doneLoading():
        '''When the page is finished loading'''
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
            UTILITYFuncs.logAndPrint("WARN", f"Classes/WebView/doneLoading: There was a problem setting labels when done loading! '{e}'")
    
    def openWebView(urlInput):
        '''Open the webview'''
        gc = UTILITYFuncs.getConnection("WebView/openWebView")
        if gc == True:
            if platform.system() == "Windows":
                window_webView.web.setUrl(QUrl(urlInput))
                window_webView.show()

            elif platform.system() == "Darwin":
                UTILITYFuncs.logAndPrint("INFO", "Classes/WebView/openWebView: You're on mac! Will just open in default webbrowser instead.")
                webbrowser.open(str(urlInput))

        elif gc == False:
            return False

        else:
            UTILITYFuncs.logAndPrint("WARN", "Classes/WebView/openWebView: There was a problem getting connection status.")

    def progress(prog):
        if prog >= 70:
            window_webView.show()
            window_webView.web.show()

        elif prog < 70:
            window_webView.web.hide()

    def goButton():
        url = window_webView.url.text()
        if "https://" in url:
            window_webView.web.setUrl(QUrl(url))

        elif "http://" in url:
            window_webView.web.setUrl(QUrl(url))

        else:
            url = "https://" + url
            window_webView.web.setUrl(QUrl(url))

class App:
    def __init__(self, dictionary, debug=False):
        self.name = dictionary["name"]
        self.description = dictionary["description"]
        self.path = dictionary["path"]
        self.version = dictionary["version"]
        self.download_folder = dictionary["download_folder"]
        self.download_url = dictionary["download_url"]
        self.exe_location = dictionary["exe_location"]
        self.version_file_location = dictionary["version_file_location"]
        self.version_url = dictionary["version_url"]
        self.dot_name = dictionary["dot_name"]
        self.button_launch = dictionary["button_launch"]
        self.button_download = dictionary["button_download"]
        self.button_update = dictionary["button_update"]
        self.button_remove = dictionary["button_remove"]
        self.label_status = dictionary["label_status"]
        self.label_version = dictionary["label_version"]
        self.main_button_launch = dictionary["main_button_launch"]
        self.button_launch_loop = dictionary["button_launch_loop"]
        self.button_download_loop = dictionary["button_download_loop"]
        self.button_update_loop = dictionary["button_update_loop"]
        self.button_remove_loop = dictionary["button_remove_loop"]
        self.label_status_loop = dictionary["label_status_loop"]
        self.label_version_loop = dictionary["label_version_loop"]
        self.main_button_launch_loop = dictionary["main_button_launch_loop"]

        if debug:
            print(f"Item self.name is '{self.name}' with type '{type(self.name)}'")
            print(f"Item self.description is '{self.description}' with type '{type(self.description)}'")
            print(f"Item self.path is '{self.path}' with type '{type(self.path)}'")
            print(f"Item self.version is '{self.version}' with type '{type(self.version)}'")
            print(f"Item self.download_folder is '{self.download_folder}' with type '{type(self.download_folder)}'")
            print(f"Item self.download_url is '{self.download_url}' with type '{type(self.download_url)}'")
            print(f"Item self.exe_location is '{self.exe_location}' with type '{type(self.exe_location)}'")
            print(f"Item self.version_file_location is '{self.version_file_location}' with type '{type(self.version_file_location)}'")
            print(f"Item self.dot_name is '{self.dot_name}' with type '{type(self.dot_name)}'")
            print(f"Item self.button_launch is '{self.button_launch}' with type '{type(self.button_launch)}'")
            print(f"Item self.button_download is '{self.button_download}' with type '{type(self.button_download)}'")
            print(f"Item self.button_update is '{self.button_update}' with type '{type(self.button_update)}'")
            print(f"Item self.button_remove is '{self.button_remove}' with type '{type(self.button_remove)}'")
            print(f"Item self.label_status is '{self.label_status}' with type '{type(self.label_status)}'")
            print(f"Item self.label_version is '{self.label_version}' with type '{type(self.label_version)}'")
            print(f"Item self.main_button_launch is '{self.main_button_launch}' with type '{type(self.main_button_launch)}'")

        self.downloadAppVar = False
        self.updateAppVar = False
        self.state = ""
        self.newVersion = ""

    def openAppMenu(self):
        global selectedApp
        UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: Opening app menu for {self.name}...")
        selectedApp = self.name
        self.label_version.setText(f"{self.version}")

        if self.state == "ready":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is ready.")
            self.button_launch.show()
            self.button_download.hide()
            self.button_update.hide()
            self.button_remove.show()
            self.label_status.setText("Up to date")

        elif self.state == "download":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is download.")
            self.button_launch.hide()
            self.button_download.show()
            self.button_update.hide()
            self.button_remove.hide()
            self.label_status.setText(f"Download version {self.newVersion}")

        elif self.state == "downloading":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is downloading.")
            self.button_launch.hide()
            self.button_download.show()
            self.button_update.hide()
            self.button_remove.hide()
            self.label_status.setText(f"Downloading version {self.newVersion}...")

        elif self.state == "update":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is updates.")
            self.button_launch.show()
            self.button_download.hide()
            self.button_update.show()
            self.button_remove.show()
            self.label_status.setText(f"Update to {self.newVersion} avaliable")

        elif self.state == "updating":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is updating.")
            self.button_launch.hide()
            self.button_download.hide()
            self.button_update.show()
            self.button_remove.hide()
            self.label_status.setText(f"Updating to version {self.newVersion}...")
            
        elif self.state == "readyoffline":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is readyoffline.")
            self.button_launch.show()
            self.button_download.hide()
            self.button_update.hide()
            self.button_remove.show()
    
        else:
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is not recognized. '{self.state}'")
            return False

        UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: Menu for {self.name} has opened.")
        window_status.show()

    def launchApp(self):
        '''Launch the app'''
        UTILITYFuncs.logAndPrint("INFO", f"App/launchApp: Launching {self.name}...")
        global killThreads
        global TruePath
        try:
            if platform.system() == "Windows":
                subprocess.Popen(self.exe_location)
                UTILITYFuncs.logAndPrint("INFO", f"App/launchApp: {self.name} was launched. (windows)")
        
            elif platform.system() == "Darwin":
                subprocess.run(["open", f"{TruePath}{self.exe_location}"])
                killThreads = True
                UTILITYFuncs.logAndPrint("INFO", f"App/launchApp: {self.name} was launched. (mac)")
                sys.exit()
                
            else:
                UTILITYFuncs.logAndPrint("FATAL", "App/launchApp: Your OS isn't supported! Please use Mac or Windows.")
                UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac or Windows.")

        except Exception as e:
            UTILITYFuncs.logAndPrint("INFO", f"UIFuncs/launchJadeAssistant: There was a problem launching {self.name}! {e}")
            UTILITYFuncs.error(f"There was a problem launching Jade Assistant! {e}")

    def downloadApp(self):
        '''Download the app'''
        UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Thread started for {self.name}")
        global guiLoopList
        global killThreads
        global progress_bar
        global TruePath

        while killThreads == False:
            if self.downloadAppVar == True:
                UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Downloading {self.name}...")
                guiLoopList.append(f'{self.button_launch_loop}.hide()')
                guiLoopList.append(f'{self.button_download_loop}.show()')
                guiLoopList.append(f'{self.button_download_loop}.setEnabled(False)')
                guiLoopList.append(f'{self.button_download_loop}.setText("Downloading...")')
                guiLoopList.append(f'{self.button_update_loop}.hide()')
                guiLoopList.append(f'{self.button_remove_loop}.hide()')

                self.newVersion = self.newVersion.replace("\n", ".")

                try:
                    UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Downloading {self.name}...")
                    guiLoopList.append(f'jadeDots.showDot("{self.dot_name}")')
                    guiLoopList.append(f'jadeDots.setDotPercent("{self.dot_name}", "Loading...")')

                    guiLoopList.append('jadeStatus.setStatus("load")')
                    
                    self.state = "downloading"
                    guiLoopList.append(f"{self.label_status_loop}.setText('{self.newVersion}')")

                    app_download = requests.get(self.download_url, stream=True)

                    total_size_in_bytes = int(app_download.headers.get('content-length', 0))
                    bytes_downloaded = 0
                    last = 0
                    
                    with open(self.exe_location, 'wb') as file:
                        for data in app_download.iter_content(1024):
                            file.write(data)
                            bytes_downloaded = bytes_downloaded + 1024
                            percent = bytes_downloaded / total_size_in_bytes
                            percent = percent * 100
                            percent = round(percent)
                            if last != percent:
                                last = percent
                                guiLoopList.append(f'{self.label_status_loop}.setText("Downloading version {self.newVersion}... [{percent}%]")')
                                guiLoopList.append(f'window_main.status_bar.setText("Downloading {self.name} {self.newVersion.replace(chr(10), "")}... [{percent}%]")') #chr(10) is a backslash
                                guiLoopList.append(f'jadeDots.setDotPercent("{self.dot_name}", "[{percent}%]")')

                            else:
                                continue

                    file.close()
                            
                    if platform.system() == "Darwin":
                        os.system(f'chmod 775 "{TruePath}{self.name}"')

                    else:
                        UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Not Chmodding.")


                    self.downloadAppVar = False
                    guiLoopList.append(f'{self.button_launch_loop}.show()')
                    guiLoopList.append(f'{self.button_download_loop}.setEnabled(True)')
                    guiLoopList.append(f'{self.button_download_loop}.setText("Download")')
                    guiLoopList.append(f'{self.button_download_loop}.hide()')
                    guiLoopList.append(f'{self.button_update_loop}.hide()')
                    guiLoopList.append(f'{self.button_remove_loop}.show()')
                    guiLoopList.append(f'{self.main_button_launch_loop}.show()')
                    guiLoopList.append(f'{self.label_status_loop}.setText("Done downloading.")')
                    self.state = "ready"
                    
                    UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Done downloading {self.name}.")
                    guiLoopList.append(f'UTILITYFuncs.alert("{self.name} was downloaded.", "{self.name} is done downloading.")')

                    versionFileName = self.path
                    versionFileName = versionFileName.replace(" ", "")
                    appVersionFile = open(self.version_file_location, "w")
                    self.version = self.newVersion
                    self.newVersion = self.newVersion.replace(".", "\n")
                    appVersionFile.write(self.newVersion)
                    appVersionFile.close()

                    guiLoopList.append(f'window_main.status_bar.setText("{self.name} was downloaded!")')
                    guiLoopList.append('jadeStatus.setStatus("ok")')
                    guiLoopList.append(f'jadeDots.setDotPercent("{self.dot_name}", "Done!")')
                    guiLoopList.append(f'jadeDots.hideDot("{self.dot_name}")')

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"App/downloadApp: There was a problem downloading {self.name}! {e}")
                    self.downloadAppVar = False
                    guiLoopList.append(f'UTILITYFuncs.alert("There was a problem!", "There was a problem downloading {self.name}!")')
                    guiLoopList.append(f'{self.button_launch_loop}.show()')
                    guiLoopList.append(f'{self.button_download_loop}.show()')
                    guiLoopList.append(f'{self.button_update_loop}.hide()')
                    guiLoopList.append(f'{self.button_remove_loop}.show()')

            else:
                sleep(1)
                continue

    def updateApp(self):
        '''Update the app'''
        UTILITYFuncs.logAndPrint("INFO", "App/updateApp: Thread started.")
        global guiLoopList
        global killThreads
        global progress_bar
        global selectedApp
        global TruePath

        while killThreads == False:
            if self.updateAppVar == True:
                UTILITYFuncs.logAndPrint("INFO", f"App/updateApp: Updating {self.name}...")
                guiLoopList.append(f'{self.button_launch_loop}.hide()')
                guiLoopList.append(f'{self.button_download_loop}.hide()')
                guiLoopList.append(f'{self.button_update_loop}.show()')
                guiLoopList.append(f'{self.button_update_loop}.setEnabled(False)')
                guiLoopList.append(f'{self.button_update_loop}.setText("Updating...")')
                guiLoopList.append(f'{self.button_remove_loop}.hide()')

                try:
                    UTILITYFuncs.logAndPrint("INFO", f"App/updateApp: Updating {self.name}...")
                    guiLoopList.append(f'jadeDots.showDot("{self.dot_name}")')
                    guiLoopList.append(f'jadeDots.setDotPercent("{self.dot_name}", "Loading...")')

                    self.state = "updating"
                    guiLoopList.append('jadeStatus.setStatus("load")')
                    
                    os.remove(self.exe_location)
                    self.path = self.path.replace(" ", "%20")

                    app_download = requests.get("https://github.com/nfoert/jadeassistant/raw/main/Jade Assistant.exe", stream=True)
                    total_size_in_bytes = int(app_download.headers.get('content-length', 0))
                    bytes_downloaded = 0
                    last = 0

                    self.path = self.path.replace("%20", " ")
                    
                    with open(self.exe_location, 'wb') as file:
                        for data in app_download.iter_content(1024):
                            file.write(data)
                            bytes_downloaded = bytes_downloaded + 1024
                            percent = bytes_downloaded / total_size_in_bytes
                            percent = percent * 100
                            percent = round(percent)
                            if last != percent:
                                last = percent
                                guiLoopList.append(f'{self.label_status_loop}.setText("Updating to version {self.newVersion.replace(chr(10), "")}... [{percent}%]")') #chr(10) is a backslash
                                guiLoopList.append(f'window_main.status_bar.setText("Updating {self.name} to {self.newVersion.replace(chr(10), "")}... [{percent}%]")')
                                guiLoopList.append(f'jadeDots.setDotPercent("{self.dot_name}", "[{percent}%]")')

                            else:
                                continue
                        
                        app_download.close()
                        file.close()

                        if platform.system() == "Darwin":
                            os.system(f'chmod 775 "{TruePath}{self.name}"')

                        else:
                            UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Not Chmodding.")

                    self.updateAppVar = False
                    self.state = "ready"

                    guiLoopList.append(f'{self.button_launch_loop}.show()')
                    guiLoopList.append(f'{self.button_download_loop}.hide()')
                    guiLoopList.append(f'{self.button_update_loop}.hide()')
                    guiLoopList.append(f'{self.button_remove_loop}.show()')
                    guiLoopList.append(f'{self.label_status_loop}.setText("Done updating.")')

                    UTILITYFuncs.logAndPrint("INFO", f"App/updateApp: Done updating {self.name}. Writing version file...")

                    versionFileName = self.path
                    versionFileName = versionFileName.replace(" ", "")
                    appVersionFile = open(self.version_file_location, "w")
                    self.version = self.newVersion
                    self.newVersion = self.newVersion.replace(".", "\n")
                    appVersionFile.write(self.newVersion)
                    appVersionFile.close()

                    guiLoopList.append(f'window_main.status_bar.setText("{self.name} was updated to {self.newVersion.replace(chr(10), "")}")') #chr(10) is a backslash
                    guiLoopList.append(f'jadeDots.setDotPercent("{self.dot_name}", "Done!")')
                    guiLoopList.append(f'jadeDots.hideDot("{self.dot_name}")')
                    guiLoopList.append('jadeStatus.setStatus("ok")')

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"App/updateApp: There was a problem updating {self.name}! {e}")
                    self.updateAppVar = False
                    guiLoopList.append(f'UTILITYFuncs.alert("There was a problem!", "There was a problem updating {self.name}!")')
                    guiLoopList.append(f'{self.button_launch_loop}.show()')
                    guiLoopList.append(f'{self.button_download_loop}.hide()')
                    guiLoopList.append(f'{self.button_update_loop}.show()')
                    guiLoopList.append(f'{self.button_update_loop}.setEnabled(True)')
                    guiLoopList.append(f'{self.button_update_loop}.setText("Update")')
                    guiLoopList.append(f'{self.button_remove_loop}.show()')


            else:
                sleep(1)
                continue

    def removeApp(self):
        '''Remove the app'''
        try:
            if platform.system() == "Windows":
                os.system(f'taskkill /F /IM "{self.path}.exe"')
                os.remove(self.exe_location)
                guiLoopList.append(f'{self.button_launch_loop}.hide()')
                guiLoopList.append(f'{self.button_download_loop}.show()')
                guiLoopList.append(f'{self.button_update_loop}.hide()')
                guiLoopList.append(f'{self.button_remove_loop}.hide()')
                guiLoopList.append(f'{self.main_button_launch_loop}.hide()')
                guiLoopList.append(f'{self.label_status_loop}.setText("Removed.")')
                UTILITYFuncs.alert(f"{self.name} was removed.", f"You just deleted {self.name}.")

            elif platform.system() == "Darwin":
                os.system(f'killall "{self.path}"')
                os.remove(self.path)
                guiLoopList.append(f'{self.button_launch_loop}.hide()')
                guiLoopList.append(f'{self.button_download_loop}.show()')
                guiLoopList.append(f'{self.button_update_loop}.hide()')
                guiLoopList.append(f'{self.button_remove_loop}.hide()')
                guiLoopList.append(f'{self.main_button_launch_loop}.hide()')
                UTILITYFuncs.alert(f"{self.name} was removed.", f"You just deleted {self.name}.")

            else:
                UTILITYFuncs.logAndPrint("INFO", "UIFuncs/removeApp: Your OS isn't supported! Please use Mac or Windows.")
                UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac or Windows.")

        except Exception as e:
            UTILITYFuncs.logAndPrint("INFO", f"UIFuncs/removeApp: There was a problem removing {self.name}! {e}")
            UTILITYFuncs.error(f"There was a problem removing {self.name}! {e}")

    def checkForUpdates(self):
        '''Check if the app needs updated'''
        global selectedApp
        global TruePath

        UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Checking if {self.name} exists or needs an update.")
        appname = self.name
        appname = appname.lower()
        appname = appname.replace(" ", "")
        AppMac = Path(f"{TruePath}{self.path}").exists()

        AppExists = Path(self.exe_location).exists()

        try:
            version_request = requests.get(self.version_url)
            version_request.raise_for_status()

        except Exception as e:
            UTILITYFuncs.logAndPrint("WARN", f"App/checkForUpdates: There was a problem checking {self.name} for updates! {e}")
            self.state = "ready"
            return False

        server_version_major = UTILITYFuncs.substring(version_request.text, "major=", ",minor")
        server_version_minor = UTILITYFuncs.substring(version_request.text, "minor=", ",patch")
        server_version_patch = UTILITYFuncs.substring(version_request.text, "patch=", "&")
        self.newVersion = f"{server_version_major}.{server_version_minor}.{server_version_patch}"
        
        if AppExists == True or AppMac == True:
            UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: {self.name} exists!")

            self.button_launch.show()
            self.button_download.hide()
            self.button_update.hide()
            self.button_remove.show()
            self.main_button_launch.show()
            
            AppVersionFileExists = Path(self.version_file_location).exists()
            if AppVersionFileExists == True:
                #It exists! Now check for updates
                UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Checking for updates for {self.name}!")
                version_file = open(self.version_file_location, "r")
                version_file_contents = version_file.readlines()

                local_version_major = version_file_contents[0]
                local_version_minor = version_file_contents[1]
                local_version_patch = version_file_contents[2]

                AppVersion = f"{local_version_major}.{local_version_minor}.{local_version_patch}"
                NewVersion = f"{server_version_major}.{server_version_minor}.{server_version_patch}"
                AppVersion = AppVersion.replace("\n", "")
                self.version = NewVersion

                if local_version_major < server_version_major:
                    self.state = "update"
                    self.button_launch.show()
                    self.button_download.hide()
                    self.button_update.show()
                    self.button_remove.show()
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates required. {local_version_major} < {server_version_major}")
                    UTILITYFuncs.alert(f"{self.name} Update Avaliable.", f"Open {self.name}'s menu to update to version {NewVersion}.")

                elif local_version_minor < server_version_minor:
                    self.state = "update"
                    self.button_launch.show()
                    self.button_download.hide()
                    self.button_update.show()
                    self.button_remove.show()
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates required. {local_version_minor} < {server_version_minor}")
                    UTILITYFuncs.alert(f"{self.name} Update Avaliable.", f"Open {self.name}'s menu to update to version {NewVersion}.")

                elif local_version_patch < server_version_patch:
                    self.state = "update"
                    self.button_launch.show()
                    self.button_download.hide()
                    self.button_update.show()
                    self.button_remove.show()
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates required. {local_version_patch} < {server_version_patch}")
                    UTILITYFuncs.alert(f"{self.name} Update Avaliable.", f"Open {self.name}'s menu to update to version {NewVersion}.")

                else:
                    self.state = "ready"
                    self.button_launch.show()
                    self.button_download.hide()
                    self.button_update.hide()
                    self.button_remove.show()
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates not required for {self.name}.")

            else:
                self.state = "ready"
                self.button_launch.show()
                self.button_download.hide()
                self.button_update.hide()
                self.button_remove.show()
                UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Version file does not exist for {self.name}.")
                        

        elif AppExists == False or AppMac == False:
            # It dosen't exist! Show button for downloading.
            UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: {self.name} dosen't exist!")
            self.state = "download"
            self.button_launch.hide()
            self.button_download.show()
            self.button_update.hide()
            self.button_remove.hide()

        else:
            #Unable to tell if it exists or not
            UTILITYFuncs.logAndPrint("WARN", f"App/checkForUpdates: Unable to tell if {self.name} exists or not.")
            UTILITYFuncs.error(f"Unable to tell if {self.name} exists or not!")



# ----------
# Functions
# ----------
'''
Note: I understand this is maybe not the best way to group functions,
but I feel this will help my code workflow. The old Jade Launcher
had a mess of functions, so I hope this will help
with organization.
UPDATE 6/12/22 when working on BETA 0.0.9: I wrote that way back when I started this program, and this technique has helped me in many ways.
'''
class UTILITYFuncs:
    '''A Group of functions for various utility purposes.'''
    
    def __init__(self):
        pass

    def log(tag, text):
        '''Log messages to JadeLauncherLog.txt'''
        global TruePath
        now = datetime.datetime.now()
        text = text.replace("\n", " ")
        try:
            logFile = open(f"{TruePath}JadeLauncherLog.txt", "a")
            logFile.write(f"\n[{now.month}/{now.day}/{now.year}] [{now.hour}:{now.minute}:{now.second}] |{tag}| >>> {text}")
        
        except Exception as e:
            print(f"There was a problem logging messgages to the log file! '{e}'")
            sys.exit()
        
        logFile.close()

    def getConnection(fromWhat):
        '''Get the connection status via https://google.com'''
        UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: Getting Connection Status from: {fromWhat}")
        try:
            gcRequest = requests.get("https://google.com")
            
            try:
                gcRequest.raise_for_status()

            except:
                UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: You're not connected! From: {fromWhat}")
                window_offline.show()
                dialog_about.idLabel.hide()
                dialog_about.id.hide()
                window_main.account_label.setText("You're offline")
                window_main.account_label.setFont(QFont("Calibri", 8))
                window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
                window_main.account_label.setStyleSheet("color: orange")
                UTILITYFuncs.alert("You're offline!", "Please connect to internet and restart.")
                return False

        except:
            UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: You're not connected! From: {fromWhat}")
            window_offline.show()
            dialog_about.idLabel.hide()
            dialog_about.id.hide()
            window_main.account_label.setText("You're offline")
            window_main.account_label.setFont(QFont("Calibri", 8))
            window_main.account_label.setAlignment(QtCore.Qt.AlignCenter)
            window_main.account_label.setStyleSheet("color: orange")
            UTILITYFuncs.alert("You're offline!", "Please connect to internet and restart.")
            return False

        
        UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: You're connected!")
        return True

    def substring(inputString, one, two):
        '''Get a string between two characters in another string'''
        global debug
        try:
            start = inputString.find(one) + len(one)

            try:
                end = inputString.find(two)
                
                try:
                    result = inputString[start:end]
        
                    if len(inputString) >= 100:
                        inputString = inputString[:100] + "..."

                    else:
                        UTILITYFuncs.logAndPrint("SUBSTRING", "Input string does not need to be shortened.")

                    if debug == True:
                        UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: Just substringed '{inputString}' with result '{inputString}'")
                        return result
                    else:
                        return result

                except:
                    UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: There was a problem finishing substringing with input '{inputString}'")
                    raise Exception("Could not finish substringing.")

            except:
                UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: Unable to find the second string with input '{inputString}'")
                raise Exception("Could not find the second string.")
        
        except:
            UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: Unable to find the first string with input '{inputString}'")
            raise Exception("Could not find the first string.")

    def error(Error):
        '''Custom error display'''
        global killThreads
        killThreads = True
        window_main.hide()
        window_createAccount.hide()
        window_signIn.hide()
        window_accountDetails.hide()
        dialog_error.ERROR.setText(Error)
        dialog_error.ERROR.setFont(QFont("Calibri", 14))
        dialog_error.show()
        print("-----")
        print("[ A Fatal Exception Occured ]")
        print("-----")
        print(Error)
        print("-----")
        UTILITYFuncs.logAndPrint("FATAL", f"UTILITYFuncs/error: A fatal exception occured: {Error}")

        app.exec()
        dialog_error.show()

    def logAndPrint(tag, text):
        '''Log to the log file and print it out'''
        UTILITYFuncs.log(tag, text)
        print(f"|{tag}| {text}")

    def alert(title, text):
        global developmental
        '''Show an alert'''
        UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/alert: Showing alert with title '{title}' and text '{text}'")
        dialog_alert.title.setText(title)
        dialog_alert.text.setText(text)
        dialog_alert.show()
        # Thanks to Цзыюнь Янь's answer here https://stackoverflow.com/questions/68531326/what-is-the-error-in-the-code-for-this-playsound-module-even-though-the-syntax-i
        if developmental == True:
            playsound.playsound("assets/audio/notification.mp3", block=False)

        else:
            playsound.playsound(resource_path("notification.mp3"), block=False)


class MAINFuncs:
    '''A Group of functions integral to the Launcher.'''
    global SignedIn
    global myAccount
    
    def __init__(self):
        pass

    def mainCode():
        '''The startup code for the Launcher. Will check for updates, sign in, fetch news, check for suspension, set the welcome message, update Id status and check Jade Assistant status.'''
        
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

        global developmental

        global jadeAssistantVersion
        global JadeAssistant

        global TruePath

        global update

        # That's a lot of global variables :)

        from timeit import default_timer as runDuration
        startElapsedTime = runDuration()

        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode: Main code thread started!")

        def show_message(text):
            text = text + "\n"
            if platform.system() == "Windows":
                window_splash.showMessage(text, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom, color=QtGui.QColor("white"))

            elif platform.system() == "Darwin":
                window_splash.showMessage(text, alignment=132 | 64)

            else:
                print("Your OS isn't supported! Please use Windows or Mac.")
                UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")

        def show_message_intro(text):
            if platform.system() == "Windows":
                intro_splash.showMessage(text, alignment=QtCore.Qt.AlignCenter, color=QtGui.QColor("white"))

            elif platform.system() == "Darwin":
                intro_splash.showMessage(text, alignment=132)

            else:
                print("Your OS isn't supported! Please use Windows or Mac.")
                UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")
        
        # Thanks to Liam on StackOverflow
        # https://stackoverflow.com/questions/58661539/create-splash-screen-in-pyqt5
        if platform.system() == "Windows":
            if developmental == False:
                splash_pix = QtGui.QPixmap(str(resource_path("JadeLauncherSplash.png")))

            elif developmental == True:
                splash_pix = QtGui.QPixmap(str(PurePath("assets/other/JadeLauncherSplash.png")))

            splash_pix = splash_pix.scaled(371, 254) # Scale down the splash screen so that it's not too big

            window_splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)

            screenSize = screen.size()
            moveHeight = screenSize.height() - 310
            window_splash.move(30, moveHeight)

            

            window_splash.setFont(QFont("Calibri", 18))
            show_message("Loading...")
            opaqueness = 0.0
            step = 0.05
            window_splash.setWindowOpacity(opaqueness)
            window_splash.show()
            while opaqueness < 1:
                window_splash.setWindowOpacity(opaqueness)
                sleep(0.01)
                opaqueness += step

            window_splash.setWindowOpacity(1)

        elif platform.system() == "Darwin":
            if developmental == False:
                splash_pix = QtGui.QPixmap(str(resource_path("JadeLauncherSplash.png")))

            elif developmental == True:
                splash_pix = QtGui.QPixmap(str(PurePath("assets/other/JadeLauncherSplash.png")))

            window_splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)

            screenSize = screen.size()
            moveHeight = screenSize.height() - 290
            window_splash.move(30, moveHeight)
            window_splash.setFont(QFont("Calibri", 24))
            window_splash.show()            
            show_message("Loading...")

        else:
            UTILITYFuncs.error("Your OS Isn't supported! Please use Windows or Mac.")


        # Check for updates
        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Checking for updates...")
        show_message("Checking for updates...")

        # Check for updates
        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Checking if there's an old update.")
        try:
            os.remove("Jade Launcher.exe.old")
        
        except:
            UTILITYFuncs.logAndPrint("WARN", "MAINFuncs/mainCode/checkForUpdates: Unable to remove 'Jade Launcher.exe.old'. does it exist?")

        if CONFIG_CheckForUpdates == True:
            gc = UTILITYFuncs.getConnection("mainCode/Check For Updates")
            if gc == True:
                try:
                    versionRequest = requests.get("https://nfoert.pythonanywhere.com/jadeLauncher/jadeLauncherVersion")
                    versionRequest.raise_for_status()

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"MAINFuncs/mainCode/checkForUpdates: There was a problem checking for updates. {e}")

                vrt = versionRequest.text
                requestMajor = UTILITYFuncs.substring(vrt, "major=", ",minor")
                requestMinor = UTILITYFuncs.substring(vrt, ",minor=", ",patch")
                requestPatch = UTILITYFuncs.substring(vrt, "patch=", "&")

                if versionRequest.ok == True:
                    UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Version requests are ok!")

                    requestMajor = int(requestMajor)
                    requestMinor = int(requestMinor)
                    requestPatch = int(requestPatch)

                    if Version_MAJOR < requestMajor:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates are avaliable. MAJOR")
                        update = "yes"

                    elif Version_MINOR < requestMinor:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates are avaliable. MINOR")
                        update = "yes"

                    elif Version_PATCH < requestPatch:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates are avaliable. PATCH")
                        update = "yes"

                    else:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates not required.")
                        update = "no"

                else:
                    UTILITYFuncs.logAndPrint("WARN", "MAINFuncs/mainCode/checkForUpdates: Version requests are not ok!")
                    update = "no"
                    window_splash.hide()
                    UTILITYFuncs.error("There was a problem checking for updates! Please check your")
                    window_status.jadeLauncher_download.hide()
                    window_status.jadeLauncher_install.hide()
                    window_status.jadeLauncher_status.setText("Error fetching update.")
                    return False
                
                if update == "yes":
                    #Update avaliable
                    UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: An update is avaliable.")
                    window_status.jadeLauncher_download.show()
                    window_status.jadeLauncher_install.hide()
                    window_status.jadeLauncher_status.setText(f"Update {requestMajor}.{requestMinor}.{requestPatch} is avaliable.")

                elif update == "no":
                    #No Update avaliable
                    UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: No update is avaliable.")
                    window_status.jadeLauncher_download.hide()
                    window_status.jadeLauncher_install.hide()
                    window_status.jadeLauncher_status.setText("Up to date.")


            elif gc == False:
                #Not connected
                UTILITYFuncs.logAndPrint("NOT CONNECTED", "MAINFuncs/mainCode/checkForUpdates: You're not connected! Skipping checking for updates.")
                update = False
                window_main.show()
                window_main.news1.hide()
                window_main.news2.hide()
                window_main.news3.hide()

        elif CONFIG_CheckForUpdates == False:
            UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Skipping checking for updates, as it's turned off.")

        else:
            UTILITYFuncs.logAndPrint("WARN", "MAINFuncs/mainCode/checkForUpdates: Skipping checking for updates, as we can't tell if it's turned off or on. '{CONFIG_CheckForUpdates}'")


        # Sign in
        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/authenticate: Signing in...")
        show_message("Signing you in...")

        if CONFIG_Authenticate == True:
            gc = UTILITYFuncs.getConnection("mainCode/Authenticate")
            if gc == True:
                UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/authenticate: Signing in...")
                myAccount.Authenticate()

            elif gc == False:
                UTILITYFuncs.logAndPrint("NOT CONNECTED", "MAINFuncs/mainCode/authenticate: Skipping signing in as you're not connected.")
                window_main.show()
                window_main.news1.hide()
                window_main.news2.hide()
                window_main.news3.hide()

            else:
                UTILITYFuncs.logAndPrint("WARN", "MAINFuncs/mainCode/authenticate: Skipping signing in as we can't tell if you're connected or not.")

        elif CONFIG_Authenticate == False:
            UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/authenticate: Skipping signing in as it's turned off.")

        else:
            UTILITYFuncs.logAndPrint("WARN", f"MAINFuncs/mainCode/authenticate: Skipping signing in as we can't tell if it's turned off or on. '{CONFIG_Authenticate}'")

        
        # Fetch news
        UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Fetching news...")
        show_message("Fetching news...")
        
        if CONFIG_FetchNews == True:
            gc = UTILITYFuncs.getConnection("mainCode/fetchNews")
            if gc == True:
                UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Fetching news...")
                UTILITYFuncs.log("INFO", "Fetching news...")
                try:
                    newsCodeRequest = requests.get("https://nfoert.pythonanywhere.com/jadeLauncher/returnNews")
                    newsCodeRequest.raise_for_status

                except Exception as e:
                    UTILITYFuncs.logAndPrint("FATAL", f"THREADFuncs/mainCode/fetchNews: There was a problem fetching news. AT: Get news codes {e}")
                    UTILITYFuncs.error(f"There was a problem fetching news. AT: Get news codes {e}")
                    return False

                ncrText = newsCodeRequest.text
                try:
                    newsCode1 = UTILITYFuncs.substring(ncrText, "1=", ",2=")
                    newsCode2 = UTILITYFuncs.substring(ncrText, "2=", ",3=")
                    newsCode3 = UTILITYFuncs.substring(ncrText, "3=", "&")

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews:There was a problem substringing the codes out of the news code request. {e}")
                    window_main.news1.hide()
                    window_main.news2.hide()
                    window_main.news3.hide()

                try:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Getting news requests...")
                    newsRequest1 = requests.get(f"https://nfoert.pythonanywhere.com/jadeLauncher/news?{newsCode1}&")
                    newsRequest2 = requests.get(f"https://nfoert.pythonanywhere.com/jadeLauncher/news?{newsCode2}&")
                    newsRequest3 = requests.get(f"https://nfoert.pythonanywhere.com/jadeLauncher/news?{newsCode3}&")
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Done.")

                except Exception as e:
                    UTILITYFuncs.logAndPrint("FATAL", f"THREADFuncs/mainCode/fetchNews: There was a problem getting the news requests. {e}")
                    UTILITYFuncs.error(f"There was a problem getting the news requests. {e}")
                    return False

                if newsRequest1.ok == True:
                    pass
                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: NEWS 1 FAIL")
                    window_main.news1.hide()

                if newsRequest2.ok == True:
                    pass
                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: NEWS 2 FAIL")
                    window_main.news2.hide()

                if newsRequest3.ok == True:
                    pass
                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: NEWS 3 FAIL")
                    window_main.news3.hide()
                    
                
                # News 1
                nr1Text = newsRequest1.text
                if "header=" in nr1Text:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: News 1 is good!")
                    news1Header = UTILITYFuncs.substring(nr1Text, "header=", ",text")
                    news1Text = UTILITYFuncs.substring(nr1Text, ",text=", ",date")
                    news1Date = UTILITYFuncs.substring(nr1Text, ",date=", ",url")
                    news1Url = UTILITYFuncs.substring(nr1Text, ",url=", "&")

                    window_main.header1.setText(f"{news1Header[:15]}...")
                    window_main.header1.setFont(QFont('Calibri Bold', 14))
                    window_main.header1.setAlignment(QtCore.Qt.AlignCenter)

                    try:
                        window_main.text1.setText(f"{news1Text[:150]}...")
                        window_main.text1.setFont(QFont('Calibri', 11))
                    except:
                        window_main.text1.setText(news1Text)

                    window_main.text1.setFont(QFont("Calibri", 10))



                elif "There is no news article that matches that code." in nr1Text:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 1. Code is '{newsCode1}'")
                    window_main.news1.hide()

                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There was a problem validating the first news request.")
                    window_main.news1.hide()

                # News 2
                nr2Text = newsRequest2.text
                if "header=" in nr2Text:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: News 2 is good!")
                    news2Header = UTILITYFuncs.substring(nr2Text, "header=", ",text")
                    news2Text = UTILITYFuncs.substring(nr2Text, ",text=", ",date")
                    news2Date = UTILITYFuncs.substring(nr2Text, ",date=", ",url")
                    news2Url = UTILITYFuncs.substring(nr2Text, "url=", "&")

                    window_main.header2.setText(f"{news2Header[:15]}...")
                    window_main.header2.setFont(QFont('Calibri Bold', 14))
                    window_main.header2.setAlignment(QtCore.Qt.AlignCenter)
                    
                    try:
                        window_main.text2.setText(f"{news2Text[:150]}...")
                        window_main.text2.setFont(QFont('Calibri', 11))
                    except:
                        window_main.text2.setText(news2Text)

                    window_main.text2.setFont(QFont("Calibri", 10))

                elif "There is no news article that matches that code." in nr2Text:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 2. Code is '{newsCode2}'")
                    window_main.news2.hide()

                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There was a problem validating the second news request.")
                    window_main.news2.hide()

                # News 3
                nr3Text = newsRequest3.text
                if "header=" in nr3Text:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: News 3 is good!")
                    news3Header = UTILITYFuncs.substring(nr3Text, "header=", ",text")
                    news3Text = UTILITYFuncs.substring(nr3Text, ",text=", ",date")
                    news3Date = UTILITYFuncs.substring(nr3Text, ",date=", ",url")
                    news3Url = UTILITYFuncs.substring(nr3Text, ",url=", "&")

                    window_main.header3.setText(f"{news3Header[:15]}...")
                    window_main.header3.setFont(QFont('Calibri Bold', 14))
                    window_main.header3.setAlignment(QtCore.Qt.AlignCenter)

                    try:
                        window_main.text3.setText(f"{news3Text[:150]}...")
                        window_main.text3.setFont(QFont('Calibri', 11))
                    except:
                        window_main.text3.setText(news3Text)

                    window_main.text3.setFont(QFont("Calibri", 10))


                elif "There is no news article that matches that code." in nr3Text:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 3. Code is '{newsCode3}'")
                    window_main.news3.hide()

                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There was a problem validating the third news request.")
                    window_main.news3.hide()


                # Check for emptiness deep inside themselves
                if newsCode1 == "000":
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Hiding news 1 as the code is 000.")
                    window_main.news1.hide()

                else:
                    pass

                if newsCode2 == "000":
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Hiding news 2 as the code is 000.")
                    window_main.news1.hide()

                else:
                    pass

                if newsCode3 == "000":
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Hiding news 3 as the code is 000.")
                    window_main.news3.hide()

                else:
                    pass


                # Set news classes
                try:
                    news1.header = news1Header
                    news1.text = news1Text
                    news1.date = news1Date
                    news1.url = news1Url
                    news1.code = newsCode1
                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews:There was a problem setting up news1 Class. {e}")
                    window_main.news1.hide()
                
                try:
                    news2.header = news2Header
                    news2.text = news2Text
                    news2.date = news2Date
                    news2.url = news2Url
                    news2.code = newsCode2
                
                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There was a problem setting up news2 Class. {e}")
                    window_main.news2.hide()

                try:
                    news3.header = news3Header
                    news3.text = news3Text
                    news3.date = news3Date
                    news3.url = news3Url
                    news3.code = newsCode3

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There was a problem setting up news3 Class. {e}")
                    window_main.news3.hide()


            elif gc == False:
                UTILITYFuncs.logAndPrint("NOT CONNECTED", "THREADFuncs/mainCode/fetchNews: Skipping fetching of news as you're not conected.")
                window_main.news1.hide()
                window_main.news2.hide()
                window_main.news3.hide()

                window_main.show()

            else:
                UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: Skipping fetching of news as we can't decide if you're connected or not.")
                window_main.news1.hide()
                window_main.news2.hide()
                window_main.news3.hide()



        elif CONFIG_FetchNews == False:
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Skipping fetching of news as it's not allowed.")
            window_main.news1.hide()
            window_main.news2.hide()
            window_main.news3.hide()

        
        else:
            UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: Skipping news fetch as we can't determine if it's allowed or not.")

        # Update Id
        UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/updateLauncherId: Updating Launcher Id...")
        show_message("Updating Launcher ID...")
        Launcher.getId()
        Launcher.username = myAccount.username
        Launcher.updateStatus()

        # Set greeting
        UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Setting greeting...")
        show_message("Setting greeting message...")
        now = datetime.datetime.now().hour
        now = str(now)
        if len(now) == 1:
            now = f"0{now}"

        else:
            now = now

        if any(x in now for x in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]) == True:
            window_main.welcomeBox_text.setText("Good morning.")
            welcomeMessage = "Good morning."
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message: Good morning.")

        elif any(x in now for x in ["12", "13", "14", "15"]) == True:
            window_main.welcomeBox_text.setText("Good afternoon.")
            welcomeMessage = "Good afternoon."
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message: Good afternoon.")

        elif any(x in now for x in ["16", "17", "18", "19", "20", "21", "22", "23"]) == True:
            window_main.welcomeBox_text.setText("Good evening.")
            welcomeMessage = "Good evening."
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message: Good evening.")

        else:
            window_main.welcomeBox_text.setText("Welcome to the Jade Launcher.")
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message (hit else): Welcome back to the Jade Launcher")


        window_main.welcomeBox_text.setFont(QFont("Arial Bold", 18))
        window_main.welcomeBox_text.setAlignment(QtCore.Qt.AlignLeft)

        
        # Check if Jade Assistant exists, or needs an update.
        show_message("Loading Jade Assistant...")
        try:
            os.mkdir("./apps/")
        except Exception as e:
            print(e)
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/loadJadeAssistant: The directories already exist!")
        
        try:
            os.mkdir("./apps/jadeassistant/")
        except Exception as e:
            print(e)
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/loadJadeAssistant: The directories already exist!")
        
        jadeAssistantCheck = Path("Jade Assistant.exe")
        if jadeAssistantCheck.exists():
            os.rename("Jade Assistant.exe", "./apps/jadeassistant/Jade Assistant.exe")

        else:
            UTILITYFuncs.logAndPrint("INFO", "loadJadeAssistant: Jade Assistant does not exist, so no moving is required.")
        JadeAssistant.checkForUpdates()

        # Check if Jade Apps exists, or needs an update.
        show_message("Loading Jade Apps...")
        try:
            os.mkdir("./apps/jadeapps/")
        except Exception as e:
            print(e)
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/loadJadeApps: The directories already exist!")
        
        JadeApps.checkForUpdates()

        # Check if "Jade Launcher.exe.download" exists
        jadeLauncherUpdateCheck = Path("Jade Launcher.exe.download")
        if jadeLauncherUpdateCheck.exists():
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/loadJadeLauncher: The Jade Launcher update exists!")
            window_status.jadeLauncher_download.hide()
            window_status.jadeLauncher_install.show()

        else:
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/loadJadeLauncher: The Jade Launcher update does not exist.")
            if update == "yes":
                window_status.jadeLauncher_download.show()
                window_status.jadeLauncher_install.hide()

            else:
                window_status.jadeLauncher_download.hide()
                window_status.jadeLauncher_install.hide()

        # Check for suspension
        if myAccount.suspended == "no":
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/suspensionCheck: Not suspended.")
            show_message("Done!")
            sleep(1.5)
            window_splash.hide()
            if developmental == False:
                intro_pix = QtGui.QPixmap(str(resource_path("intro.png")))

            elif developmental == True:
                intro_pix = QtGui.QPixmap(str(PurePath("assets/other/intro.png")))

            intro_pix = intro_pix.scaled(519, 344) #Scale down the intro screen so it's not so big

            introConfig = jadelauncher_config.getValue("intro")
            if introConfig == "true":
                UTILITYFuncs.logAndPrint("INFO", "Showing the intro!")
                intro_splash = QtWidgets.QSplashScreen(intro_pix, QtCore.Qt.WindowStaysOnTopHint)
                intro_splash.setFont(QFont("Calibri",30))
                show_message_intro(welcomeMessage)
                opaqueness = 0.0
                step = 0.05
                intro_splash.setWindowOpacity(opaqueness)
                intro_splash.show()
                while opaqueness < 1:
                    intro_splash.setWindowOpacity(opaqueness)
                    sleep(0.01)
                    opaqueness += step

                intro_splash.setWindowOpacity(1)

                sleep(5)
                
                opaqueness = 1.0
                step = 0.05
                intro_splash.setWindowOpacity(opaqueness)
                intro_splash.show()
                while opaqueness > 0:
                    intro_splash.setWindowOpacity(opaqueness)
                    sleep(0.01)
                    opaqueness -= step

                intro_splash.setWindowOpacity(0)

                sleep(1)

            elif introConfig == "false":
                UTILITYFuncs.logAndPrint("INFO", "Not showing the intro as it's turned off.")

            else:
                UTILITYFuncs.error("The value set for 'intro' in the config was not recognized!")

            
            newScreen = jadelauncher_config.getValue("new")
            if platform.system() == "Windows":
                if newScreen == "true":
                    window_new.show()

                else:
                    # Bring window to front
                    # Thanks to Kevin Newman's answer here https://stackoverflow.com/questions/12118939/how-to-make-a-pyqt4-window-jump-to-the-front
                    window_main.setWindowFlags(window_main.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
                    window_main.show()
                    window_main.setWindowFlags(window_main.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint) # clear always on top flag, makes window disappear
                    window_main.show()

            elif platform.system() == "Darwin":
                if newScreen == "true":
                    window_new.show()

                else:
                    window_main.show()

        else:
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/suspensionCheck: Suspended.")
            window_splash.hide()
            dialog_accountSuspended.show()

        elapsedTime = runDuration() - startElapsedTime
        elapsedTime = round(elapsedTime)
        window_splash.hide()

        UTILITYFuncs.logAndPrint("INFO", f"THREADFuncs/mainCode: Finished! Took {elapsedTime} seconds.")
        


        print("=================================")
        print("MAINFuncs/mainCode/: Finished! ")
        print("=================================")
            
class UIFuncs:
    '''A group of functions that the UI uses.'''
    global SignedIn
    
    def __init__(self):
        pass

    # Offline Screen
    def closeOffline():
        global TruePath

        window_offline.hide()
        jadeStatus.setStatus("offline")
        window_main.show()
        window_main.news1.hide()
        window_main.news2.hide()
        window_main.news3.hide()
        window_main.newsLabel.hide()
        window_main.line.hide()
        window_main.allNews.hide()
        window_main.status_bar.setText("You're offline! Connect to the internet, then restart the Launcher.")
        window_main.jadeAssistant_status.hide()
        window_main.jadeApps_status.hide()

        if developmental:
            if Path(f"./apps/jadeassistant/Jade Assistant.exe").exists():
                window_main.jadeAssistant_launch.show()

            if Path(f"./apps/jadeapps/Jade Apps.exe").exists():
                window_main.jadeApps_launch.show()

        else:
            if Path(f"{TruePath}/apps/jadeassistant/Jade Assistant.exe").exists():
                window_main.jadeAssistant_launch.show()

            if Path(f"{TruePath}/apps/jadeapps/Jade Apps.exe").exists():
                window_main.jadeApps_launch.show()

        

    # Main Screen
    def openAccountScreen():
        gc = UTILITYFuncs.getConnection("openAccountScreen")
        if gc == True:
            if SignedIn == True:
                window_accountDetails.show()

            elif SignedIn == False:
                window_signIn.show()

            else:
                UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openAccountScreen: There was a problem checking if you're signed in or not to open the Account screen.")

        elif gc == False:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openAccountScreen: You're not connected!")

        else:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openAccountScreen: Unable to determine connectivity.")

    def stopAll():
        global killThreads
        killThreads = True
        sys.exit()

    def signInButton():
        myAccount.signIn()

    def signOutButton():
        myAccount.signOut()

    def jadeAssistantButton():
        global SignedIn
        global selectedApp
        global TruePath
        gc = UTILITYFuncs.getConnection("Open Jade Assistant Menu")
        if gc == True:
            if SignedIn == True:
                selectedApp = "Jade Assistant"
                JadeAssistant.openAppMenu()

            else:
                UTILITYFuncs.alert("You're not signed in!", "Sign in first, then try again.")

        else:
            accountFile = open(f"{TruePath}account.txt", "r")
            accountFileRead = accountFile.readlines()
            accountFile.close()

            if len(accountFileRead) == 2:
                selectedApp = "Jade Assistant"
                JadeAssistant.state = "readyoffline"
                JadeAssistant.openAppMenu()

            else:
                UTILITYFuncs.alert("You're not signed in!", "Connnect to internet, restart the Launcher, sign in, then try again.")

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
            UTILITYFuncs.logAndPrint("WARN", "UIFuncs/passwordToggle: There was a problem setting show/hide password.")

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
        if platform.system() == "Windows":
            WEBVIEW.openWebView("https://nofoert.wixsite.com/jade/blog/categories/changelogs")

        elif platform.system() == "Darwin":
            webbrowser.open("https://nofoert.wixsite.com/jade/blog/categories/changelogs")

        else:
            UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")

    #Expanded news
    def openUrlButton():
        global expanded
        global news1
        global news2
        global news3

        if expanded == "0":
            UTILITYFuncs.logAndPrint("WARN", "UIFuncs/openUrlButton: There was a problem expanding news. Nothing is actually expanded?")

        elif expanded == "1":
            news1.openUrl()

        elif expanded == "2":
            news2.openUrl()

        elif expanded == "3":
            news3.openUrl()

        else:
            UTILITYFuncs.logAndPrint("WARN", "UIFuncs/openUrlButton: There was a problem determining what news article to open a url for.")

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
                UTILITYFuncs.logAndPrint("WARN", f"UIFuncs/restartAction: There was a problem restarting. {e}")

        elif platform.system == "Darwin":
            try:
                subprocess.Popen("Jade Launcher")
                sys.exit()

            except Exception as e:
                UTILITYFuncs.logAndPrint("INFO", f"UIFuncs/restartAction: There was a problem restarting. {e}")

    def openAbout():
        dialog_about.show()

    def aboutWebsiteButton():
        WEBVIEW.openWebView("https://nofoert.wixsite.com/jade")

    def aboutLogButton():
        if platform.system() == 'Darwin':
            subprocess.call(('open', "JadeLauncherLog.txt"))

        elif platform.system() == 'Windows':
            os.startfile("JadeLauncherLog.txt")

        else:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/aboutLogButton: Your OS isn't supported! Please use Windows or Mac.")
            UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")

    def openChangePassword():
        window_accountDetails.hide()
        global myAccount
        try:
            createVerificationCode = requests.get(f"https://nfoert.pythonanywhere.com/jadeCore/createVerificationCode?username={myAccount.username},password={myAccount.password}&")
            createVerificationCode.raise_for_status()
            print(createVerificationCode.text)
            window_changePassword.label.setText(f"We just sent a verification code to {myAccount.email}. Please enter it below.")
            window_changePassword.label.setFont(QFont("Calibri", 8))
            window_changePassword.label.setAlignment(QtCore.Qt.AlignCenter)
            window_changePassword.show()

        except Exception as e:
            UTILITYFuncs.logAndPrint("WARN", f"UIFuncs/openChangePassword: There was a problem creating a verification code. '{e}'")
            UTILITYFuncs.alert("There was a problem creating a verification code.", f"{e}")

    def changePassword():
        myAccount.changePassword()

    # App Functions
    def launchApp():
        global selectedApp
        if selectedApp == "Jade Assistant":
            JadeAssistant.launchApp()

        else:
            return False

    def removeApp():
        global selectedApp
        if selectedApp == "Jade Assistant":
            JadeAssistant.removeApp()

        else:
            return False
    
    def downloadApp():
        global selectedApp
        if selectedApp == "Jade Assistant":
            JadeAssistant.downloadAppVar = True

        else:
            return False

    def updateApp():
        global selectedApp
        if selectedApp == "Jade Assistant":
            JadeAssistant.updateAppVar = True

        else:
            return False

    def notNowUpdate():
        window_update.hide()

    def debugOpenAllWindows():
        global debugOpenAllWindows
        if debugOpenAllWindows == True:
            UTILITYFuncs.logAndPrint("DEBUG", "Opening all windows! (Much chaos ahead, beware!)")
            window_accountDetails.show()
            window_offline.show()
            window_changePassword.show()
            window_createAccount.show()
            window_changePassword.show()
            window_main.show()
            window_signIn.show()
            UTILITYFuncs.alert("Debug: Show all windows!", "This window was opened to assist in UI related debug related to apperances. test test test test test test test test test test test test test test test test test test thank you")
            window_update.show()
            dialog_about.show()
            dialog_accountSuspended.show()
            dialog_error.show()
            dialog_signInFailure.show()
            if platform.system() == "Windows":
                window_webView.show()

    def openStatus():
        JadeAssistant.openAppMenu()
        JadeApps.openAppMenu()

#Jade Assistant
    def launchJadeAssistant():
        JadeAssistant.launchApp()

    def updateJadeAssistant():
        JadeAssistant.updateAppVar = True

    def downloadJadeAssistant():
        UTILITYFuncs.logAndPrint("INFO", "Set variable for downloading Jade Assistant!")
        JadeAssistant.downloadAppVar = True

    def removeJadeAssistant():
        JadeAssistant.removeApp()


# Jade Apps
    def launchJadeApps():
        JadeApps.launchApp()

    def updateJadeApps():
        JadeApps.updateAppVar = True

    def downloadJadeApps():
        UTILITYFuncs.logAndPrint("INFO", "Set variable for downloading Jade Apps!")
        JadeApps.downloadAppVar = True

    def removeJadeApps():
        JadeApps.removeApp()


    def allNewsButton():
        WEBVIEW.openWebView("https://nfoert.pythonanywhere.com/jadesite/allposts")

    def settingsButton():
        # Get values
        introConfig = jadelauncher_config.getValue("intro")
        newConfig = jadelauncher_config.getValue("new")

        # Set checkboxes
        if introConfig == "true":
            window_settings.intro.setChecked(True)

        elif introConfig == "false":
            window_settings.intro.setChecked(False)

        else:
            UTILITYFuncs.logAndPrint("WARN", "Config: 'intro' value not recognized")

        if newConfig == "true":
            window_settings.newScreen.setChecked(True)

        elif newConfig == "false":
            window_settings.newScreen.setChecked(False)

        else:
            UTILITYFuncs.logAndPrint("WARN", "Config: 'new' value not recognized")


        # Show window
        window_settings.show()

    def saveSettings():
        UTILITYFuncs.logAndPrint("INFO", "Saving settings...")
        if window_settings.intro.isChecked():
            jadelauncher_config.setValue("intro", "true")

        else:
            jadelauncher_config.setValue("intro", "false")

        if window_settings.newScreen.isChecked():
            jadelauncher_config.setValue("new", "true")

        else:
            jadelauncher_config.setValue("new", "false")

        window_settings.hide()
        UTILITYFuncs.logAndPrint("INFO", "Done saving settings.")

    def updateJadeLauncher():
        # Start the update thread
        global downloadUpdateVar
        downloadUpdateVar = True

    def installJadeLauncher():
        global installUpdateVar
        installUpdateVar = True
        UTILITYFuncs.logAndPrint("INFO", "UIFuncs/installJadeLuancher: Set the variable for starting the installer thread.")

    def cancelInstallUpdate():
        global cancelInstallUpdateVar
        UTILITYFuncs.logAndPrint("INFO", "UIFuncs/cancelInstallUpdate: Update canceled.")
        cancelInstallUpdateVar = True

    def closeAlert():
        dialog_alert.hide()

    def getStartedNew():
        if window_new.showAgain.isChecked():
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/getStartedNew: Set the value for showing the new screen to false.")
            jadelauncher_config.setValue("new", "false")

        else:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/getStartedNew: Not effecting the config value for the what's new screen.")

        window_new.hide()
        if platform.system() == "Windows":
            # Bring window to front
            # Thanks to Kevin Newman's answer here https://stackoverflow.com/questions/12118939/how-to-make-a-pyqt4-window-jump-to-the-front
            window_main.setWindowFlags(window_main.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
            window_main.show()
            window_main.setWindowFlags(window_main.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint) # clear always on top flag, makes window disappear
            window_main.show()

        elif platform.system() == "Darwin":
            window_main.show()

    def goToLauncherUpdate():
        window_update.hide()
        UIFuncs.openStatus()
        window_status.show()

    def openChangelog():
        UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openChangelog: Opened the changelog.")
        WEBVIEW.openWebView("https://nfoert.pythonanywhere.com/jadesite/allposts/?category=changelog&")

    def uninstallAsk():
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("Jade Launcher | Uninstall")
        dlg.setText("Are you sure that you want to uninstall the Jade Launcher? This will remove everything including your installed apps and settings.")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Yes:
            UTILITYFuncs.logAndPrint("INFO", "Opening the uninstall utility...")
            window_settings.hide()
            window_main.hide()
            try:
                subprocess.Popen("./unins000.exe")
                sys.exit()

            except FileNotFoundError:
                UTILITYFuncs.logAndPrint("WARN", "Unable to find the uninstall script!")
                dlg = QtWidgets.QMessageBox()
                dlg.setWindowTitle("Jade Launcher | Uninstall")
                dlg.setText("Unable to locate the uninstall script.")
                dlg.setStandardButtons(QtWidgets.QMessageBox.Ok )
                dlg.setIcon(QtWidgets.QMessageBox.Warning)
                button = dlg.exec()
                
                if button == QtWidgets.QMessageBox.Ok:
                    UTILITYFuncs.logAndPrint("INFO", "Quitting...")
                    sys.exit()
            
        else:
            UTILITYFuncs.logAndPrint("INFO", "Not uninstalling the Jade Launcher.")
        

    # -----

# ----------
# Threads
# ----------

def downloadUpdateThread():
    global downloadUpdateVar
    global guiLoopList
    global killThreads

    UTILITYFuncs.logAndPrint("INFO", "Threads/downloadUpdateThread: Thread started.")


    while killThreads == False:
        if downloadUpdateVar == True:
            guiLoopList.append('window_status.jadeLauncher_download.hide()')
            guiLoopList.append('window_status.jadeLauncher_install.hide()')
            guiLoopList.append('window_status.jadeLauncher_status.setText("One moment...")')
            guiLoopList.append('window_main.status_bar.setText("Loading Jade Launcher update...")')
            guiLoopList.append('jadeStatus.setStatus("load")')

            UTILITYFuncs.logAndPrint("INFO", "Threads/downloadUpdateThread: Updating...")

            gc = UTILITYFuncs.getConnection("Threads/downloadUpdateThread")
            if gc == True:
                UTILITYFuncs.logAndPrint("INFO", "Threads/downloadUpdateThread: You're connected!")
                try:
                    UTILITYFuncs.logAndPrint("INFO", "Threads/downloadUpdateThread: Making download request...")
                    LauncherUpdate = requests.get("https://nfoert.pythonanywhere.com/jadeLauncher/download?Windows&", stream=True, timeout=60)
                    LauncherUpdate.raise_for_status()
                except TimeoutError:
                    UTILITYFuncs.logAndPrint("WARN", "Threads/downloadUpdateThread: 10 second timeout reached when downloading the update for the Jade Launcher.")
                    guiLoopList.append('window_status.jadeLauncher_download.show()')
                    guiLoopList.append('window_status.jadeLauncher_install.hide()')
                    guiLoopList.append('window_status.jadeLauncher_status.setText("There was a problem downloading the update.")')
                    guiLoopList.append('window_main.status_bar.setText("There was a problem downloading the update for the Jade Launcher.")')
                    guiLoopList.append('jadeStatus.setStatus("ok")')
                    downloadUpdateVar = False
                    continue

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"Threads/downloadUpdateThread: There was a problem making the download request. '{e}'")
                    guiLoopList.append('window_status.jadeLauncher_download.show()')
                    guiLoopList.append('window_status.jadeLauncher_install.hide()')
                    guiLoopList.append('window_status.jadeLauncher_status.setText("There was a problem making the update request.")')
                    guiLoopList.append('window_main.status_bar.setText("There was a problem making the update request for the Jade Launcher.")')
                    guiLoopList.append('jadeStatus.setStatus("ok")')
                    downloadUpdateVar = False
                    continue

            else:
                UTILITYFuncs.logAndPrint("INFO", "Threads/downloadUpdateThread: You're not connected!")
                guiLoopList.append('window_status.jadeLauncher_download.hide()')
                guiLoopList.append('window_status.jadeLauncher_install.hide()')
                guiLoopList.append('window_status.jadeLauncher_status.setText("You\'re not connected!")')
                guiLoopList.append('window_main.status_bar.setText("There was a problem downloading the update for the Jade Launcher. You\'re not connected!")')
                guiLoopList.append('jadeStatus.setStatus("offline")')
                downloadUpdateVar = False
                continue

            total_size_in_bytes = int(LauncherUpdate.headers.get('content-length', 0))
            bytes_downloaded = 0
            last = 0

            downloadLocation = "Jade Launcher.exe.download"

            with open(downloadLocation, "wb") as file:
                for data in LauncherUpdate.iter_content(1024):
                    file.write(data)
                    bytes_downloaded = bytes_downloaded + 1024
                    percent = bytes_downloaded / total_size_in_bytes
                    percent = percent * 100
                    percent = round(percent)
                    if last != percent:
                        last = percent
                        guiLoopList.append(f'window_status.jadeLauncher_status.setText(f"Downloading update... [{percent}%]")')
                        guiLoopList.append(f'window_main.status_bar.setText(f"Downloading an update for the Jade Launcher... [{percent}%]")')

                    else:
                        continue

            file.close()

            guiLoopList.append('window_status.jadeLauncher_status.setText("Update downloaded!")')
            guiLoopList.append('window_status.jadeLauncher_download.hide()')
            guiLoopList.append('window_status.jadeLauncher_install.show()')
            guiLoopList.append('window_main.status_bar.setText("Jade Launcher update downloaded!")')

            guiLoopList.append('UTILITYFuncs.alert("Jade Launcher update was downloaded.", "Open the app status menu to install the update.")')
            UTILITYFuncs.logAndPrint("INFO", "Threads/downloadUpdateThread: Done updating.")

            guiLoopList.append('jadeStatus.setStatus("ok")')

            downloadUpdateVar = False
            continue


        else:
            sleep(0.1)
            continue


def installUpdateThread():
    global installUpdateVar
    global killThreads
    global cancelInstallUpdateVar
    UTILITYFuncs.logAndPrint("INFO", "Threads/installUpdateThread: Thread started.")

    while True:
        if installUpdateVar == True:
            cancel = False
            cancelInstallUpdateVar = False
            guiLoopList.append('window_status.jadeLauncher_download.hide()')
            guiLoopList.append('window_status.jadeLauncher_install.hide()')
            guiLoopList.append('window_status.jadeLauncher_cancel.show()')
            for i in range(5, 0, -1): #Counts down. range(start, end, step) Thanks to Burger King's answer here: https://stackoverflow.com/questions/29292133/how-to-count-down-in-for-loop
                if cancelInstallUpdateVar == True:
                    UTILITYFuncs.logAndPrint("INFO", "Threads/installUpdateThread: Canceling the installing of the Jade Launcher update.")
                    guiLoopList.append('window_status.jadeLauncher_download.hide()')
                    guiLoopList.append('window_status.jadeLauncher_install.show()')
                    guiLoopList.append('window_status.jadeLauncher_cancel.hide()')
                    guiLoopList.append('window_status.jadeLauncher_status.setText("Installing update aborted.")')
                    installUpdateVar = False
                    cancel = True
                    
                
                else:
                    guiLoopList.append(f'window_status.jadeLauncher_status.setText("Installing in {i} seconds...")')
                    sleep(1)

            if cancel == True:
                UTILITYFuncs.logAndPrint("INFO", "Threads/installUpdateThread: Not installing update, as it was canceled.")

            else:
                guiLoopList.append('window_status.jadeLauncher_cancel.hide()')

                guiLoopList.append('window_status.jadeLauncher_status.setText("Installing now...")')
                sleep(2)

                # Thanks to Maxim Egorushkin's answer here: https://stackoverflow.com/questions/9162969/how-can-a-c-binary-replace-itself
                os.rename("Jade Launcher.exe", "Jade Launcher.exe.old")
                os.rename("Jade Launcher.exe.download", "Jade Launcher.exe")

                killThreads = True

                # Thanks to jfs' answer here: https://stackoverflow.com/questions/14797236/python-howto-launch-a-full-process-not-a-child-process-and-retrieve-the-pid
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008

                try:
                    subprocess.Popen("Jade Launcher.exe", creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP) #TODO: BROKEN IDK WHY HELP HELP HELP
                    installUpdateVar = False
                    guiLoopList.append('app.closeAllWindows()') #FIXME: IT"S ALL A MESS BROKEN NOT WORKING ASDHFJKHAJKFJKASDHFKJKA
                    guiLoopList.append('app.quit()')
                    sys.exit()
                
                except Exception as e:
                    UTILITYFuncs.error(e)

                

        else:
            sleep(0.1)
            continue

def checkForRunningAppsThread(): # TODO: Coming in 2.1.0
    print("Threads:/checkForRunningAppsThread: Thread started.")
    while True:
        # Thanks to https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
        # and Mark's answer here: https://stackoverflow.com/questions/7787120/check-if-a-process-is-running-or-not-on-windows
        for proc in psutil.process_iter():
            if proc.name() == "Jade Assistant.exe":
                print("=================== ASSISTANCY ===================")
                print("Jade Assistant is running!")
                guiLoopList.append('window_status.jadeAssistant_launch.hide()')
                guiLoopList.append('window_status.jadeAssistant_remove.hide()')
                guiLoopList.append('window_status.jadeAssistant_stop.show()')
                guiLoopList.append('window_status.jadeAssistant_status.setText("Jade Assistant is running.")')
                sleep(2)

            elif proc.name() == "Jade Apps.exe":
                print("Jade Apps is running!")
                guiLoopList.append('window_status.jadeApps_launch.hide()')
                guiLoopList.append('window_status.jadeApps_remove.hide()')
                guiLoopList.append('window_status.jadeApps_stop.show()')
                guiLoopList.append('window_status.jadeApps_status.setText("Jade Apps is running.")')
                sleep(2)

            else:
                guiLoopList.append('window_status.jadeAssistant_launch.show()')
                guiLoopList.append('window_status.jadeAssistant_remove.show()')
                guiLoopList.append('window_status.jadeAssistant_stop.hide()')

                guiLoopList.append('window_status.jadeApps_launch.show()')
                guiLoopList.append('window_status.jadeApps_remove.show()')
                guiLoopList.append('window_status.jadeApps_stop.hide()')


# Start threads
downloadUpdateManager = threading.Thread(target=downloadUpdateThread, daemon=True)
downloadUpdateManager.start()

installUpdateManager = threading.Thread(target=installUpdateThread, daemon=True)
installUpdateManager.start()

checkForRunningAppsThreadManager = threading.Thread(target=checkForRunningAppsThread, daemon=True)
#checkForRunningAppsThreadManager.start() TODO: Coming in 2.1.0

    

# ----------
# Starting prints & logs
# ----------

print("----------")
print("Jade Launcher")
print(f"Version: {Version_MAJOR}.{Version_MINOR}.{Version_PATCH}")
print("----------")

UTILITYFuncs.log("INFO", " ")
UTILITYFuncs.log("INFO", "-----")
UTILITYFuncs.log("INFO", f"| Jade Launcher | Version: {Version_MAJOR}.{Version_MINOR}.{Version_PATCH}")
UTILITYFuncs.log("INFO", "-----")

# ----------
# PyQt5
# ----------

# Create Windows
app = QtWidgets.QApplication(sys.argv)
screen = app.primaryScreen()

if developmental == False:
    UTILITYFuncs.logAndPrint("INFO", "PyQt5: Loading like it's an executable.")
    # Load like an exe
    try:
        window_accountDetails = uic.loadUi(str(PurePath(resource_path("accountDetails.ui"))))
        window_createAccount = uic.loadUi(str(PurePath(resource_path("createAccount.ui"))))
        window_main = uic.loadUi(str(PurePath(resource_path("main.ui"))))
        window_offline = uic.loadUi(str(PurePath(resource_path("offline.ui"))))
        window_signIn = uic.loadUi(str(PurePath(resource_path("signIn.ui"))))

        if platform.system() == "Windows":
            window_webView = uic.loadUi(str(PurePath(resource_path("webView.ui"))))

        else:
            UTILITYFuncs.logAndPrint("INFO", 'Not using PyQtWebEngine because it is mac os')

        window_changePassword = uic.loadUi(str(PurePath(resource_path("changePassword.ui"))))
        window_update = uic.loadUi(str(PurePath(resource_path("update.ui"))))
        window_status = uic.loadUi(str(PurePath(resource_path("appStatus.ui"))))
        window_settings = uic.loadUi(str(PurePath(resource_path("settings.ui"))))
        window_new = uic.loadUi(str(PurePath(resource_path("new.ui"))))
        dialog_signInFailure = uic.loadUi(str(PurePath(resource_path("signInFailure.ui"))))
        dialog_accountSuspended = uic.loadUi(str(PurePath(resource_path("accountSuspended.ui"))))
        dialog_error = uic.loadUi(str(PurePath(resource_path("error.ui"))))
        dialog_about = uic.loadUi(str(PurePath(resource_path("about.ui"))))
        dialog_alert = uic.loadUi(str(PurePath(resource_path("alert.ui"))))

    except Exception as e:
        UTILITYFuncs.logAndPrint("FATAL", f"PyQt5: There was a problem creating windows! (During a non-developmental run) {e}")
        UTILITYFuncs.error(f"There was a problem creating windows! (During a non-developmental run {e}")

elif developmental == True:
    UTILITYFuncs.logAndPrint("INFO", "PyQt5: Loading like it's a .py")
    # Load for development
    try:
        window_accountDetails = uic.loadUi(str(PurePath("ui/accountDetails.ui")))
        window_createAccount = uic.loadUi(str(PurePath("ui/createAccount.ui")))
        window_main = uic.loadUi(str(PurePath("ui/main.ui")))
        window_offline = uic.loadUi(str(PurePath("ui/offline.ui")))
        window_signIn = uic.loadUi(str(PurePath("ui/signIn.ui")))

        if platform.system() == "Windows":
            window_webView = uic.loadUi(str(PurePath("ui/webView.ui")))

        elif platform.system() == "Darwin":
            UTILITYFuncs.logAndPrint("INFO", "Not creating the webview window because you're on mac os")

        window_changePassword = uic.loadUi(str(PurePath("ui/changePassword.ui")))
        window_update = uic.loadUi(str(PurePath("ui/update.ui")))
        window_status = uic.loadUi(str(PurePath("ui/appStatus.ui")))
        window_settings = uic.loadUi(str(PurePath("ui/settings.ui")))
        window_new = uic.loadUi(str(PurePath("ui/new.ui")))
        dialog_signInFailure = uic.loadUi(str(PurePath("ui/signInFailure.ui")))
        dialog_accountSuspended = uic.loadUi(str(PurePath("ui/accountSuspended.ui")))
        dialog_error = uic.loadUi(str(PurePath("ui/error.ui")))
        dialog_about = uic.loadUi(str(PurePath("ui/about.ui")))
        dialog_alert = uic.loadUi(str(PurePath("ui/alert.ui")))

    except Exception as e:
       UTILITYFuncs.logAndPrint("FATAL", f"PyQt5: There was a problem creating windows! (During a developental run) {e}")
       UTILITYFuncs.error(f"There was a problem creating windows! (During a developmental run {e}")
        

else:
    UTILITYFuncs.logAndPrint("FATAL", f"PyQt5: There was a *terrible* problem when opening windows. It it in developental mode? We don't know. Variable is '{developmental}'")
    UTILITYFuncs.error(f"There was a problem determining if we're running as developental or not. Variable is '{developmental}'")
    sys.exit()

if developmental == False:
    print("not developmental!")
    dot_jadeAssistantDownloadPix = QtGui.QPixmap(str(resource_path("jadeAssistantDownloadDot.png")))
    dot_jadeAppsDownloadPix = QtGui.QPixmap(str(resource_path("jadeAppsDownloadDot.png")))

elif developmental == True:
    print("developmental!")
    dot_jadeAssistantDownloadPix = QtGui.QPixmap(str(PurePath("assets/dots/jadeAssistantDownloadDot.png")))
    dot_jadeAppsDownloadPix = QtGui.QPixmap(str(PurePath("assets/dots/jadeAppsDownloadDot.png")))

dot_jadeAssistantDownloadPix = dot_jadeAssistantDownloadPix.scaled(100, 100)
dot_jadeAppsDownloadPix = dot_jadeAppsDownloadPix.scaled(100, 100)
    
dot_jadeAssistantDownload = QtWidgets.QSplashScreen(dot_jadeAssistantDownloadPix, QtCore.Qt.WindowStaysOnTopHint)
dot_jadeAppsDownload = QtWidgets.QSplashScreen(dot_jadeAppsDownloadPix, QtCore.Qt.WindowStaysOnTopHint)

# Connect buttons to functions

# Offline
window_offline.button.clicked.connect(UIFuncs.closeOffline)
window_offline.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

# Main Screen
window_main.account_button.clicked.connect(UIFuncs.openAccountScreen)
#window_main.leftBox_jadeBarButton.clicked.connect(UIFuncs.openJadeBar)
#window_main.leftBox_plusButton.clicked.connect(UIFuncs.openPlus)
window_main.button1.clicked.connect(UIFuncs.expandNews1)
window_main.button2.clicked.connect(UIFuncs.expandNews2)
window_main.button3.clicked.connect(UIFuncs.expandNews3)
window_main.changelogsButton.clicked.connect(UIFuncs.openChangelog)
window_main.statusButton.clicked.connect(UIFuncs.openStatus)
window_main.jadeAssistant_status.clicked.connect(UIFuncs.openStatus)
window_main.jadeApps_status.clicked.connect(UIFuncs.openStatus)
window_main.jadeAssistant_launch.clicked.connect(UIFuncs.launchJadeAssistant)
window_main.jadeApps_launch.clicked.connect(UIFuncs.launchJadeApps)
window_main.allNews.clicked.connect(UIFuncs.allNewsButton)
window_main.settingsButton.clicked.connect(UIFuncs.settingsButton)

window_main.jadeAssistant_launch.hide()
window_main.jadeApps_launch.hide()

# Sign In Screen
window_signIn.signInBox_button.clicked.connect(UIFuncs.signInButton)
window_signIn.switchWindowBox_button.clicked.connect(UIFuncs.switchToCreateAccount)
window_signIn.passwordBox_show.stateChanged.connect(UIFuncs.passwordToggle)
window_signIn.signInBox_button.setShortcut("Return")

# Account details
window_accountDetails.buttonsBox_signOut.clicked.connect(UIFuncs.signOutButton)
window_accountDetails.buttonsBox_changePassword.clicked.connect(UIFuncs.openChangePassword)

# Create Account
window_createAccount.switchWindowBox_button.clicked.connect(UIFuncs.switchToSignIn)
window_createAccount.mainBox_button.clicked.connect(UIFuncs.createAccountButton)

# Account suspended dialog
dialog_accountSuspended.logOut.clicked.connect(UIFuncs.suspendedLogOut)
dialog_accountSuspended.quit.clicked.connect(UIFuncs.suspendedQuit)

# Error dialog
dialog_error.QUIT.clicked.connect(UIFuncs.quitErrorDialog)

# Web view
if platform.system() == "Windows":
    WEBVIEW = WebView
    window_webView.back.clicked.connect(WEBVIEW.back)
    window_webView.forward.clicked.connect(WEBVIEW.forward)
    window_webView.reload.clicked.connect(WEBVIEW.reload)
    window_webView.web.loadFinished.connect(WEBVIEW.doneLoading)
    window_webView.web.loadStarted.connect(WEBVIEW.startLoading)
    window_webView.web.loadProgress.connect(WEBVIEW.progress)
    window_webView.go.clicked.connect(WEBVIEW.goButton)

elif platform.system() == "Darwin":
    UTILITYFuncs.logAndPrint("INFO", "Not setting up the webview window because you're on mac os.")

# About dialog
dialog_about.version.setText(Version_TOTAL)
dialog_about.version.setFont(QFont("Calibri", 16))
dialog_about.version.setAlignment(QtCore.Qt.AlignLeft)
dialog_about.button.clicked.connect(UIFuncs.aboutWebsiteButton)
dialog_about.logButton.clicked.connect(UIFuncs.aboutLogButton)

# Change Password Window
window_changePassword.button.clicked.connect(UIFuncs.changePassword)

# Update menu
window_update.update.clicked.connect(UIFuncs.goToLauncherUpdate)
window_update.notNow.clicked.connect(UIFuncs.notNowUpdate)

# App status
window_status.jadeLauncher_download.clicked.connect(UIFuncs.updateJadeLauncher)
window_status.jadeLauncher_install.clicked.connect(UIFuncs.installJadeLauncher)
window_status.jadeLauncher_cancel.clicked.connect(UIFuncs.cancelInstallUpdate)
window_status.jadeLauncher_cancel.hide()

window_status.jadeAssistant_launch.clicked.connect(UIFuncs.launchJadeAssistant)
window_status.jadeAssistant_update.clicked.connect(UIFuncs.updateJadeAssistant)
window_status.jadeAssistant_download.clicked.connect(UIFuncs.downloadJadeAssistant)
window_status.jadeAssistant_remove.clicked.connect(UIFuncs.removeJadeAssistant)

window_status.jadeApps_launch.clicked.connect(UIFuncs.launchJadeApps)
window_status.jadeApps_update.clicked.connect(UIFuncs.updateJadeApps)
window_status.jadeApps_download.clicked.connect(UIFuncs.downloadJadeApps)
window_status.jadeApps_remove.clicked.connect(UIFuncs.removeJadeApps)

window_status.jadeLauncher_version.setText(f"{Version_MAJOR}.{Version_MINOR}.{Version_PATCH}")

# TODO: Coming in 2.1.0
# FIXME: checkForRunningAppsThread
window_status.jadeAssistant_stop.hide()
window_status.jadeApps_stop.hide()
# FIXME: checkForRunningAppsThread


# Settings menu
window_settings.save.clicked.connect(UIFuncs.saveSettings)
window_settings.aboutButton.clicked.connect(UIFuncs.openAbout)
window_settings.uninstall.clicked.connect(UIFuncs.uninstallAsk)

# Alert dialog
dialog_alert.okay.clicked.connect(UIFuncs.closeAlert)

# What's new window
window_new.getStarted.clicked.connect(UIFuncs.getStartedNew)

# Check sys.argv
def checkArgs():
    global doMain
    try:
        if sys.argv[1] == "webview":
            UTILITYFuncs.logAndPrint("INFO", "checkArgs: Found 'webview' argument")
            WEBVIEW.openWebView(sys.argv[2])
            doMain = False

        elif sys.argv[1] == "help":
            print("-----")
            print("Jade Launcher Arguments")
            print("    - Use 'Jade Launcher.exe' to open the Launcher.")
            print("    - Use 'Jade Launcher.exe webview <url>' to use the Launcher's webview capabilities.")
            print("-----")
            doMain = False

        else:
            UTILITYFuncs.logAndPrint("INFO", "checkArgs: No sys.argv detected. Running normally.")
            doMain = True

    except:
        UTILITYFuncs.logAndPrint("INFO", "checkArgs: No sys.argv detected. Running normally.")
        doMain = True

checkArgs()

# ----------
# Start App
# ----------
def guiLoop():
    global guiLoopList
    if len(guiLoopList) >= 1:
        try:
            UTILITYFuncs.logAndPrint("INFO", f"guiLoop: Running code '{guiLoopList[0]}'")
            exec(guiLoopList[0])
            guiLoopList.remove(guiLoopList[0])

        except Exception as e:
            UTILITYFuncs.logAndPrint("GUI LOOP CODE RUN FAILURE", f"guiLoop: There was a problem running some code! {e}")
            guiLoopList.remove(guiLoopList[0])
            UTILITYFuncs.error(f"The gui loop had a problem running some code! code >>'{guiLoopList[0]}'<< '{e}'")

def killCheck():
    global killThreads
    if window_main.isVisible() == False:
        killThreads = True

    if killThreads == True:
        print("DIE, FOOLISH THREADS")
        jadeDots.kill()


if doMain == True:
    guiLoopTimer = QTimer()
    guiLoopTimer.timeout.connect(guiLoop)
    guiLoopTimer.start(1)

    #killCheckTimer = QTimer()
    #killCheckTimer.timeout.connect(killCheck)
    #killCheckTimer.start(1)

    myAccount = Account("False", "no", "loading...")

    news1 = News("loading", "loading", "loading", "loading", "1", "loading")
    news2 = News("loading", "loading", "loading", "loading", "2", "loading")
    news3 = News("loading", "loading", "loading", "loading", "3", "loading")

    Launcher = LauncherId("loading", "loading")

    jade_assistant_dict = {
        "name": "Jade Assistant",
        "description": "Jade Assistant is a virtual assistant designed to help you make the most out of your day by providing information from a variety of sources including Jade Apps, and being able to open apps for you.",
        "path": "Jade Assistant",
        "version": "Loading...",
        "download_folder": "./apps/jadeassistant",
        "download_url": "https://github.com/nfoert/jadeassistant/raw/main/Jade%20Assistant.exe",
        "exe_location": "./apps/jadeassistant/Jade Assistant.exe",
        "version_file_location": "./apps/jadeassistant/JadeAssistantVersion.txt",
        "version_url": "https://nfoert.pythonanywhere.com/jadeAssistant/jadeAssistantVersion",
        "dot_name": "jadeAssistantDownload",
        "button_launch": window_status.jadeAssistant_launch,
        "button_download": window_status.jadeAssistant_download,
        "button_update": window_status.jadeAssistant_update,
        "button_remove": window_status.jadeAssistant_remove,
        "label_status": window_status.jadeAssistant_status,
        "label_version": window_status.jadeAssistant_version,
        "main_button_launch": window_main.jadeAssistant_launch,
        "button_launch_loop": "window_status.jadeAssistant_launch",
        "button_download_loop": "window_status.jadeAssistant_download",
        "button_update_loop": "window_status.jadeAssistant_update",
        "button_remove_loop": "window_status.jadeAssistant_remove",
        "label_status_loop": "window_status.jadeAssistant_status",
        "label_version_loop": "window_status.jadeAssistant_version",
        "main_button_launch_loop": "window_main.jadeAssistant_launch",
    }

    jade_apps_dict = {
        "name": "Jade Apps",
        "description": "Jade Apps is the ultimate collection of small applets that are integrated into Jade Assistant allowing you to get lots of information about different topics.",
        "path": "Jade Apps",
        "version": "Loading...",
        "download_folder": "./apps/jadeapps",
        "download_url": "https://github.com/nfoert/jadeapps/raw/main/Jade%20Apps.exe",
        "exe_location": "./apps/jadeapps/Jade Apps.exe",
        "version_file_location": "./apps/jadeapps/JadeAppsVersion.txt",
        "version_url": "https://nfoert.pythonanywhere.com/jadeapps/jadeAppsVersion",
        "dot_name": "jadeAppsDownload",
        "button_launch": window_status.jadeApps_launch,
        "button_download": window_status.jadeApps_download,
        "button_update": window_status.jadeApps_update,
        "button_remove": window_status.jadeApps_remove,
        "label_status": window_status.jadeApps_status,
        "label_version": window_status.jadeApps_version,
        "main_button_launch": window_main.jadeApps_launch,
        "button_launch_loop": "window_status.jadeApps_launch",
        "button_download_loop": "window_status.jadeApps_download",
        "button_update_loop": "window_status.jadeApps_update",
        "button_remove_loop": "window_status.jadeApps_remove",
        "label_status_loop": "window_status.jadeApps_status",
        "label_version_loop": "window_status.jadeApps_version",
        "main_button_launch_loop": "window_main.jadeApps_launch",
    }

    JadeAssistantDescription = "Jade is a virtual assistant for your computer's desktop designed to be as helpful as possible, while being able to change size to fit your workflow."
    JadeAppsDescription = "Jade Apps is the ultimate hub for information and tasks that is integrated into Jade Assistant"

    JadeAssistant = App(jade_assistant_dict)
    JadeApps = App(jade_apps_dict)

    firstGC = UTILITYFuncs.getConnection("main")
    if firstGC == True:
        
        jadelauncher_config = config.Config("jadeLauncherConfig")
        MAINFuncs.mainCode()

    elif firstGC == False:
        jadelauncher_config = config.Config("jadeLauncherConfig")

    JadeAssistant_UpdateThread = threading.Thread(target=JadeAssistant.updateApp, daemon=True)
    JadeAssistant_DownloadThread = threading.Thread(target=JadeAssistant.downloadApp, daemon=True)
    JadeApps_UpdateThread = threading.Thread(target=JadeApps.updateApp, daemon=True)
    JadeApps_DownloadThread = threading.Thread(target=JadeApps.downloadApp, daemon=True)

    JadeAssistant_UpdateThread.start()
    JadeAssistant_DownloadThread.start()
    JadeApps_UpdateThread.start()
    JadeApps_DownloadThread.start()

    jadeDots.init(guiLoopList, window_main, developmental, screen, dot_jadeAssistantDownload, dot_jadeAppsDownload)
    jadeStatus.init(window_main, developmental, resource_path)    

    jadeStatus.setStatus("ok")
    
    

    if update == "yes":
        window_update.show()

    else:
        UTILITYFuncs.logAndPrint("INFO", "Updates not required.")

    UIFuncs.debugOpenAllWindows()

    app.exec()

elif doMain == False:
    UTILITYFuncs.logAndPrint("INFO", "Start App: Argument detected. Will not do normal startup.")
    app.exec()

else:
    UTILITYFuncs.error("There was a problem checking if we need to do main startup code or not.")
    UTILITYFuncs.logAndPrint("FATAL", "Start App: There was a problem checking if we need to do main startup code or not.")

