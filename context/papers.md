# Papiers

# RESEARCH NOTES : Ant-Liquid-Brain-AI

Fichier de reference scientifique du projet.
Prioritaire sur les connaissances internes de Claude.
A completer au fur et a mesure des lectures.

Format des notes par papier :
  [LU] = lu en entier
  [PARTIEL] = abstract + sections cles
  [A LIRE] = identifie, non lu

---

## THEME 1 : Reference centrale du projet

### [A LIRE] Crosscombe et al. (2024)
**Titre** : A Simulation Environment for the Neuroevolution of Ant Colony Dynamics
**Auteurs** : Michael Crosscombe, Ilya Horiguchi, Norihiro Maruyama, Shigeto Dobata, Takashi Ikegami
**Publication** : ALIFE 2024 (Proceedings of the 2024 Artificial Life Conference), p. 92
**DOI** : https://doi.org/10.1162/isal_a_00713
**arXiv** : https://arxiv.org/abs/2406.13147

**Pourquoi lire ce papier en priorite** :
C'est la reference la plus proche du projet. Les auteurs construisent un environnement
de simulation base sur Gymnasium pour evoluer des architectures neuronales capables de
reproduire les dynamiques reelles d'une colonie de fourmis (Pristomyrmex punctatus).
L'agent controllable apprend a retracer un piste reelle en utilisant les donnees
sensorielles de la vraie fourmi. L'accent est mis sur la topologie du reseau plutot
que sur les poids (connexion directe avec Gaier & Ha 2019).

