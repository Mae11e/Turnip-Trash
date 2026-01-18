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
        self.speed = 300
        self.max_health = 100
        self.health = self.max_health
        self.sprite_sheet = sprite_sheet
        self.sprites = []
        self.current_sprite = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        # Tir automatique
        self.shoot_timer = 0
        self.shoot_interval = 0.2  # Tire 5 fois par seconde

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

        # Système de particules
        self.particle_system = ParticleSystem()

        # UI
        font_medium = self.game.assets.get_font('medium')
        font_small = self.game.assets.get_font('small')

        if not font_medium:
            font_medium = pygame.font.Font(None, 36)
        if not font_small:
            font_small = pygame.font.Font(None, 24)

        self.score_text = Text(
            "Score: 0",
            20, 20,
            font_medium,
            (255, 255, 255)
        )

        self.wave_text = Text(
            f"VAGUE {self.wave_number}",
            self.game.config.window_width // 2,
            20,
            font_medium,
            (255, 200, 100),
            center=True
        )

        # Barre de vie
        self.health_bar = HealthBar(
            20, 60, 200, 20,
            max_value=self.player.max_health
        )

        # Stats
        self.score = 0
        self.enemies_killed = 0

        # Spawn system avec config de vague
        self.spawn_timer = 0
        self.spawn_interval = self.wave_config['spawn_interval']
        self.enemies_to_spawn = self.wave_config['enemies_total']
        self.enemies_spawned = 0
        self.max_enemies_at_once = self.wave_config['max_at_once']

        # Message de début
        self.show_intro = True
        self.intro_timer = 2.0

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
                    self.game.scene_manager.change_scene('menu')

    def update(self, dt):
        """Met à jour la vague."""
        # Intro
        if self.show_intro:
            self.intro_timer -= dt
            if self.intro_timer <= 0:
                self.show_intro = False
            return

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
                            enemy.take_damage(10)
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
            self.game.scene_manager.change_scene('gameover')

    def _complete_wave(self):
        """Vague terminée."""
        self.game.scene_manager.change_scene('wave_selection')

    def draw(self, screen):
        """Dessine la vague."""
        # Fond pastel nature
        screen.fill((170, 200, 180))

        # Grille subtile
        self._draw_grid(screen)

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

        # UI
        self.score_text.draw(screen)
        self.wave_text.draw(screen)
        self.health_bar.draw(screen)

        # Compteur d'ennemis
        font_small = pygame.font.Font(None, 24)
        enemy_text = f"Ennemis: {len(self.enemies)} | Tués: {self.enemies_killed}/{self.enemies_to_spawn}"
        enemy_surface = font_small.render(enemy_text, True, (255, 255, 255))
        enemy_x = self.game.config.window_width - enemy_surface.get_width() - 20
        screen.blit(enemy_surface, (enemy_x, 20))

        # Instructions
        instructions = Text(
            "Souris: déplacer | Tir: automatique | ESC: menu",
            self.game.config.window_width // 2,
            self.game.config.window_height - 20,
            font_small,
            (100, 100, 100),
            center=True
        )
        instructions.draw(screen)

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
