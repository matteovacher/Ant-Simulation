# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Contrainte : ce fichier ne doit contenir QUE des caracteres disponibles sur un clavier classique.
Aucun emoji, aucun caractere special Unicode.

---

## 1. Objectif
Simulation d'une colonie de fourmis (SMA) en Python.
L'intelligence collective doit emerger de comportements individuels bio-inspires.

## 2. Vision Neuronale (architecture centrale)
La colonie est representee par un grand reseau de neurones.
Ce grand reseau contient un unique sous-reseau, duplique autant de fois
qu'il y a de fourmis dans la colonie.

Regles fondamentales :
- Toutes les fourmis partagent exactement les memes poids (meme sous-reseau)
- Ce qui differencie le comportement de chaque fourmi : ses entrees perceptives
  (position, pheromones detectees, obstacles, nourriture...)
- Le meme reseau produit des comportements differents car les entrees sont differentes
- C'est CE sous-reseau unique qui est evolue par l'algorithme genetique

Algorithme genetique retenu : MAP-Elites
Dimensions comportementales : a definir lors de l'Etape 4

Reference scientifique cle :
- Crosscombe et al. (2024), "A Simulation Environment for the Neuroevolution
  of Ant Colony Dynamics", ALIFE 2024. arXiv:2406.13147

## 3. Role de Claude
- JAMAIS de code complet non sollicite
- Progression par etapes -> indices -> pseudocode -> solution si demande explicite
- Mot-cle de deverrouillage : "Donne-moi la solution"
- Source de verite scientifique : context/research_notes.md (prioritaire) + connaissances internes
- Proposer une mise a jour de context/master_prompt.md apres chaque decision technique validee
  (choix de bibliotheque, architecture, parametres, contraintes machines...)
- Proposer une mise a jour apres chaque etape cochee dans l'Etat d'Avancement

### Regard critique systematique
- A chaque relecture de fichier ou audit de code : signaler TOUS les problemes detectes,
  meme mineurs (nommage, couplage, incoherence avec CLAUDE.md, bug latent, dette technique)
- Ne jamais valider un code par defaut ou par politesse
- Si une decision technique est sous-optimale, le dire explicitement avec la raison
- Distinguer clairement : bug bloquant / comportement incorrect / dette technique / style
- Ne pas attendre qu'un bug soit signale par l'utilisateur pour le mentionner

## 4. Contexte Materiel
Appareil    : Microsoft Surface Pro 9
Processeur  : Intel Core i5-1235U 12e gen (2.50 GHz, 10 coeurs)
RAM         : 16 Go (15.8 Go utilisable), partagee entre CPU et GPU
GPU         : Intel Iris Xe Graphics (integre, memoire partagee avec la RAM)
OS          : Windows 11 64 bits
IDE         : Visual Studio Code

Contraintes :
- Pas de CUDA (pas de GPU Nvidia) -> PyTorch tourne en mode CPU
- Le GPU Intel Xe est accessible via Intel Extension for PyTorch (IPEX)
  mais complexe a configurer -> approche CPU-first retenue pour l'instant
- Privilegier le batching NumPy/PyTorch plutot que le parallelisme GPU
- Memoire partagee CPU/GPU : surveiller la consommation RAM en simulation

## 5. Architecture (fichiers existants uniquement)
Ant-Liquid-Brain-AI/
|-- main.py                  # Boucle principale : Init -> Update -> Render
|-- config.py                # Parametres globaux (constantes, jamais hardcodes)
|-- core/
|   |-- pheromone_grid.py    # Grille pheromones (2, H, W) : evaporation + diffusion
|   |-- environment.py       # [LEGACY] ancienne version : orchestration + rendu melanges, conserve pour reference
|   |-- environment_bis.py   # Orchestrateur pur : step() sans rendu, remplace environment.py
|   |-- renderer.py          # Rendu pur : construit la surface numpy depuis l'etat de l'environnement
|   |-- nest.py              # Position du nid, validation des bornes
|   |-- ant.py               # Agent fourmi : mouvement, depot pheromones, antennes
|   |-- food_source.py       # Source de nourriture : type, position, quantite, recharge
|   |-- food_grid.py         # Grille nourriture (N_FOOD_TYPES, H, W) + liste FoodSource
|-- context/
|   |-- master_prompt.md     # Contexte du projet (source de verite)
|   |-- research_notes.md    # Notes scientifiques
|-- tests/
|   |-- tests_pheromones.py  # Test interactif souris : depot HOME/FOOD, rendu pygame
|   |-- tests_food.py        # Test interactif souris : depot APHID/SUGAR, rendu pygame
|-- requirements.txt         # Bibliotheques du projet

