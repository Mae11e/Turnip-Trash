#!/bin/bash
# Script de lancement simple pour Turnip Trash

case "$1" in
    --web)
        echo "🌐 Lancement du serveur web..."
        python3 launch.py --web
        ;;
    --build)
        echo "🔨 Build du jeu pour le web..."
        python3 launch.py --build
        ;;
    *)
        echo "🎮 Lancement du jeu..."
        python3 launch.py
        ;;
esac
