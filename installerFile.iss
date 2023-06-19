; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Jade Launcher"
#define MyAppVersion "2.1.1"
#define MyAppPublisher "Jade Software"
#define MyAppURL "https://nfoert.pythonanywhere.com/jadesite"
#define MyAppExeName "Jade Launcher.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{ECB9CC21-2A2C-4CC0-AF9D-38AE1CFADAA5}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputBaseFilename=Jade Launcher Installer
SetupIconFile=C:\Users\nfo23\OneDrive\Documents\Programming\THE NEW OF ALL\Jade Launcher\Jade Launcher Development Venv\Jade Launcher 2.1.1\favicon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon="{app}\{#MyAppExeName}"

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\nfo23\OneDrive\Documents\Programming\THE NEW OF ALL\Jade Launcher\Jade Launcher Development Venv\Jade Launcher 2.1.1\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}/account.txt"
Type: files; Name: "{app}/id.txt"
Type: files; Name: "{app}/jadeLauncherConfig.bak"
Type: files; Name: "{app}/jadeLauncherConfig.dat"
Type: files; Name: "{app}/jadeLauncherConfig.dir"
Type: files; Name: "{app}/jadeLauncherLog.txt"
Type: files; Name: "{app}/jadeAssistantVersion.txt"
Type: files; Name: "{app}/jadeAppsVersion.txt"
Type: files; Name: "{app}/Jade Launcher.exe.download"
Type: files; Name: "{app}/Jade Launcher.exe.old"
Type: filesandordirs; Name: "{app}/apps"