**Points d'attention a la lecture** :
- Quelles entrees sensorielles sont utilisees ? (position, angle, pheromones, voisins...)
- Quelle architecture de reseau ? (taille, couches, fonctions d'activation)
- Comment la fitness est-elle definie ?
- Quel algorithme genetique est utilise ? (et ses parametres)
- Comment les comportements collectifs emergent-ils de comportements individuels evolues ?

**Notes apres lecture** :
[A COMPLETER]

---

## THEME 2 : Neuroevolution & Architecture

### [A LIRE] Gaier & Ha (2019)
**Titre** : Weight Agnostic Neural Networks
**Auteurs** : Adam Gaier, David Ha
**Publication** : NeurIPS 2019
**arXiv** : https://arxiv.org/abs/1906.04358
**Site interactif** : https://weightagnostic.github.io/

**Pertinence pour le projet** :
Cite directement par Crosscombe et al. L'idee centrale est de chercher des topologies
de reseaux qui fonctionnent bien sans entrainement des poids -- avec un unique poids
partage echantillonne aleatoirement. C'est precisement l'approche retenue dans ce projet :
toutes les fourmis partagent les memes poids, et c'est la topologie (et les entrees) qui
differentient les comportements.

**Concept cle** :
Au lieu d'optimiser les poids, on optimise la topologie. Un seul poids partage est
utilise pour evaluer le reseau. La performance ne depend que de la structure du graphe,
pas des valeurs des connexions.

**Lien avec ce projet** :
- Justifie l'approche "poids partages entre toutes les fourmis"
- Fournit une base pour l'evolution de topologie (Etape 4)
- La recherche de topologie est inspiree de NEAT (Stanley & Miikkulainen 2002)

**Notes apres lecture** :
[A COMPLETER]

---

### [A LIRE] Stanley & Miikkulainen (2002)
**Titre** : Evolving Neural Networks through Augmenting Topologies (NEAT)
**Auteurs** : Kenneth O. Stanley, Risto Miikkulainen
**Publication** : Evolutionary Computation, vol. 10, no. 2
**Note** : Reference fondatrice de la neuroevolution de topologie.

**Pertinence** :
NEAT est l'algorithme sur lequel Gaier & Ha (2019) s'appuient pour leur recherche
topologique. Comprendre NEAT permet de mieux apprehender les operateurs de mutation
utilises (ajout de noeuds, ajout de connexions, changement d'activation).

**Notes apres lecture** :
[A COMPLETER]

---

## THEME 3 : Algorithmes Genetiques - MAP-Elites

### [A LIRE] Mouret & Clune (2015)
**Titre** : Illuminating search spaces by mapping elites
**Auteurs** : Jean-Baptiste Mouret, Jeff Clune
**Publication** : arXiv preprint
**arXiv** : https://arxiv.org/abs/1504.04909

**Pourquoi lire ce papier** :
C'est le papier fondateur de MAP-Elites, l'algorithme genetique retenu pour ce projet
(Etape 4). Il introduit l'idee de conserver non pas une seule solution optimale mais
une collection de solutions hautes-performances et qualitativement differentes.
L'espace de comportement est discretise en cellules, et chaque cellule conserve
le meilleur individu jamais trouve dans cette region.

**Concept cle** :
L'utilisateur choisit des "dimensions de variation" (descripteurs comportementaux).
MAP-Elites construit une carte : pour chaque point de cet espace, quel est le meilleur
genome trouve ? Le resultat est une archive riche, pas une solution unique.

**Lien avec ce projet** :
- Les dimensions comportementales de la colonie restent a definir (Etape 4)
- Candidats possibles : taux de retour au nid, longueur moyenne des pistes,
  efficacite de collecte, diversite des trajectoires individuelles...
- MAP-Elites permettra d'explorer simultanement plusieurs "styles" de colonie

**Notes apres lecture** :
[A COMPLETER]

---

### [A LIRE] Pugh, Soros & Stanley (2016)
**Titre** : Quality Diversity: A New Frontier for Evolutionary Computation
**Publication** : Frontiers in Robotics and AI
**URL** : https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2016.00040/full

**Pertinence** :
Vue d'ensemble des algorithmes Quality Diversity (QD), dont MAP-Elites.
Utile pour comprendre le positionnement de MAP-Elites par rapport aux autres
approches evolutionnaires (NSLC, etc.) et pour justifier ce choix dans les articles.

**Notes apres lecture** :
[A COMPLETER]

---

## THEME 4 : Stigmergie & Modeles de Pheromones

### [A LIRE] Dorigo, Di Caro & Gambardella (2000)
**Titre** : Ant algorithms and stigmergy
**Auteurs** : Marco Dorigo et al.
**Publication** : Future Generation Computer Systems, vol. 16
**URL** : https://lia.disi.unibo.it/courses/2006-2007/PSI-LS/pdf/roli/dorigo2000-ant_algorithms_and_stigmergy.pdf

**Pertinence** :
Reference classique sur la stigmergie et les algorithmes de fourmis. Definit les
concepts fondamentaux : communication indirecte via l'environnement, retroaction
positive (depot de pheromones), retroaction negative (evaporation). Indispensable
pour la conception de la grille de pheromones (Etape 1).

**Concepts cles a retenir** :
- Stigmergie = communication indirecte via modification de l'environnement
- Retroaction positive : depot renforce le trail -> plus de fourmis -> plus de depot
- Retroaction negative : evaporation permet d'abandonner les pistes sous-utilisees
- Deux types de pheromones possibles : attirant (vers nourriture) et repulsif

**Notes apres lecture** :
[A COMPLETER]

---

### [A LIRE] Bernoff et al. (ou Amorim et al.) - Modele stochastique de piste
**Titre** : A stochastic model of ant trail formation and maintenance in static and dynamic environments
**Publication** : Swarm Intelligence (Springer), 2024
**URL** : https://link.springer.com/article/10.1007/s11721-024-00237-8

**Pertinence** :
Modele recent (2024) couplant simulation individu-centree (off-lattice) et
diffusion de pheromones sur grille (on-lattice). Proche de l'architecture retenue :
les fourmis se deplacent en continu, les pheromones sont sur une grille discrete.
Teste plusieurs variantes de pheromones (1 seule, 2 tache-dependantes...).

**Points d'attention a la lecture** :
- Comment la diffusion est-elle implementee sur la grille ?
- Quels parametres pour l'evaporation et la diffusion ?
- Comment le modele gere-t-il le couplage off-lattice / on-lattice ?

**Notes apres lecture** :
[A COMPLETER]

---

### [A LIRE] Boissard, Degond & Motsch (2013)
**Titre** : A continuous model of ant foraging with pheromones and trail formation
**arXiv** : https://arxiv.org/abs/1402.5611 (preprint)

**Pertinence** :
Approche EDP (equations aux derivees partielles) pour modeliser la formation
des pistes. Moins directement applicable (approche continue vs grille discrete),
mais utile pour comprendre la physique de la diffusion-evaporation des pheromones
et pour valider qualitativement les comportements de la simulation.

**Formule cle** (diffusion-evaporation) :
dc/dt = D * nabla^2(c) - delta * c + depot(x,t)
  avec D = coefficient de diffusion, delta = taux d'evaporation

**Notes apres lecture** :
[A COMPLETER]

---

### [A LIRE] Nakamichi & Arita (2004) - Evolution de la communication par pheromones
**Titre** : An Evolutionary Simulation of the Origin of Pheromone Communication
**Pertinence** :
Etude de l'emergence de la communication par pheromones via neuroevolution.
Les reseaux neuronaux des fourmis evoluent selon les resultats de fourragement.
Directement pertinent pour l'Etape 3 (emergence) et l'Etape 4 (evolution).

**Notes apres lecture** :
[A COMPLETER]

---

## THEME 5 : Intelligence Collective & Comportement Emergent

### [A LIRE] Couzin & Krause (2003)
**Titre** : Self-organization and collective behavior in vertebrates
**Publication** : Advances in the Study of Behavior
**Note** : Cite dans Crosscombe et al. Reference sur l'auto-organisation.

**Pertinence** :
Fournit un cadre conceptuel general sur l'emergence de comportements collectifs
a partir de regles individuelles simples. Utile pour la section "contexte" des articles.

**Notes apres lecture** :
[A COMPLETER]

---

### [A LIRE] Ha & Tang (2022)
**Titre** : Collective Intelligence for Deep Learning: A Survey of Recent Developments
**Auteurs** : David Ha, Yujin Tang
**Pertinence** :
Vue d'ensemble sur l'intersection entre intelligence collective et apprentissage
profond. Cite dans Crosscombe et al. Utile pour situer le projet dans le contexte
plus large de la recherche en IA.

**Notes apres lecture** :
[A COMPLETER]

---

## ANNEXE A : Formules de reference pour l'Etape 1

### Diffusion-Evaporation des pheromones (forme discrete)

Sur une grille 2D de cellules (i,j), a chaque pas de temps t :

  P(i,j,t+1) = P(i,j,t) * (1 - evaporation_rate)
               + diffusion_kernel * P_voisins(i,j,t)
               + depot(i,j,t)

Avec :
- evaporation_rate  in [0, 1]  (ex: 0.01 a 0.05 par pas de temps)
- diffusion_kernel  : noyau gaussien (scipy.ndimage.gaussian_filter) ou
                     moyenne des 4/8 voisins pondere
- depot(i,j,t)      : quantite deposee par les fourmis presentes en (i,j)

Implementation retenue (a valider) :
- scipy.ndimage.gaussian_filter pour la diffusion (vectorise, rapide)
- Multiplication elementwise NumPy pour l'evaporation
- Clip des valeurs entre 0 et MAX_PHEROMONE (config.py)

### Entrees sensorielles de la fourmi (base de travail, a affiner)

Selon Crosscombe et al. (2024), le vecteur d'etat de l'agent inclut :
  {x, y, s, theta, theta_dot, V_fl1, V_fl2, V_fc, V_fr2, V_fr1, V_r, V_b, V_l}

Avec :
- (x, y)       : position
- s            : vitesse
- theta        : angle
- theta_dot    : vitesse angulaire
- V_*          : observations visuelles (proportion de fourmis dans le champ de vision)

Note : les pheromones ne sont pas detectees directement dans leur implementation
(impossibilite de les extraire des videos reelles). Dans ce projet, on pourra
les inclure comme entrees supplementaires.

---

## ANNEXE B : Ordre de lecture suggere

Etape 1 (Grille & Pheromones) :
  1. Dorigo et al. (2000) -> concepts fondamentaux stigmergie
  2. Bernoff et al. (2024) -> implementation couplage grille/agents
  3. Boissard et al. (2013) -> physique diffusion-evaporation

Etape 2-3 (Agents & Emergence) :
  4. Crosscombe et al. (2024) -> reference principale
  5. Nakamichi & Arita (2004) -> evolution communication pheromones
  6. Couzin & Krause (2003)   -> cadre conceptuel emergence

Etape 4 (MAP-Elites) :
  7. Mouret & Clune (2015)    -> MAP-Elites fondateur
  8. Gaier & Ha (2019)        -> topologie vs poids
  9. Stanley & Miikkulainen (2002) -> NEAT (base de Gaier & Ha)
  10. Pugh et al. (2016)      -> vue d'ensemble QD

Background general :
  11. Ha & Tang (2022)        -> intelligence collective + deep learning

---

## ANNEXE C : Base d'article Hugo - Etape 1

**Titre suggere** : "Etape 1 : Construire la memoire chimique de la colonie"
**Public** : developpeurs / chercheurs

**Structure brute (a reformuler avant publication)** :

[CONTEXTE]
Les fourmis ne se parlent pas directement. Elles communiquent en modifiant leur
environnement : chaque fourmi depose des molecules chimiques (pheromones) sur
le sol en se deplacant. Ce mecanisme s'appelle la stigmergie.
-> Reference : Dorigo et al. (2000)

[CHOIX TECHNIQUE]
La piste de pheromones est modelisee comme une grille 2D de valeurs reelles.
A chaque pas de temps, deux phenomenes se produisent simultanement :
  - Evaporation : la concentration diminue exponentiellement
  - Diffusion : les pheromones se repartissent dans les cellules voisines
    (modelisee par un filtre gaussien avec scipy)

[FORMULE CLE]
P(t+1) = gaussian_filter(P(t), sigma) * (1 - EVAPORATION_RATE) + depot(t)

[POURQUOI CE CHOIX ?]
- gaussian_filter est vectorise et tourne bien en NumPy/SciPy sur CPU
- La grille permet le batching : toute la pheromone est mise a jour en une
  seule operation matricielle, sans boucle sur les cellules
- Compatible avec l'architecture PyTorch (tenseur 2D facilement convertible)

[CE QU'ON VOIT EN SIMULATION]
Avant integration avec les agents : juste une grille qui se diffuse et s'evapore.
C'est le substrat passif sur lequel l'intelligence collective va s'ecrire.

[LIEN AVEC LA SUITE]
A l'Etape 2, les fourmis liront et ecriront sur cette grille. Le reseau neuronal
partagera les memes poids entre toutes les fourmis, mais chacune percevra une
concentration differente selon sa position -> comportements differents, meme cerveau.

**Note** : Ce texte est une base de travail brute. A reformuler completement
avant publication. Conserver le vocabulaire (grille, diffusion, evaporation,
stigmergie) pour la coherence avec le code.