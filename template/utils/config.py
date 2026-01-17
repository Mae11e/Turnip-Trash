"""Configuration du jeu."""
import json
import os


class Config:
    """Gestion de la configuration du jeu."""

    # Valeurs par défaut
    DEFAULTS = {
        'window': {
            'width': 1280,
            'height': 720,
            'title': 'Game Jam Template',
            'fps': 60
        },
        'audio': {
            'music_volume': 0.7,
            'sfx_volume': 0.8
        },
        'debug': {
            'show_fps': False,
            'show_hitboxes': False
        }
    }

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.data = self.DEFAULTS.copy()
        self.load()

    def load(self):
        """Charge la configuration depuis le fichier."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_data = json.load(f)
                    self._merge_config(loaded_data)
            except Exception as e:
                print(f"Erreur lors du chargement de la config: {e}")
                print("Utilisation de la config par défaut")

    def save(self):
        """Sauvegarde la configuration dans le fichier."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la config: {e}")

    def _merge_config(self, loaded_data):
        """Fusionne la config chargée avec les valeurs par défaut."""
        for section, values in loaded_data.items():
            if section in self.data and isinstance(values, dict):
                self.data[section].update(values)
            else:
                self.data[section] = values

    def get(self, section, key, default=None):
        """Récupère une valeur de configuration."""
        if section in self.data and key in self.data[section]:
            return self.data[section][key]
        return default

    def set(self, section, key, value):
        """Définit une valeur de configuration."""
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value

    @property
    def window_width(self):
        return self.data['window']['width']

    @property
    def window_height(self):
        return self.data['window']['height']

    @property
    def window_title(self):
        return self.data['window']['title']

    @property
    def fps(self):
        return self.data['window']['fps']

    @property
    def music_volume(self):
        return self.data['audio']['music_volume']

    @property
    def sfx_volume(self):
        return self.data['audio']['sfx_volume']

    @property
    def show_fps(self):
        return self.data['debug']['show_fps']

    @property
    def show_hitboxes(self):
        return self.data['debug']['show_hitboxes']
