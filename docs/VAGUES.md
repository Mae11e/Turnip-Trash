# 🌊 Système de Vagues

## Vue d'ensemble

Le jeu utilise un **système de vagues universel** qui génère dynamiquement la difficulté selon le numéro de la vague.

Un seul fichier gère toutes les vagues: [wave.py](../game/scenes/wave.py)

**🎮 20 vagues disponibles** avec progression automatique de la difficulté!

## 📊 Formules de Progression

### Nombre d'ennemis
```python
enemies_total = 9 * level
```
- Vague 1: 9 ennemis
- Vague 2: 18 ennemis
- Vague 5: 45 ennemis
- Vague 10: 90 ennemis
- Vague 20: 180 ennemis

### Ennemis simultanés maximum
```python
max_at_once = min(3 + level, 10)
```
- Vague 1: 4 ennemis max
- Vague 5: 8 ennemis max
- Vague 7+: 10 ennemis max (plafonné)

### Intervalle de spawn
```python
spawn_interval = max(1.0, 3.5 - (level * 0.2))
```
- Vague 1: 3.3 secondes
- Vague 10: 1.5 secondes
- Vague 13+: 1.0 seconde (minimum)

### Ratio Raccoons vs Poubelles
```python
raccoon_ratio = min(0.3 + (level * 0.05), 0.6)
```
- Vague 1: 30% raccoons, 70% poubelles
- Vague 6+: 60% raccoons (maximum)

### Multiplicateurs d'ennemis

**Points de vie:**
```python
health_multiplier = 1 + (level - 1) * 0.2
```
- Vague 1: x1.0 (Raccoon: 30 HP, Poubelle: 20 HP)
- Vague 5: x1.8 (Raccoon: 54 HP, Poubelle: 36 HP)
- Vague 20: x4.8 (Raccoon: 144 HP, Poubelle: 96 HP)

**Vitesse:**
```python
speed_multiplier = 1 + (level - 1) * 0.1
```
- Vague 1: x1.0 (Raccoon: 80, Poubelle: 60)
- Vague 20: x2.9 (Raccoon: 232, Poubelle: 174)

**Nombre de projectiles par tir:**
```python
projectiles_count = min(1 + (level // 5), 4)
```
- Vagues 1-4: 1 projectile
- Vagues 5-9: 2 projectiles
- Vagues 10-14: 3 projectiles
- Vagues 15-20: 4 projectiles

**Cadence de tir:**
```python
shoot_speed = max(1.0, 3.0 - (level * 0.15))
```
- Vague 1: Raccoon tire toutes les 2.85s
- Vague 14+: Minimum 1 seconde

## 🆕 Fonctionnalités Visuelles

### Barres de Vie
- Affichées au-dessus des ennemis quand ils perdent de la vie
- Couleur dynamique selon HP restant:
  - 🟢 Vert: > 60% HP
  - 🟡 Jaune: 30-60% HP
  - 🔴 Rouge: < 30% HP
- Bordure blanche pour meilleure visibilité

### Tirs Multiples
Les ennemis tirent plusieurs projectiles simultanément dans les vagues avancées, créant des patterns dangereux!

## 📈 Progression par Palier

### 🟢 Vagues 1-5 : Facile
**Apprentissage du jeu**

| Vague | Ennemis | Max Simul. | Raccoons | HP Multi | Description |
|-------|---------|------------|----------|----------|-------------|
| 1     | 9       | 4          | 30%      | x1.0     | Tutoriel - Introduction |
| 2     | 18      | 5          | 35%      | x1.2     | Premiers défis |
| 3     | 27      | 6          | 40%      | x1.4     | Plus d'ennemis |
| 4     | 36      | 7          | 45%      | x1.6     | Intensification |
| 5     | 45      | 8          | 50%      | x1.8     | Premier palier |

### 🟡 Vagues 6-10 : Moyen
**Difficulté croissante**

| Vague | Ennemis | Max Simul. | Raccoons | HP Multi | Description |
|-------|---------|------------|----------|----------|-------------|
| 6     | 54      | 9          | 55%      | x2.0     | Accélération |
| 7     | 63      | 10         | 60%      | x2.2     | Max simultanés atteint |
| 8     | 72      | 10         | 60%      | x2.4     | Pression continue |
| 9     | 81      | 10         | 60%      | x2.6     | Quasi-boss |
| 10    | 90      | 10         | 60%      | x2.8     | Palier majeur |

