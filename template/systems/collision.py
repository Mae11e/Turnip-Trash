"""Système de détection de collisions."""
import pygame
import math


class CollisionSystem:
    """Système de détection de collisions simple."""

    @staticmethod
    def rect_rect(rect1, rect2):
        """
        Collision rectangle-rectangle.

        Args:
            rect1: pygame.Rect
            rect2: pygame.Rect

        Returns:
            bool: True si collision
        """
        return rect1.colliderect(rect2)

    @staticmethod
    def circle_circle(pos1, radius1, pos2, radius2):
        """
        Collision cercle-cercle.

        Args:
            pos1: Tuple (x, y) du centre du cercle 1
            radius1: Rayon du cercle 1
            pos2: Tuple (x, y) du centre du cercle 2
            radius2: Rayon du cercle 2

        Returns:
            bool: True si collision
        """
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (radius1 + radius2)

    @staticmethod
    def point_rect(point, rect):
        """
        Collision point-rectangle.

        Args:
            point: Tuple (x, y)
            rect: pygame.Rect

        Returns:
            bool: True si le point est dans le rectangle
        """
        return rect.collidepoint(point)

    @staticmethod
    def point_circle(point, circle_pos, radius):
        """
        Collision point-cercle.

        Args:
            point: Tuple (x, y)
            circle_pos: Tuple (x, y) du centre du cercle
            radius: Rayon du cercle

        Returns:
            bool: True si le point est dans le cercle
        """
        dx = point[0] - circle_pos[0]
        dy = point[1] - circle_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < radius

    @staticmethod
    def check_collision_list(entity, entities, use_circle=False):
        """
        Vérifie les collisions entre une entité et une liste d'entités.

        Args:
            entity: Entité à vérifier (doit avoir .rect ou .pos + .radius)
            entities: Liste d'entités
            use_circle: Si True, utilise la collision circulaire

        Returns:
            list: Liste des entités en collision
        """
        collisions = []

        if use_circle:
            for other in entities:
                if entity != other:
                    if hasattr(entity, 'pos') and hasattr(entity, 'radius') and \
                       hasattr(other, 'pos') and hasattr(other, 'radius'):
                        if CollisionSystem.circle_circle(
                            entity.pos.to_tuple(),
                            entity.radius,
                            other.pos.to_tuple(),
                            other.radius
                        ):
                            collisions.append(other)
        else:
            if hasattr(entity, 'rect'):
                for other in entities:
                    if entity != other and hasattr(other, 'rect'):
                        if CollisionSystem.rect_rect(entity.rect, other.rect):
                            collisions.append(other)

        return collisions

    @staticmethod
    def resolve_collision(entity1, entity2, elasticity=0.5):
        """
        Résout une collision simple entre deux entités circulaires.
        Sépare les entités et ajuste leurs vitesses.

        Args:
            entity1: Première entité (doit avoir pos, velocity, radius)
            entity2: Deuxième entité
            elasticity: Coefficient de rebond (0 = pas de rebond, 1 = rebond parfait)
        """
        if not all(hasattr(e, attr) for e in [entity1, entity2]
                   for attr in ['pos', 'velocity', 'radius']):
            return

        # Calcul de la direction de collision
        dx = entity2.pos.x - entity1.pos.x
        dy = entity2.pos.y - entity1.pos.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return

        # Normalisation
        nx = dx / distance
        ny = dy / distance

        # Séparation des entités
        overlap = (entity1.radius + entity2.radius) - distance
        entity1.pos.x -= nx * overlap * 0.5
        entity1.pos.y -= ny * overlap * 0.5
        entity2.pos.x += nx * overlap * 0.5
        entity2.pos.y += ny * overlap * 0.5

        # Calcul des vitesses relatives
        dvx = entity2.velocity.x - entity1.velocity.x
        dvy = entity2.velocity.y - entity1.velocity.y
        dot_product = dvx * nx + dvy * ny

        # Application de l'impulsion
        if dot_product < 0:
            impulse = (1 + elasticity) * dot_product
            entity1.velocity.x += impulse * nx
            entity1.velocity.y += impulse * ny
            entity2.velocity.x -= impulse * nx
            entity2.velocity.y -= impulse * ny
