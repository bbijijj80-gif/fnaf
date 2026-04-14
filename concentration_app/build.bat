@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
echo ============================================
echo   Concentration Hub Build Script
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found! Install Python 3.8+
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install customtkinter pyinstaller -q

echo [2/4] Creating folder structure...
if not exist "dist\modules" mkdir dist\modules

echo [3/4] Compiling modules to EXE...

REM Main launcher
echo   - main.py to ConcentrationHub.exe
pyinstaller --onefile --windowed --name "ConcentrationHub" ^
    --icon=NONE ^
    --add-data "modules;modules" ^
    --hidden-import=customtkinter ^
    main_launcher\main.py

REM Modules
for %%f in (modules\module*.py) do (
    set "fname=%%~nf"
    echo   - !fname!.py to !fname!.exe
    pyinstaller --onefile --windowed --name "!fname!" ^
        --hidden-import=customtkinter ^
        "%%f"
)

echo [4/4] Copying EXE files...
copy /Y dist\ConcentrationHub.exe . >nul
if exist "dist\modules\*.exe" copy /Y dist\modules\*.exe modules\ 2>nul

echo.
echo ============================================
echo   Build Complete!
echo ============================================
echo.
echo Ready files:
echo   - ConcentrationHub.exe (main app)
echo   - modules/*.exe (10 modules)
echo.
pause