Note : l'arborescence sera mise a jour uniquement quand un fichier
est effectivement cree, sur instruction explicite.

## 6. Environnement Technique
Gestionnaire : Conda

Bibliotheques validees (Etape 0) :
- pygame          # Rendu visuel, boucle de jeu
- numpy           # Grille pheromones, calculs vectorises
- torch           # Sous-reseau neuronal, batching CPU
- scipy           # Diffusion gaussienne pheromones
- matplotlib      # Courbes evolution GA (optionnel)

```bash
# Lancer la simulation principale
python main.py

# Lancer le test interactif de la grille de pheromones (souris)
python tests/tests_pheromones.py
```

## 7. Conventions de Nommage
- Classes    : PascalCase        -> Ant, Colony, PheromoneGrid
- Methodes   : snake_case        -> update_pheromones(), decay_rate
- Constantes : SCREAMING_SNAKE   -> MAX_ANTS, EVAPORATION_RATE
- Fichiers   : snake_case        -> ant.py, pheromone_grid.py

## 8. Gestion des Erreurs
- Toute fonction publique gere ses cas limites (hors-bounds, colonie vide...)
- Pas d'exceptions silencieuses : log ou raise explicite
- Les parametres biologiques ne doivent jamais etre hardcodes (config.py)

## 9. Decisions Techniques Validees (Etape 1)

### Grille de pheromones
- Structure : np.zeros((2, GRID_HEIGHT, GRID_WIDTH))
- Deux types : HOME = 0 (fourmis quittant le nid), FOOD = 1 (fourmis portant de la nourriture)
- Evaporation : modele cinetique du premier ordre (Edelstein-Keshet et al. 1995)
  -> discretise en C_{t+1} = C_t * EVAPORATION_RATE
  -> implementee comme self.grids *= EVAPORATION_RATE (une seule multiplication)
- Diffusion : filtre gaussien scipy (solution exacte de la PDE de diffusion lineaire)
  -> axes=(1,2) obligatoire pour ne pas melanger HOME et FOOD
  -> parametre DIFFUSION_SIGMA a calibrer empiriquement
- Seuil de nettoyage : valeurs < 1e-4 mises a zero pour eviter accumulation numerique
- Ordre des operations : evaporation -> diffusion -> depot

### Nid (Nest)
- Classe Nest : position (x, y) + validation des bornes (raise ValueError si hors grille)
- Rayon du nid : NEST_RADIUS (config.py)
- Rendu : masque circulaire vectorise via np.ogrid

### Environnement (Environment)
- Agregat de PheromoneGrid et Nest
- Rendu pheromones : logique dominant (HOME vs FOOD) -> RGB vectorise, transposition
  pour pygame (numpy indexe (y,x), pygame attend (x,y))
- Rendu nid : surface separee superposee aux pheromones

## 10. Decisions Techniques Validees (Etape 2)

### Agent Fourmi (Ant)
- Direction : angle flottant self.direction dans [0, 2*pi]
  -> deplacement : dx = cos(theta), dy = sin(theta) (vitesse = 1 case/pas, dt = 1)
  -> pas de direction discrete (evite les if/elif pour 8 directions)
- Mouvement : move(delta_theta, put_pheromones, value_pheromone)
  -> delta_theta est passe en parametre = placeholder pour la sortie du reseau (Etape 4)
  -> marche aleatoire actuelle : delta_theta ~ U(-pi/6, pi/6)
