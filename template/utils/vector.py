"""Vector2D pour les opérations mathématiques 2D."""
import math


class Vector2D:
    """Vecteur 2D avec opérations mathématiques de base."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Addition de vecteurs."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Soustraction de vecteurs."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Multiplication par un scalaire."""
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        """Division par un scalaire."""
        if scalar == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    @property
    def magnitude(self):
        """Longueur du vecteur."""
        return math.sqrt(self.x**2 + self.y**2)

    @property
    def normalized(self):
        """Vecteur normalisé (longueur = 1)."""
        mag = self.magnitude
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def dot(self, other):
        """Produit scalaire."""
        return self.x * other.x + self.y * other.y

    def distance_to(self, other):
        """Distance à un autre vecteur."""
        return (self - other).magnitude

    def copy(self):
        """Copie du vecteur."""
        return Vector2D(self.x, self.y)

    def to_tuple(self):
        """Convertir en tuple (pour pygame)."""
        return (self.x, self.y)

    def to_int_tuple(self):
        """Convertir en tuple d'entiers (pour pygame)."""
        return (int(self.x), int(self.y))
