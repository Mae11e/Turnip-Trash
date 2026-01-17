"""Système de caméra pour le scrolling."""
from utils.vector import Vector2D


class Camera:
    """Caméra simple pour gérer le scrolling du jeu."""

    def __init__(self, width, height, world_width=None, world_height=None):
        """
        Args:
            width: Largeur de la fenêtre
            height: Hauteur de la fenêtre
            world_width: Largeur du monde (None = infini)
            world_height: Hauteur du monde (None = infini)
        """
        self.pos = Vector2D(0, 0)
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height

        # Target à suivre
        self.target = None
        self.smoothness = 0.1

    def follow(self, target, smoothness=0.1):
        """
        Configure la caméra pour suivre une cible.

        Args:
            target: Entité à suivre (doit avoir .pos)
            smoothness: Lissage du mouvement (0 = instantané, 1 = très lent)
        """
        self.target = target
        self.smoothness = smoothness

    def update(self, dt):
        """
        Met à jour la position de la caméra.

        Args:
            dt: Delta time en secondes
        """
        if self.target and hasattr(self.target, 'pos'):
            # Centre sur la cible
            target_x = self.target.pos.x - self.width / 2
            target_y = self.target.pos.y - self.height / 2

            # Lissage du mouvement
            self.pos.x += (target_x - self.pos.x) * self.smoothness
            self.pos.y += (target_y - self.pos.y) * self.smoothness

            # Limite aux bords du monde
            if self.world_width:
                self.pos.x = max(0, min(self.pos.x, self.world_width - self.width))
            if self.world_height:
                self.pos.y = max(0, min(self.pos.y, self.world_height - self.height))

    def apply(self, position):
        """
        Applique le décalage de la caméra à une position.

        Args:
            position: Vector2D de la position monde

        Returns:
            Vector2D de la position écran
        """
        return Vector2D(position.x - self.pos.x, position.y - self.pos.y)

    def apply_rect(self, rect):
        """
        Applique le décalage de la caméra à un rectangle.

        Args:
            rect: pygame.Rect

        Returns:
            pygame.Rect décalé
        """
        import pygame
        return pygame.Rect(
            rect.x - int(self.pos.x),
            rect.y - int(self.pos.y),
            rect.width,
            rect.height
        )

    def screen_to_world(self, screen_pos):
        """
        Convertit une position écran en position monde.

        Args:
            screen_pos: Tuple (x, y) en coordonnées écran

        Returns:
            Vector2D en coordonnées monde
        """
        return Vector2D(screen_pos[0] + self.pos.x, screen_pos[1] + self.pos.y)
