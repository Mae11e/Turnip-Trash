"""Scène de sélection de vague."""
import sys
import os

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene
from entities.ui import Button, Text


class WaveCard:
    """Carte représentant une vague."""

    def __init__(self, x, y, width, height, wave_number, description, difficulty):
        self.rect = pygame.Rect(x, y, width, height)
        self.wave_number = wave_number
        self.description = description
        self.difficulty = difficulty
        self.hovered = False
        self.unlocked = True  # Pour l'instant toutes les vagues sont débloquées

        # Couleurs pastel selon la difficulté
        difficulty_colors = {
            "Facile": (180, 230, 180),    # Vert pastel doux
            "Moyen": (250, 240, 180),     # Jaune pastel
            "Difficile": (255, 200, 180), # Pêche pastel
            "Extreme": (230, 180, 230)    # Violet pastel
        }
        self.base_color = difficulty_colors.get(difficulty, (200, 200, 210))
        self.hover_color = tuple(min(c + 20, 255) for c in self.base_color)

    def update(self, input_handler):
        """Met à jour la carte."""
        mouse_pos = input_handler.get_mouse_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        # Retourne True si cliqué
        if self.hovered and input_handler.is_mouse_button_pressed(1):
            return True
        return False

    def draw(self, screen):
        """Dessine la carte."""
        color = self.hover_color if self.hovered else self.base_color

        # Carte
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (180, 180, 200), self.rect, 3, border_radius=10)  # Bordure pastel

        # Numéro de vague - Texte sombre sur fond pastel
        font_large = pygame.font.Font(None, 48)
        wave_text = font_large.render(f"Vague {self.wave_number}", True, (80, 70, 90))
        wave_rect = wave_text.get_rect(center=(self.rect.centerx, self.rect.y + 40))
        screen.blit(wave_text, wave_rect)

        # Description - Texte sombre
        font_small = pygame.font.Font(None, 20)
        desc_lines = self.description.split('\n')
        y_offset = self.rect.y + 80
        for line in desc_lines:
            desc_text = font_small.render(line, True, (90, 80, 100))
            desc_rect = desc_text.get_rect(center=(self.rect.centerx, y_offset))
            screen.blit(desc_text, desc_rect)
            y_offset += 25

        # Difficulté - Couleur pastel chaude
        font_medium = pygame.font.Font(None, 28)
        diff_text = font_medium.render(self.difficulty, True, (200, 120, 140))  # Rose-pêche pastel
        diff_rect = diff_text.get_rect(center=(self.rect.centerx, self.rect.bottom - 25))
        screen.blit(diff_text, diff_rect)


class WaveSelectionScene(Scene):
    """Scène de sélection de vague."""

    def on_enter(self):
        """Initialise la scène de sélection."""
        font_large = self.game.assets.get_font('large')
        font_medium = self.game.assets.get_font('medium')

        if not font_large:
            font_large = pygame.font.Font(None, 60)
        if not font_medium:
            font_medium = pygame.font.Font(None, 36)

        # Titre - Violet pastel
        self.title = Text(
            "SELECTION DE VAGUE",
            self.game.config.window_width // 2,
            50,
            font_large,
            (180, 140, 200),  # Violet pastel
            center=True
        )

        # Créer les cartes de vagues (20 vagues en grille)
        self.wave_cards = []
        card_width = 120
        card_height = 120
        spacing_x = 20
        spacing_y = 20
        cards_per_row = 5
        rows = 4  # 5x4 = 20 vagues

        start_x = (self.game.config.window_width - (cards_per_row * card_width + (cards_per_row - 1) * spacing_x)) // 2
        start_y = 120

        for i in range(1, 21):  # 20 vagues
            row = (i - 1) // cards_per_row
            col = (i - 1) % cards_per_row

            card_x = start_x + col * (card_width + spacing_x)
            card_y = start_y + row * (card_height + spacing_y)

            # Détermine la difficulté selon le numéro
            if i <= 5:
                difficulty = "Facile"
                desc = f"{9 * i} ennemis"
            elif i <= 10:
                difficulty = "Moyen"
                desc = f"{9 * i} ennemis"
            elif i <= 15:
                difficulty = "Difficile"
                desc = f"{9 * i} ennemis"
            else:
                difficulty = "Extrême"
                desc = f"{9 * i} ennemis"

            card = WaveCard(
                card_x, card_y, card_width, card_height,
                i,
                desc,
                difficulty
            )
            self.wave_cards.append(card)

        # Bouton retour - Gris pastel
        self.back_button = Button(
            (self.game.config.window_width - 250) // 2,
            self.game.config.window_height - 100,
            250, 50,
            "RETOUR", font_medium,
            color=(200, 200, 210),  # Gris pastel
            hover_color=(220, 220, 230)
        )

        # Info supplémentaire - Texte pastel
        font_small = pygame.font.Font(None, 22)
        self.info_text = Text(
            "Sélectionnez une vague pour commencer. Les vagues plus difficiles offrent plus de récompenses!",
            self.game.config.window_width // 2,
            self.game.config.window_height - 150,
            font_small,
            (130, 140, 160),  # Gris-bleu pastel
            center=True
        )

    def handle_events(self, events):
        """Gère les événements."""
        pass

    def update(self, dt):
        """Met à jour la scène."""
        # Vérifie les clics sur les cartes
        for card in self.wave_cards:
            if card.update(self.game.input):
                # Démarre le jeu avec la vague sélectionnée
                self.game.selected_wave = card.wave_number

                # Lance la scène correspondante (système universel)
                scene_name = f'wave{card.wave_number}'
                if scene_name in self.game.scene_manager.scenes:
                    self.game.scene_manager.change_scene(scene_name)
                else:
                    # Fallback sur la scène de jeu par défaut
                    self.game.scene_manager.change_scene('game')
                return

        # Bouton retour
        if self.back_button.update(self.game.input):
            self.game.scene_manager.change_scene('menu')

    def draw(self, screen):
        """Dessine la scène."""
        # Fond pastel - Bleu-vert assombri
        screen.fill((155, 175, 165))

        # Effet de particules pastel en arrière-plan
        for i in range(10):
            x = (i * 150 + pygame.time.get_ticks() // 10) % self.game.config.window_width
            y = (i * 80) % self.game.config.window_height
            # Petites étoiles pastel
            pygame.draw.circle(screen, (255, 220, 230), (int(x), y), 3)
            pygame.draw.circle(screen, (220, 230, 255), (int(x) + 200, (y + 50) % self.game.config.window_height), 2)

        self.title.draw(screen)
        self.info_text.draw(screen)

        # Dessine les cartes
        for card in self.wave_cards:
            card.draw(screen)

        self.back_button.draw(screen)
