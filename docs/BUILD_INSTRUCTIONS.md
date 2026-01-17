# Instructions de Build - Turnip Trash

## Build Web avec Pygbag (pour itch.io)

### Prérequis
```bash
python3 -m venv build_env
build_env/bin/pip install pygbag
```

### Builder le jeu
```bash
build_env/bin/python3 -m pygbag game
```

Cela créera un dossier `game/build/web/` avec les fichiers HTML/JS/WASM.

### Créer le ZIP pour itch.io
```bash
cd game/build
zip -r turnip-trash-web.zip web/
```

Le fichier `turnip-trash-web.zip` est prêt pour upload sur itch.io!

### Upload sur itch.io

1. Va sur [itch.io](https://itch.io/game/new)
2. Crée un nouveau projet
3. Upload le fichier `turnip-trash-web.zip`
4. **Important**: Coche "This file will be played in the browser"
5. Kind of project: **HTML**
6. Embed options:
   - Width: 1280
   - Height: 720
   - Fullscreen button: Enable

### Tester localement

Pour tester le build web localement:
```bash
cd game/build/web
python3 -m http.server 8000
```

Puis ouvre ton navigateur sur `http://localhost:8000`

## Notes importantes

- Le code a été adapté pour asyncio (requis par pygbag)
- Les assets sont chargés avec des chemins relatifs
- Le jeu est compatible navigateur moderne (Chrome, Firefox, Safari)

## Fichier final

Le fichier **turnip-trash-web.zip** (36 KB) est prêt dans le dossier racine du projet.
