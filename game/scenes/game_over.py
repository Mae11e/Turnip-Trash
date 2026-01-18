"""Scène de Game Over."""
import sys
import os

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene


class GameOverScene(Scene):
    """Scène affichée quand le joueur meurt."""

    def __init__(self, game):
        super().__init__(game)
        self.score = 0
        self.wave_reached = 0
        self.enemies_killed = 0
        self.time_survived = 0
        self.input_delay = 0.5  # Délai avant de pouvoir interagir (secondes)
        self.current_delay = 0

    def set_stats(self, score, wave, enemies_killed, time_survived):
        """Définit les statistiques à afficher."""
        self.score = score
        self.wave_reached = wave
        self.enemies_killed = enemies_killed
        self.time_survived = time_survived

    def on_enter(self):
        """Appelée quand on entre dans la scène."""
        self.current_delay = self.input_delay

    def handle_events(self, events):
        """Gère les événements."""
        # Ignore les inputs pendant le délai
        if self.current_delay > 0:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Recommencer la même vague
                    self.game.scene_manager.change_scene(f'wave{self.wave_reached}')
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                    # Retour au menu
                    self.game.scene_manager.change_scene('menu')
                elif event.key == pygame.K_s:
                    # Sélection de vague
                    self.game.scene_manager.change_scene('wave_selection')

    def update(self, dt):
        """Met à jour la scène."""
        # Diminue le délai
        if self.current_delay > 0:
            self.current_delay -= dt

    def draw(self, screen):
        """Dessine la scène."""
        # Fond rouge sombre
        screen.fill((60, 20, 20))

        # Overlay sombre pour effet dramatique
        overlay = pygame.Surface((self.game.config.window_width, self.game.config.window_height))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Polices
        font_title = pygame.font.Font(None, 120)
        font_big = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)

        center_x = self.game.config.window_width // 2

        # GAME OVER avec effet d'ombre
        title_text = "GAME OVER"
        # Ombre
        title_shadow = font_title.render(title_text, True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(center=(center_x + 4, 124))
        screen.blit(title_shadow, title_shadow_rect)
        # Texte principal
        title = font_title.render(title_text, True, (255, 80, 80))
        title_rect = title.get_rect(center=(center_x, 120))
        screen.blit(title, title_rect)

        # Ligne de séparation
        pygame.draw.line(screen, (255, 80, 80), (200, 220), (1080, 220), 3)

        # Statistiques
        stats_y = 280

        # Vague atteinte
        wave_text = f"Vague atteinte: {self.wave_reached}"
        wave_surface = font_big.render(wave_text, True, (255, 200, 100))
        wave_rect = wave_surface.get_rect(center=(center_x, stats_y))
        screen.blit(wave_surface, wave_rect)

        stats_y += 90

        # Score
        score_text = f"Score: {self.score}"
        score_surface = font_medium.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(center_x, stats_y))
        screen.blit(score_surface, score_rect)

        stats_y += 60

        # Ennemis tués
        enemies_text = f"Ennemis \u00e9limin\u00e9s: {self.enemies_killed}"
        enemies_surface = font_medium.render(enemies_text, True, (200, 200, 200))
        enemies_rect = enemies_surface.get_rect(center=(center_x, stats_y))
        screen.blit(enemies_surface, enemies_rect)

        stats_y += 60

        # Temps survécu
        minutes = int(self.time_survived // 60)
        seconds = int(self.time_survived % 60)
        time_text = f"Temps: {minutes:02d}:{seconds:02d}"
        time_surface = font_medium.render(time_text, True, (200, 200, 200))
        time_rect = time_surface.get_rect(center=(center_x, stats_y))
        screen.blit(time_surface, time_rect)

        # Instructions (en bas)
        instructions_y = 570

        if self.current_delay > 0:
            # Message de délai
            wait_text = "..."
            wait_surface = font_small.render(wait_text, True, (150, 150, 150))
            wait_rect = wait_surface.get_rect(center=(center_x, instructions_y))
            screen.blit(wait_surface, wait_rect)
        else:
            # Instructions normales
            inst1 = f"SPACE: Réessayer (Vague {self.wave_reached})"
            inst1_surface = font_small.render(inst1, True, (150, 255, 150))
            inst1_rect = inst1_surface.get_rect(center=(center_x, instructions_y))
            screen.blit(inst1_surface, inst1_rect)

            instructions_y += 45

            inst2 = "S: S\u00e9lection de vague  |  M: Menu  |  ESC: Quitter"
            inst2_surface = font_small.render(inst2, True, (180, 180, 180))
            inst2_rect = inst2_surface.get_rect(center=(center_x, instructions_y))
            screen.blit(inst2_surface, inst2_rect)
