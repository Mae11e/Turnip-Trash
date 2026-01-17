"""Exemple de classe Player avec plus de fonctionnalités."""
import pygame
from entities.entity import Entity
from utils import Cooldown


class Player(Entity):
    """
    Exemple de Player avec mouvement, tir, vie, etc.
    À personnaliser selon les besoins de votre jeu.
    """

    def __init__(self, x, y):
        super().__init__(x, y, 32, 32)

        # Statistiques
        self.speed = 250
        self.max_health = 100
        self.health = self.max_health

        # Capacités
        self.can_shoot = True
        self.shoot_cooldown = Cooldown(0.3)

        # État
        self.facing_direction = 1

    def take_damage(self, amount):
        """
        Inflige des dégâts au joueur.

        Args:
            amount: Montant des dégâts
        """
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.destroy()

    def heal(self, amount):
        """
        Soigne le joueur.

        Args:
            amount: Montant de soin
        """
        self.health = min(self.health + amount, self.max_health)

    def shoot(self):
        """
        Tire un projectile.

        Returns:
            Projectile ou None si en cooldown
        """
        if self.can_shoot and self.shoot_cooldown.is_ready():
            self.shoot_cooldown.trigger()
            # Retourne un projectile (à créer)
            # from entities.projectile import Projectile
            # return Projectile(self.pos.x, self.pos.y, self.facing_direction)
            return None
        return None

    def update(self, dt, input_handler):
        """
        Met à jour le joueur.

        Args:
            dt: Delta time
            input_handler: InputHandler
        """
        # Mouvement
        move_x = input_handler.get_axis('left', 'right')
        move_y = input_handler.get_axis('up', 'down')

        self.velocity.x = move_x * self.speed
        self.velocity.y = move_y * self.speed

        # Direction
        if move_x != 0:
            self.facing_direction = int(move_x)

        # Tir
        if input_handler.is_action_just_pressed('shoot'):
            projectile = self.shoot()
            # Gérer le projectile...

        # Met à jour les cooldowns
        self.shoot_cooldown.update(dt)

        # Applique le mouvement
        super().update(dt)

    def draw(self, screen, camera=None):
        """Dessine le joueur."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        # Couleur change selon la santé
        if self.health > 60:
            color = (50, 150, 255)
        elif self.health > 30:
            color = (255, 200, 50)
        else:
            color = (255, 50, 50)

        pygame.draw.rect(screen, color,
                        (draw_pos.x, draw_pos.y, self.width, self.height))

        # Indicateur de direction
        if self.facing_direction > 0:
            eye_x = draw_pos.x + self.width - 8
        else:
            eye_x = draw_pos.x + 8

        pygame.draw.circle(screen, (255, 255, 255),
                          (int(eye_x), int(draw_pos.y + 10)), 4)
