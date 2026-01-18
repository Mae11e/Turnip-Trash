"""Système de vagues universel."""
import sys
import os
import random
import math

# Ajoute le dossier template au path
template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'template')
if template_path not in sys.path:
    sys.path.insert(0, template_path)

import pygame
from scenes.scene_manager import Scene
from entities import Entity, ParticleSystem
from entities.ui import Text, HealthBar


# Système d'améliorations global (persiste entre les scènes)
class PlayerUpgrades:
    """Stocke les améliorations du joueur."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.reset()

    def reset(self):
        """Remet les améliorations à zéro."""
        self.seeds = 0

        # Niveaux des améliorations (0 = pas amélioré)
        self.health_level = 0      # +20 vie max par niveau
        self.speed_level = 0       # +15% vitesse par niveau
        self.damage_level = 0      # +25% dégâts par niveau
        self.fire_rate_level = 0   # +20% cadence par niveau

        # Niveau max pour chaque amélioration
        self.max_level = 5

    def get_health_bonus(self):
        """Retourne le bonus de vie max."""
        return self.health_level * 20

    def get_speed_multiplier(self):
        """Retourne le multiplicateur de vitesse."""
        return 1.0 + (self.speed_level * 0.15)

    def get_damage_multiplier(self):
        """Retourne le multiplicateur de dégâts."""
        return 1.0 + (self.damage_level * 0.25)

    def get_fire_rate_multiplier(self):
        """Retourne le multiplicateur de cadence de tir."""
        return 1.0 + (self.fire_rate_level * 0.20)

    def get_upgrade_cost(self, current_level):
        """Retourne le coût pour passer au niveau suivant."""
        # Coût progressif: 5, 10, 20, 35, 55
        costs = [5, 10, 20, 35, 55]
        if current_level >= len(costs):
            return 999999  # Impossible
        return costs[current_level]


# Instance globale
player_upgrades = PlayerUpgrades()


# Configuration des vagues
WAVE_CONFIG = {
    # Formule: enemies = 8 * level + level = 9 * level
    # Formule: max_at_once = 3 + level
    # Formule: spawn_interval = 3.5 - (level * 0.2)
}

def get_wave_config(level):
    """Retourne la configuration pour une vague donnée."""
    return {
        'enemies_total': 9 * level,
        'max_at_once': min(3 + level, 10),  # Max 10 ennemis simultanés
        'spawn_interval': max(1.0, 3.5 - (level * 0.2)),  # Min 1 seconde
        'raccoon_ratio': min(0.3 + (level * 0.05), 0.6),  # Plus de raccoons dans les niveaux avancés
        'enemy_health_multiplier': 1 + (level - 1) * 0.2,  # +20% HP par niveau
        'enemy_speed_multiplier': 1 + (level - 1) * 0.1,   # +10% vitesse par niveau
        'enemy_shoot_speed': max(1.0, 3.0 - (level * 0.15)),  # Tirent plus vite
        'enemy_projectiles_count': min(1 + (level // 5), 4),  # +1 projectile tous les 5 niveaux, max 4
    }


class Seed:
    """Graine dropée par les ennemis."""

    def __init__(self, x, y, sprite=None):
        self.pos = type('Vector2D', (), {'x': x, 'y': y})()
        self.alive = True
        self.bob_offset = 0  # Pour l'effet de flottement
        self.bob_speed = 3
        self.sprite = sprite

        # Taille si sprite fourni
        if sprite:
            self.width = sprite.get_width()
            self.height = sprite.get_height()
        else:
            self.width = 16
            self.height = 16

    def update(self, dt):
        """Met à jour la graine."""
        self.bob_offset += self.bob_speed * dt

    def draw(self, screen):
        """Dessine la graine."""
        # Effet de flottement
        y_offset = math.sin(self.bob_offset) * 3
        draw_y = self.pos.y + y_offset

        if self.sprite:
            # Dessine le sprite centré
            draw_x = self.pos.x - self.width // 2
            draw_y_adjusted = draw_y - self.height // 2
            screen.blit(self.sprite, (int(draw_x), int(draw_y_adjusted)))
        else:
            # Fallback: cercle doré
            pygame.draw.circle(screen, (255, 220, 100), (int(self.pos.x), int(draw_y)), 8)
            pygame.draw.circle(screen, (200, 160, 50), (int(self.pos.x), int(draw_y)), 8, 2)


class Decoration:
    """Décoration de fond (arbre ou buisson)."""

    def __init__(self, x, y, sprite=None, decoration_type='tree'):
        self.pos = type('Vector2D', (), {'x': x, 'y': y})()
        self.type = decoration_type
        self.sprite = sprite

        # Taille si sprite fourni
        if sprite:
            self.width = sprite.get_width()
            self.height = sprite.get_height()

    def draw(self, screen):
        """Dessine la décoration."""
        if self.sprite:
            # Dessine le sprite centré
            draw_x = self.pos.x - self.width // 2
            draw_y = self.pos.y - self.height // 2
            screen.blit(self.sprite, (int(draw_x), int(draw_y)))
        else:
            # Fallback: formes géométriques
            if self.type == 'tree':
                # Tronc marron
                trunk_rect = pygame.Rect(self.pos.x - 8, self.pos.y - 20, 16, 40)
                pygame.draw.rect(screen, (120, 80, 50), trunk_rect)

                # Feuillage vert (3 cercles)
                pygame.draw.circle(screen, (80, 150, 80), (int(self.pos.x), int(self.pos.y - 40)), 25)
                pygame.draw.circle(screen, (90, 160, 90), (int(self.pos.x - 15), int(self.pos.y - 30)), 20)
                pygame.draw.circle(screen, (90, 160, 90), (int(self.pos.x + 15), int(self.pos.y - 30)), 20)

            elif self.type == 'bush':
                # Buisson - cercles verts superposés
                pygame.draw.circle(screen, (70, 140, 70), (int(self.pos.x), int(self.pos.y)), 20)
                pygame.draw.circle(screen, (80, 150, 80), (int(self.pos.x - 10), int(self.pos.y - 5)), 15)
                pygame.draw.circle(screen, (80, 150, 80), (int(self.pos.x + 10), int(self.pos.y - 5)), 15)
                pygame.draw.circle(screen, (90, 160, 90), (int(self.pos.x), int(self.pos.y - 10)), 12)


class Projectile(Entity):
    """Projectile du joueur ou ennemi."""

    def __init__(self, x, y, angle=None, is_player=True):
        super().__init__(x, y, 8, 8)
        self.speed = 400 if is_player else 250
        self.is_player = is_player

        # Direction aléatoire ou spécifiée
        if angle is None:
            angle = random.uniform(0, 360)

        # Convertit l'angle en vélocité
        self.velocity.x = math.cos(math.radians(angle)) * self.speed
        self.velocity.y = math.sin(math.radians(angle)) * self.speed

        self.lifetime = 3.0  # Durée de vie en secondes

    def update(self, dt, screen_width, screen_height):
        """Met à jour le projectile."""
        super().update(dt)

        # Réduit la durée de vie
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()

        # Détruit si hors écran
        if (self.pos.x < -50 or self.pos.x > screen_width + 50 or
            self.pos.y < -50 or self.pos.y > screen_height + 50):
            self.destroy()

    def draw(self, screen, camera=None):
        """Dessine le projectile."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        if self.is_player:
            # Projectile jaune/orange pour le joueur
            pygame.draw.circle(screen, (255, 200, 50),
                             (int(draw_pos.x), int(draw_pos.y)), 4)
            pygame.draw.circle(screen, (255, 255, 100),
                             (int(draw_pos.x), int(draw_pos.y)), 2)
        else:
            # Projectile rouge pour les ennemis
            pygame.draw.circle(screen, (200, 50, 50),
                             (int(draw_pos.x), int(draw_pos.y)), 4)
            pygame.draw.circle(screen, (255, 100, 100),
                             (int(draw_pos.x), int(draw_pos.y)), 2)


