'''
Jade Launcher (NEW)
The Jade Launcher is what launches, updates and downloads apps like Jade Assistant,
and where you can manage your Jade Account.

The Jade Launcher went through another iteration before this one. The previous one used guizero (https://lawsie.github.io/guizero/about/)
which is an incredible and easy to use GUI library. Guizero treated me well but I began to require more features which made me decide
to switch to PyQt5. (https://pypi.org/project/PyQt5/) Unfortunately, that was such a large change so I decided to start the Launcher over.

Jade Software was built by a teenager over nearly a year and a half.
'''


# ----------
# Imports aren't cool THEY"RE VERY COOL THEY LET YOU USE OtHer THIRD PARTY MODULES 
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
import sys

# Third Party Imports
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl, QTimer

import requests
import pwnedpasswords
from tqdm import tqdm

if platform.system() == "Windows":
    from PyQt5.QtWebEngineWidgets import *

else:
    print("Not importing QtWebEngine because it's not required for mac OS")

# Local Imports
import assets #The resources for PyQt

# ----------
# Set up variables
# ----------

Version_MAJOR = 1
Version_MINOR = 0
Version_PATCH = 0
developmental = False #True = for .py & False = for .exe / mac executable
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
            UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/Authenticate: Authenticating with username: {USERNAME}")
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

                    window_main.leftBox_accountLabel.setText(f"Hello, {USERNAME}")
                    window_main.leftBox_accountLabel.setFont(QFont("Calibri Bold", 10))
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
                    UTILITYFuncs.logAndPrint("FATAL", f"Classes/Account/Authenticate: There was a problem doing a bunch of essential stuff when Authenticating. {e}")
                    UTILITYFuncs.error(f"There was a problem doing a bunch of essential stuff when Authenticating. {e}")

                

            elif "not" in authenticateRequest.text:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/Authenticate: Failed to sign in. Incorrect credentials.")
                dialog_signInFailure.show()
                SignedIn = False
                return False

        except Exception as e:
            UTILITYFuncs.logAndPrint("WARN", f"Classes/Account/Authenticate: There was a problem signing you in. (Account file may have no content.) '{e}'")
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

                window_main.leftBox_accountLabel.setText(f"Hello, {usernameInput}")
                window_main.leftBox_accountLabel.setFont(QFont("Calibri Bold", 9))
                window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
                window_main.leftBox_accountLabel.setStyleSheet("color: green")

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

        window_main.leftBox_accountLabel.setText(f"Not signed in.")
        window_main.leftBox_accountLabel.setFont(QFont("Calibri", 8))
        window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
        window_main.leftBox_accountLabel.setStyleSheet("color: red")

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

                            UTILITYFuncs.notification("Account successfully created.", "Your Account has been created.")

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
                            UTILITYFuncs.notification("That account already exists!", "That username matches another username in our database. Maybe you created an account, then forgot it existed?")
                            window_createAccount.mainBox_button.setEnabled(True)
                            window_createAccount.mainBox_button.setText("Create Account")

                        else:
                            UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: There was a problem.")
                            UTILITYFuncs.notification("There was a problem creating an Account.", "We couldn't create your account.")
                            window_createAccount.mainBox_button.setEnabled(True)
                            window_createAccount.mainBox_button.setText("Create Account")

                    except Exception as e:
                        UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/createAccount: There was a problem creating an account. {e}")
                        UTILITYFuncs.notification("There was a problem creating an Account.", "We couldn't create your account.")
                        window_createAccount.mainBox_button.setEnabled(True)
                        window_createAccount.mainBox_button.setText("Create Account")
                    
                elif passwordCheck >= 1:
                    UTILITYFuncs.logAndPrint("INFO", f"Classes/Account/createAccount: Password is not safe! Has been leaked {passwordCheck} times.")
                    UTILITYFuncs.notification("That password is not safe!", f"That password has been leaked {passwordCheck} times.")
                    window_createAccount.mainBox_button.setEnabled(True)
                    window_createAccount.mainBox_button.setText("Create Account")

                else:
                    UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: There was a problem checking password safety.")
                    UTILITYFuncs.notification("There was a problem checking password safety.", "We were not able to confirm that your password is safe.")
                    window_createAccount.mainBox_button.setEnabled(True)
                    window_createAccount.mainBox_button.setText("Create Account")    


            else:
                UTILITYFuncs.logAndPrint("INFO", "Classes/Account/createAccount: Please select a password with more than 8 characters.")
                UTILITYFuncs.notification("Password is too short!", "Please make sure your password has eight or more characters.")
                window_createAccount.mainBox_button.setEnabled(True)
                window_createAccount.mainBox_button.setText("Create Account")

        elif gc == False:
            UTILITYFuncs.notification("There was a problem creating an Account.", "You're not connected!")

        else:
            UTILITYFuncs.notification("There was a problem creating an Account.", "There was a problem getting connection status.")

    def changePassword(self):
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
                        UTILITYFuncs.notification("Password changed", "Your password has been changed.")

                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                        myAccount.writeAccountFile(self.username, newPassword)

                        window_accountDetails.show()

                    elif changePasswordRequest.text == "There was a problem getting Verification Code data.":
                        window_changePassword.passwordBox_edit.clear()
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: Your verification code is not correct. '{changePasswordRequest.text}'")
                        UTILITYFuncs.notification("Your verification code is not correct.", f"Please check your email account {self.email} to view your verification code.")
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                    elif changePasswordRequest.text == "There was a problem getting Account data.":
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: There was a problem getting Account data.. '{changePasswordRequest.text}'")
                        UTILITYFuncs.notification("There was a problem getting Account data.", "It looks like your username is not correct for some reason.")
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                    elif changePasswordRequest.text == "That username and password don't match any Account in the database.":
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: Your old password is not correct. '{changePasswordRequest.text}'")
                        UTILITYFuncs.notification("Your old password is not correct.", f"Please confirm that your old password is correct.")
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                    else:
                        window_changePassword.passwordBox_edit.clear()
                        UTILITYFuncs.logAndPrint("WARN", f"Account/changePassword: There was a problem changing your password. '{changePasswordRequest.text}'")
                        UTILITYFuncs.notification("There was a problem changing your password.", changePasswordRequest.text)
                        window_changePassword.button.setEnabled(True)
                        window_changePassword.button.setText("Change Password")

                        
                except Exception as e:
                    UTILITYFuncs.logAndPrint("FATAL", f"Account/changePassword: An exception occured when changing your password. '{e}'")
                    UTILITYFuncs.error(f"An exception occured when changing your password. '{e}'")
                    window_changePassword.button.setEnabled(True)
                    window_changePassword.button.setText("Change Password")

            else:
                UTILITYFuncs.notification("That password is not safe!", f"Your new password has been leaked {passwordCheck} times.")
                window_changePassword.passwordBox_edit.clear()
                window_changePassword.button.setEnabled(True)
                window_changePassword.button.setText("Change Password")

        else:
            UTILITYFuncs.notification("That password is not long enough!", "Please make your new password eight or more characters.")
            window_changePassword.passwordBox_edit.clear()
        
