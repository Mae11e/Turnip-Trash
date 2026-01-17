"""Gestion des scènes du jeu."""
from .scene_manager import SceneManager, Scene
from .menu import MenuScene
from .game import GameScene
from .gameover import GameOverScene
from .settings import SettingsScene

__all__ = ['SceneManager', 'Scene', 'MenuScene', 'GameScene', 'GameOverScene', 'SettingsScene']
