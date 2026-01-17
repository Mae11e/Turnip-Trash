"""Classe de base pour toutes les entités du jeu."""
import pygame
from utils.vector import Vector2D


class Entity:
    """Classe de base pour les entités du jeu."""

    def __init__(self, x, y, width=32, height=32):
        """
        Args:
            x: Position X
            y: Position Y
            width: Largeur
            height: Hauteur
        """
        self.pos = Vector2D(x, y)
        self.velocity = Vector2D(0, 0)
        self.width = width
        self.height = height
        self.alive = True

        # Rectangle de collision
        self.rect = pygame.Rect(x, y, width, height)

        # Pour les collisions circulaires
        self.radius = max(width, height) / 2

        # Sprite (à définir dans les classes enfants)
        self.sprite = None

    def update(self, dt):
        """
        Met à jour l'entité.

        Args:
            dt: Delta time en secondes
        """
        # Applique la vélocité
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

        # Met à jour le rect
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def draw(self, screen, camera=None):
        """
        Dessine l'entité.

        Args:
            screen: Surface pygame
            camera: Caméra optionnelle pour le scrolling
        """
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        if self.sprite:
            screen.blit(self.sprite, draw_pos.to_int_tuple())
        else:
            # Placeholder si pas de sprite
            pygame.draw.rect(screen, (255, 255, 255),
                           (draw_pos.x, draw_pos.y, self.width, self.height))

    def destroy(self):
        """Détruit l'entité."""
        self.alive = False

    def get_center(self):
        """Retourne le centre de l'entité."""
        return Vector2D(self.pos.x + self.width / 2, self.pos.y + self.height / 2)
