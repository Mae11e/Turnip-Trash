# Idées de Jeu - Mini Jam 202

## Thème : Power-up | Limitation : Ridiculously Overpowered

---

## Brainstorming

### Interprétations possibles de "Ridiculously Overpowered"

- Un personnage qui devient absurdement puissant
- Des power-ups qui rendent le jeu "cassé" volontairement
- Ennemi/boss ridiculement surpuissant
- Escalade absurde de puissance
- Le joueur commence OP et doit gérer ce pouvoir
- Satire des jeux P2W / power creep

---

## Idées de jeu

### Idée 1 : Shooter Arena / Survival
**Genre** : Top-down ou Twin-stick shooter
**Concept** : Survivre à des vagues d'ennemis qui arrivent de tous côtés
**Lien avec la limitation** : Power-ups qui rendent le joueur absurdement OP

---

## Idée retenue : Shooter Arena "Ridiculously Overpowered"

**Pitch** : Shooter top-down où le joueur affronte des vagues d'ennemis. De temps en temps, un **mini-boss ultra puissant** apparaît. En le tuant, il drop un **power-up complètement broken** qui rend le joueur ridiculement overpowered.

### Concept Core
- **Vue** : Top-down
- **Contrôles** : Le joueur suit la souris + tir automatique
- **Ennemis normaux** : vagues continues, faciles
- **Mini-boss OP** : apparaît périodiquement, très dangereux
- **Power-ups broken** : droppés par les mini-boss, effets absurdes et cumulatifs

### Loop de gameplay
1. Survivre aux vagues d'ennemis normaux
2. Ennemis drop des **gems** → collecter pour XP
3. Au niveau suivant → **choix d'upgrade** (stats)
4. Mini-boss arrive → challenge intense
5. Tuer le mini-boss → **power-up broken** (effet spécial)
6. Devenir de plus en plus OP
7. Répéter jusqu'à la mort

### Deux systèmes de progression

**1. Gems / XP (ennemis normaux)**
- Ennemis drop des gems à leur mort
- Le joueur les ramasse en passant dessus
- Barre d'XP → level up → choix d'upgrade

**2. Power-ups Broken (mini-boss)**
- Effet spécial unique et surpuissant
- Se stacke avec les autres power-ups
- Rend le joueur "ridiculously overpowered"

**3. Pickups (spawn aléatoire)**
- **Bouclier** : Absorbe X dégâts (spawn au hasard sur la map)
- Potentiellement d'autres pickups : heal, magnet (attire gems), etc.

---

## Upgrades (via Gems/XP)

| Upgrade | Effet | Max level |
|---------|-------|-----------|
| **Fire Rate** | Vitesse de tir | +10% par level |
| **Move Speed** | Vitesse de déplacement | +10% par level |
| **Projectiles** | Nombre de projectiles | +1 par level |
| **Damage** | Dégâts par projectile | +15% par level |
| **Max HP** | Points de vie max | +20 par level |
| **Pickup Range** | Rayon de collecte gems | +20% par level |
| **Crit Chance** | Chance de coup critique | +5% par level |

> À chaque level up, le joueur choisit 1 upgrade parmi 3 proposées aléatoirement

---

## Idées de Power-ups Broken (Mini-boss)

| Power-up | Effet | Niveau de broken |
|----------|-------|------------------|
| **Multishot** | Tire dans toutes les directions | Stack: +8 projectiles |
| **Laser Beam** | Rayon qui traverse tout | Stack: +1 rayon |
| **Explosion** | Projectiles explosent à l'impact | Stack: +rayon explosion |
| **Homing** | Projectiles auto-guidés | Stack: meilleur tracking |
| **Time Slow** | Ralentit le temps (sauf joueur) | Stack: +lent |
| **Giant** | Projectiles énormes | Stack: +taille |
| **Ricochet** | Rebondit sur les murs/ennemis | Stack: +rebonds |
| **Vampiric** | Vol de vie sur hit | Stack: +% vol |
| **Nuclear** | Explosion géante toutes les X sec | Stack: -cooldown |

## Idées de Mini-boss OP

| Mini-boss | Attaque signature | Difficulté |
|-----------|-------------------|------------|
| **Tank** | Charge brutale, très tanky | Endurance |
| **Sniper** | Tirs précis ultra rapides | Esquive |
| **Summoner** | Spawn des hordes d'ennemis | Overwhelm |
| **Berserker** | Devient plus fort quand blessé | DPS race |
| **Teleporter** | Se téléporte partout | Imprévisible |

---

## Tech Stack
- **Moteur** : Pygame (template existante)
- **Langage** : Python 3.12
- **Art** : Formes géométriques / Minimaliste (rapide à faire)
- **Son** : À voir (sfxr, bfxr pour les effets)

---

## Notes
- Inspiration : Vampire Survivors, Brotato, Nuclear Throne, Enter the Gungeon
- La template a déjà : player, enemy, projectiles, particles, collision, scenes
