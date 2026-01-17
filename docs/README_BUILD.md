# Build Web - Turnip Trash

## 🚀 Scripts de Lancement

### Lancer le jeu (mode normal)
```bash
python3 launch.py
# ou
./launch.sh
```

### Build pour le web
```bash
python3 launch.py --build
# ou
./launch.sh --build
```

### Tester le build web localement
```bash
python3 launch.py --web
# ou
./launch.sh --web
```

Le serveur sera disponible sur `http://localhost:8000`

⚠️ **Note**: La page peut être noire en local à cause des restrictions CORS. Pour un test complet, upload sur itch.io!

---

## Build avec Pygbag (TERMINÉ ✅)

Le jeu a été buildé avec succès pour le web!

### Fichier prêt pour itch.io

📦 **turnip-trash-web.zip** (36 KB) - Prêt à uploader!

### Upload sur itch.io

1. Va sur https://itch.io/game/new
2. Crée un nouveau projet
3. Upload le fichier **turnip-trash-web.zip**
4. **IMPORTANT**: Coche "This file will be played in the browser"
5. Kind of project: **HTML**
6. Embed options recommandées:
   - Width: 1280
   - Height: 720
   - Fullscreen button: Enable

### Le jeu sera jouable directement dans le navigateur! 🎮

## Pourquoi la page est noire en local?

Si tu testes avec `python3 -m http.server`, la page peut être noire parce que:

1. **Pygbag utilise un CDN**: Le jeu charge pygame-wasm depuis `https://pygame-web.github.io/archives/0.9/`
2. **Connexion internet requise**: Pour tester localement, assure-toi d'avoir une connexion internet
3. **CORS**: Certains navigateurs bloquent le chargement depuis le CDN en local

### Solution: Upload sur itch.io!

Sur itch.io, tout fonctionnera parfaitement car:
- itch.io gère le CORS correctement
- Le CDN pygame-web est accessible
- L'environnement est optimisé pour pygbag

## Rebuild (si nécessaire)

```bash
# Installer pygbag
python3 -m venv build_env
build_env/bin/pip install pygbag

# Builder
build_env/bin/python3 -m pygbag --build game

# Créer le ZIP
cd game/build
zip -r turnip-trash-web.zip web/
```

## Caractéristiques du jeu

- ✅ Vague 1 fonctionnelle avec tir aléatoire
- ✅ Joueur suit la souris
- ✅ Ennemis (raccoons et poubelles) avec tir aléatoire
- ✅ Sprites animés (80x80px)
- ✅ Système de particules
- ✅ Collisions et dégâts
- ✅ Compatible asyncio pour le web
