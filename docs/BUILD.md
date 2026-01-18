# 🔨 Build & Déploiement - Turnip Trash

## 🚀 Lancement Rapide

### Jouer localement
```bash
python3 launch.py
# ou
./launch.sh
```

### Build pour le web (itch.io)
```bash
python3 launch.py --build
```

### Tester le build web localement
```bash
python3 launch.py --web
```
Ouvre `http://localhost:8000` dans ton navigateur.

⚠️ **Note**: Page noire en local? C'est normal (CORS). Le build fonctionne sur itch.io!

## 📦 Build Web avec Pygbag

### Installation (si pas déjà fait)
```bash
python3 -m venv build_env
build_env/bin/pip install pygbag
```

### Build Manuel
```bash
build_env/bin/python3 -m pygbag --build game
```

Crée: `game/build/web/` avec les fichiers HTML/JS/WASM

### Créer le ZIP
```bash
cd game/build
zip -r ../../turnip-trash-web.zip web/
```

Fichier prêt: `turnip-trash-web.zip` (36 KB)

## 🌐 Upload sur itch.io

### Étapes
1. Va sur https://itch.io/game/new
2. Crée un nouveau projet
3. Upload `turnip-trash-web.zip`
4. **Important**: Coche "This file will be played in the browser"
5. Kind of project: **HTML**
6. Embed options:
   - Width: **1280**
   - Height: **720**
   - Fullscreen button: **Enable**

### Le jeu sera jouable directement dans le navigateur! 🎮

## 🔧 Configuration Pygbag

### Fichier modifié pour le web
`game/main.py` utilise asyncio:
```python
import asyncio

async def main():
    game = Game()
    await game.run()

async def run(self):
    while self.running:
        # Game loop
        await asyncio.sleep(0)  # Requis pour pygbag
```

### Pourquoi la page est noire en local?
- Pygbag charge pygame-wasm depuis un CDN: `https://pygame-web.github.io/archives/0.9/`
- En local, les restrictions CORS peuvent bloquer le CDN
- **Solution**: Uploader sur itch.io où tout fonctionne!

## 📁 Structure du Build

```
game/build/web/
├── index.html       # Page du jeu
├── game.apk         # Archive du jeu Python
└── favicon.png      # Icône
```

Le CDN pygame-web charge automatiquement:
- pygame WASM
- Python 3.12 WASM
- Dépendances

## 🐛 Problèmes Courants

**"ModuleNotFoundError: pygbag"**
→ Utilise le bon environnement: `build_env/bin/python3`

**"Page blanche/noire en local"**
→ Normal! Upload sur itch.io pour tester

**"asyncio errors"**
→ Vérifie que `await asyncio.sleep(0)` est dans la game loop

## 🎯 Alternative: Build Desktop

### PyInstaller (Windows .exe)
```bash
pip install pyinstaller
cd game
pyinstaller --onefile --windowed main.py
```

Génère: `dist/main.exe`

**Note**: Nécessite Windows pour créer .exe

## 📋 Checklist Avant Upload

- [ ] Le jeu fonctionne en local
- [ ] Build créé avec `launch.py --build`
- [ ] ZIP testé (vérifie la taille ~36 KB)
- [ ] Projet itch.io créé
- [ ] Options HTML configurées (1280×720)
- [ ] Testé sur itch.io après upload

## 🔗 Fichiers Utiles

- **Scripts de lancement**: `launch.py`, `launch.sh`
- **Build final**: `turnip-trash-web.zip`
- **Documentation**: Ce fichier!
