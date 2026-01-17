"""Scène des paramètres."""
import sys
import os

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene
from entities.ui import Button, Text


class Slider:
    """Slider simple pour les valeurs numériques."""

    def __init__(self, x, y, width, height, min_val=0, max_val=1, value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.dragging = False

    def update(self, input_handler):
        """Met à jour le slider."""
        mouse_pos = input_handler.get_mouse_pos()

        if input_handler.is_mouse_button_pressed(1):
            if self.dragging or self.rect.collidepoint(mouse_pos):
                self.dragging = True
                # Calcule la nouvelle valeur
                relative_x = mouse_pos[0] - self.rect.x
                relative_x = max(0, min(relative_x, self.rect.width))
                self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
        else:
            self.dragging = False

        return self.value

    def draw(self, screen):
        """Dessine le slider."""
        # Fond - Gris pastel clair
        pygame.draw.rect(screen, (220, 220, 230), self.rect)

        # Remplissage - Bleu pastel
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, (180, 210, 255), fill_rect)  # Bleu pastel

        # Bordure - Violet pastel
        pygame.draw.rect(screen, (180, 180, 200), self.rect, 2)

        # Curseur - Rose pastel
        cursor_x = self.rect.x + fill_width
        pygame.draw.line(screen, (255, 180, 200),  # Rose pastel
                        (cursor_x, self.rect.y),
                        (cursor_x, self.rect.y + self.rect.height), 3)


