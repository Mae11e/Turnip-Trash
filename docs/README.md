# Ridiculously Overpowered

Shooter Arena Survival - Mini Jam 202

## Thème
Un **navet héroïque** défend le monde végétal pastel contre une invasion de **ratons laveurs** et de **poubelles** polluantes!
Collecte des gems, level up et deviens ridiculement overpowered pour sauver la prairie!

## Comment lancer le jeu

### Option 1: Script automatique
```bash
./run.sh
```

### Option 2: Manuel
```bash
# Depuis le dossier racine du projet
source template/venv/bin/activate
cd game
python3 main.py
```

## Fonctionnalités actuelles

### Menu Principal
- **Jouer** : Lance le jeu avec la première vague
- **Sélection de vague** : Choisis ta vague (1-4) avec différentes difficultés
- **Paramètres** : Ajuste le volume et les options de debug
- **Quitter** : Ferme le jeu

### Sélection de vagues
4 vagues disponibles avec des difficultés croissantes:
1. **Tutoriel** (Facile) - Ennemis faibles, boss toutes les 3 vagues
2. **Standard** (Moyen) - Équilibré, boss toutes les 2 vagues
3. **Intense** (Difficile) - Ennemis nombreux, boss fréquents
4. **Chaos** (Extrême) - Spawn continu, boss aléatoires

### Paramètres
- Volume musique (slider)
- Volume effets sonores (slider)
- Toggle FPS (affichage du compteur)
- Toggle Hitboxes (affichage des zones de collision)

## Raccourcis clavier
- **F3** : Toggle affichage FPS
- **F4** : Toggle affichage Hitboxes
- **ESC** : Retour au menu (depuis le jeu)

## Structure du projet

```
game/
├── main.py              # Point d'entrée du jeu
├── config.json          # Configuration du jeu
├── scenes/              # Scènes personnalisées
│   ├── menu.py         # Menu principal
│   ├── wave_selection.py # Sélection de vague
│   └── settings.py     # Paramètres
└── run.sh              # Script de lancement
```

Le jeu utilise la template située dans `../template/` pour les systèmes de base (input, audio, assets, etc.).

## À faire
- Implémenter la scène de jeu avec le système de vagues
- Ajouter le joueur et les ennemis
- Système de power-ups ridiculement overpowered
- Système de level-up et upgrades
- Boss fights
- Effets visuels et particules
