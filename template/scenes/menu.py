"""Scène du menu principal."""
import pygame
from scenes.scene_manager import Scene
from entities.ui import Button, Text


class MenuScene(Scene):
    """Menu principal du jeu."""

    def on_enter(self):
        """Initialise le menu."""
        # Récupère la police par défaut
        font_large = self.game.assets.get_font('large')
        font_medium = self.game.assets.get_font('medium')

        if not font_large:
            font_large = pygame.font.Font(None, 72)
        if not font_medium:
            font_medium = pygame.font.Font(None, 48)

        # Titre
        self.title = Text(
            "GAME JAM TEMPLATE",
            self.game.config.window_width // 2,
            150,
            font_large,
            (255, 255, 255),
            center=True
        )

        # Boutons
        button_width = 300
        button_height = 60
        button_x = (self.game.config.window_width - button_width) // 2
        start_y = 280

        self.play_button = Button(
            button_x, start_y, button_width, button_height,
            "JOUER", font_medium
        )

        self.settings_button = Button(
            button_x, start_y + 80, button_width, button_height,
            "PARAMETRES", font_medium
        )

        self.quit_button = Button(
            button_x, start_y + 160, button_width, button_height,
            "QUITTER", font_medium
        )

    def handle_events(self, events):
        """Gère les événements du menu."""
        pass

    def update(self, dt):
        """Met à jour le menu."""
        # Met à jour les boutons
        if self.play_button.update(self.game.input):
            self.game.scene_manager.change_scene('game')

        if self.settings_button.update(self.game.input):
            self.game.scene_manager.change_scene('settings')

        if self.quit_button.update(self.game.input):
            self.game.running = False

    def draw(self, screen):
        """Dessine le menu."""
        screen.fill((30, 30, 50))

        self.title.draw(screen)
        self.play_button.draw(screen)
        self.settings_button.draw(screen)
        self.quit_button.draw(screen)

        # Instructions
        font_small = pygame.font.Font(None, 24)
        instructions = Text(
            "Utilisez ZQSD pour bouger, ESPACE pour sauter",
            self.game.config.window_width // 2,
            self.game.config.window_height - 50,
            font_small,
            (150, 150, 150),
            center=True
        )
        instructions.draw(screen)
