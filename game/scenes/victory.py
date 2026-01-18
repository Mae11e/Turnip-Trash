"""Scène de victoire après avoir terminé une vague."""
import sys
import os

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene


class VictoryScene(Scene):
    """Scène affichée quand le joueur termine une vague."""

    def __init__(self, game):
        super().__init__(game)
        self.wave_number = 1
        self.score = 0
        self.enemies_killed = 0
        self.time_taken = 0
        self.input_delay = 0.5  # Délai avant de pouvoir interagir (secondes)
        self.current_delay = 0

    def set_stats(self, wave_number, score, enemies_killed, time_taken):
        """Définit les statistiques à afficher."""
        self.wave_number = wave_number
        self.score = score
        self.enemies_killed = enemies_killed
        self.time_taken = time_taken

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
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Aller au shop avant la prochaine vague
                    next_wave = self.wave_number + 1
                    shop_scene = self.game.scene_manager.scenes['shop']
                    shop_scene.set_next_wave(next_wave)
                    self.game.scene_manager.change_scene('shop')
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
        # Fond vert sombre
        screen.fill((20, 60, 30))

        # Overlay pour effet
        overlay = pygame.Surface((self.game.config.window_width, self.game.config.window_height))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Polices
        font_title = pygame.font.Font(None, 120)
        font_big = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)

        center_x = self.game.config.window_width // 2

        # VICTOIRE avec effet d'ombre
        title_text = "BRAVO !"
        # Ombre
        title_shadow = font_title.render(title_text, True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(center=(center_x + 4, 104))
        screen.blit(title_shadow, title_shadow_rect)
        # Texte principal
        title = font_title.render(title_text, True, (100, 255, 100))
        title_rect = title.get_rect(center=(center_x, 100))
        screen.blit(title, title_rect)

        # Vague terminée
        wave_text = f"Vague {self.wave_number} termin\u00e9e !"
        wave_surface = font_big.render(wave_text, True, (255, 220, 100))
        wave_rect = wave_surface.get_rect(center=(center_x, 220))
        screen.blit(wave_surface, wave_rect)

        # Ligne de séparation
        pygame.draw.line(screen, (100, 255, 100), (200, 290), (1080, 290), 3)

        # Statistiques
        stats_y = 340

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

        # Temps
        minutes = int(self.time_taken // 60)
        seconds = int(self.time_taken % 60)
        time_text = f"Temps: {minutes:02d}:{seconds:02d}"
        time_surface = font_medium.render(time_text, True, (200, 200, 200))
        time_rect = time_surface.get_rect(center=(center_x, stats_y))
        screen.blit(time_surface, time_rect)

        # Instructions (en bas)
        instructions_y = 550

        if self.current_delay > 0:
            # Message de délai
            wait_text = "..."
            wait_surface = font_small.render(wait_text, True, (150, 150, 150))
            wait_rect = wait_surface.get_rect(center=(center_x, instructions_y))
            screen.blit(wait_surface, wait_rect)
        else:
            # Vérifier s'il y a une prochaine vague
            if self.wave_number < 20:
                inst1 = f"SPACE: Vague {self.wave_number + 1}"
                inst1_surface = font_medium.render(inst1, True, (150, 255, 150))
                inst1_rect = inst1_surface.get_rect(center=(center_x, instructions_y))
                screen.blit(inst1_surface, inst1_rect)

                instructions_y += 50

                inst2 = "S: S\u00e9lection de vague  |  M: Menu  |  ESC: Quitter"
                inst2_surface = font_small.render(inst2, True, (180, 180, 180))
                inst2_rect = inst2_surface.get_rect(center=(center_x, instructions_y))
                screen.blit(inst2_surface, inst2_rect)
            else:
                # Toutes les vagues terminées!
                complete_text = "TOUTES LES VAGUES TERMIN\u00c9ES !"
                complete_surface = font_big.render(complete_text, True, (255, 220, 50))
                complete_rect = complete_surface.get_rect(center=(center_x, instructions_y))
                screen.blit(complete_surface, complete_rect)

                instructions_y += 60

                inst = "SPACE: Retour au menu"
                inst_surface = font_small.render(inst, True, (180, 180, 180))
                inst_rect = inst_surface.get_rect(center=(center_x, instructions_y))
                screen.blit(inst_surface, inst_rect)