class SettingsScene(Scene):
    """Menu des paramètres."""

    def __init__(self, game):
        super().__init__(game)
        self.music_slider = None
        self.sfx_slider = None

    def on_enter(self):
        """Initialise le menu des paramètres."""
        font_large = self.game.assets.get_font('large')
        font_medium = self.game.assets.get_font('medium')
        font_small = self.game.assets.get_font('small')

        if not font_large:
            font_large = pygame.font.Font(None, 72)
        if not font_medium:
            font_medium = pygame.font.Font(None, 42)
        if not font_small:
            font_small = pygame.font.Font(None, 28)

        # Titre - Rose pastel
        self.title = Text(
            "PARAMETRES",
            self.game.config.window_width // 2,
            70,
            font_large,
            (255, 179, 186),  # Rose pastel
            center=True
        )

        # Section Audio - Bleu pastel
        self.audio_title = Text(
            "Audio",
            self.game.config.window_width // 2,
            170,
            font_medium,
            (180, 210, 255),  # Bleu pastel
            center=True
        )

        slider_x = self.game.config.window_width // 2 - 150
        slider_width = 300
        slider_height = 25

        # Labels et sliders de volume - Texte pastel
        self.music_label = Text(
            "Volume Musique:",
            slider_x - 180,
            235,
            font_small,
            (120, 130, 150)  # Gris-bleu pastel
        )

        self.music_slider = Slider(
            slider_x, 230, slider_width, slider_height,
            0, 1, self.game.audio.music_volume
        )

        self.sfx_label = Text(
            "Volume Effets:",
            slider_x - 180,
            285,
            font_small,
            (120, 130, 150)  # Gris-bleu pastel
        )

        self.sfx_slider = Slider(
            slider_x, 280, slider_width, slider_height,
            0, 1, self.game.audio.sfx_volume
        )

        # Section Gameplay - Violet pastel
        self.gameplay_title = Text(
            "Gameplay",
            self.game.config.window_width // 2,
            360,
            font_medium,
            (200, 180, 220),  # Violet pastel
            center=True
        )

        # Toggle pour afficher les FPS - Couleurs pastel
        self.fps_toggle = Button(
            slider_x - 180, 410, 200, 45,
            "FPS: " + ("ON" if self.game.show_fps else "OFF"),
            font_small,
            color=(180, 230, 180) if self.game.show_fps else (230, 180, 180),  # Vert ou rose pastel
            hover_color=(160, 250, 160) if self.game.show_fps else (250, 160, 160)
        )

        # Toggle pour afficher les hitboxes - Couleurs pastel
        self.hitbox_toggle = Button(
            slider_x - 180, 470, 200, 45,
            "Hitboxes: " + ("ON" if self.game.show_hitboxes else "OFF"),
            font_small,
            color=(180, 230, 180) if self.game.show_hitboxes else (230, 180, 180),  # Vert ou rose pastel
            hover_color=(160, 250, 160) if self.game.show_hitboxes else (250, 160, 160)
        )

        # Bouton retour - Gris pastel
        self.back_button = Button(
            (self.game.config.window_width - 300) // 2,
            self.game.config.window_height - 100,
            300, 60,
            "RETOUR AU MENU", font_medium,
            color=(200, 200, 210),  # Gris pastel
            hover_color=(220, 220, 230)
        )

    def handle_events(self, events):
        """Gère les événements."""
        pass

    def update(self, dt):
        """Met à jour le menu."""
        # Sliders de volume
        music_vol = self.music_slider.update(self.game.input)
        self.game.audio.set_music_volume(music_vol)
        self.game.config.set('audio', 'music_volume', music_vol)

        sfx_vol = self.sfx_slider.update(self.game.input)
        self.game.audio.set_sfx_volume(sfx_vol)
        self.game.config.set('audio', 'sfx_volume', sfx_vol)

        # Toggle FPS
        if self.fps_toggle.update(self.game.input):
            self.game.show_fps = not self.game.show_fps
            self.fps_toggle.text = "FPS: " + ("ON" if self.game.show_fps else "OFF")
            self.fps_toggle.color = (60, 80, 60) if self.game.show_fps else (80, 60, 60)
            self.fps_toggle.hover_color = (80, 120, 80) if self.game.show_fps else (120, 80, 80)
            self.game.config.set('debug', 'show_fps', self.game.show_fps)

        # Toggle Hitboxes
        if self.hitbox_toggle.update(self.game.input):
            self.game.show_hitboxes = not self.game.show_hitboxes
            self.hitbox_toggle.text = "Hitboxes: " + ("ON" if self.game.show_hitboxes else "OFF")
            self.hitbox_toggle.color = (60, 80, 60) if self.game.show_hitboxes else (80, 60, 60)
            self.hitbox_toggle.hover_color = (80, 120, 80) if self.game.show_hitboxes else (120, 80, 80)
            self.game.config.set('debug', 'show_hitboxes', self.game.show_hitboxes)

        # Bouton retour
        if self.back_button.update(self.game.input):
            self.game.config.save()  # Sauvegarde avant de quitter
            self.game.scene_manager.change_scene('menu')

    def draw(self, screen):
        """Dessine le menu."""
        # Fond - Vert grisé assombri (monde végétal)
        screen.fill((160, 180, 155))

        # Titre
        self.title.draw(screen)

        # Section Audio
        self.audio_title.draw(screen)
        self.music_label.draw(screen)
        self.music_slider.draw(screen)
        self.sfx_label.draw(screen)
        self.sfx_slider.draw(screen)

        # Affiche les pourcentages
        font_small = pygame.font.Font(None, 24)
        music_percent = Text(
            f"{int(self.music_slider.value * 100)}%",
            self.music_slider.rect.x + self.music_slider.rect.width + 30,
            self.music_slider.rect.y + 5,
            font_small,
            (200, 200, 200)
        )
        music_percent.draw(screen)

        sfx_percent = Text(
            f"{int(self.sfx_slider.value * 100)}%",
            self.sfx_slider.rect.x + self.sfx_slider.rect.width + 30,
            self.sfx_slider.rect.y + 5,
            font_small,
            (200, 200, 200)
        )
        sfx_percent.draw(screen)

        # Section Gameplay
        self.gameplay_title.draw(screen)
        self.fps_toggle.draw(screen)
        self.hitbox_toggle.draw(screen)

        # Bouton retour
        self.back_button.draw(screen)

        # Instructions
        font_tiny = pygame.font.Font(None, 18)
        instructions = Text(
            "F3 pour toggle FPS | F4 pour toggle Hitboxes",
            self.game.config.window_width // 2,
            self.game.config.window_height - 30,
            font_tiny,
            (120, 120, 120),
            center=True
        )
        instructions.draw(screen)