class Player(Entity):
    """Joueur Navet - suit la souris."""

    def __init__(self, x, y, sprite_sheet=None):
        super().__init__(x, y, 48, 48)

        # Stats de base avec améliorations
        base_speed = 300
        base_max_health = 100
        base_shoot_interval = 0.2  # Tire 5 fois par seconde

        # Applique les améliorations
        self.speed = base_speed * player_upgrades.get_speed_multiplier()
        self.max_health = base_max_health + player_upgrades.get_health_bonus()
        self.health = self.max_health
        self.damage_multiplier = player_upgrades.get_damage_multiplier()
        self.shoot_interval = base_shoot_interval / player_upgrades.get_fire_rate_multiplier()

        self.sprite_sheet = sprite_sheet
        self.sprites = []
        self.current_sprite = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        # Tir automatique
        self.shoot_timer = 0

        # Charge les sprites
        if sprite_sheet:
            self._load_sprites()

    def _load_sprites(self):
        """Découpe la sprite sheet en frames."""
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()

        # Essaie de détecter si c'est une sprite sheet ou une image simple
        if sheet_width > sheet_height * 1.5:
            # C'est probablement une sprite sheet horizontale
            frame_width = sheet_width // 4
            for i in range(4):
                frame = self.sprite_sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
                self.sprites.append(pygame.transform.scale(frame, (80, 80)))
        else:
            # Image simple, on crée des variations
            scaled = pygame.transform.scale(self.sprite_sheet, (80, 80))
            for i in range(4):
                self.sprites.append(scaled)

    def take_damage(self, amount):
        """Inflige des dégâts au joueur."""
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.destroy()

    def update(self, dt, mouse_pos):
        """Met à jour le joueur - suit la souris."""
        # Mouvement vers la souris
        target_x, target_y = mouse_pos
        dx = target_x - self.pos.x
        dy = target_y - self.pos.y
        distance = math.sqrt(dx * dx + dy * dy)

        # Déplace seulement si on est loin de la souris
        if distance > 10:
            self.velocity.x = (dx / distance) * self.speed
            self.velocity.y = (dy / distance) * self.speed
        else:
            self.velocity.x = 0
            self.velocity.y = 0

        # Animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % max(len(self.sprites), 1)

        # Applique le mouvement
        super().update(dt)

    def can_shoot(self, dt):
        """Vérifie si le joueur peut tirer."""
        self.shoot_timer += dt
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            return True
        return False

    def draw(self, screen, camera=None):
        """Dessine le joueur."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        if self.sprites:
            sprite = self.sprites[self.current_sprite]
            screen.blit(sprite, (draw_pos.x - 40, draw_pos.y - 40))
        elif self.sprite_sheet:
            # Utilise l'image telle quelle
            scaled = pygame.transform.scale(self.sprite_sheet, (80, 80))
            screen.blit(scaled, (draw_pos.x - 40, draw_pos.y - 40))
        else:
            # Fallback - dessine un carré vert (navet)
            color = (100, 200, 100)
            pygame.draw.rect(screen, color,
                            (draw_pos.x - 24, draw_pos.y - 24, 48, 48))


class Enemy(Entity):
    """Ennemi basique."""

    def __init__(self, x, y, enemy_type='basic', sprite_sheet=None, wave_config=None):
        super().__init__(x, y, 48, 48)
        self.enemy_type = enemy_type
        self.sprite_sheet = sprite_sheet
        self.sprites = []
        self.current_sprite = 0
        self.animation_timer = 0

        # Config de base
        if enemy_type == 'raccoon':
            base_speed = 80
            base_health = 30
            self.damage = 5
            self.score_value = 15
            self.animation_speed = 0.2
            base_shoot_interval = 2.0
        else:  # basic trash
            base_speed = 60
            base_health = 20
            self.damage = 3
            self.score_value = 10
            self.animation_speed = 0.25
            base_shoot_interval = 3.0

        # Applique les multiplicateurs de vague
        if wave_config:
            self.speed = base_speed * wave_config['enemy_speed_multiplier']
            self.health = int(base_health * wave_config['enemy_health_multiplier'])
            self.max_health = self.health  # Pour afficher la barre de vie
            self.shoot_interval = base_shoot_interval * wave_config['enemy_shoot_speed']
            self.projectiles_count = wave_config['enemy_projectiles_count']
        else:
            self.speed = base_speed
            self.health = base_health
            self.max_health = base_health
            self.shoot_interval = base_shoot_interval
            self.projectiles_count = 1

        # Tir
        self.shoot_timer = random.uniform(0, self.shoot_interval)

        # Charge les sprites
        if sprite_sheet:
            self._load_sprites()

    def _load_sprites(self):
        """Découpe la sprite sheet en frames."""
        sheet_width = self.sprite_sheet.get_width()
        sheet_height = self.sprite_sheet.get_height()

        if sheet_width > sheet_height * 1.5:
            frame_width = sheet_width // 4
            for i in range(4):
                frame = self.sprite_sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
                self.sprites.append(pygame.transform.scale(frame, (80, 80)))
        else:
            scaled = pygame.transform.scale(self.sprite_sheet, (80, 80))
            for i in range(4):
                self.sprites.append(scaled)

    def take_damage(self, amount):
        """Inflige des dégâts à l'ennemi."""
        self.health -= amount
        if self.health <= 0:
            self.destroy()

    def update(self, dt, player=None):
        """Met à jour l'ennemi."""
        if player and player.alive:
            # Poursuit le joueur
            dx = player.pos.x - self.pos.x
            dy = player.pos.y - self.pos.y

            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                self.velocity.x = (dx / distance) * self.speed
                self.velocity.y = (dy / distance) * self.speed

        # Animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % max(len(self.sprites), 1)

        # Tir
        self.shoot_timer += dt

        # Applique le mouvement
        super().update(dt)

    def can_shoot(self):
        """Vérifie si l'ennemi peut tirer et retourne le nombre de projectiles."""
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            return self.projectiles_count
        return 0

    def draw(self, screen, camera=None):
        """Dessine l'ennemi."""
        if camera:
            draw_pos = camera.apply(self.pos)
        else:
            draw_pos = self.pos

        if self.sprites:
            # Animation avec rebond
            offset_y = math.sin(self.animation_timer * 10) * 3
            sprite = self.sprites[self.current_sprite]
            screen.blit(sprite, (draw_pos.x - 40, draw_pos.y - 40 + offset_y))
        elif self.sprite_sheet:
            # Utilise l'image telle quelle
            offset_y = math.sin(self.animation_timer * 10) * 3
            scaled = pygame.transform.scale(self.sprite_sheet, (80, 80))
            screen.blit(scaled, (draw_pos.x - 40, draw_pos.y - 40 + offset_y))
        else:
            # Fallback selon le type
            if self.enemy_type == 'raccoon':
                color = (150, 100, 80)
            else:
                color = (80, 80, 80)
            pygame.draw.rect(screen, color,
                            (draw_pos.x - 24, draw_pos.y - 24, 48, 48))

        # Barre de vie au-dessus de l'ennemi
        if self.health < self.max_health:
            bar_width = 60
            bar_height = 6
            bar_x = draw_pos.x - bar_width // 2
            bar_y = draw_pos.y - 50

            # Fond de la barre (rouge foncé)
            pygame.draw.rect(screen, (80, 20, 20),
                           (bar_x, bar_y, bar_width, bar_height))

            # Barre de vie (vert -> jaune -> rouge selon le pourcentage)
            health_percent = self.health / self.max_health
            current_bar_width = int(bar_width * health_percent)

            if health_percent > 0.6:
                bar_color = (50, 200, 50)  # Vert
            elif health_percent > 0.3:
                bar_color = (255, 200, 50)  # Jaune
            else:
                bar_color = (255, 50, 50)  # Rouge

            if current_bar_width > 0:
                pygame.draw.rect(screen, bar_color,
                               (bar_x, bar_y, current_bar_width, bar_height))

            # Bordure de la barre
            pygame.draw.rect(screen, (200, 200, 200),
                           (bar_x, bar_y, bar_width, bar_height), 1)


