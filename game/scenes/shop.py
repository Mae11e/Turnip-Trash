"""Scène de shop pour améliorer le joueur avec les graines."""
import sys
import os

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene


class ShopScene(Scene):
    """Scène du shop pour acheter des améliorations."""

    def __init__(self, game):
        super().__init__(game)
        self.selected_index = 0
        self.next_wave = 1
        self.input_delay = 0.3
        self.current_delay = 0
        self.upgrades = None  # Sera défini dans on_enter

        # Définition des améliorations
        self.upgrade_items = [
            {
                'name': 'Vie',
                'description': '+20 vie maximum',
                'attr': 'health_level',
                'color': (255, 100, 100)
            },
            {
                'name': 'Vitesse',
                'description': '+15% vitesse de deplacement',
                'attr': 'speed_level',
                'color': (100, 200, 255)
            },
            {
                'name': 'Degats',
                'description': '+25% degats des projectiles',
                'attr': 'damage_level',
                'color': (255, 200, 100)
            },
            {
                'name': 'Cadence',
                'description': '+20% cadence de tir',
                'attr': 'fire_rate_level',
                'color': (200, 100, 255)
            }
        ]

        # Charge le sprite de graine
        self.seed_image = None
        assets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        seed_path = os.path.join(assets_path, 'seed.png')
        if os.path.exists(seed_path):
            seed_img = pygame.image.load(seed_path).convert_alpha()
            self.seed_image = pygame.transform.scale(seed_img, (40, 40))

    def _get_upgrades(self):
        """Récupère l'instance player_upgrades depuis wave.py."""
        # Import dynamique pour éviter les imports circulaires
        wave_scene = self.game.scene_manager.scenes.get('wave1')
        if wave_scene:
            # Accède à player_upgrades depuis le module wave
            import importlib.util
            game_dir = os.path.dirname(os.path.dirname(__file__))
            spec = importlib.util.spec_from_file_location("wave_module", os.path.join(game_dir, "scenes", "wave.py"))
            wave_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(wave_module)
            return wave_module.player_upgrades
        return None

    def set_next_wave(self, wave_number):
        """Définit la prochaine vague."""
        self.next_wave = wave_number

    def on_enter(self):
        """Appelée quand on entre dans la scène."""
        self.current_delay = self.input_delay
        self.selected_index = 0
        self.upgrades = self._get_upgrades()

    def _buy_upgrade(self, index):
        """Achète une amélioration."""
        if not self.upgrades:
            return False

        item = self.upgrade_items[index]
        attr = item['attr']
        current_level = getattr(self.upgrades, attr)
        cost = self.upgrades.get_upgrade_cost(current_level)

        if self.upgrades.seeds >= cost and current_level < self.upgrades.max_level:
            self.upgrades.seeds -= cost
            setattr(self.upgrades, attr, current_level + 1)
            return True
        return False

    def handle_events(self, events):
        """Gère les événements."""
        if self.current_delay > 0:
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_index = (self.selected_index - 1) % len(self.upgrade_items)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % len(self.upgrade_items)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Acheter l'amélioration sélectionnée
                    self._buy_upgrade(self.selected_index)
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    # Continuer vers la prochaine vague
                    if self.next_wave <= 20:
                        self.game.scene_manager.change_scene(f'wave{self.next_wave}')
                    else:
                        self.game.scene_manager.change_scene('menu')
                elif event.key == pygame.K_m:
                    self.game.scene_manager.change_scene('menu')

    def update(self, dt):
        """Met à jour la scène."""
        if self.current_delay > 0:
            self.current_delay -= dt

    def draw(self, screen):
        """Dessine la scène."""
        if not self.upgrades:
            self.upgrades = self._get_upgrades()

        # Fond
        screen.fill((30, 40, 50))

        # Polices
        font_title = pygame.font.Font(None, 80)
        font_big = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        center_x = self.game.config.window_width // 2

        # Titre
        title = font_title.render("SHOP", True, (255, 220, 100))
        title_rect = title.get_rect(center=(center_x, 60))
        screen.blit(title, title_rect)

        # Affiche les graines disponibles
        seeds_y = 120
        if self.seed_image:
            screen.blit(self.seed_image, (center_x - 80, seeds_y - 15))
        seeds_text = f"x {self.upgrades.seeds if self.upgrades else 0}"
        seeds_surface = font_big.render(seeds_text, True, (255, 220, 100))
        screen.blit(seeds_surface, (center_x - 30, seeds_y))

        # Ligne de séparation
        pygame.draw.line(screen, (100, 100, 100), (100, 180), (self.game.config.window_width - 100, 180), 2)

        # Affiche les améliorations
        start_y = 220
        item_height = 100

        for i, item in enumerate(self.upgrade_items):
            y = start_y + i * item_height
            level = getattr(self.upgrades, item['attr']) if self.upgrades else 0
            cost = self.upgrades.get_upgrade_cost(level) if self.upgrades else 999
            is_maxed = level >= (self.upgrades.max_level if self.upgrades else 5)
            can_afford = (self.upgrades.seeds if self.upgrades else 0) >= cost and not is_maxed
            is_selected = i == self.selected_index

            # Fond de l'item (rectangle)
            bg_color = (60, 70, 80) if is_selected else (40, 50, 60)
            box_rect = pygame.Rect(150, y - 10, self.game.config.window_width - 300, item_height - 20)
            pygame.draw.rect(screen, bg_color, box_rect, border_radius=10)

            # Bordure si sélectionné
            if is_selected:
                pygame.draw.rect(screen, item['color'], box_rect, 3, border_radius=10)

            # Nom de l'amélioration
            name_color = item['color'] if can_afford or is_maxed else (150, 150, 150)
            name_surface = font_big.render(item['name'], True, name_color)
            screen.blit(name_surface, (180, y))

            # Description
            desc_surface = font_small.render(item['description'], True, (180, 180, 180))
            screen.blit(desc_surface, (180, y + 40))

            # Niveau actuel (barres)
            max_level = self.upgrades.max_level if self.upgrades else 5
            bar_x = self.game.config.window_width - 350
            for lvl in range(max_level):
                bar_rect = pygame.Rect(bar_x + lvl * 25, y + 10, 20, 30)
                if lvl < level:
                    pygame.draw.rect(screen, item['color'], bar_rect, border_radius=3)
                else:
                    pygame.draw.rect(screen, (80, 80, 80), bar_rect, border_radius=3)

            # Coût
            cost_x = self.game.config.window_width - 200
            if is_maxed:
                cost_text = "MAX"
                cost_color = (100, 255, 100)
            else:
                cost_text = f"{cost}"
                cost_color = (255, 220, 100) if can_afford else (255, 100, 100)

            cost_surface = font_medium.render(cost_text, True, cost_color)
            screen.blit(cost_surface, (cost_x + 40, y + 15))

            # Petite icône de graine à côté du coût
            if not is_maxed and self.seed_image:
                small_seed = pygame.transform.scale(self.seed_image, (25, 25))
                screen.blit(small_seed, (cost_x + 10, y + 15))

        # Instructions en bas
        instructions_y = self.game.config.window_height - 80

        inst1 = "HAUT/BAS: Naviguer  |  SPACE: Acheter  |  C/ESC: Continuer"
        inst1_surface = font_medium.render(inst1, True, (150, 150, 150))
        inst1_rect = inst1_surface.get_rect(center=(center_x, instructions_y))
        screen.blit(inst1_surface, inst1_rect)

        if self.next_wave <= 20:
            inst2 = f"Prochaine vague: {self.next_wave}"
        else:
            inst2 = "Toutes les vagues terminees!"
        inst2_surface = font_small.render(inst2, True, (100, 200, 100))
        inst2_rect = inst2_surface.get_rect(center=(center_x, instructions_y + 35))
        screen.blit(inst2_surface, inst2_rect)
