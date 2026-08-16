# Kynex — TODO

> Feuille de route du projet.
> Cette liste évolue au fur et à mesure du développement.

---

## 📷 Phase 0 — Hand Tracking

### 0.1 — Mise en place
- [ ] Vérifier la webcam
- [ ] Créer l'environnement Python
- [ ] Installer OpenCV
- [ ] Installer le framework de hand tracking
- [ ] Tester la détection d'une main

### 0.2 — Landmarks
- [ ] Récupérer les 21 landmarks de la main
- [ ] Identifier chaque landmark
- [ ] Afficher les coordonnées X/Y/Z dans le terminal
- [ ] Tester la stabilité des coordonnées
- [ ] Tester la détection avec différentes positions de main
- [ ] Tester la profondeur Z

### 0.3 — Calcul des mouvements
- [ ] Calculer l'angle MCP
- [ ] Calculer l'angle latéral MCP
- [ ] Calculer l'angle PIP
- [ ] Calculer l'angle DIP
- [ ] Calculer les mouvements du pouce
- [ ] Définir les limites des mouvements
- [ ] Afficher les angles dans le terminal

### 0.4 — Abstraction du tracking
- [ ] Créer une structure représentant l'état de la main
- [ ] Séparer le tracking du calcul des angles
- [ ] Créer une représentation indépendante du hardware
- [ ] Préparer le futur mapping humain → robot

---

## 🦾 Phase 1 — Architecture mécanique

- [ ] Définir l'architecture d'un doigt
- [ ] Utiliser l'index comme doigt de référence
- [ ] Définir l'articulation MCP
- [ ] Définir le mouvement latéral du MCP
- [ ] Définir l'articulation PIP
- [ ] Concevoir la transmission PIP → DIP
- [ ] Définir le système de retour du doigt
- [ ] Définir les butées mécaniques
- [ ] Définir les axes
- [ ] Définir l'emplacement des moteurs
- [ ] Vérifier les contraintes mécaniques
- [ ] Vérifier que l'architecture est adaptable aux autres doigts

---

## 📐 Phase 2 — Schéma 2D

- [ ] Faire le schéma 2D de l'index
- [ ] Vue de côté
- [ ] Vue de dessus
- [ ] Ajouter les articulations
- [ ] Ajouter les axes
- [ ] Ajouter les moteurs
- [ ] Ajouter les tendons
- [ ] Ajouter la transmission PIP → DIP
- [ ] Ajouter les dimensions
- [ ] Ajouter les limites de mouvement
- [ ] Valider l'architecture

---

## 🧩 Phase 3 — Modélisation 3D

- [ ] Choisir la méthode de modélisation
- [ ] Modéliser la première phalange
- [ ] Modéliser la deuxième phalange
- [ ] Modéliser la troisième phalange
- [ ] Modéliser les articulations
- [ ] Modéliser le MCP à deux axes
- [ ] Modéliser la transmission DIP
- [ ] Prévoir les passages des tendons
- [ ] Prévoir les logements des axes
- [ ] Modéliser la paume
- [ ] Vérifier les assemblages
- [ ] Vérifier les collisions
- [ ] Préparer les fichiers pour impression

---

## 🧪 Phase 4 — Simulation

- [ ] Rechercher un logiciel de simulation adapté
- [ ] Importer le modèle
- [ ] Tester les mouvements
- [ ] Vérifier les collisions
- [ ] Vérifier les amplitudes
- [ ] Vérifier la transmission PIP → DIP
- [ ] Identifier les points de blocage
- [ ] Modifier le modèle si nécessaire

---

## 🔌 Phase 5 — Composants

- [ ] Identifier le filament disponible
- [ ] Choisir le matériau d'impression
- [ ] Choisir les servomoteurs
- [ ] Choisir le contrôleur PWM
- [ ] Choisir les axes
- [ ] Choisir les tendons
- [ ] Choisir les guides de tendon
- [ ] Choisir les ressorts
- [ ] Choisir l'alimentation
- [ ] Définir le câblage
- [ ] Vérifier la consommation électrique
- [ ] Commander les composants validés

---

## 🖨️ Phase 6 — Premier doigt

- [ ] Imprimer un premier prototype
- [ ] Tester les pièces individuellement
- [ ] Tester les axes
- [ ] Tester les articulations
- [ ] Tester les tendons
- [ ] Tester les ressorts
- [ ] Tester les servos
- [ ] Tester le MCP
- [ ] Tester le PIP
- [ ] Tester le DIP
- [ ] Tester le mouvement latéral
- [ ] Vérifier les blocages
- [ ] Modifier et réimprimer si nécessaire

---

## ⚡ Phase 7 — Firmware

- [ ] Définir l'architecture du firmware
- [ ] Créer le projet C pour Raspberry Pi Pico
- [ ] Tester la communication USB
- [ ] Définir le protocole de communication
- [ ] Implémenter la réception des commandes
- [ ] Implémenter le contrôle PWM
- [ ] Contrôler un servo
- [ ] Contrôler plusieurs servos
- [ ] Ajouter les limites de sécurité
- [ ] Tester le firmware indépendamment du tracking

---

## 🔗 Phase 8 — Python → Pico

- [ ] Connecter Python au Pico
- [ ] Envoyer une commande simple
- [ ] Recevoir la commande côté Pico
- [ ] Commander un servo depuis Python
- [ ] Commander plusieurs servos
- [ ] Définir le format des paquets
- [ ] Envoyer tous les angles dans un paquet
- [ ] Ajouter la calibration
- [ ] Connecter le hand tracking au protocole
- [ ] Tester :

      Caméra → Python → Pico → Servo

---

## 🖐️ Phase 9 — Main complète

- [ ] Concevoir la paume
- [ ] Intégrer l'index
- [ ] Tester l'index sur la paume
- [ ] Adapter l'architecture au majeur
- [ ] Tester le majeur
- [ ] Intégrer le majeur
- [ ] Adapter l'architecture à l'annulaire
- [ ] Tester l'annulaire
- [ ] Intégrer l'annulaire
- [ ] Adapter l'architecture à l'auriculaire
- [ ] Tester l'auriculaire
- [ ] Intégrer l'auriculaire
- [ ] Concevoir le pouce
- [ ] Tester le pouce
- [ ] Intégrer le pouce
- [ ] Tester la main complète

---

## 🧵 Phase 10 — Finition

- [ ] Organiser le câblage
- [ ] Installer les caches
- [ ] Installer le tissu noir
- [ ] Vérifier que le tissu ne gêne aucun mouvement
- [ ] Vérifier les tendons
- [ ] Ajouter les protections mécaniques
- [ ] Vérifier les butées
- [ ] Vérifier la sécurité électrique
- [ ] Tester la main sur une longue durée

---

## 🔋 Phase 11 — Autonomie

> Optionnel — à faire une fois le système fonctionnel.

- [ ] Déplacer le programme Python sur Raspberry Pi 5
- [ ] Connecter la caméra au Raspberry Pi
- [ ] Connecter le Raspberry Pi au Pico
- [ ] Ajouter une batterie
- [ ] Gérer l'alimentation de l'ensemble
- [ ] Rendre le système autonome

---

## 🚀 Phase 12 — Améliorations futures

- [ ] Améliorer la précision du hand tracking
- [ ] Améliorer la fluidité des mouvements
- [ ] Ajouter une interpolation des mouvements
- [ ] Ajouter une compensation de latence
- [ ] Améliorer la calibration
- [ ] Ajouter une détection des erreurs mécaniques
- [ ] Étudier le suivi du bras
- [ ] Étudier une extension vers un bras robotique complet