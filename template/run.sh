#!/bin/bash
# Script de lancement rapide

echo "🎮 Lancement du Game Jam Template..."
echo ""

# Vérifie si le venv existe
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel non trouvé"
    echo "Lancement du setup..."
    ./setup.sh
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors du setup"
        exit 1
    fi
fi

# Active le venv
source venv/bin/activate

# Lance le jeu
python main.py
