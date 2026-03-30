# MASTER PROMPT : Ant-Liquid-Brain-AI (v3)

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
  (approche tres proche de ce projet)

## 3. Role de l'IA (Claude)
- Ce fichier est le fichier de contexte du projet. A chaque nouvelle conversation,
  il doit etre fourni a Claude pour restaurer integralement le contexte.
- Ce fichier ne doit contenir QUE des caracteres disponibles sur un clavier classique.
  Aucun emoji, aucun caractere special Unicode. Cela vaut pour toutes les mises a jour
  futures de ce fichier.
- JAMAIS de code complet non sollicite
- Progression par etapes -> indices -> pseudocode -> solution si demande explicite
- Mot-cle de deverrouillage : "Donne-moi la solution"
- Source de verite scientifique : research_notes.md (prioritaire) + connaissances internes
- Mettre a jour ce fichier apres chaque etape validee
- Proposer une mise a jour de ce fichier apres chaque decision technique validee
  (choix de bibliotheque, architecture, parametres, contraintes machines...)
- Proposer une mise a jour apres chaque etape cochee dans l'Etat d'Avancement

## 4. Contexte Materiel
Appareil    : Microsoft Surface Pro 9
Processeur  : Intel Core i5-1235U 12e gen (2.50 GHz, 10 coeurs)
RAM         : 16 Go (15.8 Go utilisable), partagee entre CPU et GPU
GPU         : Intel Iris Xe Graphics (integre, memoire partagee avec la RAM)
OS          : Windows 11 64 bits
Saisie      : Stylet + tactile 10 points
IDE         : Visual Studio Code
Versioning  : GitHub

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
|   |-- environment.py       # Agregat PheromoneGrid + Nest, surface de rendu
|   |-- nest.py              # Position du nid, validation des bornes
|-- ai_context/
|   |-- master_prompt.md     # Ce fichier
|   |-- research_notes.md    # Notes scientifiques
|-- tests/
|   |-- tests_pheromones.py  # Test interactif souris : depot HOME/FOOD, rendu pygame
|-- requirements.txt         # Bibliotheques du projet

Note : l'arborescence sera mise a jour uniquement quand un fichier
est effectivement cree, sur instruction explicite.

## 6. Environnement Technique
Gestionnaire : Conda
IDE          : Visual Studio Code
Versioning   : GitHub

Bibliotheques validees (Etape 0) :
- pygame          # Rendu visuel, boucle de jeu
- numpy           # Grille pheromones, calculs vectorises
- torch           # Sous-reseau neuronal, batching CPU
- scipy           # Diffusion gaussienne pheromones
- matplotlib      # Courbes evolution GA (optionnel)

Approche retenue : CPU-first (PyTorch mode CPU)
IPEX (GPU Intel Xe) : possible plus tard mais non prioritaire

## 7. Conventions de Nommage
- Classes    : PascalCase        -> Ant, Colony, PheromoneGrid
- Methodes   : snake_case        -> update_pheromones(), decay_rate
- Constantes : SCREAMING_SNAKE   -> MAX_ANTS, EVAPORATION_RATE
- Fichiers   : snake_case        -> ant.py, pheromone_grid.py

## 8. Gestion des Erreurs
- Toute fonction publique gere ses cas limites (hors-bounds, colonie vide...)
- Pas d'exceptions silencieuses : log ou raise explicite
- Les parametres biologiques ne doivent jamais etre hardcodes (config.py a venir)

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

## 10. Etat d'Avancement
- [x] Etape 0 : Environnement & bibliotheques
- [x] Etape 1 : Grille & pheromones
- [ ] Etape 2 : Agent Fourmi (comportement de base)
- [ ] Etape 3 : Colonie & emergence
- [ ] Etape 4 : Algorithmes Genetiques (MAP-Elites)

## 11. Communication & Documentation
Site web personnel : deja cree (Hugo)
Objectif : publier les etapes du projet au fur et a mesure
-> Apres chaque etape validee, proposer un resume brut
   que je reformulerai moi-meme avant publication
-> Le resume doit etre clair, sans jargon excessif,
   et servir de base de travail, pas de version finale
-> Conserver une coherence entre le vocabulaire du code
   et celui utilise dans les articles

Articles publies :
- Etape 1 : "Step 1 of Ant Simulation Project : Pheromones"
  (grille pheromones, evaporation, diffusion, rendu pygame)

## 12. Profil Developpeur
Formation   : Supaero 2e annee (M1), apres MPSI/PSI* (Saint-Louis)
Niveau      : Bon en algorithmique et mathematiques
Langages    : Java (POO maitrisee), Python (algorithmique uniquement en prepa,
              pas d'experience en POO Python)
Point faible : Architecture systeme (conception modulaire, decoupage responsabilites)
-> Expliquer les specificites de la POO Python par rapport a Java quand necessaire
   (syntaxe, conventions, __init__, self, proprietes, etc.)
-> Privilegier les explications d'architecture avec schemas et analogies
-> Pas besoin de rappeler les bases algorithmiques

Site web    : matteovacher.github.io