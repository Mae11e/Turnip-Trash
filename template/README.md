# Game Jam Template - Python + Pygame

Template béton mais facilement compréhensible pour créer rapidement des jeux en game jam avec Python et Pygame.

## Installation

### Méthode 1 : Setup automatique (Recommandé)

**Linux/Mac:**
```bash
chmod +x setup.sh run.sh
./setup.sh    # Crée le venv et installe les dépendances
./run.sh      # Lance le jeu
```

**Windows:**
```bash
setup.bat     # Crée le venv et installe les dépendances
run.bat       # Lance le jeu
```

### Méthode 2 : Manuel

```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer le venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate.bat

# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python main.py
```

## Structure du Projet

```
template/
├── main.py                 # Point d'entrée avec game loop
├── config.json            # Configuration (généré automatiquement)
├── requirements.txt       # Dépendances Python
│
├── assets/               # Ressources du jeu
│   ├── images/          # Images et sprites
│   ├── sounds/          # Effets sonores et musiques
│   └── fonts/           # Polices de caractères
│
├── utils/               # Utilitaires
│   ├── vector.py        # Classe Vector2D
│   ├── timer.py         # Timer et Cooldown
│   └── config.py        # Gestion de la config
│
├── systems/             # Systèmes de jeu
│   ├── input_handler.py    # Gestion des entrées
│   ├── audio_manager.py    # Gestion de l'audio
│   ├── asset_manager.py    # Gestion des assets
│   └── collision.py        # Système de collision
│
├── entities/            # Entités du jeu
│   ├── entity.py        # Classe Entity de base
│   ├── camera.py        # Système de caméra
│   ├── particle.py      # Système de particules
│   ├── ui.py           # Composants UI (Button, Text, HealthBar)
│   ├── player.py       # Exemple de Player
│   ├── enemy.py        # Exemple d'Enemy
│   └── projectile.py   # Exemple de Projectile
│
└── scenes/              # Scènes du jeu
    ├── scene_manager.py # Gestionnaire de scènes
    ├── menu.py         # Menu principal
    ├── settings.py     # Menu paramètres
    ├── game.py         # Scène de jeu
    └── gameover.py     # Game over
```

## Fonctionnalités

### Game Loop Principal
- Delta time pour un mouvement fluide
- Gestion des FPS configurable
- États du jeu (running, paused)
- Fermeture propre

### Scene Manager
- Système de scènes facile à utiliser
- Transitions fluides entre scènes
- Scènes incluses: Menu, Settings (paramètres), Game, GameOver
- Menu Settings avec:
  - Réglages audio (musique et effets sonores)
  - Changement de keybindings en temps réel
  - Préréglages AZERTY/QWERTY
  - Sauvegarde automatique

### Input Handler
- Gestion clavier et souris
- États: pressed, just_pressed, just_released
- Système de bindings personnalisables
- Helper pour axes de mouvement

### Asset Manager
- Chargement centralisé des images
- Support des spritesheets
- Gestion des polices
- Images de remplacement automatiques

### Audio Manager
- Musique de fond avec fondu
- Effets sonores multiples
- Volume réglable indépendamment

### Système d'Entités
- Classe Entity de base réutilisable
- Position, vélocité, collision rect
- Support des collisions circulaires
- Exemples: Player, Enemy, Projectile

### Collision System
- Rectangle-Rectangle
- Cercle-Cercle
- Point-Rectangle, Point-Cercle
- Résolution de collisions basique

### Camera/Viewport
- Scrolling fluide
- Suivi d'entités
- Limites du monde
- Conversion écran ↔ monde

### Particle System
- Création facile de particules
- Personnalisation complète
- Alpha fade automatique
- Angles et vitesses configurables

### UI Components
- Button (cliquable avec hover)
- Text (avec centrage)
- HealthBar (avec changement de couleur)

### Utilitaires
- **Vector2D**: Opérations mathématiques (+, -, *, /, normalize, distance, etc.)
- **Timer**: Mesure de temps avec progression
- **Cooldown**: Limite la fréquence d'actions
- **Config**: Fichier JSON pour les paramètres

### Mode Debug
- **F3**: Toggle FPS counter
- **F4**: Toggle hitboxes (à implémenter)
- Configuration sauvegardée

## Guide de Démarrage Rapide

### 1. Créer une Nouvelle Entité

```python
from entities.entity import Entity
import pygame

class MyEntity(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.speed = 200

    def update(self, dt):
        # Votre logique ici
        super().update(dt)

    def draw(self, screen, camera=None):
        draw_pos = camera.apply(self.pos) if camera else self.pos
        pygame.draw.rect(screen, (255, 0, 0),
                        (draw_pos.x, draw_pos.y, self.width, self.height))
```

### 2. Ajouter une Nouvelle Scène

```python
from scenes.scene_manager import Scene

class MyScene(Scene):
    def on_enter(self):
        # Initialisation
        pass

    def update(self, dt):
        # Logique de jeu
        pass

    def draw(self, screen):
        # Rendu
        pass
```

Puis dans `main.py`:
```python
self.scene_manager.add_scene('my_scene', MyScene(self))
```

### 3. Charger et Utiliser des Assets

```python
# Dans _load_assets() de main.py
self.assets.load_image('player', 'assets/images/player.png', scale=(32, 32))
self.audio.load_sound('jump', 'assets/sounds/jump.wav')

# Utilisation
sprite = self.game.assets.get_image('player')
self.game.audio.play_sound('jump')
```

