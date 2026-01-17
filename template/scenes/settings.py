"""Scène des paramètres/préférences."""
import pygame
from scenes.scene_manager import Scene
from entities.ui import Button, Text


class Slider:
    """Slider simple pour les valeurs numériques."""

    def __init__(self, x, y, width, height, min_val=0, max_val=1, value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.dragging = False

    def update(self, input_handler):
        """Met à jour le slider."""
        mouse_pos = input_handler.get_mouse_pos()

        if input_handler.is_mouse_button_pressed(1):
            if self.dragging or self.rect.collidepoint(mouse_pos):
                self.dragging = True
                # Calcule la nouvelle valeur
                relative_x = mouse_pos[0] - self.rect.x
                relative_x = max(0, min(relative_x, self.rect.width))
                self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
        else:
            self.dragging = False

        return self.value

    def draw(self, screen):
        """Dessine le slider."""
        # Fond
        pygame.draw.rect(screen, (50, 50, 50), self.rect)

        # Remplissage
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, (100, 150, 255), fill_rect)

        # Bordure
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        # Curseur
        cursor_x = self.rect.x + fill_width
        pygame.draw.line(screen, (255, 255, 255),
                        (cursor_x, self.rect.y),
                        (cursor_x, self.rect.y + self.rect.height), 3)


