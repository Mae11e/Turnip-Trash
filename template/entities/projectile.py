"""Exemple de classe Projectile."""
import pygame
from entities.entity import Entity
from utils import Vector2D


class Projectile(Entity):
    """
    Exemple de projectile.
    À personnaliser selon les besoins de votre jeu.
    """

    def __init__(self, x, y, direction_x, direction_y, speed=400):
        super().__init__(x, y, 8, 8)

        # Normalise la direction
        import math
        length = math.sqrt(direction_x**2 + direction_y**2)
        if length > 0:
            direction_x /= length
            direction_y /= length

        # Vélocité
        self.velocity = Vector2D(direction_x * speed, direction_y * speed)

        # Propriétés
        self.damage = 25
        self.lifetime = 3.0
        self.age = 0

    def update(self, dt):
        """Met à jour le projectile."""
        super().update(dt)

        self.age += dt
        if self.age >= self.lifetime:
            self.destroy()

    def draw(self, screen, camera=None):
        """Dessine le projectile."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        # Dessine un cercle jaune
        pygame.draw.circle(screen, (255, 255, 100),
                          (int(draw_pos.x + 4), int(draw_pos.y + 4)), 4)

    def on_hit(self, target):
        """
        Appelé quand le projectile touche une cible.

        Args:
            target: Entité touchée
        """
        if hasattr(target, 'take_damage'):
            target.take_damage(self.damage)
        self.destroy()
