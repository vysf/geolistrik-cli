[Setup]
#define MyAppVersion "{{VERSION}}"
#define MyAppVersionInfo "{{VERSION_INFO}}"
#define AppName "Geolistrik"

AppName={#AppName}
AppVersion={#MyAppVersion}
AppPublisher=Yusuf Umar Al Hakim
DefaultDirName={pf}\{#AppName}
DefaultGroupName={#AppName}
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
uses
  Windows, Messages, SysUtils;

{ ---- Fungsi Utility ---- }
function IsEnvPathVariableContaining(const VarName, Value: string): Boolean;
var
  EnvValue: string;
begin
  EnvValue := GetEnv(VarName);
  Result := Pos(LowerCase(Value), LowerCase(EnvValue)) > 0;
end;

procedure AddToPath(const Value: string);
var
  OldPath: string;
begin
  OldPath := GetEnv('PATH');
  if (OldPath = '') or (OldPath[Length(OldPath)] <> ';') then
    OldPath := OldPath + ';';
  RegWriteStringValue(HKEY_CURRENT_USER,
                      'Environment',
                      'PATH',
                      OldPath + Value);
end;

procedure RefreshEnvironment;
var
  R: Integer;
begin
  SendMessageTimeout(HWND_BROADCAST, WM_SETTINGCHANGE, 0,
                     LPARAM(PChar('Environment')), SMTO_ABORTIFHUNG, 5000, R);
end;

{ ---- Main Post-Install ---- }
procedure CurStepChanged(CurStep: TSetupStep);
var
  NewPath: string;
begin
  if CurStep = ssPostInstall then
  begin
    NewPath := ExpandConstant('{app}');
    { Tambahkan PATH hanya jika belum ada }
    if not IsEnvPathVariableContaining('PATH', NewPath) then
    begin
      AddToPath(NewPath);
      RefreshEnvironment;
    end;

    MsgBox('Geolistrik CLI sudah siap digunakan dari Command Prompt.'#13#10 +
           'Path telah otomatis ditambahkan (untuk pengguna baru).',
           mbInformation, MB_OK);
  end;
end;
