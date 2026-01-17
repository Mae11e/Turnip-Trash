@echo off
REM Script de lancement pour Windows

echo Game Jam Template - Lancement...
echo.

REM Vérifie si le venv existe
if not exist "venv\" (
    echo Environnement virtuel non trouve
    echo Lancement du setup...
    call setup.bat
    if errorlevel 1 (
        echo Erreur lors du setup
        pause
        exit /b 1
    )
)

REM Active le venv
call venv\Scripts\activate.bat

REM Lance le jeu
python main.py

pause
