"""
evaluation_parameters.py
------------------------
Diagnostic des parametres de la simulation de fourmis.
Lancer depuis la racine : python evaluation_parameters.py

Hypothese : a l'equilibre depot/evaporation/diffusion, le profil de concentration
perpendiculairement a la piste suit une gaussienne :
  C(x) = C_max * exp( -x^2 / (2 * sigma_eff^2) )
ou C(x, y) = pheromone_grid.grids[type, y, x] est dans [0, 1].

Indicateurs :
  [OK]  valeur dans la plage cible
  [!]   valeur hors plage, a regler
"""

import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import *


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------

W = 64

def header(title):
    print()
    print("=" * W)
    print(f"  {title}")
    print("=" * W)

def section(title):
    print()
    print(f"  {'-'*(W-4)}")
    print(f"  {title}")
    print(f"  {'-'*(W-4)}")

def row(label, value, unit="", note="", warn=False, good=False):
    tag = "  [!]" if warn else "  [OK]" if good else "     "
    val_str = f"{value:.3f} {unit}".strip()
    print(f"{tag}  {label:<32} {val_str:>12}   {note}")

def info(text):
    print(f"       -> {text}")

def verdict(snr):
    if snr >= 3:
        return "[OK] BON    : traces nettes attendues"
    elif snr >= 1.5:
        return "[~]  FRAGILE: traces emergent mais instables"
    else:
        return "[X]  MAUVAIS: bruit dominant, pas de traces"


# -----------------------------------------------------------------------------
# 1. PHEROMONES : DEMI-VIE ET ETALEMENT
# -----------------------------------------------------------------------------

header("1. PHEROMONES - DEMI-VIE ET ETALEMENT")

# A chaque step : C_new = C * EVAPORATION_RATE  (cf. pheromone_grid.py)
# Apres n steps  : C(n) = C(0) * EVAPORATION_RATE^n
# Demi-vie = n tel que C(n) = C(0)/2
#   => n = log(2) / log(1/EVAPORATION_RATE)
half_life_home = np.log(2) / np.log(1 / EVAPORATION_RATE_HOME)
half_life_food = np.log(2) / np.log(1 / EVAPORATION_RATE_FOOD)

section("Demi-vie : temps avant que la concentration soit divisee par 2")
info("Grand = traces persistantes, renforcement possible sur plusieurs passages")
info("Petit = traces fugaces, disparaissent avant d'etre renforcees")
info("Cible HOME : 200-2000 steps | FOOD : 100-1000 steps")
print()
row("HOME  demi-vie", half_life_home, "steps",
    warn=(half_life_home < 100), good=(200 < half_life_home < 2000))
row("HOME  demi-vie", half_life_home / FPS, "s")
row("FOOD  demi-vie", half_life_food, "steps",
    warn=(half_life_food < 50), good=(100 < half_life_food < 1000))
row("FOOD  demi-vie", half_life_food / FPS, "s")

# scipy.gaussian_filter avec sigma=DIFFUSION_SIGMA est applique a chaque step.
# Chaque convolution ajoute DIFFUSION_SIGMA^2 a la variance du profil.
# Apres N steps : variance = N * DIFFUSION_SIGMA^2  =>  sigma_eff = DIFFUSION_SIGMA * sqrt(N)
# N = demi-vie : a cet instant la trace est a mi-hauteur, c'est son etat "utile".
sigma_eff_home = DIFFUSION_SIGMA * np.sqrt(half_life_home)
sigma_eff_food = DIFFUSION_SIGMA * np.sqrt(half_life_food)

section("sigma_eff : ecart-type caracteristique de la trace a la demi-vie")
info("C'est la largeur de la bosse de pheromones a l'ecran.")
info("A une distance sigma_eff du centre, C vaut 61% du max.")
info("A une distance 2*sigma_eff, C vaut 14% du max.")
info("Grand = trace large, gradient plat | Petit = trace fine, difficile a detecter")
info("Cible : 2-20 cellules")
print()
row("HOME  sigma_eff", sigma_eff_home, "cellules",
    warn=(sigma_eff_home < 1.5), good=(3 < sigma_eff_home < 20))
row("FOOD  sigma_eff", sigma_eff_food, "cellules",
    warn=(sigma_eff_food < 1.5), good=(2 < sigma_eff_food < 15))