class SettingsScene(Scene):
    """Menu des paramètres."""

    def __init__(self, game):
        super().__init__(game)
        self.waiting_for_key = None
        self.key_buttons = {}
        self.music_slider = None
        self.sfx_slider = None

    def on_enter(self):
        """Initialise le menu des paramètres."""
        font_large = self.game.assets.get_font('large')
        font_medium = self.game.assets.get_font('medium')
        font_small = self.game.assets.get_font('small')

        if not font_large:
            font_large = pygame.font.Font(None, 72)
        if not font_medium:
            font_medium = pygame.font.Font(None, 36)
        if not font_small:
            font_small = pygame.font.Font(None, 24)

        # Titre
        self.title = Text(
            "PARAMETRES",
            self.game.config.window_width // 2,
            50,
            font_large,
            (255, 255, 255),
            center=True
        )

        # Section Audio
        self.audio_title = Text(
            "Audio",
            self.game.config.window_width // 2,
            110,
            font_medium,
            (200, 200, 255),
            center=True
        )

        slider_x = self.game.config.window_width // 2 - 100
        slider_width = 200
        slider_height = 20

        # Labels et sliders de volume
        self.music_label = Text(
            "Musique:",
            slider_x - 120,
            150,
            font_small,
            (200, 200, 200)
        )

        self.music_slider = Slider(
            slider_x, 145, slider_width, slider_height,
            0, 1, self.game.audio.music_volume
        )

        self.sfx_label = Text(
            "Effets sonores:",
            slider_x - 120,
            190,
            font_small,
            (200, 200, 200)
        )

        self.sfx_slider = Slider(
            slider_x, 185, slider_width, slider_height,
            0, 1, self.game.audio.sfx_volume
        )

        # Section Keybindings
        self.keybind_title = Text(
            "Controles",
            self.game.config.window_width // 2,
            250,
            font_medium,
            (200, 200, 255),
            center=True
        )

        # Crée les boutons pour chaque action
        actions = ['up', 'down', 'left', 'right', 'jump', 'shoot', 'pause']
        action_names = {
            'up': 'Haut',
            'down': 'Bas',
            'left': 'Gauche',
            'right': 'Droite',
            'jump': 'Sauter',
            'shoot': 'Tirer',
            'pause': 'Pause'
        }

        start_y = 300
        spacing = 50
        button_width = 200
        button_height = 45
        label_x = self.game.config.window_width // 2 - 250
        button_x = self.game.config.window_width // 2 + 50

        self.action_labels = []
        self.key_buttons = {}

        for i, action in enumerate(actions):
            y = start_y + i * spacing

            # Label de l'action
            label = Text(
                action_names[action] + ":",
                label_x,
                y + 15,
                font_small,
                (200, 200, 200)
            )
            self.action_labels.append(label)

            # Bouton avec la touche actuelle
            key = self.game.input.bindings[action]
            key_name = pygame.key.name(key).upper()

            button = Button(
                button_x, y, button_width, button_height,
                key_name, font_small,
                color=(60, 60, 80),
                hover_color=(80, 80, 120)
            )
            self.key_buttons[action] = button

        # Boutons de préréglages
        preset_y = start_y + len(actions) * spacing + 40

        self.preset_title = Text(
            "Prereglages:",
            label_x,
            preset_y + 15,
            font_small,
            (200, 200, 200)
        )

        self.azerty_button = Button(
            button_x, preset_y, 95, button_height,
            "AZERTY", font_small,
            color=(60, 80, 60),
            hover_color=(80, 120, 80)
        )

        self.qwerty_button = Button(
            button_x + 105, preset_y, 95, button_height,
            "QWERTY", font_small,
            color=(60, 80, 60),
            hover_color=(80, 120, 80)
        )

        # Bouton retour
        self.back_button = Button(
            (self.game.config.window_width - 250) // 2,
            self.game.config.window_height - 100,
            250, 50,
            "RETOUR", font_medium
        )

        # Message d'attente de touche
        self.waiting_text = Text(
            "Appuyez sur une touche...",
            self.game.config.window_width // 2,
            self.game.config.window_height - 180,
            font_small,
            (255, 200, 100),
            center=True
        )
        self.waiting_text.visible = False

    def handle_events(self, events):
        """Gère les événements."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Si on attend une touche
                if self.waiting_for_key:
                    # Évite d'assigner ESC (pour pouvoir annuler)
                    if event.key != pygame.K_ESCAPE:
                        # Assigne la nouvelle touche
                        self.game.input.bindings[self.waiting_for_key] = event.key

                        # Met à jour le texte du bouton
                        key_name = pygame.key.name(event.key).upper()
                        self.key_buttons[self.waiting_for_key].text = key_name

                        # Sauvegarde dans la config
                        self._save_keybindings()

                    # Arrête d'attendre
                    self.waiting_for_key = None
                    self.waiting_text.visible = False

    def update(self, dt):
        """Met à jour le menu."""
        # Si on attend une touche, ne traite pas les boutons
        if self.waiting_for_key:
            return

        # Sliders de volume
        music_vol = self.music_slider.update(self.game.input)
        self.game.audio.set_music_volume(music_vol)
        self.game.config.set('audio', 'music_volume', music_vol)

        sfx_vol = self.sfx_slider.update(self.game.input)
        self.game.audio.set_sfx_volume(sfx_vol)
        self.game.config.set('audio', 'sfx_volume', sfx_vol)

        # Vérifie les clics sur les boutons de touches
        for action, button in self.key_buttons.items():
            if button.update(self.game.input):
                self.waiting_for_key = action
                self.waiting_text.visible = True

        # Préréglages
        if self.azerty_button.update(self.game.input):
            self._apply_azerty_preset()

        if self.qwerty_button.update(self.game.input):
            self._apply_qwerty_preset()

        # Bouton retour
        if self.back_button.update(self.game.input):
            self.game.config.save()  # Sauvegarde avant de quitter
            self.game.scene_manager.change_scene('menu')

    def draw(self, screen):
        """Dessine le menu."""
        screen.fill((30, 30, 50))

        # Titre
        self.title.draw(screen)

        # Section Audio
        self.audio_title.draw(screen)
        self.music_label.draw(screen)
        self.music_slider.draw(screen)
        self.sfx_label.draw(screen)
        self.sfx_slider.draw(screen)

        # Affiche les pourcentages
        font_small = pygame.font.Font(None, 24)
        music_percent = Text(
            f"{int(self.music_slider.value * 100)}%",
            self.music_slider.rect.x + self.music_slider.rect.width + 20,
            self.music_slider.rect.y,
            font_small,
            (200, 200, 200)
        )
        music_percent.draw(screen)

        sfx_percent = Text(
            f"{int(self.sfx_slider.value * 100)}%",
            self.sfx_slider.rect.x + self.sfx_slider.rect.width + 20,
            self.sfx_slider.rect.y,
            font_small,
            (200, 200, 200)
        )
        sfx_percent.draw(screen)

        # Section keybindings
        self.keybind_title.draw(screen)

        # Labels et boutons
        for label in self.action_labels:
            label.draw(screen)

        for button in self.key_buttons.values():
            button.draw(screen)

        # Préréglages
        self.preset_title.draw(screen)
        self.azerty_button.draw(screen)
        self.qwerty_button.draw(screen)

        # Bouton retour
        self.back_button.draw(screen)

        # Message d'attente
        if self.waiting_text.visible:
            self.waiting_text.draw(screen)

            # Instructions
            font_small = pygame.font.Font(None, 20)
            esc_text = Text(
                "ESC pour annuler",
                self.game.config.window_width // 2,
                self.game.config.window_height - 160,
                font_small,
                (150, 150, 150),
                center=True
            )
            esc_text.draw(screen)

    def _apply_azerty_preset(self):
        """Applique le préréglage AZERTY."""
        self.game.input.bindings['up'] = pygame.K_z
        self.game.input.bindings['left'] = pygame.K_q
        self._update_button_texts()
        self._save_keybindings()

    def _apply_qwerty_preset(self):
        """Applique le préréglage QWERTY."""
        self.game.input.bindings['up'] = pygame.K_w
        self.game.input.bindings['left'] = pygame.K_a
        self._update_button_texts()
        self._save_keybindings()

    def _update_button_texts(self):
        """Met à jour le texte de tous les boutons."""
        for action, button in self.key_buttons.items():
            key = self.game.input.bindings[action]
            key_name = pygame.key.name(key).upper()
            button.text = key_name

    def _save_keybindings(self):
        """Sauvegarde les keybindings dans la config."""
        if not hasattr(self.game.config.data, 'get'):
            return

        # Crée la section keybindings si elle n'existe pas
        if 'keybindings' not in self.game.config.data:
            self.game.config.data['keybindings'] = {}

        # Sauvegarde chaque binding
        for action, key in self.game.input.bindings.items():
            self.game.config.data['keybindings'][action] = key

        # Sauvegarde le fichier
        self.game.config.save()