class News:
    '''A class to control news expansion and opening url.'''
    def __init__(self, header, date, text, url, number):
        self.header = header
        self.date = date
        self.text = text
        self.url = url
        self.number = number

    def expand(self):
        '''Expand news'''
        UTILITYFuncs.logAndPrint("INFO", f"Classes/News/expand: Expanding news {self.number}")
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
            if platform.system() == "Windows":
                WEBVIEW.openWebView(self.url)

            elif platform.system() == "Darwin":
                webbrowser.open(self.url)

            else:
                UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")

        
        
        print("Done expanding.")

    def openUrl(self):
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

class App:
    def __init__(self, name, description, path, version):
        self.name = name
        self.description = description
        self.path = path
        self.version = version
        self.downloadAppVar = False
        self.updateAppVar = False
        self.state = ""
        self.newVersion = ""

    def openAppMenu(self):
        global selectedApp
        UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: Opening app menu for {self.name}...")
        selectedApp = self.name
        window_appMenu.description.setText(self.description)
        window_appMenu.description.setFont(QFont("Calibri", 11))
        window_appMenu.description.setAlignment(QtCore.Qt.AlignCenter)

        if self.state == "ready":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is ready.")
            window_appMenu.launchButton.show()
            window_appMenu.downloadButton.hide()
            window_appMenu.updateButton.hide()
            window_appMenu.removeButton.show()
            window_appMenu.version.setText(f"Version {self.version}")
            window_appMenu.version.setFont(QFont("Calibri", 11))
            window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)
        

        elif self.state == "download":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is download.")
            window_appMenu.launchButton.hide()
            window_appMenu.downloadButton.show()
            window_appMenu.updateButton.hide()
            window_appMenu.removeButton.hide()
            window_appMenu.version.setText(f"Download version {self.newVersion}")
            window_appMenu.version.setFont(QFont("Calibri", 11))
            window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)

        elif self.state == "downloading":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is downloading.")
            window_appMenu.launchButton.hide()
            window_appMenu.downloadButton.show()
            window_appMenu.updateButton.hide()
            window_appMenu.removeButton.hide()
            window_appMenu.version.setText(f"Downloading version {self.newVersion}...")
            window_appMenu.version.setFont(QFont("Calibri", 11))
            window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)
        

        elif self.state == "update":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is updates.")
            window_appMenu.launchButton.show()
            window_appMenu.downloadButton.hide()
            window_appMenu.updateButton.show()
            window_appMenu.removeButton.show()
            window_appMenu.version.setText(f"Update to version {self.newVersion}")
            window_appMenu.version.setFont(QFont("Calibri", 11))
            window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)

        elif self.state == "updating":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is updating.")
            window_appMenu.launchButton.hide()
            window_appMenu.downloadButton.hide()
            window_appMenu.updateButton.show()
            window_appMenu.removeButton.hide()
            window_appMenu.version.setText(f"Updating to version {self.newVersion}...")
            window_appMenu.version.setFont(QFont("Calibri", 11))
            window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)
        
            
        elif self.state == "readyoffline":
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is readyoffline.")
            window_appMenu.launchButton.show()
            window_appMenu.downloadButton.hide()
            window_appMenu.updateButton.hide()
            window_appMenu.removeButton.show()
            window_appMenu.version.setText("You're offline!")
            window_appMenu.version.setFont(QFont("Calibri", 11))
            window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)
        

        else:
            UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: State for {self.name} is not recognized. '{self.state}'")
            return False

        UTILITYFuncs.logAndPrint("INFO", f"App/openAppMenu: Menu for {self.name} has opened.")
        window_appMenu.show()

    def launchApp(self):
        UTILITYFuncs.logAndPrint("INFO", f"App/launchApp: Launching {self.name}...")
        global killThreads
        global TruePath
        try:
            if platform.system() == "Windows":
                subprocess.Popen(f"{TruePath}{self.path}.exe")
                killThreads = True
                UTILITYFuncs.logAndPrint("INFO", f"App/launchApp: {self.name} was launched. (windows)")
                sys.exit()
                
            elif platform.system() == "Darwin":
                subprocess.run(["open", f"{TruePath}{self.path}"])
                killThreads = True
                UTILITYFuncs.logAndPrint("INFO", f"App/launchApp: {self.name} was launched. (mac)")
                sys.exit()
                
            else:
                UTILITYFuncs.logAndPrint("FATAL", "UIFuncs/launchJadeAssistant: Your OS isn't supported! Please use Mac or Windows.")
                UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac or Windows.")

        except Exception as e:
            UTILITYFuncs.logAndPrint("INFO", f"UIFuncs/launchJadeAssistant: There was a problem launching Jade Assistant! {e}")
            UTILITYFuncs.error(f"There was a problem launching Jade Assistant! {e}")

    def downloadApp(self):
        UTILITYFuncs.logAndPrint("INFO", "App/downloadApp: Thread started.")
        global guiLoopList
        global killThreads
        global progress_bar
        global TruePath
        while killThreads == False:
            if self.downloadAppVar == True:
                UTILITYFuncs.logAndPrint("INFO", "App/downloadApp: Downloading Jade Assistant...")
                guiLoopList.append('window_appMenu.launchButton.hide()')
                guiLoopList.append('window_appMenu.updateButton.hide()')
                guiLoopList.append('window_appMenu.downloadButton.show()')
                guiLoopList.append('window_appMenu.removeButton.hide()')
                guiLoopList.append('window_appMenu.downloadButton.setEnabled(False)')
                guiLoopList.append('window_appMenu.downloadButton.setText("Downloading...")')
                guiLoopList.append('window_appMenu.progressBar.show()')
                
                if platform.system() == "Windows":
                    end = ".exe"

                elif platform.system() == "Darwin":
                    end = ""

                else:
                    UTILITYFuncs.error("You're OS isn't supported! Please use Mac or Windows.")

                try:
                    UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Downloading {self.name}...")
                    self.state = "downloading"
                    guiLoopList.append('window_appMenu.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)')
                    guiLoopList.append('window_main.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)')
                    guiLoopList.append('window_main.show()')
                    guiLoopList.append('JadeAssistant.openAppMenu()')
                    DownloadAppPath = self.path.replace(" ", "%20")
                    AppDownload = requests.get(f"https://github.com/nfoert/jadeassistant/raw/main/{DownloadAppPath}{end}", stream=True)
                    total_size_in_bytes = int(AppDownload.headers.get('content-length', 0))
                    bytes_downloaded = 0
                    last = 0
                    
                    with open(f'{TruePath}{self.path}{end}', 'wb') as file:
                        for data in AppDownload.iter_content(1024):
                            file.write(data)
                            bytes_downloaded = bytes_downloaded + 1024
                            percent = bytes_downloaded / total_size_in_bytes
                            percent = percent * 100
                            percent = round(percent)
                            if last != percent:
                                last = percent
                                guiLoopList.append(f'window_appMenu.progressBar.setValue({percent})')
                            else:
                                continue


                    file.close()
                            
                    if platform.system() == "Darwin":
                        print("CHMOD!!!")
                        os.system(f'chmod 775 "{TruePath}Jade Assistant"')
                    
                    else:
                        UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Not Chmodding.")


                    self.downloadAppVar = False
                    guiLoopList.append('window_appMenu.launchButton.show()')
                    guiLoopList.append('window_appMenu.updateButton.hide()')
                    guiLoopList.append('window_appMenu.downloadButton.setEnabled(True)')
                    guiLoopList.append('window_appMenu.downloadButton.setText("Download")')
                    guiLoopList.append('window_appMenu.downloadButton.hide()')
                    guiLoopList.append('window_appMenu.removeButton.show()')
                    guiLoopList.append('window_appMenu.progressBar.hide()')
                    self.state = "ready"
                    guiLoopList.append('window_appMenu.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)')
                    guiLoopList.append('window_main.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)')
                    guiLoopList.append('window_main.show()')
                    guiLoopList.append('JadeAssistant.openAppMenu()')
                    UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Done downloading {self.name}.")
                    guiLoopList.append(f'UTILITYFuncs.notification("{self.name} was downloaded.", "{self.name} is done downloading.")')
                    versionFileName = self.path
                    versionFileName = versionFileName.replace(" ", "")
                    appVersionFile = open(f"{TruePath}{versionFileName}Version.txt", "w")
                    self.version = self.newVersion
                    print(appVersionFile.name)
                    print(versionFileName)
                    file = open("file.txt", "w")
                    self.newVersion = self.newVersion.replace(".", "\n")
                    appVersionFile.write(self.newVersion)
                    appVersionFile.close()

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"App/downloadApp: There was a problem downloading {self.name}! {e}")
                    self.downloadAppVar = False
                    guiLoopList.append(f'UTILITYFuncs.notification("There was a problem!", "There was a problem downloading {self.name}!")')
                    guiLoopList.append('window_appMenu.launchButton.show()')
                    guiLoopList.append('window_appMenu.updateButton.hide()')
                    guiLoopList.append('window_appMenu.downloadButton.show()')
                    guiLoopList.append('window_appMenu.downloadButton.setEnabled(True)')
                    guiLoopList.append('window_appMenu.downloadButton.setText("Download")')
                    guiLoopList.append('window_appMenu.removeButton.show()')
                    guiLoopList.append('window_appMenu.progressBar.hide()')

                

            elif window_main.isVisible() == False:
                return False

            else:
                sleep(1)
                continue

    def updateApp(self):
        UTILITYFuncs.logAndPrint("INFO", "App/updateApp: Thread started.")
        global guiLoopList
        global killThreads
        global progress_bar
        global selectedApp
        global TruePath
        while killThreads == False:
            if self.updateAppVar == True:
                UTILITYFuncs.logAndPrint("INFO", "App/updateApp: Updating Jade Assistant...")
                guiLoopList.append('window_appMenu.launchButton.hide()')
                guiLoopList.append('window_appMenu.updateButton.show()')
                guiLoopList.append('window_appMenu.downloadButton.hide()')
                guiLoopList.append('window_appMenu.removeButton.hide()')
                guiLoopList.append('window_appMenu.updateButton.setEnabled(False)')
                guiLoopList.append('window_appMenu.updateButton.setText("Updating...")')
                guiLoopList.append('window_appMenu.progressBar.show()')


                if platform.system() == "Windows":
                    end = ".exe"

                elif platform.system() == "Darwin":
                    end = ""

                else:
                    UTILITYFuncs.error("You're OS isn't supported! Please use Mac or Windows.")

                try:
                    UTILITYFuncs.logAndPrint("INFO", f"App/updateApp: Updating {self.name}...")
                    self.state = "updating"
                    guiLoopList.append('window_appMenu.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)')
                    guiLoopList.append('window_main.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)')
                    guiLoopList.append('window_main.show()')
                    guiLoopList.append('JadeAssistant.openAppMenu()')
                    
                    os.remove(f"{TruePath}{self.path}{end}")
                    self.path = self.path.replace(" ", "%20")
                    AppDownload = requests.get(f"https://github.com/nfoert/jadeassistant/raw/main/{self.path}{end}", stream=True)
                    total_size_in_bytes = int(AppDownload.headers.get('content-length', 0))
                    bytes_downloaded = 0
                    last = 0

                    self.path = self.path.replace("%20", " ")
                    
                    with open(f'{TruePath}{self.path}{end}', 'wb') as file:
                        for data in AppDownload.iter_content(1024):
                            file.write(data)
                            bytes_downloaded = bytes_downloaded + 1024
                            percent = bytes_downloaded / total_size_in_bytes
                            percent = percent * 100
                            percent = round(percent)
                            if last != percent:
                                last = percent
                                guiLoopList.append(f'window_appMenu.progressBar.setValue({percent})')
                            else:
                                continue
                        
                        AppDownload.close()
                        file.close()

                        if platform.system() == "Darwin":

                            os.system('chmod 775 "Jade Assistant"')

                        else:
                            UTILITYFuncs.logAndPrint("INFO", f"App/downloadApp: Not Chmodding.")

        


                    self.updateAppVar = False
                    self.state = "ready"
                    guiLoopList.append('window_appMenu.launchButton.show()')
                    guiLoopList.append('window_appMenu.updateButton.hide()')
                    guiLoopList.append('window_appMenu.downloadButton.hide()')
                    guiLoopList.append('window_appMenu.removeButton.show()')
                    guiLoopList.append('window_appMenu.progressBar.hide()')
                    guiLoopList.append('window_appMenu.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)')
                    guiLoopList.append('window_main.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)')
                    guiLoopList.append('window_main.show()')
                    guiLoopList.append('JadeAssistant.openAppMenu()')
                    UTILITYFuncs.logAndPrint("INFO", f"App/updateApp: Done updating {self.name}. Writing version file...")
                    versionFileName = self.path
                    versionFileName = versionFileName.replace(" ", "")
                    appVersionFile = open(f"{TruePath}{versionFileName}Version.txt", "w")
                    print(appVersionFile.name)
                    print(versionFileName)
                    self.version = self.newVersion
                    file = open("file.txt", "w")
                    self.newVersion = self.newVersion.replace(".", "\n")
                    appVersionFile.write(self.newVersion)
                    appVersionFile.close()
                    
                    guiLoopList.append(f'UTILITYFuncs.notification("{self.name} was updated.", "{self.name} is done updating.")')

                    sleep(5)

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"App/updateApp: There was a problem updating {self.name}! {e}")
                    self.updateAppVar = False
                    guiLoopList.append(f'UTILITYFuncs.notification("There was a problem!", "There was a problem updating {self.name}!")')
                    guiLoopList.append('window_appMenu.launchButton.show()')
                    guiLoopList.append('window_appMenu.updateButton.show()')
                    guiLoopList.append('window_appMenu.downloadButton.hide()')
                    guiLoopList.append('window_appMenu.updateButton.setEnabled(True)')
                    guiLoopList.append('window_appMenu.updateButton.setText("Update")')
                    guiLoopList.append('window_appMenu.removeButton.show()')
                    guiLoopList.append('window_appMenu.progressBar.hide()')

                

            elif window_main.isVisible() == False:
                return False

            else:
                sleep(1)
                continue

    def removeApp(self):
        try:
            if platform.system() == "Windows":
                os.system(f'taskkill /F /IM "{self.path}.exe"')
                os.remove("Jade Assistant.exe")
                guiLoopList.append('window_appMenu.launchButton.hide()')
                guiLoopList.append('window_appMenu.updateButton.hide()')
                guiLoopList.append('window_appMenu.downloadButton.show()')
                guiLoopList.append('window_appMenu.removeButton.hide()')
                UTILITYFuncs.notification("Jade Assistant was removed.", "You just deleted Jade Assistant.")

            elif platform.system() == "Darwin":
                os.system(f'killall "{self.path}"')
                os.remove("Jade Assistant")
                guiLoopList.append('window_appMenu.launchButton.hide()')
                guiLoopList.append('window_appMenu.updateButton.hide()')
                guiLoopList.append('window_appMenu.downloadButton.show()')
                guiLoopList.append('window_appMenu.removeButton.hide()')
                UTILITYFuncs.notification("Jade Assistant was removed.", "You just deleted Jade Assistant.")

            else:
                UTILITYFuncs.logAndPrint("INFO", "UIFuncs/removeJadeAssistant: Your OS isn't supported! Please use Mac or Windows.")
                UTILITYFuncs.error("Hey there! Your OS isn't supported! Please use Mac or Windows.")

        except Exception as e:
            UTILITYFuncs.logAndPrint("INFO", f"UIFuncs/removeJadeAssistant: There was a problem removing Jade Assistant! {e}")
            UTILITYFuncs.error(f"There was a problem removing Jade Assistant! {e}")

    def checkForUpdates(self):
        global selectedApp
        global TruePath

        UTILITYFuncs.logAndPrint("INFO", "App/checkForUpdates: Checking if Jade Assistant exists or needs an update.")
        AppWindows = Path(f"{TruePath}{self.path}.exe").exists()
        AppMac = Path(f"{TruePath}{self.path}").exists()

        try:
            AppVersionFromServer = requests.get("https://nfoert.pythonanywhere.com/jadeAssistant/jadeAssistantVersion")
            AppVersionFromServer.raise_for_status()

        except Exception as e:
            UTILITYFuncs.logAndPrint("WARN", f"App/checkForUpdates: There was a problem checking {self.name} for updates! {e}")
            self.state = "ready"
            return False

        fsMAJOR = UTILITYFuncs.substring(AppVersionFromServer.text, "major=", ",minor")
        fsMINOR = UTILITYFuncs.substring(AppVersionFromServer.text, "minor=", ",patch")
        fsPATCH = UTILITYFuncs.substring(AppVersionFromServer.text, "patch=", "&")
        self.newVersion = f"{fsMAJOR}.{fsMINOR}.{fsPATCH}"
        
        if AppWindows == True or AppMac == True:
            UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: {self.name} exists!")
            # It exists! Now check for existance of version file
            
            UTILITYFuncs.logAndPrint("INFO", "App/checkForUpdates: App is Jade Assistant!")
            versionFile = self.path
            versionFile = versionFile.replace(" ", "")
            AppVersionFileExists = Path(f"{TruePath}{versionFile}Version.txt").exists()
            
            if AppVersionFileExists == True:
                #It exists! Now check for updates
                UTILITYFuncs.logAndPrint("INFO", "App/checkForUpdates: Checking for updates for Jade Assistant!")
                versionFileName = self.path.replace(" ", "")
                AppVersionFile = open(f"{TruePath}{versionFileName}Version.txt", "r")
                AppVersionFileContents = AppVersionFile.readlines()
                AppVersion_MAJOR = AppVersionFileContents[0]
                AppVersion_MINOR = AppVersionFileContents[1]
                AppVersion_PATCH =AppVersionFileContents[2]
                AppVersion = f"{AppVersion_MAJOR}.{AppVersion_MINOR}.{AppVersion_PATCH}"
                NewVersion = f"{fsMAJOR}.{fsMINOR}.{fsPATCH}"
                AppVersion = AppVersion.replace("\n", "")
                self.version = NewVersion

                if AppVersion_MAJOR < fsMAJOR:
                    # Updates required
                    self.state = "update"
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates required. {AppVersion_MAJOR} < {fsMAJOR}")
                    UTILITYFuncs.notification(f"{self.name} Update Avaliable.", f"Open {self.name}'s menu to update to version {NewVersion}.")

                elif AppVersion_MINOR < fsMINOR:
                    # Updates required
                    self.state = "update"
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates required. {AppVersion_MINOR} < {fsMINOR}")
                    UTILITYFuncs.notification(f"{self.name} Update Avaliable.", f"Open {self.name}'s menu to update to version {NewVersion}.")

                elif AppVersion_PATCH < fsPATCH:
                    # Updates required
                    self.state = "update"
                    UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: Updates required. {AppVersion_PATCH} < {fsPATCH}")
                    UTILITYFuncs.notification(f"{self.name} Update Avaliable.", f"Open {self.name}'s menu to update to version {NewVersion}.")

                else:
                    # Updates not required
                    self.state = "ready"
                    UTILITYFuncs.logAndPrint("INFO", "App/checkForUpdates: Updates not required.")

            else:
                self.state = "ready"
                UTILITYFuncs.logAndPrint("INFO", "App/checkForUpdates: Version file does not exist.")
                window_appMenu.version.hide()
                        

        elif AppWindows == False or AppMac == False:
            # It dosen't exist! Show button for downloading.
            UTILITYFuncs.logAndPrint("INFO", f"App/checkForUpdates: {self.name} dosen't exist!")
            self.state = "download"

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
        UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: Getting Connection Status from: {fromWhat}")
        try:
            gcRequest = requests.get("https://google.com")
            
            try:
                gcRequest.raise_for_status()

            except:
                UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: You're not connected! From: {fromWhat}")
                window_offline.show()
                window_main.offlineLabel.show()
                dialog_about.idLabel.hide()
                dialog_about.id.hide()
                window_main.leftBox_accountLabel.setText("You're offline")
                window_main.leftBox_accountLabel.setFont(QFont("Calibri", 8))
                window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
                window_main.leftBox_accountLabel.setStyleSheet("color: orange")
                UTILITYFuncs.notification("You're offline!", "Please connect to internet and restart.")
                return(False)

        except:
            UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: You're not connected! From: {fromWhat}")
            window_offline.show()
            window_main.offlineLabel.show()
            dialog_about.idLabel.hide()
            dialog_about.id.hide()
            window_main.leftBox_accountLabel.setText("You're offline")
            window_main.leftBox_accountLabel.setFont(QFont("Calibri", 8))
            window_main.leftBox_accountLabel.setAlignment(QtCore.Qt.AlignCenter)
            window_main.leftBox_accountLabel.setStyleSheet("color: orange")
            UTILITYFuncs.notification("You're offline!", "Please connect to internet and restart.")
            return(False)

        
        UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/getConnection: You're connected!")
        return(True)

    def substring(inputString, one, two):
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
                    UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: There was a problem substringing.")
                    UTILITYFuncs.error("Could not finish substringing!")

            except:
                UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: Unable to find the second string while substringing.")
                UTILITYFuncs.error("Could not find the second string while substringing!")
        
        except:
            UTILITYFuncs.logAndPrint("SUBSTRING", f"UTILTYFuncs/substring: Unable to find the first string while substringing.")
            UTILITYFuncs.error("Could not find the first string while substringing!")

    def error(Error):
        global killThreads
        killThreads = True
        window_main.hide()
        window_appMenu.hide()
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

    def notification(header, text):
        UTILITYFuncs.logAndPrint("INFO", f"UTILITYFuncs/notification: Showing notification with header '{header}' and text '{text}'")
        if window_notification.isVisible() == True:
            window_notification.hide()
            sleep(0.5)
            window_notification.show()
            window_notification.move(10, 10)

            window_notification.header.setText(header)
            window_notification.header.setFont(QFont("Calibri Bold", 14))
            window_notification.header.setAlignment(QtCore.Qt.AlignLeft)

            window_notification.body.setText(text)
            window_notification.body.setFont(QFont("Calibri", 12))
            window_notification.body.setAlignment(QtCore.Qt.AlignLeft)

        else:
            window_notification.show()
            window_notification.move(10, 10)

            window_notification.header.setText(header)
            window_notification.header.setFont(QFont("Calibri Bold", 12))
            window_notification.header.setAlignment(QtCore.Qt.AlignLeft)

            window_notification.body.setText(text)
            window_notification.body.setFont(QFont("Calibri", 10))
            window_notification.body.setAlignment(QtCore.Qt.AlignLeft)

    def logAndPrint(tag, text):
        UTILITYFuncs.log(tag, text)
        print(f"|{tag}| {text}")


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
                window_splash.show()
                window_splash.showMessage(text, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

            elif platform.system() == "Darwin":
                window_splash.show()
                window_splash.showMessage(text, alignment=132 | 64)

            else:
                print("Your OS isn't supported! Please use Windows or Mac.")
                UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")
        
        # Thanks to Liam on StackOverflow
        # https://stackoverflow.com/questions/58661539/create-splash-screen-in-pyqt5
        if platform.system() == "Windows":
            if developmental == False:
                splash_pix = QtGui.QPixmap(str(resource_path("JadeLauncherSplash.png")))

            elif developmental == True:
                splash_pix = QtGui.QPixmap(str(PurePath("assets/JadeLauncherSplash.png")))

            window_splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)

            screenSize = screen.size()
            moveHeight = screenSize.height() - 310
            window_splash.move(30, moveHeight)

            window_splash.setFont(QFont("Calibri", 18))
            show_message("Loading...")
            opaqueness = 0.0
            step = 0.03
            window_splash.setWindowOpacity(opaqueness)
            window_splash.show()
            while opaqueness < 1:
                window_splash.setWindowOpacity(opaqueness)
                sleep(step)
                opaqueness += step

        elif platform.system() == "Darwin":
            if developmental == False:
                splash_pix = QtGui.QPixmap(str(resource_path("JadeLauncherSplash.png")))

            elif developmental == True:
                splash_pix = QtGui.QPixmap(str(PurePath("assets/JadeLauncherSplash.png")))

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
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates are required.")
                        update = "yes"

                    elif Version_MINOR < requestMinor:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates are required.")
                        update = "yes"

                    elif Version_PATCH < requestPatch:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates are required.")
                        update = "yes"

                    else:
                        UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Updates not required.")
                        update = "no"

                else:
                    UTILITYFuncs.logAndPrint("WARN", "MAINFuncs/mainCode/checkForUpdates: Version requests are not ok!")
                    update = "no"
                    window_splash.hide()
                    UTILITYFuncs.error("It looks like my web server is down. Wait a bit and see if it fixes, otherwise please send me an email and I'll take a look at it. You could also check PythonAnywhere's twitter page to see if it's down. (That's who hosts the web server for me.)")
                    return(False)
                
                if update == "yes":
                    UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: An update is avaliable.")
                
                # Automatic updates was removed in 0.0.12, will be re added in 2.0.0 most likely

                #     show_message("Downloading update file...")

                #     if platform.system() == "Windows":
                #         OS = "Windows"
                #         path = f"{TruePath}Jade Launcher.exe.download"

                #     elif platform.system() == "Darwin":
                #         OS = "Mac"
                #         path = f"{TruePath}Jade Launcher.download.app"

                #     else:
                #         UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")


                #     LauncherDownload = requests.get(f"https://nfoert.pythonanywhere.com/jadeLauncher/download?{OS}&", stream=True)
                #     total_size_in_bytes = int(LauncherDownload.headers.get('content-length', 0))
                #     bytes_downloaded = 0
                #     last = 0
                        
                #     with open(f'{path}', 'wb') as file:

                #         for data in LauncherDownload.iter_content(1024):
                #             file.write(data)
                #             bytes_downloaded = bytes_downloaded + 1024
                #             percent = bytes_downloaded / total_size_in_bytes
                #             percent = percent * 100
                #             percent = round(percent)
                #             if last != percent:
                #                 last = percent
                #                 show_message(f"Downloading update... [{percent}%]")
                #             else:
                #                 continue


                #     LauncherDownload.close()
                #     file.close()



                #     if platform.system() == "Windows":
                #         window_splash.hide()
                #         app.quit()
                #         subprocess.call(["updateWindows.bat", f"{TruePath}"])
                #         sys.exit()


                #     elif platform.system() == "Darwin":
                #         window_splash.hide()
                #         app.quit()
                #         subprocess.run(["sh", f"{TruePath}updateMac.sh", f"{TruePath}"])
                #         sys.exit()

                #     else:
                #         UTILITYFuncs.error("Your OS isn't supported! Please use Windows or Mac.")

                
                # elif update == "no":
                #     UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Not updating. Going to try to remove the updater - just in case it exists.")

                # else:
                #     UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: Not updating. Couldn't figure out if we're supposed to or not, so let's say no.")

                elif update == "no":
                    UTILITYFuncs.logAndPrint("INFO", "MAINFuncs/mainCode/checkForUpdates: No update is avaliable.")


            elif gc == False:
                UTILITYFuncs.logAndPrint("NOT CONNECTED", "MAINFuncs/mainCode/checkForUpdates: You're not connected! Skipping checking for updates.")
                update = False
                window_main.show()
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()

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
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()

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
                    window_main.newsBox1.hide()
                    window_main.newsBox2.hide()
                    window_main.newsBox3.hide()

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
                    window_main.newsBox1.hide()

                if newsRequest2.ok == True:
                    pass
                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: NEWS 2 FAIL")
                    window_main.newsBox2.hide()

                if newsRequest3.ok == True:
                    pass
                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: NEWS 3 FAIL")
                    window_main.newsBox3.hide()
                    
                
                # News 1
                nr1Text = newsRequest1.text
                if "header=" in nr1Text:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: News 1 is good!")
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
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 1. Code is '{newsCode1}'")
                    window_main.newsBox1.hide()

                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There was a problem validating the first news request.")
                    window_main.newsBox1.hide()

                # News 2
                nr2Text = newsRequest2.text
                if "header=" in nr2Text:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: News 2 is good!")
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
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 2. Code is '{newsCode2}'")
                    window_main.newsBox2.hide()

                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There was a problem validating the second news request.")
                    window_main.newsBox2.hide()

                # News 3
                nr3Text = newsRequest3.text
                if "header=" in nr3Text:
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: News 3 is good!")
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
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There's no news article that matches that code for news article 3. Code is '{newsCode3}'")
                    window_main.newsBox3.hide()

                else:
                    UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: There was a problem validating the third news request.")
                    window_main.newsBox3.hide()


                # Check for emptiness deep inside themselves
                if newsCode1 == "000":
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Hiding news 1 as the code is 000.")
                    window_main.newsBox1.hide()

                else:
                    pass

                if newsCode2 == "000":
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Hiding news 2 as the code is 000.")
                    window_main.newsBox2.hide()

                else:
                    pass

                if newsCode3 == "000":
                    UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Hiding news 3 as the code is 000.")
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
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews:There was a problem setting up news1 Class. {e}")
                    window_main.newsBox1.hide()
                
                try:
                    news2.header = news2Header
                    news2.text = news2Text
                    news2.date = news2Date
                    news2.url = news2Url
                
                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There was a problem setting up news2 Class. {e}")
                    window_main.newsBox2.hide()

                try:
                    news3.header = news3Header
                    news3.text = news3Text
                    news3.date = news3Date
                    news3.url = news3Url

                except Exception as e:
                    UTILITYFuncs.logAndPrint("WARN", f"THREADFuncs/mainCode/fetchNews: There was a problem setting up news3 Class. {e}")
                    window_main.newsBox3.hide()


            elif gc == False:
                UTILITYFuncs.logAndPrint("NOT CONNECTED", "THREADFuncs/mainCode/fetchNews: Skipping fetching of news as you're not conected.")
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()
                window_main.show()

            else:
                UTILITYFuncs.logAndPrint("WARN", "THREADFuncs/mainCode/fetchNews: Skipping fetching of news as we can't decide if you're connected or not.")
                window_main.newsBox1.hide()
                window_main.newsBox2.hide()
                window_main.newsBox3.hide()


        elif CONFIG_FetchNews == False:
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/fetchNews: Skipping fetching of news as it's not allowed.")
            window_main.newsBox1.hide()
            window_main.newsBox2.hide()
            window_main.newsBox3.hide()
        
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
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message: Good morning.")

        elif any(x in now for x in ["12", "13", "14", "15"]) == True:
            window_main.welcomeBox_text.setText("Good afternoon.")
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message: Good afternoon.")

        elif any(x in now for x in ["16", "17", "18", "19", "20", "21", "22", "23"]) == True:
            window_main.welcomeBox_text.setText("Good evening.")
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message: Good evening.")

        else:
            window_main.welcomeBox_text.setText("Welcome back to the")
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/setGreeting: Selected welcome message (hit else): Welcome back to the ")


        window_main.welcomeBox_text.setFont(QFont("Calibri Bold", 16))
        window_main.welcomeBox_text.setAlignment(QtCore.Qt.AlignCenter)

        
        # Check if Jade Assistant exists, or needs an update.
        show_message("Loading Jade Assistant...")
        JadeAssistant.checkForUpdates()

        # Check for suspension
        if myAccount.suspended == "no":
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/suspensionCheck: Not suspended.")
            show_message("Done!")
            sleep(1.5)
            window_main.show()
            window_main.show()

        else:
            UTILITYFuncs.logAndPrint("INFO", "THREADFuncs/mainCode/suspensionCheck: Suspended.")
            window_splash.hide()
            dialog_accountSuspended.show()

        elapsedTime = runDuration() - startElapsedTime
        elapsedTime = round(elapsedTime)

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
                UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openAccountScreen: There was a problem checking if you're signed in or not to open the Account screen.")

        elif gc == False:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openAccountScreen: You're not connected!")

        else:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openAccountScreen: Unable to determine connectivity.")

    def openPlus():
        global myAccount

        if myAccount.plus == "True":
            window_plusOwned.show()

        elif myAccount.plus == "False":
            window_plus.show()

        else:
            UTILITYFuncs.logAndPrint("INFO", "UIFuncs/openPlus: There was a problem checking if you have Jade Plus or not.")

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
        global SignedIn
        global selectedApp
        global TruePath
        gc = UTILITYFuncs.getConnection("Open Jade Assistant Menu")
        if gc == True:
            if SignedIn == True:
                selectedApp = "Jade Assistant"
                JadeAssistant.openAppMenu()

            else:
                UTILITYFuncs.notification("You're not signed in!", "Sign in first, then try again.")

        else:
            accountFile = open(f"{TruePath}account.txt", "r")
            accountFileRead = accountFile.readlines()
            accountFile.close()

            if len(accountFileRead) == 2:
                selectedApp = "Jade Assistant"
                JadeAssistant.state = "readyoffline"
                JadeAssistant.openAppMenu()

            else:
                UTILITYFuncs.notification("You're not signed in!", "Connnect to internet, restart the Launcher, sign in, then try again.")

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
            WEBVIEW.openWebView("https://nfoert.pythonanywhere.com/jadesite/allposts?category=changelog&")

        elif platform.system() == "Darwin":
            webbrowser.open("https://nfoert.pythonanywhere.com/jadesite/allposts?category=changelog&")

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

    def closeNotification():
        window_notification.hide()

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
            UTILITYFuncs.notification("There was a problem creating a verification code.", f"{e}")

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

    def openUpdatePage():
        # TODO:
        webbrowser.open("https://nofoert.wixsite.com/jade/download")

    def notNowUpdate():
        window_update.hide()

    def debugOpenAllWindows():
        global debugOpenAllWindows
        if debugOpenAllWindows == True:
            UTILITYFuncs.logAndPrint("DEBUG", "Opening all windows! (Much chaos ahead, beware!)")
            window_accountDetails.show()
            window_offline.show()
            window_appMenu.show()
            window_changePassword.show()
            window_createAccount.show()
            window_changePassword.show()
            window_main.show()
            window_signIn.show()
            UTILITYFuncs.notification("Debug: Show all windows!", "This window was opened to assist in UI related debug related to apperances. test test test test test test test test test test test test test test test test test test thank you")
            window_update.show()
            dialog_about.show()
            dialog_accountSuspended.show()
            dialog_error.show()
            dialog_signInFailure.show()
            if platform.system() == "Windows":
                window_webView.show()

    # -----

    

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
        window_expandedNews = uic.loadUi(str(PurePath(resource_path("expandedNews.ui"))))
        window_changelog = uic.loadUi(str(PurePath(resource_path("changelog.ui"))))
        if platform.system() == "Windows":
            window_webView = uic.loadUi(str(PurePath(resource_path("webView.ui"))))

        else:
            UTILITYFuncs.logAndPrint("INFO", 'Not using PyQtWebEngine because it is mac os')
        window_changePassword = uic.loadUi(str(PurePath(resource_path("changePassword.ui"))))
        window_appMenu = uic.loadUi(str(PurePath(resource_path("appMenu.ui"))))
        window_update = uic.loadUi(str(PurePath(resource_path("update.ui"))))
        dialog_signInFailure = uic.loadUi(str(PurePath(resource_path("signInFailure.ui"))))
        dialog_accountSuspended = uic.loadUi(str(PurePath(resource_path("accountSuspended.ui"))))
        dialog_error = uic.loadUi(str(PurePath(resource_path("error.ui"))))
        dialog_about = uic.loadUi(str(PurePath(resource_path("about.ui"))))

    except Exception as e:
        UTILITYFuncs.logAndPrint("FATAL", f"PyQt5: There was a problem creating windows! (During a non-developmental run) {e}")
        UTILITYFuncs.error(f"There was a problem creating windows! (During a non-developmental run {e}")

