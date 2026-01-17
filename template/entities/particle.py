"""Système de particules pour les effets visuels."""
import pygame
import random
import math
from utils.vector import Vector2D


class Particle:
    """Particule individuelle."""

    def __init__(self, x, y, velocity, color, size, lifetime):
        """
        Args:
            x, y: Position de départ
            velocity: Vector2D de la vélocité
            color: Couleur (R, G, B)
            size: Taille de la particule
            lifetime: Durée de vie en secondes
        """
        self.pos = Vector2D(x, y)
        self.velocity = velocity
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        self.alive = True

    def update(self, dt):
        """Met à jour la particule."""
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt
        self.age += dt

        if self.age >= self.lifetime:
            self.alive = False

    def draw(self, screen, camera=None):
        """Dessine la particule."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        # Calcul de l'alpha basé sur l'âge
        alpha = int(255 * (1 - self.age / self.lifetime))
        color_with_alpha = (*self.color, alpha)

        # Crée une surface temporaire avec alpha
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color_with_alpha, (self.size, self.size), self.size)
        screen.blit(surf, draw_pos.to_int_tuple())


class ParticleSystem:
    """Système de gestion des particules."""

    def __init__(self):
        self.particles = []

    def emit(self, x, y, count=10, color=(255, 255, 255), speed_range=(50, 150),
             size_range=(2, 5), lifetime_range=(0.5, 1.5), angle_range=(0, 360)):
        """
        Émet des particules.

        Args:
            x, y: Position d'émission
            count: Nombre de particules
            color: Couleur des particules
            speed_range: Tuple (min, max) de la vitesse
            size_range: Tuple (min, max) de la taille
            lifetime_range: Tuple (min, max) de la durée de vie
            angle_range: Tuple (min, max) de l'angle en degrés
        """
        for _ in range(count):
            # Angle aléatoire
            angle = math.radians(random.uniform(*angle_range))
            speed = random.uniform(*speed_range)

            # Vélocité
            velocity = Vector2D(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )

            # Propriétés
            size = random.uniform(*size_range)
            lifetime = random.uniform(*lifetime_range)

            # Crée la particule
            particle = Particle(x, y, velocity, color, size, lifetime)
            self.particles.append(particle)

    def update(self, dt):
        """Met à jour toutes les particules."""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, screen, camera=None):
        """Dessine toutes les particules."""
        for particle in self.particles:
            particle.draw(screen, camera)

    def clear(self):
        """Supprime toutes les particules."""
        self.particles.clear()
