"""Gestion de l'audio (musique et effets sonores)."""
import pygame
import os


class AudioManager:
    """Gestionnaire de l'audio du jeu."""

    def __init__(self, music_volume=0.7, sfx_volume=0.8):
        """
        Args:
            music_volume: Volume de la musique (0.0 à 1.0)
            sfx_volume: Volume des effets sonores (0.0 à 1.0)
        """
        pygame.mixer.init()
        self.music_volume = music_volume
        self.sfx_volume = sfx_volume

        # Stockage des sons chargés
        self.sounds = {}
        self.current_music = None

        # Applique les volumes
        pygame.mixer.music.set_volume(self.music_volume)

    def load_sound(self, name, filepath):
        """
        Charge un effet sonore.

        Args:
            name: Nom pour référencer le son
            filepath: Chemin vers le fichier audio
        """
        if not os.path.exists(filepath):
            print(f"Fichier audio non trouvé: {filepath}")
            return

        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
        except Exception as e:
            print(f"Erreur lors du chargement de {filepath}: {e}")

    def play_sound(self, name, loops=0):
        """
        Joue un effet sonore.

        Args:
            name: Nom du son à jouer
            loops: Nombre de répétitions (-1 pour infini)
        """
        if name in self.sounds:
            self.sounds[name].play(loops=loops)
        else:
            print(f"Son non trouvé: {name}")

    def stop_sound(self, name):
        """Arrête un effet sonore."""
        if name in self.sounds:
            self.sounds[name].stop()

    def play_music(self, filepath, loops=-1):
        """
        Joue une musique de fond.

        Args:
            filepath: Chemin vers le fichier audio
            loops: Nombre de répétitions (-1 pour infini)
        """
        if not os.path.exists(filepath):
            print(f"Fichier musique non trouvé: {filepath}")
            return

        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play(loops=loops)
            self.current_music = filepath
        except Exception as e:
            print(f"Erreur lors de la lecture de la musique: {e}")

    def stop_music(self):
        """Arrête la musique."""
        pygame.mixer.music.stop()
        self.current_music = None

    def pause_music(self):
        """Met en pause la musique."""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Reprend la musique."""
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        """
        Définit le volume de la musique.

        Args:
            volume: Volume (0.0 à 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """
        Définit le volume des effets sonores.

        Args:
            volume: Volume (0.0 à 1.0)
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def fadeout_music(self, duration_ms=1000):
        """
        Fait un fondu de sortie de la musique.

        Args:
            duration_ms: Durée du fondu en millisecondes
        """
        pygame.mixer.music.fadeout(duration_ms)
