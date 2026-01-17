"""Gestion centralisée des assets (images, fonts)."""
import pygame
import os


class AssetManager:
    """Gestionnaire centralisé des assets du jeu."""

    def __init__(self):
        self.images = {}
        self.fonts = {}

    def load_image(self, name, filepath, scale=None, convert_alpha=True):
        """
        Charge une image.

        Args:
            name: Nom pour référencer l'image
            filepath: Chemin vers le fichier image
            scale: Tuple (width, height) pour redimensionner, ou None
            convert_alpha: Si True, optimise l'image avec transparence
        """
        if not os.path.exists(filepath):
            print(f"Fichier image non trouvé: {filepath}")
            # Crée une surface de remplacement
            self.images[name] = self._create_placeholder(
                scale[0] if scale else 32,
                scale[1] if scale else 32
            )
            return

        try:
            image = pygame.image.load(filepath)
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()

            if scale:
                image = pygame.transform.scale(image, scale)

            self.images[name] = image
        except Exception as e:
            print(f"Erreur lors du chargement de {filepath}: {e}")
            self.images[name] = self._create_placeholder(
                scale[0] if scale else 32,
                scale[1] if scale else 32
            )

    def get_image(self, name):
        """
        Récupère une image chargée.

        Args:
            name: Nom de l'image

        Returns:
            Surface pygame ou None
        """
        return self.images.get(name)

    def load_spritesheet(self, name, filepath, sprite_width, sprite_height, count=None, convert_alpha=True):
        """
        Charge une spritesheet et la découpe en sprites individuels.

        Args:
            name: Nom de base pour les sprites (sera suffixé par _0, _1, etc.)
            filepath: Chemin vers le fichier spritesheet
            sprite_width: Largeur d'un sprite
            sprite_height: Hauteur d'un sprite
            count: Nombre de sprites à extraire (None = tous)
            convert_alpha: Si True, optimise avec transparence
        """
        if not os.path.exists(filepath):
            print(f"Fichier spritesheet non trouvé: {filepath}")
            return

        try:
            sheet = pygame.image.load(filepath)
            if convert_alpha:
                sheet = sheet.convert_alpha()

            sheet_width, sheet_height = sheet.get_size()
            sprites_per_row = sheet_width // sprite_width
            sprites_per_col = sheet_height // sprite_height
            total_sprites = sprites_per_row * sprites_per_col

            if count is None:
                count = total_sprites

            for i in range(min(count, total_sprites)):
                x = (i % sprites_per_row) * sprite_width
                y = (i // sprites_per_row) * sprite_height

                sprite = sheet.subsurface((x, y, sprite_width, sprite_height))
                self.images[f"{name}_{i}"] = sprite

        except Exception as e:
            print(f"Erreur lors du chargement de la spritesheet {filepath}: {e}")

    def load_font(self, name, filepath=None, size=24):
        """
        Charge une police de caractères.

        Args:
            name: Nom pour référencer la police
            filepath: Chemin vers le fichier .ttf (None = police système)
            size: Taille de la police
        """
        try:
            if filepath and os.path.exists(filepath):
                font = pygame.font.Font(filepath, size)
            else:
                font = pygame.font.Font(None, size)
            self.fonts[name] = font
        except Exception as e:
            print(f"Erreur lors du chargement de la police: {e}")
            self.fonts[name] = pygame.font.Font(None, size)

    def get_font(self, name):
        """
        Récupère une police chargée.

        Args:
            name: Nom de la police

        Returns:
            Font pygame ou None
        """
        return self.fonts.get(name)

    def _create_placeholder(self, width, height):
        """Crée une image de remplacement."""
        surface = pygame.Surface((width, height))
        surface.fill((255, 0, 255))
        pygame.draw.line(surface, (0, 0, 0), (0, 0), (width, height), 2)
        pygame.draw.line(surface, (0, 0, 0), (width, 0), (0, height), 2)
        return surface

    def clear(self):
        """Libère tous les assets."""
        self.images.clear()
        self.fonts.clear()
