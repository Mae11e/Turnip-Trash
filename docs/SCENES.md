# 🎬 Comment Ajouter des Scènes

Guide pour créer de nouvelles scènes dans le jeu.

## 📚 Structure des Scènes

Le jeu utilise un système de gestion de scènes (`SceneManager`) pour organiser les différents écrans du jeu.

### Scènes Existantes

```
game/scenes/
├── menu.py              # Menu principal
├── wave_selection.py    # Sélection des vagues
└── wave.py              # Scène de vague universelle
```

## 🔨 Créer une Nouvelle Scène

### 1. Créer le fichier de scène

Crée un nouveau fichier dans `game/scenes/`, par exemple `game/scenes/settings.py`:

```python
from template.scene import Scene
import pygame

class SettingsScene(Scene):
    """Scène des paramètres."""

    def __init__(self, game):
        super().__init__(game)

        # Initialise tes variables ici
        self.volume = 0.5
        self.fullscreen = False

    def handle_event(self, event):
        """Gère les événements (clavier, souris, etc.)."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Retour au menu
                self.game.scene_manager.change_scene('menu')

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clics sur les boutons
            mouse_pos = pygame.mouse.get_pos()
            # ... logique des boutons

    def update(self, dt):
        """Met à jour la logique de la scène."""
        # dt = delta time en secondes
        pass

    def draw(self, screen):
        """Dessine la scène."""
        screen.fill((30, 30, 40))  # Fond

        # Dessine ton UI ici
        font = pygame.font.Font(None, 48)
        title = font.render("Settings", True, (255, 255, 255))
        screen.blit(title, (100, 50))
```

### 2. Importer la scène dans main.py

Dans [main.py](../game/main.py), ajoute l'import:

```python
from scenes.settings import SettingsScene  # Ajoute cette ligne
from scenes.menu import MenuScene
from scenes.wave_selection import WaveSelectionScene
from scenes.wave import WaveScene
```

### 3. Enregistrer la scène

Dans la méthode `_setup_scenes()` de [main.py](../game/main.py):

```python
def _setup_scenes(self):
    """Initialise toutes les scènes."""
    # Scènes existantes
    self.scene_manager.add_scene('menu', MenuScene(self))
    self.scene_manager.add_scene('wave_selection', WaveSelectionScene(self))

    # Ta nouvelle scène
    self.scene_manager.add_scene('settings', SettingsScene(self))

    # Vagues
    for i in range(1, 21):
        self.scene_manager.add_scene(f'wave{i}', WaveScene(self, wave_number=i))
```

### 4. Naviguer vers la scène

Depuis n'importe quelle autre scène:

```python
# Aller aux settings
self.game.scene_manager.change_scene('settings')

# Retour au menu
self.game.scene_manager.change_scene('menu')
```

## 📝 Méthodes de la Classe Scene

### Méthodes Obligatoires

```python
class MyScene(Scene):
    def __init__(self, game):
        """Initialisation de la scène."""
        super().__init__(game)
        # Tes variables ici

    def handle_event(self, event):
        """Gère un événement pygame."""
        pass

    def update(self, dt):
        """Met à jour la logique (appelé chaque frame)."""
        pass

    def draw(self, screen):
        """Dessine la scène (appelé chaque frame)."""
        pass
```

### Méthodes Optionnelles

```python
def on_enter(self):
    """Appelée quand on entre dans la scène."""
    # Réinitialise l'état, charge des ressources, etc.
    pass

def on_exit(self):
    """Appelée quand on quitte la scène."""
    # Sauvegarde l'état, libère des ressources, etc.
    pass
```

## 🎮 Exemples de Scènes

### Scène de Pause

```python
class PauseScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.previous_scene = None

    def on_enter(self):
        # Sauvegarde quelle scène était active
        self.previous_scene = self.game.scene_manager.current_scene_name

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Reprendre le jeu
                self.game.scene_manager.change_scene(self.previous_scene)
            elif event.key == pygame.K_q:
                # Quitter vers le menu
                self.game.scene_manager.change_scene('menu')

    def draw(self, screen):
        # Fond semi-transparent
        overlay = pygame.Surface((self.game.config.window_width,
                                 self.game.config.window_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Texte
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSE", True, (255, 255, 255))
        rect = text.get_rect(center=(self.game.config.window_width // 2,
                                     self.game.config.window_height // 2))
        screen.blit(text, rect)
```

### Scène de Game Over

