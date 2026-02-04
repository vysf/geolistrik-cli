[Setup]
#define MyAppVersion "{{VERSION}}"
#define MyAppVersionInfo "{{VERSION_INFO}}"
#define AppName "Geolistrik"

AppName={#AppName}
AppVersion={#MyAppVersion}
AppPublisher=Yusuf Umar Al Hakim

DefaultDirName={pf}\{#AppName}
DisableDirPage=yes
DefaultGroupName={#AppName}

UninstallDisplayIcon={app}\geolistrik.exe
OutputBaseFilename=geolistriksetup-{#MyAppVersion}
OutputDir=output

Compression=lzma
SolidCompression=yes

PrivilegesRequired=admin
CloseApplications=yes
RestartApplications=no

VersionInfoVersion={#MyAppVersionInfo}
VersionInfoCompany=Yusuf Umar Al Hakim
VersionInfoDescription=Geolistrik CLI App
VersionInfoProductName=Geolistrik
VersionInfoProductVersion={#MyAppVersion}

SetupIconFile=assets\icon.ico
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "addtopath"; \
Description: "Add Geolistrik to PATH environment variable (Recommended)"; \
Flags: checkedonce

Name: "opendocs"; \
Description: "Open documentation after installation"; \
Flags: unchecked

[Files]
Source: "build\__main__.exe"; DestDir: "{app}"; DestName: "geolistrik.exe"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Geolistrik CLI"; Filename: "{app}\geolistrik.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Command Prompt (Geolistrik)"; Filename: "{cmd}"; Parameters: "/K cd /d ""{app}"""; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall Geolistrik"; Filename: "{uninstallexe}"; IconFilename: "{app}\icon.ico"

[Code]
const
  WM_SETTINGCHANGE = $001A;
  DocsURL = 'https://github.com/vysf/geolistrik-cli';

procedure AddToPath(Path: string);
var
  Paths: string;
begin
  if not RegQueryStringValue(HKCU, 'Environment', 'Path', Paths) then
    Paths := '';

  if Pos(Path, Paths) = 0 then
  begin
    if paths <> '' then
      Paths := Paths + ';';
    Paths := Paths + Path;

    RegWriteStringValue(HKCU, 'Environment', 'Path', Paths);
  end;
end;

procedure RemoveFromPath(Path: string);
var
  Paths: string;
  Items: TStringList;
  I: Integer;
begin
  if not RegQueryStringValue(HKCU, 'Environment', 'Path', Paths) then
    Exit;
  
  Items := TStringList.Create;
  try
    Items.Delimiter := ';';
    Items.StrictDelimiter := True;
    Items.DelimitedText := Paths;

    for I := Items.Count - 1 downto 0 do
      if CompareText(Trim(Items[I]), Path) = 0 then
        Items.Delete(I);

    RegWriteStringValue(HKCU, 'Environment', 'Path', Items.DelimitedText);
  finally
    Items.Free;
  end;
end;

procedure RefreshEnvironment;
begin
  SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, 0, 0);
end;

procedure BackupOldExe;
var
  ExePath, BackupPath: string;
begin
  ExePath := ExpandConstant('{app}\geolistrik.exe');
  BackupPath := ExePath + '.bak';
  if FileExists(ExePath) then
  begin
    if FileExists(BackupPath) then
      DeleteFile(BackupPath);
    RenameFile(ExePath, BackupPath);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    { Kill current geolistrik.exe if running from app folder }
    Exec(
      'taskkill',
      '/F /IM geolistrik.exe',
      '',
      SW_HIDE,
      ewWaitUntilTerminated,
      ResultCode
    );

    { Add to PATH }
    if wizardIsTaskSelected('addtopath') then
    begin
      AddToPath(ExpandConstant('{app}'));
      RefreshEnvironment;
    end;

    { Open documentation }
    if wizardIsTaskSelected('opendocs') then
    begin
      ShellExec('open', DocsURL, '', '', SW_SHOWNORMAL, ewNoWait, ResultCode);
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    RemoveFromPath(ExpandConstant('{app}'));
    RefreshEnvironment;
  end;
end;
