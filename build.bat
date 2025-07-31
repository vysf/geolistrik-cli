@echo off
setlocal

REM ─── Konfigurasi Versi ──────────────────────────────
set VERSION=dev
echo [INFO] Menggunakan versi: %VERSION%

REM ─── Generate geolistrik_setup.iss dari template ────
echo [INFO] Membuat file geolistrik_setup.iss dari template...
powershell -Command ^
  "(Get-Content geolistrik_setup.iss.in) -replace '\{\{VERSION\}\}', '%VERSION%' | Set-Content geolistrik_setup.iss"

REM ─── Set environment variable untuk config.py ───────
set GEOLISTRIK_VERSION=%VERSION%

REM ─── Build CLI dengan Nuitka ────────────────────────
echo [INFO] Build dengan Nuitka...
nuitka ^
  --standalone ^
  --onefile ^
  --include-package=geolistrik ^
  --windows-icon-from-ico=assets\icon.ico ^
  --output-dir=build ^
  geolistrik\__main__.py

IF EXIST build\__main__.exe (
    echo [OK] Build selesai: build\__main__.exe
) ELSE (
    echo [ERROR] Build gagal!
    exit /b 1
)

REM ─── Kompilasi installer dengan Inno Setup ──────────
echo [INFO] Kompilasi installer dengan Inno Setup...
IF EXIST "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" geolistrik_setup.iss
    echo [OK] Installer selesai dibuat di folder output\
) ELSE (
    echo [WARNING] Inno Setup tidak ditemukan. Lewati kompilasi installer.
)

endlocal
pause
