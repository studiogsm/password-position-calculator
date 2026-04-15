@echo off
chcp 65001 >nul
echo ============================================================
echo   Password Position Calculator v1.0
echo   Laboratorium Elektroniki
echo   Kompilacja do EXE
echo ============================================================
echo.

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo BLAD: Python nie znaleziony. Zainstaluj Python 3.x
    pause & exit /b 1
)

echo [1/4] Sprawdzam PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Instaluje PyInstaller...
    python -m pip install pyinstaller --quiet
)
echo PyInstaller OK.

echo.
echo [2/4] Czyszcze poprzednie buildy...
if exist build        rmdir /s /q build
if exist dist         rmdir /s /q dist
if exist __pycache__  rmdir /s /q __pycache__
if exist PasswordPositionCalculator.spec del /f PasswordPositionCalculator.spec

echo.
echo [3/4] Kompiluje EXE...
if exist icon.ico (
    pyinstaller --noconfirm --clean --onefile --windowed --name="PasswordPositionCalculator" --icon="icon.ico" password_position_calculator.py
) else (
    pyinstaller --noconfirm --clean --onefile --windowed --name="PasswordPositionCalculator" password_position_calculator.py
)

if errorlevel 1 (
    echo.
    echo BLAD kompilacji!
    pause & exit /b 1
)

echo.
echo [4/4] Kopiowanie ikony obok EXE...
if exist icon.ico (
    copy icon.ico dist\icon.ico >nul
    echo Ikona skopiowana.
)

echo.
echo ============================================================
echo   SUKCES! Plik: dist\PasswordPositionCalculator.exe
echo ============================================================
echo.
explorer dist
pause
