@echo off
chcp 65001 >nul
echo ============================================
echo   Сборка приложения Concentration Hub
echo ============================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Ошибка] Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)

echo [1/4] Установка зависимостей...
pip install customtkinter pyinstaller -q

echo [2/4] Создание структуры папок...
if not exist "dist\modules" mkdir dist\modules

echo [3/4] Компиляция модулей в EXE...

REM Главный лаунчер
echo   - main.py -> ConcentrationHub.exe
pyinstaller --onefile --windowed --name "ConcentrationHub" ^
    --icon=NONE ^
    --add-data "modules;modules" ^
    --hidden-import=customtkinter ^
    main_launcher\main.py 2>nul

REM Модули
for %%f in (modules\module*.py) do (
    set fname=%%~nf
    echo   - !fname!.py -> !fname!.exe
    pyinstaller --onefile --windowed --name "!fname!" ^
        --hidden-import=customtkinter ^
        "%%f" 2>nul
)

echo [4/4] Копирование EXE файлов...
copy /Y dist\ConcentrationHub.exe . >nul
copy /Y dist\modules\*.exe modules\ 2>nul

echo.
echo ============================================
echo   Сборка завершена!
echo ============================================
echo.
echo Файлы готовы:
echo   - ConcentrationHub.exe (главное приложение)
echo   - modules/*.exe (10 модулей)
echo.
pause
