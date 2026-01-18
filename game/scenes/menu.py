"""Scène du menu principal."""
import sys
import os

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene
from entities.ui import Button, Text


class MenuScene(Scene):
    """Menu principal du jeu."""

    def __init__(self, game):
        super().__init__(game)
        self.input_delay = 0.3  # Délai avant de pouvoir interagir (secondes)
        self.current_delay = 0

    def on_enter(self):
        """Initialise le menu."""
        # Réinitialise le délai à chaque entrée dans le menu
        self.current_delay = self.input_delay

        # Récupère la police par défaut
        font_large = self.game.assets.get_font('large')
        font_medium = self.game.assets.get_font('medium')

        if not font_large:
            font_large = pygame.font.Font(None, 72)
        if not font_medium:
            font_medium = pygame.font.Font(None, 48)

        # Titre - Couleur pastel pêche/corail
        self.title = Text(
            "RIDICULOUSLY OVERPOWERED",
            self.game.config.window_width // 2,
            100,
            font_large,
            (255, 179, 186),  # Rose pastel
            center=True
        )

        # Sous-titre
        font_small = pygame.font.Font(None, 32)
        self.subtitle = Text(
            "Navet vs Poubelles & Ratons Laveurs",
            self.game.config.window_width // 2,
            170,
            font_small,
            (200, 220, 230),  # Bleu pastel très clair
            center=True
        )

        # Boutons avec couleurs pastel
        button_width = 350
        button_height = 70
        button_x = (self.game.config.window_width - button_width) // 2
        start_y = 280

        # Bouton jouer - Vert pastel (navet)
        self.play_button = Button(
            button_x, start_y, button_width, button_height,
            "JOUER", font_medium,
            color=(180, 220, 180),  # Vert pastel
            hover_color=(160, 240, 160)
        )

        # Bouton sélection - Violet pastel
        self.wave_select_button = Button(
            button_x, start_y + 90, button_width, button_height,
            "SELECTION DE VAGUE", font_medium,
            color=(200, 180, 220),  # Violet pastel
            hover_color=(220, 200, 240)
        )

        # Bouton shop - Jaune/Or pastel
        self.shop_button = Button(
            button_x, start_y + 180, button_width, button_height,
            "SHOP (AMELIORATIONS)", font_medium,
            color=(240, 220, 150),  # Jaune pastel
            hover_color=(255, 240, 170)
        )

        # Bouton paramètres - Bleu pastel
        self.settings_button = Button(
            button_x, start_y + 270, button_width, button_height,
            "PARAMETRES", font_medium,
            color=(180, 210, 230),  # Bleu pastel
            hover_color=(200, 230, 250)
        )

        # Bouton quitter - Gris pastel
        self.quit_button = Button(
            button_x, start_y + 360, button_width, button_height,
            "QUITTER", font_medium,
            color=(200, 200, 210),  # Gris pastel
            hover_color=(220, 220, 230)
        )

    def handle_events(self, events):
        """Gère les événements du menu."""
        pass

    def update(self, dt):
        """Met à jour le menu."""
        # Diminue le délai
        if self.current_delay > 0:
            self.current_delay -= dt
            return  # Ne traite pas les inputs pendant le délai

        # Met à jour les boutons
        if self.play_button.update(self.game.input):
            # Démarre le jeu avec la première vague
            self.game.scene_manager.change_scene('wave1')

        if self.wave_select_button.update(self.game.input):
            self.game.scene_manager.change_scene('wave_selection')

        if self.shop_button.update(self.game.input):
            # Aller au shop
            shop_scene = self.game.scene_manager.scenes['shop']
            shop_scene.set_next_wave(1)  # Prochaine vague = 1 depuis le menu
            self.game.scene_manager.change_scene('shop')

        if self.settings_button.update(self.game.input):
            self.game.scene_manager.change_scene('settings')

        if self.quit_button.update(self.game.input):
            self.game.running = False

    def draw(self, screen):
        """Dessine le menu."""
        # Fond pastel doux - Vert grisé plus foncé
        screen.fill((160, 175, 160))

        # Effet de fond - cercles pastel
        for i in range(5):
            # Cercles rose pastel
            color = (255 - i * 10, 200 - i * 5, 210 - i * 5)
            pygame.draw.circle(screen, color,
                             (self.game.config.window_width // 2, 100),
                             200 + i * 30, 2)

        self.title.draw(screen)
        self.subtitle.draw(screen)
        self.play_button.draw(screen)
        self.wave_select_button.draw(screen)
        self.shop_button.draw(screen)
        self.settings_button.draw(screen)
        self.quit_button.draw(screen)

        # Instructions en bas - couleur pastel
        font_small = pygame.font.Font(None, 20)
        instructions = Text(
            "Un navet contre des ratons laveurs et des poubelles - Collecte des gems pour level up!",
            self.game.config.window_width // 2,
            self.game.config.window_height - 30,
            font_small,
            (150, 150, 170),  # Gris-bleu pastel
            center=True
        )
        instructions.draw(screen)
