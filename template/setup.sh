#!/bin/bash
# Script de setup pour créer le venv et installer les dépendances

echo "🎮 Setup Game Jam Template"
echo ""

# Vérifie si python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé!"
    exit 1
fi

# Crée le venv s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel déjà existant"
fi

# Active le venv
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Install les dépendances
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup terminé!"
echo ""
echo "Pour lancer le jeu:"
echo "  ./run.sh"
echo ""
echo "Ou manuellement:"
echo "  source venv/bin/activate"
echo "  python main.py"
