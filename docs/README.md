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

### Build pour le web
```bash
python3 launch.py --build
```

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
│   │   └── wave.py   # Système de vagues universel (20 niveaux)
│   └── config.json   # Configuration
├── assets/           # Images et sons
│   ├── player.png
│   ├── racoon_ennemie.png
│   └── ennemie_basic.png
├── template/         # Framework de jeu
├── docs/             # Documentation
├── launch.py         # Script de lancement
└── launch.sh         # Alternative bash
```

## 🎨 Caractéristiques

### Système de Vagues
- ✅ **20 vagues** avec progression automatique
- ✅ Difficulté dynamique basée sur des formules
- ✅ 2 types d'ennemis (raccoons rapides, poubelles lentes)
- ✅ Barres de vie colorées au-dessus des ennemis
- ✅ Tirs multiples des ennemis (augmente tous les 5 niveaux)

### Système de Tir
- **Joueur**: Tire 2 projectiles dans des directions aléatoires (5 tirs/sec)
- **Ennemis**: Tirent aussi dans des directions aléatoires
  - Vagues 1-4: 1 projectile
  - Vagues 5-9: 2 projectiles
  - Vagues 10-14: 3 projectiles
  - Vagues 15-20: 4 projectiles

### Visuel
- Sprites animés (80x80px)
- Barres de vie dynamiques (vert → jaune → rouge)
- Effets de particules
- Interface claire

## 📚 Documentation

- [VAGUES.md](VAGUES.md) - Système de vagues et progression
- [BUILD.md](BUILD.md) - Instructions de build et déploiement
- [SCENES.md](SCENES.md) - Comment ajouter de nouvelles scènes
- [JAM_RULES.md](JAM_RULES.md) - Règles de la game jam
- [IDEAS.md](IDEAS.md) - Idées et améliorations futures

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