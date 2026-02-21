import random

cost_matrix = [
    [9, 2, 7],
    [1, 5, 2],
    [6, 4, 3],
]

N             = len(cost_matrix)
POP_SIZE      = 6
MAX_GEN       = 4
MUTATION_RATE = 0.2

def fitness(individu):
    return sum(cost_matrix[i][j] for i, j in enumerate(individu))

def creer_individu():
    individu = list(range(N))
    random.shuffle(individu)
    return individu

def selection(population):
    candidats = random.sample(population, 3)
    return min(candidats, key=fitness)

def croisement(p1, p2):
    point = random.randint(1, N - 1)
    enfant = p1[:point]
    for gene in p2:
        if gene not in enfant:
            enfant.append(gene)
    return enfant

def mutation(individu):
    individu = individu[:]
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(N), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu

def algorithme_genetique():
    random.seed(42)
    population = [creer_individu() for _ in range(POP_SIZE)]

    print("=" * 50)
    couts = "  ".join(str(fitness(ind)) for ind in population)
    print(f"Level 0 (Initial)  : {couts}")

    for gen in range(1, MAX_GEN + 1):
        nouvelle_population = [min(population, key=fitness)]
        while len(nouvelle_population) < POP_SIZE:
            enfant = croisement(selection(population), selection(population))
            nouvelle_population.append(mutation(enfant))
        population = nouvelle_population

        couts = "  ".join(str(fitness(ind)) for ind in population)
        print(f"Level {gen} (Gen {gen})       : {couts}")

    meilleur = min(population, key=fitness)
    print("=" * 50)
    print(f"Meilleure solution : {meilleur}  →  Coût = {fitness(meilleur)}")
    print("Détail :")
    for i, j in enumerate(meilleur):
        print(f"  Agent {i+1} → Tâche {j+1}  (coût = {cost_matrix[i][j]})")
    print("=" * 50)

algorithme_genetique()
