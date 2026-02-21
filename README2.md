# Algorithme Génétique – Problème d’Affectation (Assignment Problem)

Une implémentation simple d’un **algorithme génétique** pour résoudre un **problème d’affectation** à partir d’une matrice de coûts.

## What It Does
Étant donnée une matrice `cost_matrix` où `cost_matrix[i][j]` représente le coût d’affecter l’agent (ou travailleur) `i` à la tâche (ou job) `j`, le programme cherche une affectation **1–à–1** (une tâche par agent, sans répétition) avec un coût total minimal.

L’algorithme manipule des solutions candidates sous forme de **permutations** (ex: `[1, 0, 2]` signifie : Agent 0 → Tâche 1, Agent 1 → Tâche 0, Agent 2 → Tâche 2).

## How It Works
### Représentation (Individu)
- Un individu est une liste de taille `N`.
- L’index `i` correspond à l’agent `i`.
- La valeur `individu[i]` correspond à la tâche attribuée à l’agent `i`.

### Fitness (Coût)
La fonction `fitness(individu)` calcule le coût total :

`sum(cost_matrix[i][individu[i]] for i in range(N))`

Plus le coût est faible, meilleure est la solution.

### Initialisation
La population initiale est construite avec `POP_SIZE` individus aléatoires (des permutations de `0..N-1`).

### Sélection (Tournament Selection)
À chaque sélection :
- on choisit 3 individus au hasard,
- on garde celui qui a le **meilleur fitness** (le coût minimal).

### Croisement (Crossover)
Le croisement `croisement(p1, p2)` :
- choisit un point de coupe aléatoire,
- copie le préfixe de `p1`,
- complète ensuite avec les gènes de `p2` dans l’ordre, en évitant les doublons.

Ce mécanisme produit un enfant qui reste une permutation valide (pas de tâches répétées).

### Mutation
La mutation `mutation(individu)` :
- avec une probabilité `MUTATION_RATE`, échange deux positions (swap) choisies aléatoirement.

### Élitisme
À chaque génération, la meilleure solution de la population courante est conservée automatiquement dans la nouvelle population.

### Affichage par niveaux
Le programme affiche les coûts de tous les individus :
- `Level 0 (Initial)` : coûts de la population initiale,
- `Level k (Gen k)` : coûts de la population après la génération `k`.

## Example Cost Matrix
Pour l’exemple fourni :

|        | Job 1 | Job 2 | Job 3 |
|--------|-------|-------|-------|
| Agent 1 | 9     | 2     | 7     |
| Agent 2 | 1     | 5     | 2     |
| Agent 3 | 6     | 4     | 3     |

## Output (Example)
Le script affiche :
- les coûts de la population à chaque génération,
- puis la meilleure affectation trouvée, son coût total, et le détail agent → tâche.

## Requirements
- Python 3.x
- Aucune bibliothèque externe

## Run
Depuis le dossier du projet :

```bash
python algorithme_genetique.py
```