- Rebond mural : reflexion trigonometrique (pas de boucle while, pas de direction aleatoire)
  -> mur vertical (x hors bornes)   : theta = pi - theta (inverse cos, conserve sin)
  -> mur horizontal (y hors bornes) : theta = -theta     (inverse sin, conserve cos)
  -> detection : new_x != x_clipped ou new_y != y_clipped apres np.clip
- Depot de pheromones : toujours actif, type selon has_food
  -> has_food = True  -> PheromoneGrid.FOOD
  -> has_food = False -> PheromoneGrid.HOME
  -> put_pheromones en parametre pour compatibilite future avec sortie reseau
- Antennes : deux positions calculees a la volee dans get_antenna_pos()
  -> antenne gauche : (x + cos(theta + ANGLE_ANTENNA), y + sin(theta + ANGLE_ANTENNA))
  -> antenne droite : (x + cos(theta - ANGLE_ANTENNA), y + sin(theta - ANGLE_ANTENNA))
  -> ANGLE_ANTENNA = pi/4 (config.py)
- Position stockee en float -> int() pour indexer la grille (une fourmi peut ne pas avancer d'une case entiere par pas)

### Config ajoutee (Etape 2)
- N_ANTS = 10           # nombre de fourmis
- ANGLE_ANTENNA = pi/4  # demi-angle entre les deux antennes
- COLOR_ANT = (255, 165, 0)  # orange

### Rendu dans main.py
- Ordre de calques : pheromones -> fourmis -> nid
- Les fourmis disparaissent visuellement dans le nid (nid dessine par-dessus)
- env_surface[int(ant.y), int(ant.x)] = COLOR_ANT

## 11. Decisions Techniques Validees (Etape 2 - suite : Nourriture)

### Sources de nourriture (FoodSource)
- Deux types : APHID = 0 (pucerons, en bancs, se rechargent), SUGAR = 1 (ponctuel, recharge_rate=0.0)
- Quantite normalisee dans ]0, 1] (raise ValueError sinon) -> mapping direct vers intensite RGB
- recharge() : quantity = min(quantity + recharge_rate, 1.0)
- consume(amount) : retourne ce qui a vraiment ete pris (min(quantity, amount))
- max_quantity = 1 systematiquement

### Grille nourriture (FoodGrid)
- Structure : np.zeros((N_FOOD_TYPES, GRID_HEIGHT, GRID_WIDTH))
- _build_grid() : remplit la grille depuis la liste de FoodSource
- update() : recharge() chaque source + met a jour la case correspondante
- get_food_surface() : logique dominante aphid/sugar -> RGB, intensite proportionnelle a quantity
- Rendu : COLOR_APHID = (255, 220, 0), COLOR_SUGAR = (100, 200, 255)

### Integration dans Environment
- Environment devient agregat de PheromoneGrid + Nest + FoodGrid
- update_environnement() appelle food_grid.update()
- get_food_surface() delegue a food_grid.get_food_surface()

### Depot interactif (tests/tests_food, implemente)
- Clic gauche souris : poser une source APHID a la position du curseur
- Clic droit souris  : poser une source SUGAR a la position du curseur
- Les pucerons ont un recharge_rate > 0, le sucre a recharge_rate = 0.0
- Integration dans main.py : terminee (mouse_brush(food_grid), env.step() + renderer.render(env))

### Bugs corriges (Etape 2b)
- eating_timer declenche meme si taken == 0 (source epuisee) : fourmi bloquee indefiniment
  -> Fix : eating_timer = EAT_DURATION uniquement si taken > 0 (ant.py:interact)
- RANDOM_DIR = np.pi/8j dans config.py : le suffixe j crée un complexe en Python
  -> Fix : RANDOM_DIR = np.pi/8

### Config ajoutee
- N_FOOD_TYPES = 2
- COLOR_APHID = (255, 220, 0)
- COLOR_SUGAR = (100, 200, 255)

## 12. Decisions Techniques Validees (Etape 3)

