# 🎮 Turnip Trash - Quick Start

## Lancer le Jeu

### Option 1: Script Python (Recommandé)
```bash
python3 launch.py
```

### Option 2: Script Bash
```bash
./launch.sh
```

### Option 3: Direct
```bash
template/venv/bin/python3 game/main.py
```

## Tester le Build Web

```bash
python3 launch.py --web
```

Puis ouvre http://localhost:8000 dans ton navigateur.

⚠️ Page noire? C'est normal! Le build web fonctionne sur itch.io.

## Upload sur itch.io

Le fichier est déjà prêt: **turnip-trash-web.zip** ✅

1. https://itch.io/game/new
2. Upload `turnip-trash-web.zip`
3. Coche "This file will be played in the browser"
4. Type: HTML
5. Dimensions: 1280x720

C'est tout! 🚀

## Rebuild (si besoin)

```bash
python3 launch.py --build
```

---

**Bon jeu!** 🥕 vs 🦝 🗑️