# -----------------------------------------------------------------------------
# 2. ANTENNES : GEOMETRIE ET ACCORD AVEC LA TRACE
# -----------------------------------------------------------------------------

header("2. ANTENNES - GEOMETRIE ET ACCORD AVEC LA TRACE")

# La tete est a HALF_LENGTH_BODY du centre dans la direction theta (cf. ant.py).
# ANT_RADIUS sert uniquement au rendu visuel.
# Separation laterale entre les deux pointes (perpendiculaire a theta) :
#   lateral_sep = 2 * LENGTH_ANTENNA * sin(ANGLE_ANTENNA)
# Portee avant (projection de l'antenne sur theta) :
#   forward_reach = HALF_LENGTH_BODY + LENGTH_ANTENNA * cos(ANGLE_ANTENNA)
#   (pas HALF_LENGTH_BODY + LENGTH_ANTENNA : l'antenne est inclinee a ANGLE_ANTENNA)
lateral_sep = 2 * LENGTH_ANTENNA * np.sin(ANGLE_ANTENNA)
forward_reach = HALF_LENGTH_BODY + LENGTH_ANTENNA * np.cos(ANGLE_ANTENNA)

section("Dimensions  (ANT_RADIUS={} est visuel uniquement)".format(ANT_RADIUS))
row("Separation laterale  2*L*sin(alpha)", lateral_sep, "cellules")
row("Portee avant  HALF_BODY+L*cos(alpha)", forward_reach, "cellules")

# Ratio separation / sigma_eff :
# Les deux antennes echantillonnent le profil gaussien a deux points distants de lateral_sep.
# Si lateral_sep << sigma_eff (ratio ~ 0) : les deux points sont au sommet de la bosse,
#   les deux antennes lisent presque la meme valeur -> pas de difference -> pas de signal.
# Si lateral_sep >> sigma_eff (ratio >> 1) : un cote est dans la trace, l'autre toujours
#   dehors -> la fourmi detecte juste "gauche ou droite" sans info de distance -> pas de gradient.
# Optimal a ratio ~ 1.0 : les antennes tombent au point d'inflexion de la gaussienne,
#   la ou la pente est la plus forte -> difference maximale pour un meme deplacement lateral.
section("Ratio separation / sigma_eff  (cible : 0.3-1.5, optimal : 1.0)")
info("Mesure si les antennes sont bien calibrees pour la largeur de trace.")
info("ratio << 1 : les deux antennes lisent pareil  -> signal nul")
info("ratio >> 1 : une antenne toujours hors trace  -> pas d'info de position")
info("ratio ~ 1  : antennes au point d'inflexion    -> gradient maximal")
print()
ratio_home = lateral_sep / sigma_eff_home
ratio_food = lateral_sep / sigma_eff_food
row("ratio HOME  lateral_sep / sigma_eff", ratio_home, "",
    warn=(ratio_home < 0.2 or ratio_home > 2.5),
    good=(0.3 <= ratio_home <= 1.5))
row("ratio FOOD  lateral_sep / sigma_eff", ratio_food, "",
    warn=(ratio_food < 0.2 or ratio_food > 2.5),
    good=(0.3 <= ratio_food <= 1.5))


# -----------------------------------------------------------------------------
# 3. SNR : SIGNAL SUR BRUIT
# -----------------------------------------------------------------------------

header("3. SNR - SIGNAL SUR BRUIT")

# delta_C : difference de concentration max entre les deux antennes.
# Quand la fourmi longe le bord de la trace (a x = sigma_eff du centre),
# la pente du profil gaussien en ce point vaut :
#   dC/dx = -(x/sigma_eff^2) * exp(-x^2/2*sigma_eff^2)
#   en x = sigma_eff : dC/dx = -(1/sigma_eff) * exp(-1/2) = -0.607 / sigma_eff
# Pour lateral_sep << sigma_eff, on linearise :
#   delta_C_max ~ 0.607 * lateral_sep / sigma_eff
# Hypothese valide si lateral_sep / sigma_eff < 0.5 (sinon formule trop optimiste).
approx_ratio_home = lateral_sep / sigma_eff_home
approx_ratio_food = lateral_sep / sigma_eff_food