```python
class GameOverScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.score = 0
        self.wave_reached = 0

    def set_stats(self, score, wave):
        """Définit les stats à afficher."""
        self.score = score
        self.wave_reached = wave

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Rejouer
                self.game.scene_manager.change_scene('wave1')
            elif event.key == pygame.K_ESCAPE:
                # Menu
                self.game.scene_manager.change_scene('menu')

    def draw(self, screen):
        screen.fill((40, 20, 20))

        font_big = pygame.font.Font(None, 96)
        font_small = pygame.font.Font(None, 48)

        # GAME OVER
        title = font_big.render("GAME OVER", True, (255, 50, 50))
        title_rect = title.get_rect(center=(640, 200))
        screen.blit(title, title_rect)

        # Score
        score_text = font_small.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(640, 350))
        screen.blit(score_text, score_rect)

        # Vague
        wave_text = font_small.render(f"Vague atteinte: {self.wave_reached}", True, (255, 255, 255))
        wave_rect = wave_text.get_rect(center=(640, 420))
        screen.blit(wave_text, wave_rect)

        # Instructions
        hint = font_small.render("SPACE: Rejouer  |  ESC: Menu", True, (150, 150, 150))
        hint_rect = hint.get_rect(center=(640, 600))
        screen.blit(hint, hint_rect)
```

### Scène de Victory

```python
class VictoryScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.total_score = 0
        self.time_taken = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.scene_manager.change_scene('wave_selection')

    def draw(self, screen):
        screen.fill((20, 40, 20))

        font = pygame.font.Font(None, 72)
        title = font.render("VICTOIRE!", True, (50, 255, 50))
        screen.blit(title, (400, 200))

        # Statistiques...
```

## 🎨 UI Components

### Créer un Bouton

```python
class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.callback()

    def draw(self, screen):
        color = (100, 200, 100) if self.hovered else (50, 150, 50)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
```

Utilisation dans une scène:

```python
class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.play_button = Button(
            400, 300, 200, 60,
            "Play",
            lambda: self.game.scene_manager.change_scene('wave_selection')
        )
        self.quit_button = Button(
            400, 400, 200, 60,
            "Quit",
            lambda: self.game.running = False
        )

    def handle_event(self, event):
        self.play_button.handle_event(event)
        self.quit_button.handle_event(event)

    def draw(self, screen):
        screen.fill((30, 30, 40))
        self.play_button.draw(screen)
        self.quit_button.draw(screen)
```

## 🔧 Accéder aux Ressources du Jeu

Depuis une scène, tu as accès à:

```python
# Configuration
self.game.config.window_width
self.game.config.window_height
self.game.config.fps

# Gestionnaire de scènes
self.game.scene_manager.change_scene('other_scene')
self.game.scene_manager.current_scene_name

# Assets (si tu utilises un asset manager)
self.game.assets.get_image('player.png')
self.game.assets.get_sound('explosion.wav')

# Quitter le jeu
self.game.running = False
```

## 📊 Passage de Données entre Scènes

### Méthode 1: Variables de la classe Game

```python
# Dans main.py
class Game:
    def __init__(self):
        # ...
        self.player_score = 0
        self.current_wave = 1

# Dans une scène
self.game.player_score += 100
```

### Méthode 2: Méthodes setter

```python
# Dans GameOverScene
def set_stats(self, score, wave):
    self.score = score
    self.wave_reached = wave

# Lors du changement de scène
game_over = self.game.scene_manager.scenes['game_over']
game_over.set_stats(self.score, self.wave_number)
self.game.scene_manager.change_scene('game_over')
```

## ✅ Checklist pour une Nouvelle Scène

- [ ] Créer le fichier dans `game/scenes/`
- [ ] Hériter de la classe `Scene`
- [ ] Implémenter `__init__`, `handle_event`, `update`, `draw`
- [ ] Importer la scène dans `main.py`
- [ ] Enregistrer avec `scene_manager.add_scene()`
- [ ] Tester la navigation vers/depuis la scène
- [ ] Gérer ESC pour retour au menu (optionnel)
- [ ] Ajouter `on_enter`/`on_exit` si nécessaire

## 🐛 Debug

Pour voir quelle scène est active:

```python
print(f"Scène actuelle: {self.game.scene_manager.current_scene_name}")
```

Pour lister toutes les scènes:

```python
print(f"Scènes disponibles: {list(self.game.scene_manager.scenes.keys())}")
```
