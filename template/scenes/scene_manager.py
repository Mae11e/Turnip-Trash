"""Gestionnaire de scènes."""


class Scene:
    """Classe de base pour les scènes."""

    def __init__(self, game):
        """
        Args:
            game: Instance du jeu principal
        """
        self.game = game

    def on_enter(self):
        """Appelé quand on entre dans la scène."""
        pass

    def on_exit(self):
        """Appelé quand on sort de la scène."""
        pass

    def handle_events(self, events):
        """
        Gère les événements.

        Args:
            events: Liste des événements pygame
        """
        pass

    def update(self, dt):
        """
        Met à jour la scène.

        Args:
            dt: Delta time en secondes
        """
        pass

    def draw(self, screen):
        """
        Dessine la scène.

        Args:
            screen: Surface pygame
        """
        pass


class SceneManager:
    """Gestionnaire de scènes."""

    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.next_scene = None

    def add_scene(self, name, scene):
        """
        Ajoute une scène.

        Args:
            name: Nom de la scène
            scene: Instance de Scene
        """
        self.scenes[name] = scene

    def change_scene(self, name):
        """
        Change de scène.

        Args:
            name: Nom de la scène cible
        """
        if name in self.scenes:
            self.next_scene = name
        else:
            print(f"Scène inconnue: {name}")

    def _perform_scene_change(self):
        """Effectue le changement de scène."""
        if self.next_scene:
            if self.current_scene:
                self.scenes[self.current_scene].on_exit()

            self.current_scene = self.next_scene
            self.next_scene = None
            self.scenes[self.current_scene].on_enter()

    def handle_events(self, events):
        """Gère les événements de la scène courante."""
        if self.current_scene:
            self.scenes[self.current_scene].handle_events(events)

    def update(self, dt):
        """Met à jour la scène courante."""
        self._perform_scene_change()

        if self.current_scene:
            self.scenes[self.current_scene].update(dt)

    def draw(self, screen):
        """Dessine la scène courante."""
        if self.current_scene:
            self.scenes[self.current_scene].draw(screen)
