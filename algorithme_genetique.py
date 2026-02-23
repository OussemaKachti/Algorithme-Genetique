import random
import ast

def lire_dataset(fichier):
    with open(fichier, 'r') as f:
        contenu = f.read()

    contenu_stripped = contenu.lstrip()
    if contenu_stripped and contenu_stripped[0].isdigit():
        valeurs = contenu.split()
        try:
            n = int(valeurs[0])
        except ValueError as e:
            raise ValueError("Format de dataset invalide : N doit être un entier.") from e

        nums = list(map(int, valeurs[1:]))
        attendu = n * n
        if len(nums) < attendu:
            raise ValueError(
                f"Format de dataset invalide : attendu {attendu} valeurs après N, trouvé {len(nums)}."
            )
        nums = nums[:attendu]
        matrice = [nums[i * n:(i + 1) * n] for i in range(n)]
        return n, matrice

    debut = contenu.find('[')
    fin = contenu.rfind(']')
    if debut == -1 or fin == -1 or fin <= debut:
        raise ValueError("Format de dataset invalide : matrice non trouvée.")

    matrice = ast.literal_eval(contenu[debut:fin + 1])
    if not isinstance(matrice, list) or not matrice or not all(isinstance(r, list) for r in matrice):
        raise ValueError("Format de dataset invalide : cost_matrix doit être une liste de listes.")

    nb_lignes = len(matrice)
    nb_colonnes = min(len(r) for r in matrice)
    n = min(nb_lignes, nb_colonnes)
    matrice = [r[:n] for r in matrice[:n]]
    return n, matrice

N, cost_matrix = lire_dataset("assign100.txt")
POP_SIZE      = 100
MAX_GEN       = 500
MUTATION_RATE = 0.3

#Ce qu'elle fait : calcule le coût total d'une solution.

def fitness(individu):
    return sum(cost_matrix[i][j] for i, j in enumerate(individu))


#Ce qu'elle fait : crée une affectation aléatoire valide.

def creer_individu():
    individu = list(range(N))
    random.shuffle(individu)
    return individu


#Ce qu'elle fait : choisit le meilleur parmi 3 individus tirés au hasard.

def selection(population):
    candidats = random.sample(population, 3)
    return min(candidats, key=fitness)


#Ce qu'elle fait : mélange deux parents pour créer un enfant qui hérite du meilleur des deux.

def croisement(p1, p2):
    point = random.randint(1, N - 1)
    enfant = p1[:point]
    for gene in p2:
        if gene not in enfant:
            enfant.append(gene)
    return enfant


#Ce qu'elle fait : avec 20% de chance, échange 2 positions pour explorer de nouvelles solutions.

def mutation(individu):
    individu = individu[:]
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(N), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu


#Ce qu'elle fait : orchestre tout le processus sur MAX_GEN générations.

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
