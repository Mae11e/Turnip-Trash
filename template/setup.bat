@echo off
REM Script de setup pour Windows

echo Game Jam Template - Setup
echo.

REM Vérifie si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo Python n'est pas installe ou n'est pas dans le PATH!
    pause
    exit /b 1
)

REM Crée le venv s'il n'existe pas
if not exist "venv\" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
    echo Environnement virtuel cree
) else (
    echo Environnement virtuel deja existant
)

REM Active le venv
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Install les dépendances
echo Installation des dependances...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup termine!
echo.
echo Pour lancer le jeu, double-cliquez sur run.bat
echo Ou executez: venv\Scripts\activate.bat puis python main.py
echo.
pause
