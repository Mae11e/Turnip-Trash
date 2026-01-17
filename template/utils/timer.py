"""Système de timers et cooldowns."""


class Timer:
    """Timer simple pour mesurer le temps écoulé."""

    def __init__(self, duration):
        """
        Args:
            duration: Durée en secondes
        """
        self.duration = duration
        self.elapsed = 0
        self.running = False

    def start(self):
        """Démarre le timer."""
        self.running = True
        self.elapsed = 0

    def stop(self):
        """Arrête le timer."""
        self.running = False

    def reset(self):
        """Remet le timer à zéro."""
        self.elapsed = 0

    def update(self, dt):
        """
        Met à jour le timer.

        Args:
            dt: Delta time en secondes
        """
        if self.running:
            self.elapsed += dt

    def is_finished(self):
        """Vérifie si le timer est terminé."""
        return self.elapsed >= self.duration

    def get_progress(self):
        """Retourne la progression (0 à 1)."""
        if self.duration == 0:
            return 1.0
        return min(1.0, self.elapsed / self.duration)


class Cooldown:
    """Cooldown pour limiter la fréquence d'actions."""

    def __init__(self, duration):
        """
        Args:
            duration: Durée du cooldown en secondes
        """
        self.duration = duration
        self.time_remaining = 0

    def update(self, dt):
        """
        Met à jour le cooldown.

        Args:
            dt: Delta time en secondes
        """
        if self.time_remaining > 0:
            self.time_remaining -= dt
            if self.time_remaining < 0:
                self.time_remaining = 0

    def is_ready(self):
        """Vérifie si le cooldown est prêt."""
        return self.time_remaining <= 0

    def trigger(self):
        """Active le cooldown."""
        self.time_remaining = self.duration

    def reset(self):
        """Remet le cooldown à zéro (prêt immédiatement)."""
        self.time_remaining = 0
