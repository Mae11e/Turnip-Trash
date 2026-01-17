"""Scène de jeu principale."""
import pygame
from scenes.scene_manager import Scene
from entities import Entity, ParticleSystem
from entities.ui import Text, HealthBar


class Player(Entity):
    """Exemple de classe Player."""

    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)
        self.speed = 200
        self.health = 100
        self.max_health = 100

    def update(self, dt, input_handler):
        """Met à jour le joueur."""
        # Mouvement
        move_x = input_handler.get_axis('left', 'right')
        move_y = input_handler.get_axis('up', 'down')

        self.velocity.x = move_x * self.speed
        self.velocity.y = move_y * self.speed

        # Applique le mouvement
        super().update(dt)

    def draw(self, screen, camera=None):
        """Dessine le joueur."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        # Dessine un carré bleu comme placeholder
        pygame.draw.rect(screen, (50, 150, 255),
                        (draw_pos.x, draw_pos.y, self.width, self.height))


class GameScene(Scene):
    """Scène de jeu principale."""

    def on_enter(self):
        """Initialise le jeu."""
        # Crée le joueur
        self.player = Player(
            self.game.config.window_width // 2,
            self.game.config.window_height // 2
        )

        # Système de particules
        self.particle_system = ParticleSystem()

        # UI
        font_medium = self.game.assets.get_font('medium')
        if not font_medium:
            font_medium = pygame.font.Font(None, 36)

        self.score_text = Text(
            "Score: 0",
            20, 20,
            font_medium
        )

        # Barre de vie
        self.health_bar = HealthBar(
            20, 60, 200, 20,
            max_value=self.player.max_health
        )

        self.score = 0

        # Exemple: émet des particules au démarrage
        self.particle_system.emit(
            self.player.pos.x + 16,
            self.player.pos.y + 16,
            count=20,
            color=(255, 200, 50)
        )

    def handle_events(self, events):
        """Gère les événements."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.scene_manager.change_scene('menu')
                # Exemple: crée des particules en appuyant sur E
                elif event.key == pygame.K_e:
                    self.particle_system.emit(
                        self.player.pos.x + 16,
                        self.player.pos.y + 16,
                        count=30,
                        color=(255, 100, 100)
                    )

    def update(self, dt):
        """Met à jour le jeu."""
        # Met à jour le joueur
        self.player.update(dt, self.game.input)

        # Met à jour les particules
        self.particle_system.update(dt)

        # Met à jour l'UI
        self.score_text.set_text(f"Score: {self.score}")
        self.health_bar.set_value(self.player.health)

    def draw(self, screen):
        """Dessine le jeu."""
        # Fond
        screen.fill((20, 20, 40))

        # Grille pour montrer le monde
        self._draw_grid(screen)

        # Entités
        self.player.draw(screen)

        # Particules
        self.particle_system.draw(screen)

        # UI
        self.score_text.draw(screen)
        self.health_bar.draw(screen)

        # Instructions
        font_small = pygame.font.Font(None, 20)
        instructions = Text(
            "ZQSD: bouger | E: particules | ESC: menu",
            self.game.config.window_width // 2,
            self.game.config.window_height - 20,
            font_small,
            (100, 100, 100),
            center=True
        )
        instructions.draw(screen)

    def _draw_grid(self, screen):
        """Dessine une grille de fond."""
        grid_size = 50
        color = (30, 30, 50)

        for x in range(0, self.game.config.window_width, grid_size):
            pygame.draw.line(screen, color, (x, 0), (x, self.game.config.window_height))

        for y in range(0, self.game.config.window_height, grid_size):
            pygame.draw.line(screen, color, (0, y), (self.game.config.window_width, y))
