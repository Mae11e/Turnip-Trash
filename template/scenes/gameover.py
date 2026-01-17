"""Scène de game over."""
import pygame
from scenes.scene_manager import Scene
from entities.ui import Button, Text


class GameOverScene(Scene):
    """Scène de game over."""

    def __init__(self, game):
        super().__init__(game)
        self.final_score = 0

    def set_score(self, score):
        """Définit le score final."""
        self.final_score = score

    def on_enter(self):
        """Initialise la scène."""
        font_large = self.game.assets.get_font('large')
        font_medium = self.game.assets.get_font('medium')

        if not font_large:
            font_large = pygame.font.Font(None, 72)
        if not font_medium:
            font_medium = pygame.font.Font(None, 48)

        # Titre
        self.title = Text(
            "GAME OVER",
            self.game.config.window_width // 2,
            150,
            font_large,
            (255, 100, 100),
            center=True
        )

        # Score
        self.score_text = Text(
            f"Score Final: {self.final_score}",
            self.game.config.window_width // 2,
            250,
            font_medium,
            (255, 255, 255),
            center=True
        )

        # Boutons
        button_width = 300
        button_height = 60
        button_x = (self.game.config.window_width - button_width) // 2
        start_y = 350

        self.retry_button = Button(
            button_x, start_y, button_width, button_height,
            "REJOUER", font_medium
        )

        self.menu_button = Button(
            button_x, start_y + 100, button_width, button_height,
            "MENU", font_medium
        )

    def update(self, dt):
        """Met à jour la scène."""
        if self.retry_button.update(self.game.input):
            self.game.scene_manager.change_scene('game')

        if self.menu_button.update(self.game.input):
            self.game.scene_manager.change_scene('menu')

    def draw(self, screen):
        """Dessine la scène."""
        screen.fill((20, 20, 30))

        self.title.draw(screen)
        self.score_text.draw(screen)
        self.retry_button.draw(screen)
        self.menu_button.draw(screen)