class WaveScene(Scene):
    """Scène de vague universelle."""

    def __init__(self, game, wave_number=1):
        super().__init__(game)
        self.wave_number = wave_number
        self.wave_config = get_wave_config(wave_number)

    def on_enter(self):
        """Initialise la vague."""
        # Charge les assets
        self._load_assets()

        # Crée le joueur au centre
        player_x = self.game.config.window_width // 2
        player_y = self.game.config.window_height // 2
        self.player = Player(player_x, player_y, self.player_image)

        # Listes
        self.enemies = []
        self.projectiles = []
        self.seeds = []  # Graines à collecter
        self.decorations = []  # Décorations de fond

        # Crée les décorations
        self._create_decorations()

        # Système de particules
        self.particle_system = ParticleSystem()

        # UI - Tout en haut en colonnes
        font_medium = self.game.assets.get_font('medium')
        font_small = self.game.assets.get_font('small')

        if not font_medium:
            font_medium = pygame.font.Font(None, 32)
        if not font_small:
            font_small = pygame.font.Font(None, 24)

        # Crée les objets UI pour compatibilité (mis à jour dans update())
        self.score_text = Text("Score: 0", 10, 10, font_small, (255, 255, 255))
        self.health_bar = HealthBar(10, 40, 200, 20, self.player.max_health)

        # Stats
        self.score = 0
        self.enemies_killed = 0
        self.seeds_collected = 0  # Compteur de graines
        self.wave_time = 0  # Temps écoulé dans la vague

        # Spawn system avec config de vague
        self.spawn_timer = 0
        self.spawn_interval = self.wave_config['spawn_interval']
        self.enemies_to_spawn = self.wave_config['enemies_total']
        self.enemies_spawned = 0
        self.max_enemies_at_once = self.wave_config['max_at_once']

        # Message de début
        self.show_intro = True
        self.intro_timer = 2.0

        # Menu shop en jeu
        self.show_shop_menu = False
        self.shop_selected = 0

    def _load_assets(self):
        """Charge les assets du jeu."""
        assets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')

        # Charge l'image du joueur
        player_path = os.path.join(assets_path, 'player.png')
        if os.path.exists(player_path):
            self.player_image = pygame.image.load(player_path).convert_alpha()
        else:
            self.player_image = None

        # Charge l'image du raccoon
        raccoon_path = os.path.join(assets_path, 'racoon_ennemie.png')
        if os.path.exists(raccoon_path):
            self.raccoon_image = pygame.image.load(raccoon_path).convert_alpha()
        else:
            self.raccoon_image = None

        # Charge l'image de l'ennemi basique
        enemy_path = os.path.join(assets_path, 'ennemie_basic.png')
        if os.path.exists(enemy_path):
            self.enemy_image = pygame.image.load(enemy_path).convert_alpha()
        else:
            self.enemy_image = None

        # Charge les sprites de décoration (arbres x5, buissons x3)
        tree_path = os.path.join(assets_path, 'tree.png')
        if os.path.exists(tree_path):
            tree_img = pygame.image.load(tree_path).convert_alpha()
            new_width = tree_img.get_width() * 5
            new_height = tree_img.get_height() * 5
            self.tree_image = pygame.transform.scale(tree_img, (new_width, new_height))
        else:
            self.tree_image = None

        bush_path = os.path.join(assets_path, 'bush.png')
        if os.path.exists(bush_path):
            bush_img = pygame.image.load(bush_path).convert_alpha()
            new_width = bush_img.get_width() * 3
            new_height = bush_img.get_height() * 3
            self.bush_image = pygame.transform.scale(bush_img, (new_width, new_height))
        else:
            self.bush_image = None

        # Charge le sprite de graine (agrandi x2)
        seed_path = os.path.join(assets_path, 'seed.png')
        if os.path.exists(seed_path):
            seed_img = pygame.image.load(seed_path).convert_alpha()
            new_width = seed_img.get_width() * 2
            new_height = seed_img.get_height() * 2
            self.seed_image = pygame.transform.scale(seed_img, (new_width, new_height))
        else:
            self.seed_image = None

    def _create_decorations(self):
        """Crée les décorations de fond (arbres et buissons)."""
        # Nombre de décorations basé sur la taille de l'écran
        num_trees = 8
        num_bushes = 12

        # Arbres
        for _ in range(num_trees):
            x = random.randint(50, self.game.config.window_width - 50)
            y = random.randint(50, self.game.config.window_height - 50)
            self.decorations.append(Decoration(x, y, self.tree_image, 'tree'))

        # Buissons
        for _ in range(num_bushes):
            x = random.randint(30, self.game.config.window_width - 30)
            y = random.randint(30, self.game.config.window_height - 30)
            self.decorations.append(Decoration(x, y, self.bush_image, 'bush'))

    def _spawn_enemy(self):
        """Fait apparaître un ennemi."""
        # Choix aléatoire du type selon le ratio de la vague
        enemy_type = 'raccoon' if random.random() < self.wave_config['raccoon_ratio'] else 'basic'

        # Position aléatoire hors écran
        side = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'top':
            x = random.randint(0, self.game.config.window_width)
            y = -30
        elif side == 'bottom':
            x = random.randint(0, self.game.config.window_width)
            y = self.game.config.window_height + 30
        elif side == 'left':
            x = -30
            y = random.randint(0, self.game.config.window_height)
        else:  # right
            x = self.game.config.window_width + 30
            y = random.randint(0, self.game.config.window_height)

        # Crée l'ennemi avec la config de vague
        image = self.raccoon_image if enemy_type == 'raccoon' else self.enemy_image
        enemy = Enemy(x, y, enemy_type, image, self.wave_config)
        self.enemies.append(enemy)
        self.enemies_spawned += 1

    def handle_events(self, events):
        """Gère les événements."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.show_shop_menu:
                        self.show_shop_menu = False
                    else:
                        self.game.scene_manager.change_scene('menu')
                elif event.key == pygame.K_TAB:
                    # Ouvre/ferme le menu shop
                    self.show_shop_menu = not self.show_shop_menu
                    self.shop_selected = 0
                elif self.show_shop_menu:
                    # Navigation dans le menu shop
                    if event.key == pygame.K_UP or event.key == pygame.K_z:
                        self.shop_selected = (self.shop_selected - 1) % 4
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.shop_selected = (self.shop_selected + 1) % 4
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        # Acheter l'amélioration
                        self._buy_upgrade(self.shop_selected)

    def _buy_upgrade(self, index):
        """Achète une amélioration."""
        upgrades = [
            ('health_level', player_upgrades.health_level),
            ('speed_level', player_upgrades.speed_level),
            ('damage_level', player_upgrades.damage_level),
            ('fire_rate_level', player_upgrades.fire_rate_level)
        ]

        attr_name, current_level = upgrades[index]
        cost = player_upgrades.get_upgrade_cost(current_level)

        # Calcule le total de graines disponibles
        total_seeds = player_upgrades.seeds + self.seeds_collected

        if total_seeds >= cost and current_level < player_upgrades.max_level:
            # Dépense d'abord les graines de la vague actuelle
            if self.seeds_collected >= cost:
                self.seeds_collected -= cost
            else:
                # Dépense les graines de la vague puis les globales
                remaining = cost - self.seeds_collected
                self.seeds_collected = 0
                player_upgrades.seeds -= remaining

            setattr(player_upgrades, attr_name, current_level + 1)

            # Recrée le joueur avec les nouvelles stats
            old_health_ratio = self.player.health / self.player.max_health
            self.player = Player(self.player.pos.x, self.player.pos.y, self.player_image)
            self.player.health = int(self.player.max_health * old_health_ratio)

    def update(self, dt):
        """Met à jour la vague."""
        # Pause si menu shop ouvert
        if self.show_shop_menu:
            return

        # Intro
        if self.show_intro:
            self.intro_timer -= dt
            if self.intro_timer <= 0:
                self.show_intro = False
            return

        # Incrémente le temps de la vague
        self.wave_time += dt

        # Position de la souris
        mouse_pos = self.game.input.get_mouse_pos()

        # Met à jour le joueur
        if self.player.alive:
            self.player.update(dt, mouse_pos)

            # Tir automatique dans des directions aléatoires
            if self.player.can_shoot(dt):
                # Tire 2 projectiles dans des directions aléatoires
                for _ in range(2):
                    angle = random.uniform(0, 360)
                    projectile = Projectile(
                        self.player.pos.x,
                        self.player.pos.y,
                        angle=angle,
                        is_player=True
                    )
                    self.projectiles.append(projectile)

        # Met à jour les projectiles
        for proj in self.projectiles[:]:
            if not proj.alive:
                self.projectiles.remove(proj)
            else:
                proj.update(dt, self.game.config.window_width, self.game.config.window_height)

        # Spawn des ennemis
        if self.enemies_spawned < self.enemies_to_spawn and len(self.enemies) < self.max_enemies_at_once:
            self.spawn_timer += dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self._spawn_enemy()

        # Met à jour les ennemis
        for enemy in self.enemies[:]:
            if not enemy.alive:
                # Crée des particules
                self.particle_system.emit(
                    enemy.pos.x + 24,
                    enemy.pos.y + 24,
                    count=20,
                    color=(255, 150, 50)
                )
                self.score += enemy.score_value
                self.enemies_killed += 1

                # Drop de graine (30% de chance)
                if random.random() < 0.3:
                    seed = Seed(enemy.pos.x, enemy.pos.y, self.seed_image)
                    self.seeds.append(seed)

                self.enemies.remove(enemy)
            else:
                enemy.update(dt, self.player)

                # Tir aléatoire des ennemis (plusieurs projectiles selon la vague)
                projectiles_count = enemy.can_shoot()
                if projectiles_count > 0:
                    for _ in range(projectiles_count):
                        angle = random.uniform(0, 360)
                        projectile = Projectile(
                            enemy.pos.x,
                            enemy.pos.y,
                            angle=angle,
                            is_player=False
                        )
                        self.projectiles.append(projectile)

                # Collision avec le joueur
                if self.player.alive:
                    dx = enemy.pos.x - self.player.pos.x
                    dy = enemy.pos.y - self.player.pos.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < 50:
                        self.player.take_damage(enemy.damage)
                        enemy.take_damage(999)

                # Collision avec les projectiles du joueur
                for proj in self.projectiles[:]:
                    if proj.alive and proj.is_player:
                        dx = proj.pos.x - enemy.pos.x
                        dy = proj.pos.y - enemy.pos.y
                        distance = math.sqrt(dx * dx + dy * dy)

                        if distance < 30:
                            # Dégâts de base * multiplicateur d'amélioration
                            damage = int(10 * self.player.damage_multiplier)
                            enemy.take_damage(damage)
                            proj.destroy()
                            self.particle_system.emit(
                                proj.pos.x,
                                proj.pos.y,
                                count=5,
                                color=(255, 255, 100)
                            )

        # Collision des projectiles ennemis avec le joueur
        if self.player.alive:
            for proj in self.projectiles[:]:
                if proj.alive and not proj.is_player:
                    dx = proj.pos.x - self.player.pos.x
                    dy = proj.pos.y - self.player.pos.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < 30:
                        self.player.take_damage(5)
                        proj.destroy()
                        self.particle_system.emit(
                            proj.pos.x,
                            proj.pos.y,
                            count=5,
                            color=(255, 100, 100)
                        )

        # Collisions entre ennemis (les repousse pour éviter qu'ils se superposent)
        for i, enemy1 in enumerate(self.enemies):
            for enemy2 in self.enemies[i + 1:]:
                dx = enemy2.pos.x - enemy1.pos.x
                dy = enemy2.pos.y - enemy1.pos.y
                distance = math.sqrt(dx * dx + dy * dy)

                # Si les ennemis sont trop proches, les repousse
                min_distance = 60  # Distance minimale entre ennemis
                if distance < min_distance and distance > 0:
                    # Normalise la direction
                    nx = dx / distance
                    ny = dy / distance

                    # Force de répulsion
                    push_force = (min_distance - distance) * 0.5

                    # Applique la force aux deux ennemis
                    enemy1.pos.x -= nx * push_force
                    enemy1.pos.y -= ny * push_force
                    enemy2.pos.x += nx * push_force
                    enemy2.pos.y += ny * push_force

        # Met à jour les graines
        for seed in self.seeds[:]:
            seed.update(dt)

        # Collecte des graines
        if self.player.alive:
            for seed in self.seeds[:]:
                dx = seed.pos.x - self.player.pos.x
                dy = seed.pos.y - self.player.pos.y
                distance = math.sqrt(dx * dx + dy * dy)

                # Si le joueur est assez proche, collecte la graine
                if distance < 40:
                    self.seeds_collected += 1
                    self.seeds.remove(seed)
                    # Particules dorées
                    self.particle_system.emit(
                        seed.pos.x,
                        seed.pos.y,
                        count=10,
                        color=(255, 220, 100)
                    )

        # Met à jour les particules
        self.particle_system.update(dt)

        # Met à jour l'UI
        self.score_text.set_text(f"Score: {self.score}")
        self.health_bar.set_value(self.player.health)

        # Vérifie la fin de la vague
        if self.enemies_spawned >= self.enemies_to_spawn and len(self.enemies) == 0:
            self._complete_wave()

        # Game Over
        if not self.player.alive:
            # Passe les stats à la scène game_over
            game_over_scene = self.game.scene_manager.scenes['game_over']
            game_over_scene.set_stats(
                score=self.score,
                wave=self.wave_number,
                enemies_killed=self.enemies_killed,
                time_survived=self.wave_time
            )
            self.game.scene_manager.change_scene('game_over')

    def _complete_wave(self):
        """Vague terminée."""
        # Ajoute les graines collectées au système global
        player_upgrades.seeds += self.seeds_collected

        # Passe les stats à la scène victory
        victory_scene = self.game.scene_manager.scenes['victory']
        victory_scene.set_stats(
            wave_number=self.wave_number,
            score=self.score,
            enemies_killed=self.enemies_killed,
            time_taken=self.wave_time
        )
        self.game.scene_manager.change_scene('victory')

    def draw(self, screen):
        """Dessine la vague."""
        # Fond pastel nature
        screen.fill((170, 200, 180))

        # Grille subtile
        self._draw_grid(screen)

        # Décorations (arbres et buissons en arrière-plan)
        for decoration in self.decorations:
            decoration.draw(screen)

        # Graines
        for seed in self.seeds:
            seed.draw(screen)

        # Entités
        for enemy in self.enemies:
            enemy.draw(screen)

        # Projectiles
        for proj in self.projectiles:
            proj.draw(screen)

        if self.player.alive:
            self.player.draw(screen)

        # Particules
        self.particle_system.draw(screen)

        # ===== UI EN HAUT DE L'ÉCRAN EN COLONNES =====
        font_ui = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)
        y_pos = 15

        # Barre de fond semi-transparente pour l'UI
        ui_bar = pygame.Surface((self.game.config.window_width, 50))
        ui_bar.set_alpha(150)
        ui_bar.fill((40, 40, 50))
        screen.blit(ui_bar, (0, 0))

        # Colonne 1: Vague (centrée)
        wave_text = f"VAGUE {self.wave_number}"
        wave_surface = font_title.render(wave_text, True, (255, 200, 100))
        wave_x = self.game.config.window_width // 2 - wave_surface.get_width() // 2
        screen.blit(wave_surface, (wave_x, y_pos))

        # Colonne 2 (gauche): Score
        score_text = f"Score: {self.score}"
        score_surface = font_ui.render(score_text, True, (255, 255, 255))
        screen.blit(score_surface, (20, y_pos + 5))

        # Colonne 3 (sous score): Vie
        hp_text = f"Vie: {self.player.health}/{self.player.max_health}"
        hp_color = (255, 100, 100) if self.player.health < self.player.max_health / 2 else (100, 255, 100)
        hp_surface = font_ui.render(hp_text, True, hp_color)
        screen.blit(hp_surface, (150, y_pos + 5))

        # Colonne 4 (droite): Graines avec sprite
        seeds_text = f"Graines: {self.seeds_collected}"
        seeds_surface = font_ui.render(seeds_text, True, (255, 220, 100))
        seeds_x = self.game.config.window_width - seeds_surface.get_width() - 200

        # Dessine le sprite de graine à côté du texte
        if self.seed_image:
            # Version bien visible du sprite (70x70)
            small_seed = pygame.transform.scale(self.seed_image, (70, 70))
            screen.blit(small_seed, (seeds_x - 75, y_pos - 30))

        screen.blit(seeds_surface, (seeds_x, y_pos + 5))

        # Colonne 5 (droite): Ennemis
        enemy_text = f"Ennemis: {self.enemies_killed}/{self.enemies_to_spawn}"
        enemy_surface = font_ui.render(enemy_text, True, (255, 150, 150))
        enemy_x = self.game.config.window_width - enemy_surface.get_width() - 20
        screen.blit(enemy_surface, (enemy_x, y_pos + 5))

        # Instructions (en bas)
        font_instructions = pygame.font.Font(None, 22)
        instructions = Text(
            "Souris: déplacer | Tir: automatique | ESC: menu",
            self.game.config.window_width // 2,
            self.game.config.window_height - 20,
            font_instructions,
            (100, 100, 100),
            center=True
        )
        instructions.draw(screen)

        # Menu shop en jeu (Tab)
        if self.show_shop_menu:
            self._draw_shop_menu(screen)

        # Intro
        if self.show_intro:
            overlay = pygame.Surface((self.game.config.window_width, self.game.config.window_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            font_large = self.game.assets.get_font('large')
            if not font_large:
                font_large = pygame.font.Font(None, 72)

            intro_text = Text(
                f"VAGUE {self.wave_number}",
                self.game.config.window_width // 2,
                self.game.config.window_height // 2 - 40,
                font_large,
                (255, 200, 100),
                center=True
            )
            intro_text.draw(screen)

            font_medium = self.game.assets.get_font('medium')
            if not font_medium:
                font_medium = pygame.font.Font(None, 36)

            # Message dynamique selon le niveau
            if self.wave_number == 1:
                msg = "Bougez avec la souris et tirez automatiquement !"
            else:
                msg = f"{self.enemies_to_spawn} ennemis à éliminer - Bonne chance !"

            sub_text = Text(
                msg,
                self.game.config.window_width // 2,
                self.game.config.window_height // 2 + 40,
                font_medium,
                (200, 200, 200),
                center=True
            )
            sub_text.draw(screen)

    def _draw_grid(self, screen):
        """Dessine une grille de fond."""
        grid_size = 50
        color = (180, 210, 190)

        for x in range(0, self.game.config.window_width, grid_size):
            pygame.draw.line(screen, color, (x, 0), (x, self.game.config.window_height), 1)

        for y in range(0, self.game.config.window_height, grid_size):
            pygame.draw.line(screen, color, (0, y), (self.game.config.window_width, y), 1)

    def _draw_shop_menu(self, screen):
        """Dessine le menu shop en jeu."""
        # Overlay sombre
        overlay = pygame.Surface((self.game.config.window_width, self.game.config.window_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Polices
        font_title = pygame.font.Font(None, 60)
        font_big = pygame.font.Font(None, 40)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)

        center_x = self.game.config.window_width // 2

        # Titre
        title = font_title.render("AMELIORATIONS", True, (255, 220, 100))
        title_rect = title.get_rect(center=(center_x, 80))
        screen.blit(title, title_rect)

        # Graines disponibles (total global + collectées dans cette vague)
        total_seeds = player_upgrades.seeds + self.seeds_collected
        seeds_text = f"Graines disponibles: {total_seeds}"
        seeds_surface = font_big.render(seeds_text, True, (255, 220, 100))
        seeds_rect = seeds_surface.get_rect(center=(center_x, 130))
        screen.blit(seeds_surface, seeds_rect)

        # Liste des améliorations
        upgrades_info = [
            ('Vie', player_upgrades.health_level, '+20 vie max', (255, 100, 100)),
            ('Vitesse', player_upgrades.speed_level, '+15% vitesse', (100, 200, 255)),
            ('Degats', player_upgrades.damage_level, '+25% degats', (255, 200, 100)),
            ('Cadence', player_upgrades.fire_rate_level, '+20% cadence', (200, 100, 255))
        ]

        start_y = 200
        item_height = 80

        for i, (name, level, desc, color) in enumerate(upgrades_info):
            y = start_y + i * item_height
            is_selected = i == self.shop_selected
            is_maxed = level >= player_upgrades.max_level
            cost = player_upgrades.get_upgrade_cost(level)
            can_afford = total_seeds >= cost and not is_maxed

            # Fond
            bg_color = (60, 70, 80) if is_selected else (40, 50, 60)
            box_rect = pygame.Rect(200, y, self.game.config.window_width - 400, item_height - 10)
            pygame.draw.rect(screen, bg_color, box_rect, border_radius=8)

            # Bordure si sélectionné
            if is_selected:
                pygame.draw.rect(screen, color, box_rect, 3, border_radius=8)

            # Nom
            name_color = color if can_afford or is_maxed else (150, 150, 150)
            name_surface = font_big.render(name, True, name_color)
            screen.blit(name_surface, (220, y + 10))

            # Description
            desc_surface = font_small.render(desc, True, (180, 180, 180))
            screen.blit(desc_surface, (220, y + 45))

            # Barres de niveau
            bar_x = self.game.config.window_width - 350
            for lvl in range(player_upgrades.max_level):
                bar_rect = pygame.Rect(bar_x + lvl * 22, y + 15, 18, 25)
                if lvl < level:
                    pygame.draw.rect(screen, color, bar_rect, border_radius=2)
                else:
                    pygame.draw.rect(screen, (80, 80, 80), bar_rect, border_radius=2)

            # Coût
            cost_x = self.game.config.window_width - 230
            if is_maxed:
                cost_text = "MAX"
                cost_color = (100, 255, 100)
            else:
                cost_text = f"{cost}"
                cost_color = (255, 220, 100) if can_afford else (255, 100, 100)

            cost_surface = font_medium.render(cost_text, True, cost_color)
            screen.blit(cost_surface, (cost_x, y + 20))

        # Instructions en bas
        inst_y = self.game.config.window_height - 60
        inst_text = "HAUT/BAS: Naviguer | SPACE: Acheter | TAB/ESC: Fermer"
        inst_surface = font_medium.render(inst_text, True, (150, 150, 150))
        inst_rect = inst_surface.get_rect(center=(center_x, inst_y))
        screen.blit(inst_surface, inst_rect)
