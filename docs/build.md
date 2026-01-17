# Build & Soumission

## Pygbag (Build Web - Recommandé)

Permet de jouer directement dans le navigateur sur itch.io.

### Installation
```bash
pip install pygbag
```

### Build
```bash
cd Template
pygbag main.py
```

### Résultat
- Génère un dossier `build/web/`
- Contient les fichiers web (HTML, JS, WASM)
- Zipper ce dossier pour itch.io

### Upload sur itch.io
1. Créer un nouveau projet sur itch.io
2. Upload le `.zip` du dossier `build/web/`
3. Cocher "This file will be played in the browser"
4. Kind of project: HTML

### Notes Pygbag
- Le code doit être compatible asyncio (ajouter `await asyncio.sleep(0)` dans la game loop)
- Pas de chemins absolus pour les assets
- Tester localement : `python -m http.server` dans `build/web/`

---

## Alternative : PyInstaller (Windows .exe)

```bash
pip install pyinstaller
cd Template
pyinstaller --onefile --windowed main.py
```

→ Génère `dist/main.exe`
