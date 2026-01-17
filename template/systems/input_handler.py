"""Gestion des entrées clavier et souris."""
import pygame


class InputHandler:
    """Gestionnaire des entrées utilisateur."""

    def __init__(self):
        self.keys_pressed = set()
        self.keys_just_pressed = set()
        self.keys_just_released = set()

        self.mouse_pos = (0, 0)
        self.mouse_buttons = {1: False, 2: False, 3: False}
        self.mouse_buttons_just_pressed = {1: False, 2: False, 3: False}
        self.mouse_buttons_just_released = {1: False, 2: False, 3: False}

        # Bindings personnalisables (AZERTY par défaut)
        # Pour QWERTY, changez: up=K_w, left=K_a
        self.bindings = {
            'up': pygame.K_z,      # Z pour AZERTY (W pour QWERTY)
            'down': pygame.K_s,
            'left': pygame.K_q,    # Q pour AZERTY (A pour QWERTY)
            'right': pygame.K_d,
            'jump': pygame.K_SPACE,
            'shoot': pygame.K_e,
            'pause': pygame.K_ESCAPE
        }

    def update(self, events):
        """
        Met à jour l'état des entrées.

        Args:
            events: Liste des événements pygame
        """
        # Reset des états "just pressed/released"
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        self.mouse_buttons_just_pressed = {k: False for k in self.mouse_buttons_just_pressed}
        self.mouse_buttons_just_released = {k: False for k in self.mouse_buttons_just_released}

        # Traite les événements
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.keys_just_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                self.keys_just_released.add(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_buttons[event.button] = True
                self.mouse_buttons_just_pressed[event.button] = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_buttons[event.button] = False
                self.mouse_buttons_just_released[event.button] = True

        # Met à jour la position de la souris
        self.mouse_pos = pygame.mouse.get_pos()

    def is_key_pressed(self, key):
        """Vérifie si une touche est pressée."""
        return key in self.keys_pressed

    def is_key_just_pressed(self, key):
        """Vérifie si une touche vient d'être pressée."""
        return key in self.keys_just_pressed

    def is_key_just_released(self, key):
        """Vérifie si une touche vient d'être relâchée."""
        return key in self.keys_just_released

    def is_action_pressed(self, action):
        """Vérifie si une action est pressée (via binding)."""
        if action in self.bindings:
            return self.is_key_pressed(self.bindings[action])
        return False

    def is_action_just_pressed(self, action):
        """Vérifie si une action vient d'être pressée (via binding)."""
        if action in self.bindings:
            return self.is_key_just_pressed(self.bindings[action])
        return False

    def is_mouse_button_pressed(self, button):
        """Vérifie si un bouton de la souris est pressé (1=gauche, 2=milieu, 3=droit)."""
        return self.mouse_buttons.get(button, False)

    def is_mouse_button_just_pressed(self, button):
        """Vérifie si un bouton de la souris vient d'être pressé."""
        return self.mouse_buttons_just_pressed.get(button, False)

    def get_mouse_pos(self):
        """Retourne la position de la souris."""
        return self.mouse_pos

    def get_axis(self, negative_action, positive_action):
        """
        Retourne un axe (-1, 0, ou 1) basé sur deux actions.
        Utile pour les mouvements directionnels.
        """
        value = 0
        if self.is_action_pressed(negative_action):
            value -= 1
        if self.is_action_pressed(positive_action):
            value += 1
        return value