elif developmental == True:
    UTILITYFuncs.logAndPrint("INFO", "PyQt5: Loading like it's a .py")
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
        window_expandedNews = uic.loadUi(str(PurePath("ui/expandedNews.ui")))
        window_changelog = uic.loadUi(str(PurePath("ui/changelog.ui")))
        if platform.system() == "Windows":
            window_webView = uic.loadUi(str(PurePath("ui/webView.ui")))

        elif platform.system() == "Darwin":
            UTILITYFuncs.logAndPrint("INFO", "Not creating the webview window because you're on mac os")
        window_changePassword = uic.loadUi(str(PurePath("ui/changePassword.ui")))
        window_appMenu = uic.loadUi(str(PurePath("ui/appMenu.ui")))
        window_update = uic.loadUi(str(PurePath("ui/update.ui")))
        dialog_signInFailure = uic.loadUi(str(PurePath("ui/signInFailure.ui")))
        dialog_accountSuspended = uic.loadUi(str(PurePath("ui/accountSuspended.ui")))
        dialog_error = uic.loadUi(str(PurePath("ui/error.ui")))
        dialog_about = uic.loadUi(str(PurePath("ui/about.ui")))

    except Exception as e:
       UTILITYFuncs.logAndPrint("FATAL", f"PyQt5: There was a problem creating windows! (During a developental run) {e}")
       UTILITYFuncs.error(f"There was a problem creating windows! (During a developmental run {e}")
        

