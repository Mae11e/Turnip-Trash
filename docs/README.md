# 🥕 Turnip Trash

**Ridiculously Overpowered** - Shooter Arena Survival
> Un navet contre des ratons laveurs et des poubelles!

Mini Jam 202 - Game Jam Entry

## 🎮 Comment Jouer

### Contrôles
- **Souris**: Déplacer le joueur (le navet suit le curseur)
- **Tir**: Automatique (2 projectiles dans des directions aléatoires)
- **ESC**: Retour au menu

### Objectif
Survivre aux vagues d'ennemis (raccoons et poubelles) qui tirent aussi!
Collecte des points en éliminant les ennemis.

## 🚀 Lancement Rapide

### Jouer en local
```bash
python3 launch.py
# ou
./launch.sh
```

### Build pour le web (itch.io)
```bash
python3 launch.py --build
```

Cela créera `turnip-trash-web.zip` prêt pour upload!

### Tester le build web
```bash
python3 launch.py --web
```

Ouvre `http://localhost:8000` dans ton navigateur.

⚠️ **Note**: Le test local peut afficher une page noire à cause des restrictions CORS. Le build fonctionne parfaitement sur itch.io!

## 📦 Structure du Projet

```
Turnip-Trash/
├── game/              # Code du jeu
│   ├── main.py       # Point d'entrée (compatible asyncio)
│   ├── scenes/       # Scènes du jeu
│   │   ├── menu.py
│   │   ├── wave_selection.py
│   │   └── wave1.py  # Vague 1 - Tutoriel
│   └── config.json   # Configuration
├── assets/           # Images et sons
│   ├── player.png
│   ├── racoon_ennemie.png
│   └── ennemie_basic.png
├── template/         # Framework de jeu
├── launch.py         # Script de lancement
└── launch.sh         # Alternative bash
```

## 🎨 Caractéristiques

### Vague 1 - Tutoriel
- ✅ 15 ennemis à éliminer
- ✅ 2 types d'ennemis (raccoons rapides, poubelles lentes)
- ✅ Tir automatique aléatoire (joueur et ennemis)
- ✅ Sprites animés (80x80px)
- ✅ Système de particules
- ✅ Collisions et dégâts
- ✅ Score et statistiques

### Système de Tir
- **Joueur**: Tire 2 projectiles dans des directions aléatoires (5 tirs/sec)
- **Ennemis**: Tirent aussi dans des directions aléatoires
  - Raccoons: toutes les 2 secondes
  - Poubelles: toutes les 3 secondes

### Visuel
- Style pastel nature
- Animations fluides
- Effets de particules
- Interface claire

## 🔧 Développement

### Prérequis
```bash
# Environnement virtuel pour le jeu
python3 -m venv template/venv
template/venv/bin/pip install pygame

# Pour le build web
python3 -m venv build_env
build_env/bin/pip install pygbag
```

### Lancer en mode développement
```bash
template/venv/bin/python3 game/main.py
```

## 📤 Upload sur itch.io

1. Build le jeu: `python3 launch.py --build`
2. Va sur https://itch.io/game/new
3. Upload `turnip-trash-web.zip`
4. Coche "This file will be played in the browser"
5. Kind of project: **HTML**
6. Dimensions: 1280x720

## 📝 Notes Techniques

- **Moteur**: Pygame + Template personnalisé
- **Build Web**: Pygbag (pygame → WebAssembly)
- **Compatibilité**: Python 3.12, asyncio pour le web
- **Assets**: PNG avec transparence

## 👥 Crédits

- **Développement**: Game Jam Team
- **Framework**: Template Pygame personnalisé
- **Build**: Pygbag

---

**Mini Jam 202** - Thème: Ridiculously Overpowered