section("Validite de l'approximation  (lateral_sep / sigma_eff < 0.5 requis)")
info("La formule de delta_C linearise le gradient. Valide si les antennes")
info("sont proches l'une de l'autre devant la largeur de la trace.")
print()
row("lateral_sep / sigma_eff HOME", approx_ratio_home, "",
    note="< 0.5 requis",
    warn=(approx_ratio_home > 0.5), good=(approx_ratio_home <= 0.5))
row("lateral_sep / sigma_eff FOOD", approx_ratio_food, "",
    note="< 0.5 requis",
    warn=(approx_ratio_food > 0.5), good=(approx_ratio_food <= 0.5))

delta_C_home = min(0.607 * lateral_sep / sigma_eff_home, 1.0)
delta_C_food = min(0.607 * lateral_sep / sigma_eff_food, 1.0)

# Signal = biais angulaire applique a la direction de la fourmi par les pheromones.
#   A chaque step : delta_theta += ANTENNA_WEIGHT * (C_gauche - C_droite)
#   Dans le meilleur cas : C_gauche - C_droite = delta_C_max
#   => signal_max = ANTENNA_WEIGHT * delta_C_max  [en radians]
#
# Bruit = perturbation aleatoire de direction a chaque step.
#   delta_theta += bruit  avec  bruit ~ U(-RANDOM_DIR, RANDOM_DIR)
#   => amplitude max du bruit = RANDOM_DIR  [en radians]
#
# Les deux sont des angles en radians -> on peut les comparer directement.
# SNR = signal_max / bruit_max = ANTENNA_WEIGHT * delta_C_max / RANDOM_DIR
# Si SNR < 1 : meme en detection optimale, le bruit peut effacer le signal.
# Si SNR > 3 : le signal domine, les fourmis suivent les traces nettement.
signal_home = ANTENNA_WEIGHT * delta_C_home
signal_food = ANTENNA_WEIGHT * delta_C_food
snr_home = signal_home / RANDOM_DIR
snr_food = signal_food / RANDOM_DIR

section("Calcul du SNR")
info("Signal = biais angulaire max en rad  = ANTENNA_WEIGHT * delta_C_max")
info("Bruit  = perturbation aleatoire max  = RANDOM_DIR  [en rad aussi]")
info("SNR    = signal / bruit  -> les deux sont des angles, comparaison directe")
print()
row("delta_C_max HOME  (gradient detecte)", delta_C_home, "",
    note="difference de concentration max")
row("delta_C_max FOOD", delta_C_food, "")
row("signal HOME  ANTENNA_WEIGHT*delta_C", signal_home, "rad")
row("signal FOOD  ANTENNA_WEIGHT*delta_C", signal_food, "rad")
row("bruit   RANDOM_DIR", RANDOM_DIR, "rad")

section("SNR = signal / bruit  (>3 bon | 1-3 fragile | <1 mauvais)")
row("SNR HOME", snr_home, "",
    warn=(snr_home < 1.2), good=(snr_home >= 2.5))
row("SNR FOOD", snr_food, "",
    warn=(snr_food < 1.2), good=(snr_food >= 2.5))
if signal_home > LIM_ANGLE:
    print(f"       [!] signal HOME ({signal_home:.3f} rad) > LIM_ANGLE ({LIM_ANGLE:.3f} rad) : clip actif")
if signal_food > LIM_ANGLE:
    print(f"       [!] signal FOOD ({signal_food:.3f} rad) > LIM_ANGLE ({LIM_ANGLE:.3f} rad) : clip actif")
print()
print(f"       Verdict HOME : {verdict(snr_home)}")
print(f"       Verdict FOOD : {verdict(snr_food)}")


# -----------------------------------------------------------------------------
# 4. INVENTAIRE : DECAY_FACTOR_STEP
# -----------------------------------------------------------------------------

header("4. INVENTAIRE - DECAY_FACTOR_STEP")