else:
    UTILITYFuncs.logAndPrint("FATAL", f"PyQt5: There was a *terrible* problem when opening windows. It it in developental mode? We dont know. Variable is '{developmental}'")
    UTILITYFuncs.error(f"There was a problem determining if we're running as developental or not. Variable is '{developmental}'")
    sys.exit()

# Connect buttons to functions

# Offline
window_offline.button.clicked.connect(UIFuncs.closeOffline)

# Main Screen
window_main.leftBox_jadeAccountButton.clicked.connect(UIFuncs.openAccountScreen)
#window_main.leftBox_jadeBarButton.clicked.connect(UIFuncs.openJadeBar)
#window_main.leftBox_plusButton.clicked.connect(UIFuncs.openPlus)
window_main.leftBox_jadeAssistantButton.clicked.connect(UIFuncs.jadeAssistantButton)
window_main.button1.clicked.connect(UIFuncs.expandNews1)
window_main.button2.clicked.connect(UIFuncs.expandNews2)
window_main.button3.clicked.connect(UIFuncs.expandNews3)
window_main.changelogButton.clicked.connect(UIFuncs.openChangelog)
window_main.actionQuit_Jade_Launcher.triggered.connect(UIFuncs.stopAll)
window_main.actionRestart_Jade_Launcher.triggered.connect(UIFuncs.restartAction)
window_main.action_About.triggered.connect(UIFuncs.openAbout)

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

