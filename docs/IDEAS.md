# 💡 Idées et Améliorations Futures

## 🎯 Fonctionnalités à Implémenter

### Gameplay

- [ ] **Power-ups** qui apparaissent aléatoirement
  - Tir rapide (augmente la cadence)
  - Bouclier temporaire
  - Ralentissement du temps
  - Multi-tir (plus de projectiles)
  - Vie supplémentaire

- [ ] **Ennemis Boss** toutes les 5 vagues
  - Boss à la vague 5, 10, 15, 20
  - Patterns de tir spéciaux
  - Plus de HP et comportements uniques

- [ ] **Combo System**
  - Multiplicateur de score pour les kills rapides
  - Bonus pour tuer plusieurs ennemis sans être touché

- [ ] **Armes différentes**
  - Shotgun (plusieurs projectiles en éventail)
  - Laser (tir continu)
  - Missiles guidés
  - Grenades avec zone d'effet

### Progression

- [ ] **Système de niveau du joueur**
  - XP gagnée par vague
  - Améliorations permanentes (HP, vitesse, dégâts)
  - Arbre de compétences

- [ ] **Achievements**
  - Terminer vague 10 sans dégâts
  - Tuer 1000 ennemis totaux
  - Speedrun vague 5 en moins de 2 minutes
  - Marathon: vagues 1-20 sans pause

- [ ] **Leaderboard**
  - High scores par vague
  - Score total toutes vagues
  - Meilleur temps

### Variété

- [ ] **Nouveaux types d'ennemis**
  - Ennemis volants (plus rapides, moins de HP)
  - Tanks (très lents, beaucoup de HP)
  - Kamikazes (foncent sur le joueur)
  - Snipers (tirent depuis loin)

- [ ] **Modes de jeu**
  - Survival (combien de temps tu tiens)
  - Rush (tue X ennemis le plus vite possible)
  - Boss Rush (vagues 5, 10, 15, 20 enchaînées)
  - Hard Mode (2x ennemis, 0.5x HP joueur)

- [ ] **Environnements différents**
  - Forêt (thème actuel)
  - Ville (rues, immeubles)
  - Décharge (poubelles partout)
  - Nuit (visibilité réduite)

### Visuel & Audio

- [ ] **Effets visuels**
  - Flash lors des tirs
  - Traînées de projectiles
  - Screen shake lors des impacts
  - Particules améliorées

- [ ] **Sons**
  - Musique de fond (intensité augmente avec les vagues)
  - SFX pour tirs (joueur et ennemis)
  - SFX pour impacts et explosions
  - SFX pour menu et UI

- [ ] **Animations**
  - Animation de mort des ennemis
  - Animation d'apparition (spawn)
  - Animations de victoire/défaite

### UI/UX

- [ ] **Pause menu**
  - Continuer
  - Options
  - Quitter la vague

- [ ] **Statistiques détaillées**
  - Précision des tirs
  - Dégâts infligés/reçus
  - Temps de survie
  - Graphiques de progression

- [ ] **Tutoriel**
  - Première vague guidée
  - Tooltips explicatifs
  - Skip pour joueurs expérimentés

## 🔧 Améliorations Techniques

### Performance

- [ ] Object pooling pour projectiles et particules
- [ ] Optimisation du rendu (culling hors écran)
- [ ] Profiling et optimisation des hotspots

### Code

- [ ] Tests unitaires pour les systèmes critiques
- [ ] Refactoring du système de collision
- [ ] Documentation des fonctions principales

### Build

- [ ] Support desktop (PyInstaller pour Windows/Mac/Linux)
- [ ] Optimisation de la taille du build web
- [ ] CI/CD automatique (GitHub Actions)

## 🎨 Polish

- [ ] Particules customisées par type d'ennemi
- [ ] Camera shake proportionnel aux dégâts
- [ ] Feedback haptique (si contrôleur)
- [ ] Transitions entre vagues plus smooth
- [ ] Victory screen avec récap de stats

## 🌟 Idées Originales

### Mode "Ridiculously Overpowered"
- Après vague 20, débloquer un mode où le joueur a TOUTES les armes
- Tir automatique dans toutes les directions
- Projectiles qui rebondissent
- Écran rempli de particules et de chaos

### Mode Coopératif Local
- 2 joueurs sur le même écran
- Partage des kills et du score
- Revive system

### Secrets & Easter Eggs
- Code Konami pour débloquer quelque chose
- Navet doré rare qui donne bonus énorme
- Boss secret si conditions spéciales

## 📊 Priorités

### Court terme (pour la jam)
1. Finir les 20 vagues ✅
2. Sons basiques
3. Menu pause
4. Polish visuel

### Moyen terme (post-jam)
1. Power-ups
2. Boss fights
3. Nouveaux ennemis
4. Achievements

### Long terme (si le jeu décolle)
1. Mode coop
2. Leaderboard en ligne
3. DLC avec nouveaux contenus
4. Portage mobile