### 4. Gérer les Collisions

```python
from systems.collision import CollisionSystem

# Collision rectangle-rectangle
if CollisionSystem.rect_rect(entity1.rect, entity2.rect):
    # Collision détectée!
    pass

# Collision cercle-cercle
if CollisionSystem.circle_circle(
    entity1.pos.to_tuple(), entity1.radius,
    entity2.pos.to_tuple(), entity2.radius
):
    # Collision!
    pass

# Vérifier contre une liste
collisions = CollisionSystem.check_collision_list(player, enemies)
for enemy in collisions:
    # Traiter la collision
    pass
```

### 5. Créer des Particules

```python
from entities.particle import ParticleSystem

# Dans votre scène
self.particles = ParticleSystem()

# Émission
self.particles.emit(
    x=100, y=100,
    count=20,
    color=(255, 100, 50),
    speed_range=(50, 150),
    lifetime_range=(0.5, 1.5)
)

# Update et draw
self.particles.update(dt)
self.particles.draw(screen)
```

### 6. Input Personnalisés

```python
# Vérifier une action
if self.game.input.is_action_just_pressed('jump'):
    player.jump()

# Axes de mouvement
move_x = self.game.input.get_axis('left', 'right')  # -1, 0, ou 1
move_y = self.game.input.get_axis('up', 'down')

# Souris
if self.game.input.is_mouse_button_just_pressed(1):  # Clic gauche
    mouse_pos = self.game.input.get_mouse_pos()
```

### 7. UI Simple

```python
from entities.ui import Button, Text, HealthBar

# Bouton
self.button = Button(100, 100, 200, 50, "PLAY", font)
if self.button.update(self.game.input):
    # Bouton cliqué!
    pass
self.button.draw(screen)

# Texte
self.text = Text("Score: 0", 10, 10, font, center=False)
self.text.draw(screen)

# Barre de vie
self.health_bar = HealthBar(10, 50, 200, 20, max_value=100)
self.health_bar.set_value(player.health)
self.health_bar.draw(screen)
```

### 8. Menu Settings et Paramètres

Le menu Settings est déjà intégré et fonctionnel. Les joueurs peuvent:

**Régler le volume:**
- Musique et effets sonores séparément
- Sliders interactifs avec pourcentage
- Sauvegarde automatique

**Personnaliser les touches:**
- Cliquer sur un bouton de touche
- Appuyer sur la nouvelle touche souhaitée
- ESC pour annuler
- Préréglages AZERTY/QWERTY en un clic

**Accès:**
```python
# Dans main.py, c'est déjà configuré
self.scene_manager.add_scene('settings', SettingsScene(self))

# Pour aller au menu settings depuis n'importe où
self.game.scene_manager.change_scene('settings')
```

Les paramètres sont sauvegardés dans `config.json` automatiquement.

## Configuration

Le fichier `config.json` est généré automatiquement avec ces valeurs par défaut:

```json
{
    "window": {
        "width": 1280,
        "height": 720,
        "title": "Game Jam Template",
        "fps": 60
    },
    "audio": {
        "music_volume": 0.7,
        "sfx_volume": 0.8
    },
    "debug": {
        "show_fps": false,
        "show_hitboxes": false
    }
}
```

## Contrôles par Défaut

- **ZQSD**: Mouvement (clavier AZERTY)
- **SPACE**: Saut/Action principale
- **E**: Action secondaire (exemple: particules)
- **ESC**: Pause/Retour au menu
- **F3**: Toggle FPS
- **F4**: Toggle hitboxes

Personnalisables dans `systems/input_handler.py` (par défaut configuré pour AZERTY).

## Conseils pour Game Jams

1. **Gardez-le simple**: Ne sur-architecturez pas, utilisez ce qui est fourni
2. **Prototypez vite**: Utilisez des carrés colorés avant de faire des sprites
3. **Assets de remplacement**: Le système crée automatiquement des placeholders magenta
4. **Debug visuel**: Activez les hitboxes et FPS pour débugger rapidement
5. **Scènes modulaires**: Créez une scène par écran de jeu
6. **Particules**: Utilisez-les pour du feedback visuel rapide et efficace

## Extensibilité

Ce template est conçu pour être étendu facilement:

- **Nouvelles entités**: Héritez de `Entity`
- **Nouveaux systèmes**: Ajoutez dans `/systems`
- **Nouvelles scènes**: Héritez de `Scene`
- **Nouveaux utilitaires**: Ajoutez dans `/utils`

## Exemple de Game Loop Custom

```python
# Dans votre scene
def update(self, dt):
    # 1. Input
    if self.game.input.is_action_pressed('shoot'):
        self.player.shoot()

    # 2. Update
    self.player.update(dt, self.game.input)
    for enemy in self.enemies:
        enemy.update(dt, self.player)
    for projectile in self.projectiles:
        projectile.update(dt)

    # 3. Collisions
    for proj in self.projectiles:
        hits = CollisionSystem.check_collision_list(proj, self.enemies)
        for enemy in hits:
            proj.on_hit(enemy)

    # 4. Cleanup
    self.enemies = [e for e in self.enemies if e.alive]
    self.projectiles = [p for p in self.projectiles if p.alive]

    # 5. Camera
    if self.camera:
        self.camera.update(dt)
```

## License

Template libre d'utilisation pour vos game jams!

## Bon jam! 🎮