# Expanded news screen
window_expandedNews.openUrl.clicked.connect(UIFuncs.openUrlButton)

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

elif platform.system() == "Darwin":
    UTILITYFuncs.logAndPrint("INFO", "Not setting up the webview window because you're on mac os.")

# Jade Assistant menu
window_appMenu.launchButton.clicked.connect(UIFuncs.launchApp)
window_appMenu.downloadButton.clicked.connect(UIFuncs.downloadApp)
window_appMenu.updateButton.clicked.connect(UIFuncs.updateApp)
window_appMenu.removeButton.clicked.connect(UIFuncs.removeApp)
window_appMenu.version.setAlignment(QtCore.Qt.AlignCenter)

# Notification window
window_notification.button.clicked.connect(UIFuncs.closeNotification)
window_notification.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

# About dialog
dialog_about.version.setText(Version_TOTAL)
dialog_about.version.setFont(QFont("Calibri", 16))
dialog_about.version.setAlignment(QtCore.Qt.AlignLeft)
dialog_about.button.clicked.connect(UIFuncs.aboutWebsiteButton)
dialog_about.logButton.clicked.connect(UIFuncs.aboutLogButton)

# Change Password Window
window_changePassword.button.clicked.connect(UIFuncs.changePassword)

# App Menu
window_appMenu.progressBar.hide()

