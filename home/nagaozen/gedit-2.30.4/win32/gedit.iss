[Setup]
AppName=gedit
AppVerName=gedit 2.30.4
DefaultDirName={pf}\gedit
DefaultGroupName=gedit
UninstallDisplayIcon={app}\gedit.exe
Uninstallable=yes
AppPublisher=GNOME
AppPublisherURL=http:\\www.gedit.org\
AppVersion=2.30.4
OutputBaseFilename=gedit-setup-2.30.4-INSTALLERREVISION
LicenseFile=gedit\share\doc\COPYING

[Components]
Name: "gtk"; Description: "GTK+ runtime environment"; Types: full compact custom; Flags: fixed
Name: "main"; Description: "Gedit"; Types: full compact custom; Flags: fixed

; TODO: Enable languages separately
Name: "python"; Description: "Python runtime and modules"; Types: full compact custom; Flags: fixed
Name: "locale"; Description: "Translations"; Types: full compact custom; Flags: fixed

[Tasks]
Name: common; Description: "For all users"; Components: main; Flags: exclusive
Name: user; Description: "For the current user only"; Components: main; Flags: exclusive unchecked
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Icons]
; Common task icons
Name: "{commonprograms}\{groupname}\gedit"; Filename: "{app}\bin\gedit.exe"; Tasks: common
Name: "{commonprograms}\{groupname}\Uninstall gedit"; Filename: "{uninstallexe}"; Tasks: common
Name: "{commondesktop}\gedit"; Filename: "{app}\bin\gedit.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\gedit"; Filename: "{app}\bin\gedit.exe"; Tasks: quicklaunchicon

; User task icons
Name: "{userprograms}\{groupname}\gedit"; Filename: "{app}\bin\gedit.exe"; Tasks: user
Name: "{userprograms}\{groupname}\Uninstall gedit"; Filename: "{uninstallexe}"; Tasks: user

[Files]

; All files
Source: "gtk\*"; DestDir: "{app}\"; Components: gtk; Flags: recursesubdirs
Source: "gedit\*"; DestDir: "{app}\"; Components: main; Flags: recursesubdirs
Source: "python\*"; DestDir: "{app}\bin"; Components: python; Flags: recursesubdirs
Source: "locale\*"; DestDir: "{app}\"; Components: locale; Flags: recursesubdirs

[Run]
Filename: "{app}\bin\querymodules.bat"; StatusMsg: "Querying modules..."; Flags: runhidden

[Code]
{ Remove generated files not generated by the installer }

// Skip Components selection, all components are required anyway
function ShouldSkipPage(CurPageID: Integer): Boolean;
begin
	if CurPageID = wpSelectComponents then
		Result := True
	else
		Result := False;
end;