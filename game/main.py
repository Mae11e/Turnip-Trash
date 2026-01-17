"""
Ridiculously Overpowered - Main
Shooter Arena Survival - Mini Jam 202
"""
import sys
import os

# Ajoute le dossier template au path pour importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'template'))

import pygame

from utils import Config
from systems import InputHandler, AudioManager, AssetManager
from scenes import SceneManager, GameScene, GameOverScene

# Import des scènes custom - utilise importlib pour éviter les conflits
import importlib.util

def load_scene_module(module_name, file_path):
    """Charge un module de scène personnalisé."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Charge les scènes custom
game_dir = os.path.dirname(__file__)
menu_module = load_scene_module("menu", os.path.join(game_dir, "scenes", "menu.py"))
wave_module = load_scene_module("wave_selection", os.path.join(game_dir, "scenes", "wave_selection.py"))
settings_module = load_scene_module("settings_scene", os.path.join(game_dir, "scenes", "settings.py"))

MenuScene = menu_module.MenuScene
WaveSelectionScene = wave_module.WaveSelectionScene
SettingsScene = settings_module.SettingsScene


class Game:
    """Classe principale du jeu."""

    def __init__(self):
        """Initialise le jeu."""
        pygame.init()

        # Configuration (charge depuis game/config.json)
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.config = Config(config_path)

        # Fenêtre
        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height)
        )
        pygame.display.set_caption(self.config.window_title)

        # Horloge pour gérer les FPS
        self.clock = pygame.time.Clock()

        # Gestionnaires
        self.input = InputHandler()
        self.audio = AudioManager(
            self.config.music_volume,
            self.config.sfx_volume
        )
        self.assets = AssetManager()

        # Charge les keybindings personnalisés depuis la config
        self._load_keybindings()

        # Scene Manager
        self.scene_manager = SceneManager()

        # État du jeu
        self.running = True
        self.paused = False
        self.selected_wave = 1  # Vague sélectionnée par défaut

        # Debug
        self.show_fps = self.config.show_fps
        self.show_hitboxes = self.config.show_hitboxes

        # Initialise les assets et scènes
        self._load_assets()
        self._setup_scenes()

    def _load_assets(self):
        """Charge les assets du jeu."""
        # Charge les polices
        self.assets.load_font('large', None, 72)
        self.assets.load_font('medium', None, 48)
        self.assets.load_font('small', None, 28)

        # TODO: Charger les images et sons
        # self.assets.load_image('player', 'assets/images/player.png', scale=(32, 32))
        # self.audio.load_sound('shoot', 'assets/sounds/shoot.wav')
        # self.audio.play_music('assets/sounds/music.mp3')

    def _load_keybindings(self):
        """Charge les keybindings personnalisés depuis la config."""
        if 'keybindings' in self.config.data:
            for action, key in self.config.data['keybindings'].items():
                if action in self.input.bindings:
                    self.input.bindings[action] = key

    def _setup_scenes(self):
        """Configure les scènes."""
        # Scènes custom pour le menu et settings
        self.scene_manager.add_scene('menu', MenuScene(self))
        self.scene_manager.add_scene('wave_selection', WaveSelectionScene(self))
        self.scene_manager.add_scene('settings', SettingsScene(self))

        # Scènes de la template pour le jeu
        self.scene_manager.add_scene('game', GameScene(self))
        self.scene_manager.add_scene('gameover', GameOverScene(self))

        # Démarre sur le menu
        self.scene_manager.change_scene('menu')

    def handle_events(self):
        """Gère les événements pygame."""
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            # Toggle debug avec F3 et F4
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F3:
                    self.show_fps = not self.show_fps
                elif event.key == pygame.K_F4:
                    self.show_hitboxes = not self.show_hitboxes

        # Met à jour l'input handler
        self.input.update(events)

        # Passe les événements à la scène courante
        self.scene_manager.handle_events(events)

    def update(self, dt):
        """
        Met à jour le jeu.

        Args:
            dt: Delta time en secondes
        """
        if not self.paused:
            self.scene_manager.update(dt)

    def draw(self):
        """Dessine le jeu."""
        # Dessine la scène courante
        self.scene_manager.draw(self.screen)

        # Affiche les infos de debug
        if self.show_fps:
            self._draw_fps()

        # Met à jour l'affichage
        pygame.display.flip()

    def _draw_fps(self):
        """Affiche le compteur de FPS."""
        font = pygame.font.Font(None, 28)
        fps = int(self.clock.get_fps())
        fps_text = font.render(f"FPS: {fps}", True, (0, 255, 0))
        self.screen.blit(fps_text, (10, 10))

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            # Delta time en secondes
            dt = self.clock.tick(self.config.fps) / 1000.0

            # Game loop
            self.handle_events()
            self.update(dt)
            self.draw()

        self.quit()

    def quit(self):
        """Quitte le jeu proprement."""
        # Sauvegarde la config
        self.config.set('debug', 'show_fps', self.show_fps)
        self.config.set('debug', 'show_hitboxes', self.show_hitboxes)
        self.config.save()

        pygame.quit()
        sys.exit()


def main():
    """Point d'entrée du programme."""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