### 🟠 Vagues 11-15 : Difficile
**Combat intense**

| Vague | Ennemis | Max Simul. | Raccoons | HP Multi | Description |
|-------|---------|------------|----------|----------|-------------|
| 11    | 99      | 10         | 60%      | x3.0     | Cent ennemis approche |
| 12    | 108     | 10         | 60%      | x3.2     | Endurance testée |
| 13    | 117     | 10         | 60%      | x3.4     | Spawn minimum (1s) |
| 14    | 126     | 10         | 60%      | x3.6     | Chaos organisé |
| 15    | 135     | 10         | 60%      | x3.8     | Palier expert |

### 🔴 Vagues 16-20 : Extrême
**Pour les maîtres**

| Vague | Ennemis | Max Simul. | Raccoons | HP Multi | Description |
|-------|---------|------------|----------|----------|-------------|
| 16    | 144     | 10         | 60%      | x4.0     | Au-delà de l'extrême |
| 17    | 153     | 10         | 60%      | x4.2     | Presque impossible |
| 18    | 162     | 10         | 60%      | x4.4     | Survie pure |
| 19    | 171     | 10         | 60%      | x4.6     | Avant la fin |
| 20    | 180     | 10         | 60%      | x4.8     | **DÉFI ULTIME** |

## 📊 Vague 1 vs Vague 20

| Métrique | Vague 1 | Vague 20 | Multiplication |
|----------|---------|----------|----------------|
| Ennemis totaux | 9 | 180 | x20 |
| Ennemis simultanés | 4 | 10 | x2.5 |
| HP Raccoon | 30 | 144 | x4.8 |
| Vitesse Raccoon | 80 | 232 | x2.9 |
| Projectiles/Tir | 1 | 4 | x4 |
| Intervalle Tir | 2.85s | 0.85s | /3.35 |
| **Dégâts/sec potentiel** | ~2 | ~20+ | **x10+** |

## 🎮 Conseils de Gameplay

### Vagues 1-5 (Facile)
- Apprends les mécaniques
- Pratique le mouvement avec la souris
- Habitue-toi au tir aléatoire

### Vagues 6-10 (Moyen)
- Reste mobile constamment
- Gère les vagues de projectiles ennemis
- Utilise tout l'espace de l'écran

### Vagues 11-15 (Difficile)
- Anticipe les spawns
- Optimise tes déplacements
- Ne te laisse pas encercler
- Utilise les barres de vie pour prioriser les cibles

### Vagues 16-20 (Extrême)
- Maîtrise parfaite requise
- Connais les patterns d'ennemis
- Concentration maximale
- 4 projectiles par ennemi = esquive constante
- Bonne chance! 🍀

## 🔧 Personnalisation

### Modifier les formules

Édite [wave.py](../game/scenes/wave.py), fonction `get_wave_config()`:

```python
def get_wave_config(level):
    return {
        'enemies_total': 9 * level,  # Modifie ici
        'max_at_once': min(3 + level, 10),
        'enemy_projectiles_count': min(1 + (level // 5), 4),
        # ... etc
    }
```

### Créer une vague boss

Tu peux ajouter des cas spéciaux:

```python
def get_wave_config(level):
    config = {
        # ... config par défaut
    }

    # Boss à la vague 10
    if level == 10:
        config['enemies_total'] = 1
        config['enemy_health_multiplier'] = 20
        config['enemy_projectiles_count'] = 8

    return config
```

### Ajouter plus de vagues

Dans [main.py](../game/main.py), ligne 114:

```python
for i in range(1, 31):  # 30 vagues au lieu de 20
    self.scene_manager.add_scene(f'wave{i}', WaveScene(self, wave_number=i))
```

N'oublie pas de mettre à jour [wave_selection.py](../game/scenes/wave_selection.py) aussi!

## 🐛 Debug

Pour tester une vague spécifique rapidement:

```python
# Dans main.py, change la scène de départ
self.scene_manager.change_scene('wave15')  # Lance directement la vague 15
```

## 🎯 Avantages du Système

- ✅ **Un seul fichier** à maintenir
- ✅ **Progression automatique** de la difficulté
- ✅ **Facilement personnalisable** avec des formules simples
- ✅ **Extensible** pour autant de vagues que nécessaire
- ✅ **Testable** facilement (change juste le numéro)
