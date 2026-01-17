"""Exemple de classe Enemy."""
import pygame
import random
from entities.entity import Entity


class Enemy(Entity):
    """
    Exemple d'ennemi basique.
    À personnaliser selon les besoins de votre jeu.
    """

    def __init__(self, x, y):
        super().__init__(x, y, 24, 24)

        # Statistiques
        self.speed = 100
        self.health = 50
        self.damage = 10

        # Comportement
        self.behavior = 'wander'
        self.change_direction_timer = 0
        self.change_direction_interval = 2.0

    def take_damage(self, amount):
        """
        Inflige des dégâts à l'ennemi.

        Args:
            amount: Montant des dégâts
        """
        self.health -= amount
        if self.health <= 0:
            self.destroy()

    def update(self, dt, player=None):
        """
        Met à jour l'ennemi.

        Args:
            dt: Delta time
            player: Référence au joueur (optionnel)
        """
        if self.behavior == 'wander':
            self._wander(dt)
        elif self.behavior == 'chase' and player:
            self._chase(player, dt)

        # Applique le mouvement
        super().update(dt)

    def _wander(self, dt):
        """Comportement d'errance."""
        self.change_direction_timer += dt

        if self.change_direction_timer >= self.change_direction_interval:
            self.change_direction_timer = 0

            # Change de direction aléatoirement
            angle = random.uniform(0, 360)
            import math
            self.velocity.x = math.cos(math.radians(angle)) * self.speed
            self.velocity.y = math.sin(math.radians(angle)) * self.speed

    def _chase(self, player, dt):
        """Poursuit le joueur."""
        # Direction vers le joueur
        dx = player.pos.x - self.pos.x
        dy = player.pos.y - self.pos.y

        # Normalise
        import math
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 0:
            self.velocity.x = (dx / distance) * self.speed
            self.velocity.y = (dy / distance) * self.speed

    def draw(self, screen, camera=None):
        """Dessine l'ennemi."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        # Dessine l'ennemi en rouge
        pygame.draw.rect(screen, (255, 50, 50),
                        (draw_pos.x, draw_pos.y, self.width, self.height))

        # Yeux
        pygame.draw.circle(screen, (255, 255, 0),
                          (int(draw_pos.x + 8), int(draw_pos.y + 8)), 3)
        pygame.draw.circle(screen, (255, 255, 0),
                          (int(draw_pos.x + 16), int(draw_pos.y + 8)), 3)
