"""Composants d'interface utilisateur."""
import pygame


class Text:
    """Affichage de texte simple."""

    def __init__(self, text, x, y, font, color=(255, 255, 255), center=False):
        """
        Args:
            text: Texte à afficher
            x, y: Position
            font: Police pygame
            color: Couleur du texte
            center: Si True, centre le texte sur (x, y)
        """
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.center = center
        self.visible = True

    def set_text(self, text):
        """Change le texte."""
        self.text = text

    def draw(self, screen):
        """Dessine le texte."""
        if not self.visible:
            return

        surface = self.font.render(str(self.text), True, self.color)
        if self.center:
            rect = surface.get_rect(center=(self.x, self.y))
            screen.blit(surface, rect)
        else:
            screen.blit(surface, (self.x, self.y))


class Button:
    """Bouton cliquable."""

    def __init__(self, x, y, width, height, text, font,
                 color=(70, 70, 70), hover_color=(100, 100, 100),
                 text_color=(255, 255, 255), border_radius=5):
        """
        Args:
            x, y: Position
            width, height: Dimensions
            text: Texte du bouton
            font: Police pygame
            color: Couleur normale
            hover_color: Couleur au survol
            text_color: Couleur du texte
            border_radius: Rayon des coins arrondis
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.hovered = False
        self.clicked = False
        self.visible = True
        self.enabled = True

    def update(self, input_handler):
        """
        Met à jour l'état du bouton.

        Args:
            input_handler: InputHandler du jeu

        Returns:
            bool: True si le bouton a été cliqué
        """
        if not self.visible or not self.enabled:
            return False

        mouse_pos = input_handler.get_mouse_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if self.hovered and input_handler.is_mouse_button_just_pressed(1):
            self.clicked = True
            return True

        return False

    def draw(self, screen):
        """Dessine le bouton."""
        if not self.visible:
            return

        # Choisit la couleur
        current_color = self.hover_color if self.hovered else self.color
        if not self.enabled:
            current_color = (50, 50, 50)

        # Dessine le fond
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)

        # Dessine le texte
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class HealthBar:
    """Barre de vie."""

    def __init__(self, x, y, width, height, max_value=100,
                 fg_color=(0, 255, 0), bg_color=(50, 50, 50),
                 border_color=(255, 255, 255), border_width=2):
        """
        Args:
            x, y: Position
            width, height: Dimensions
            max_value: Valeur maximale
            fg_color: Couleur de la barre
            bg_color: Couleur du fond
            border_color: Couleur de la bordure
            border_width: Épaisseur de la bordure
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.current_value = max_value
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.visible = True

    def set_value(self, value):
        """Définit la valeur actuelle."""
        self.current_value = max(0, min(value, self.max_value))

    def get_percentage(self):
        """Retourne le pourcentage (0 à 1)."""
        if self.max_value == 0:
            return 0
        return self.current_value / self.max_value

    def draw(self, screen):
        """Dessine la barre de vie."""
        if not self.visible:
            return

        # Fond
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, bg_rect)

        # Barre de progression
        percentage = self.get_percentage()
        if percentage > 0:
            fg_width = int(self.width * percentage)
            fg_rect = pygame.Rect(self.x, self.y, fg_width, self.height)

            # Change la couleur selon le pourcentage
            if percentage > 0.6:
                color = self.fg_color
            elif percentage > 0.3:
                color = (255, 200, 0)
            else:
                color = (255, 0, 0)

            pygame.draw.rect(screen, color, fg_rect)

        # Bordure
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, bg_rect, self.border_width)