### Suivi de traces par gradient differentiel
- Regle hand-crafted : delta_theta = ANTENNA_WEIGHT * (C_gauche - C_droite) + bruit_uniforme
- Type de pheromone selon etat :
  -> food_carried > TRESHOLD_FOOD : deposite FOOD, suit HOME (rentre au nid)
  -> food_carried <= TRESHOLD_FOOD : deposite HOME, suit FOOD (cherche nourriture)
- Bug corrige : ancien code utilisait le meme p_type pour depot et suivi
  -> Correction : deux variables separees p_type_deposit et p_type_follow dans environment_bis.py
- Modele antennes corrige : les antennes partent de la tete, pas du centre
  -> get_antenna_pos() : position = (x + HALF_LENGTH_BODY*cos(theta) + L*cos(theta +/- alpha), ...)
  -> HALF_LENGTH_BODY = 0.5 ajoute dans config.py
- Demi-tour a la source : declenche dans move() au dernier step de gel (eating_timer == 1)
  -> self.direction += np.pi au moment ou eating_timer passe de 2 a 1

### Affichage multi-modes (a implementer)
- Deux touches pour naviguer entre 3 modes d'affichage, fenetre toujours de taille fixe :
  -> Touche "f" : display_mode = (display_mode - 1) % 3
  -> Touche "j" : display_mode = (display_mode + 1) % 3
  -> Mode 0 : HOME uniquement (brun)
  -> Mode 1 : FOOD uniquement (vert)
  -> Mode 2 : dominant (mode actuel, max des deux par case)
- Variable display_mode dans main.py

### Calibration parametres (observations Step 3)
- EVAPORATION_RATE 0.997 -> 0.999 (demi-vie ~693 steps, traces plus persistantes)
- N_ANTS 20 -> 50 (densite plus forte, meilleur renforcement des traces)
- PHEROMONE_DEPOSIT 0.7 -> 0.8
- NEST_RADIUS augmente pour faciliter retour au nid
- ANTENNA_WEIGHT np.pi/3 -> np.pi/6 (biais max reduit, suivi plus fluide)
- RANDOM_DIR np.pi/8 -> np.pi/10

## 13. Etat d'Avancement
- [x] Etape 0 : Environnement & bibliotheques
- [x] Etape 1 : Grille & pheromones
- [x] Etape 2a : Agent Fourmi (ant.py : mouvement, rebond, depot pheromones, antennes)
- [x] Etape 2b : Nourriture (FoodSource + FoodGrid + tests_food + integration Environment
                 + rendu main.py + compteur food_collected + bugs corriges)
- [x] Etape 3 : Colonie & emergence (suivi de traces par gradient differentiel, calibration parametres)
- [ ] Etape 4 : Algorithmes Genetiques (MAP-Elites)

## 14. Communication & Documentation
Site web personnel : matteovacher.github.io (Hugo)
-> Apres chaque etape validee, proposer un resume brut
   que Matteo reformulera avant publication
-> Le resume doit etre clair, sans jargon excessif
-> Conserver une coherence entre le vocabulaire du code
   et celui utilise dans les articles

Articles publies :
- Etape 1 : "Step 1 of Ant Simulation Project : Pheromones"
- Etape 2 : "Step 2 of Ant Simulation Project : Ant Agent" (brouillon nourriture redige, a publier)
- Etape 3 : "Step 3 of Ant Simulation Project : Colony and Emergence" (brouillon en cours, draft = true)

## 15. Profil Developpeur
Formation   : Supaero 2e annee (M1), apres MPSI/PSI* (Saint-Louis)
Niveau      : Bon en algorithmique et mathematiques
Langages    : Java (POO maitrisee), Python (algorithmique uniquement en prepa,
              pas d'experience en POO Python)
Point faible : Architecture systeme (conception modulaire, decoupage responsabilites)
-> Expliquer les specificites de la POO Python par rapport a Java quand necessaire
   (syntaxe, conventions, __init__, self, proprietes, etc.)
-> Privilegier les explications d'architecture avec schemas et analogies
-> Pas besoin de rappeler les bases algorithmiques
