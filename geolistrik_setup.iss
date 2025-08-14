[Setup]
#define MyAppVersion "{{VERSION}}"
#define MyAppVersionInfo "{{VERSION_INFO}}"
#define AppName "Geolistrik"

AppName={#AppName}
AppVersion={#MyAppVersion}
AppPublisher=Yusuf Umar Al Hakim
DefaultDirName={pf}\{#AppName} {#MyAppVersion}
DefaultGroupName={#AppName} {#MyAppVersion}
UninstallDisplayIcon={app}\geolistrik.exe
OutputBaseFilename=geolistriksetup-{#MyAppVersion}
OutputDir=output
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
VersionInfoVersion={#MyAppVersionInfo}
VersionInfoCompany=Yusuf Umar Al Hakim
VersionInfoDescription=Geolistrik CLI App
VersionInfoProductName=Geolistrik
VersionInfoProductVersion={#MyAppVersion}
SetupIconFile=assets\icon.ico

[Files]
Source: "build\__main__.exe"; DestDir: "{app}"; DestName: "geolistrik.exe"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
; Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme

[Icons]
Name: "{group}\Geolistrik CLI"; Filename: "{app}\geolistrik.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Command Prompt (Geolistrik)"; Filename: "{cmd}"; Parameters: "/K cd /d ""{app}"""; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall Geolistrik"; Filename: "{uninstallexe}"; IconFilename: "{app}\icon.ico"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox(
      'Untuk menggunakan Geolistrik CLI dari Command Prompt, ' +
      'tambahkan path berikut ke PATH lingkungan sistem Anda:' + #13#13 +
      ExpandConstant('{app}') + #13#13 +
      'Atau jalankan langsung dengan path penuh:' + #13 +
      '"' + ExpandConstant('{app}') + '\geolistrik' + '.exe"',
      mbInformation, MB_OK
    );
  end;
end;
