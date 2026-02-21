# Algorithme Génétique – Problème d'Affectation

Une implémentation simple de l'Algorithme Génétique pour résoudre le problème d'affectation à l'aide d'opérations évolutives : sélection, croisement et mutation.

## Ce que ça fait

À partir d'une matrice de coûts où `cost_matrix[i][j]` est le coût d'affecter l'agent `i` à la tâche `j`, l'algorithme fait évoluer une population de solutions candidates sur plusieurs générations afin de trouver une affectation **quasi-optimale** avec un coût total minimum.

> ⚠️ Contrairement au Branch and Bound (qui donne une solution **exacte**), l'Algorithme Génétique donne une solution **approchée**. Il ne garantit pas toujours l'optimum global, mais il s'exécute efficacement même sur de grandes instances.

## Comment ça fonctionne

1. **Initialisation** – Une population d'affectations aléatoires est générée.
2. **Sélection** – Les meilleurs individus sont sélectionnés (tournoi parmi 3 candidats aléatoires).
3. **Croisement** – Deux parents sont combinés via le croisement par ordre (OX) pour produire un enfant valide.
4. **Mutation** – Avec une faible probabilité, deux tâches de l'enfant sont échangées pour maintenir la diversité.
5. **Élitisme** – Le meilleur individu de chaque génération est toujours conservé dans la suivante.
6. **Répétition** – Les étapes 2 à 5 sont répétées pendant `MAX_GEN` générations.

## Exemple de Matrice de Coûts

```
            Tâche 0  Tâche 1  Tâche 2
Agent 0 :     9        2        7
Agent 1 :     1        5        2
Agent 2 :     6        4        3
```

## Affichage par Génération

```
Level 0 (Initial)  : 6  18  10  10  6  17   ← population aléatoire (coûts)
Level 1 (Gen 1)    : 6   6  10  18  10  6   ← après sélection/croisement/mutation
Level 2 (Gen 2)    : 6   6   6   6   6  6   ← la population converge
Level 3 (Gen 3)    : 6  12   6   6   6  12
Level 4 (Gen 4)    : 6   6  17   6   6  6
```

Chaque niveau montre la **fitness (coût total)** de chaque individu dans la population à cette génération. L'algorithme conserve le coût le plus bas trouvé sur toutes les générations.

## Résultat

```
Meilleure solution trouvée : [1, 0, 2]  →  Coût = 6
  Agent 1 → Tâche 2  (coût = 2)
  Agent 2 → Tâche 1  (coût = 1)
  Agent 3 → Tâche 3  (coût = 3)
```

## Comparaison avec Branch and Bound

| | Branch and Bound | Algorithme Génétique |
|--|--|--|
| Type | Exact | Approché |
| Résultat | Toujours optimal | Quasi-optimal |
| Exploration | Tous les chemins (élagués) | Un échantillon de solutions |
| Affichage par niveau | Coûts partiels de chaque nœud | Fitness de chaque individu |
| Adapté pour | Petites instances | Grandes instances |

Les deux algorithmes trouvent **Coût = 6** sur cet exemple, mais l'Algorithme Génétique n'est pas garanti de le faire à chaque exécution.

## Paramètres

| Paramètre | Valeur | Rôle |
|--|--|--|
| `POP_SIZE` | 6 | Nombre d'individus dans la population |
| `MAX_GEN` | 4 | Nombre de générations à faire évoluer |
| `MUTATION_RATE` | 0.2 | Probabilité de muter un enfant (20%) |

## Prérequis

- Python 3.x
- Aucune bibliothèque externe nécessaire