# pheromone_deposit *= DECAY_FACTOR_STEP a chaque step (cf. ant.py : move())
# Demarre a PHEROMONE_DEPOSIT = 1.0 et decroit exponentiellement.
# Coupe a 0 quand pheromone_deposit < 0.001 (seuil dans ant.py).
# => duree : DECAY_FACTOR_STEP^n = 0.001  =>  n = log(0.001) / log(DECAY_FACTOR_STEP)
steps_to_zero = np.log(0.001) / np.log(DECAY_FACTOR_STEP)
deposit_at_100 = DECAY_FACTOR_STEP ** 100
deposit_at_300 = DECAY_FACTOR_STEP ** 300

section("Duree avant que la fourmi arrete de deposer  (cible : 400-3000 steps)")
info("L'inventaire demarre a 1.0 et decroit a chaque pas.")
info("La fourmi depose fort pres du nid/nourriture, presque rien au milieu.")
print()
row("Steps avant depot < 0.001", steps_to_zero, "steps",
    warn=(steps_to_zero < 200), good=(400 < steps_to_zero < 3000))
row("En secondes", steps_to_zero / FPS, "s")
row("Depot restant a 100 steps", deposit_at_100, "",
    warn=(deposit_at_100 < 0.3))
row("Depot restant a 300 steps", deposit_at_300, "",
    warn=(deposit_at_300 < 0.05))

# Si la fourmi fait demi-tour apres steps_to_zero steps (inventaire vide),
# elle doit pouvoir suivre la trace HOME qu'elle a laissee en partant.
# Cette trace a continu d'evaporer pendant steps_to_zero steps.
# Concentration restante de la trace HOME deposee au debut du trajet :
#   C_remaining = EVAPORATION_RATE_HOME ^ steps_to_zero
# Nombre de demi-vies HOME ecoule :
#   n_halflife = steps_to_zero / half_life_home
# Regle pratique : si n_halflife > 3, la trace est a moins de 12.5% -> risque de perte.
n_halflife_at_turnback = steps_to_zero / half_life_home
c_remaining_at_turnback = EVAPORATION_RATE_HOME ** steps_to_zero

section("Si demi-tour quand inventaire vide : trace HOME encore visible ?")
info("Quand la fourmi fait demi-tour, la trace HOME du debut de son trajet")
info("a evapore pendant steps_to_zero steps.")
info("Si la concentration restante est trop faible, la fourmi ne peut plus")
info("suivre la trace pour rentrer. Cible : < 3 demi-vies HOME ecoules.")
print()
row("Demi-vies HOME ecoules au demi-tour", n_halflife_at_turnback, "",
    note="< 3 pour que la trace soit encore lisible",
    warn=(n_halflife_at_turnback > 3), good=(n_halflife_at_turnback <= 2))
row("C restante trace HOME au debut", c_remaining_at_turnback, "",
    note="fraction de la concentration initiale")


# -----------------------------------------------------------------------------
# 5. PORTEE : MARCHE ALEATOIRE CORRELEE
# -----------------------------------------------------------------------------

header("5. PORTEE - MARCHE ALEATOIRE CORRELEE")

# La formule classique sqrt(steps) suppose des directions tirees independamment.
# Ici delta_theta ~ U(-RANDOM_DIR, RANDOM_DIR) a chaque step.
# Avec RANDOM_DIR petit, la fourmi tourne peu -> ses directions successives sont correlees
# -> elle va presque en ligne droite -> elle explore beaucoup plus loin que sqrt(N).
#
# Correlation entre deux steps consecutifs (correlation de direction) :
#   p = E[cos(delta_theta)] = sin(RANDOM_DIR) / RANDOM_DIR
#   (formule exacte pour une loi uniforme symetrique)
#   p proche de 1 = fourmi quasiment rectiligne.
#
# Longueur de persistance L_persist = 1 / (1-p) :
#   Nombre de steps avant que la direction soit "oubliee".
#   Intuition : apres L_persist steps de petits virages, la fourmi a tourne
#   en moyenne d'un angle suffisant pour perdre sa direction initiale.
#
# Deplacement quadratique moyen pour N >> L_persist :
#   <r^2(N)> = N * (1+p) / (1-p)
#   reach_crw = sqrt(N * (1+p) / (1-p))
#
# La formule est valide seulement si N >> L_persist (regime diffusif atteint).
# On affiche le ratio N / L_persist pour verifier.
p = np.sin(RANDOM_DIR) / RANDOM_DIR
L_persist = 1.0 / (1.0 - p)
reach_crw = np.sqrt(steps_to_zero * (1 + p) / (1 - p))
reach_naive = np.sqrt(steps_to_zero)
diag_grid = np.sqrt(GRID_WIDTH**2 + GRID_HEIGHT**2)

