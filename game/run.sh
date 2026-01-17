#!/bin/bash

# Script de lancement pour Ridiculously Overpowered
cd "$(dirname "$0")"

# Active l'environnement virtuel de la template
source ../template/venv/bin/activate

# Lance le jeu
python3 main.py