# Update menu
window_update.download.clicked.connect(UIFuncs.openUpdatePage)
window_update.notNow.clicked.connect(UIFuncs.notNowUpdate)

# -----
# Set properties of windows
# -----
window_jadeBar.move(10, 10)

# Splash Text
splashTexts = ["It's nice to see you!", "Hey there!", "This is some splash text!"]
splashTextChoice = random.choice(splashTexts)
UTILITYFuncs.logAndPrint("INFO", f"PyQt5: Selected splash text: '{splashTextChoice}'")
window_main.splash.setText(f"[ {splashTextChoice} ]")
window_main.splash.setFont(QFont("Calibri", 18))

window_main.splash.hide()
#Yes, I removed it. Not needed right now.

window_main.offlineLabel.hide()


#Can't seem to get to work.

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
            UTILITYFuncs.error(f"The gui loop had a problem running some code! '{e}'")

if doMain == True:
    guiLoopTimer = QTimer()
    guiLoopTimer.timeout.connect(guiLoop)
    guiLoopTimer.start(1)

    myAccount = Account("False", "no", "loading...")

    news1 = News("loading", "loading", "loading", "loading", "1")
    news2 = News("loading", "loading", "loading", "loading", "2")
    news3 = News("loading", "loading", "loading", "loading", "3")

    Launcher = LauncherId("loading", "loading") 

    firstGC = UTILITYFuncs.getConnection("main")
    if firstGC == True:
        JadeAssistantDescription = "Jade is a virtual assistant for your computer's desktop designed to be as helpful as possible, while being able to change size to fit your workflow."
        JadeAssistant = App("Jade Assistant", JadeAssistantDescription, "Jade Assistant", "Loading...")
        MAINFuncs.mainCode()

    JadeAssistant_UpdateThread = threading.Thread(target=JadeAssistant.updateApp)
    JadeAssistant_DownloadThread = threading.Thread(target=JadeAssistant.downloadApp)

    JadeAssistant_UpdateThread.start()
    JadeAssistant_DownloadThread.start()

    if update == "yes":
        window_update.show()

    else:
        UTILITYFuncs.logAndPrint("INFO", "Updates not required.")

    UIFuncs.debugOpenAllWindows()
    #UTILITYFuncs.logAndPrint("TRUEPATH", TruePath)

    app.exec()

elif doMain == False:
    UTILITYFuncs.logAndPrint("INFO", "Start App: Argument detected. Will not do normal startup.")
    app.exec()

else:
    UTILITYFuncs.error("There was a problem checking if we need to do main startup code or not.")
    UTILITYFuncs.logAndPrint("FATAL", "Start App: There was a problem checking if we need to do main startup code or not.")