section("Persistance de direction")
info("p = correlation entre deux steps consecutifs (0=aleatoire, 1=ligne droite).")
info("L_persist = nombre de steps avant que la direction soit vraiment aleatoire.")
print()
row("Correlation p = sin(RANDOM_DIR)/RANDOM_DIR", p, "",
    note="proche de 1 = fourmi va droit")
row("L_persist = 1/(1-p)", L_persist, "steps")
row("Ratio N_inventaire / L_persist", steps_to_zero / L_persist, "",
    note="> 5 requis pour formule valide",
    warn=(steps_to_zero / L_persist < 5),
    good=(steps_to_zero / L_persist >= 5))

section("Portee estimee sur la duree d'un inventaire")
info("Portee naive sqrt(N) : valable si la fourmi tourne completement aleatoirement.")
info("Portee correlee      : valable ici car RANDOM_DIR est petit.")
print()
row("Portee naive  sqrt(N)  [fausse ici]", reach_naive, "cellules")
row("Portee correlee  sqrt(N*(1+p)/(1-p))", reach_crw, "cellules")
row("Diagonale de la grille", diag_grid, "cellules")
row("Portee / diagonale", reach_crw / diag_grid, "",
    note="1.0 = peut traverser toute la grille",
    warn=(reach_crw / diag_grid < 0.1))


# -----------------------------------------------------------------------------
# 6. RESUME DES VALEURS CALCULEES
# -----------------------------------------------------------------------------

header("6. RESUME - VALEURS CALCULEES")

print(f"""
  {'Grandeur calculee':<38} {'Valeur':>10}   {'Unite'}
  {'-'*60}
  -- Pheromones --
  {'demi-vie HOME':<38} {half_life_home:>10.0f}   steps
  {'demi-vie HOME':<38} {half_life_home/FPS:>10.1f}   s
  {'demi-vie FOOD':<38} {half_life_food:>10.0f}   steps
  {'demi-vie FOOD':<38} {half_life_food/FPS:>10.1f}   s
  {'sigma_eff HOME':<38} {sigma_eff_home:>10.2f}   cellules
  {'sigma_eff FOOD':<38} {sigma_eff_food:>10.2f}   cellules
  {'-'*60}
  -- Antennes --
  {'separation laterale':<38} {lateral_sep:>10.2f}   cellules
  {'portee avant':<38} {forward_reach:>10.2f}   cellules
  {'ratio sep/sigma HOME':<38} {ratio_home:>10.3f}
  {'ratio sep/sigma FOOD':<38} {ratio_food:>10.3f}
  {'-'*60}
  -- Signal --
  {'delta_C_max HOME':<38} {delta_C_home:>10.3f}
  {'delta_C_max FOOD':<38} {delta_C_food:>10.3f}
  {'signal HOME (rad)':<38} {signal_home:>10.3f}   rad
  {'signal FOOD (rad)':<38} {signal_food:>10.3f}   rad
  {'bruit RANDOM_DIR (rad)':<38} {RANDOM_DIR:>10.3f}   rad
  {'SNR HOME':<38} {snr_home:>10.2f}   -> {verdict(snr_home)}
  {'SNR FOOD':<38} {snr_food:>10.2f}   -> {verdict(snr_food)}
  {'-'*60}
  -- Inventaire --
  {'duree inventaire':<38} {steps_to_zero:>10.0f}   steps
  {'duree inventaire':<38} {steps_to_zero/FPS:>10.1f}   s
  {'demi-vies HOME au demi-tour':<38} {n_halflife_at_turnback:>10.2f}
  {'C_HOME restante au demi-tour':<38} {c_remaining_at_turnback:>10.3f}
  {'-'*60}
  -- Portee --
  {'persistance L_persist':<38} {L_persist:>10.0f}   steps
  {'portee correlee':<38} {reach_crw:>10.0f}   cellules
  {'portee / diagonale grille':<38} {reach_crw/diag_grid:>10.3f}
""")

print("=" * W)
print()
