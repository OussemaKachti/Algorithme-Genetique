import random
import ast
import matplotlib.pyplot as plt
import numpy as np

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
POP_SIZE      = 200
MAX_GEN       = 1000
MUTATION_RATE = 0.5


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

    historique_meilleur = []
    historique_moyen    = []
    historique_pire     = []
    snapshots           = {}

    def enregistrer(gen, pop):
        couts = [fitness(ind) for ind in pop]
        historique_meilleur.append(min(couts))
        historique_moyen.append(sum(couts) / len(couts))
        historique_pire.append(max(couts))
        if gen in [0, MAX_GEN]:
            snapshots[gen] = couts[:]

    print("=" * 50)
    enregistrer(0, population)
    couts_str = "  ".join(str(fitness(ind)) for ind in population)
    print(f"Level 0 (Initial)  : {couts_str}")

    for gen in range(1, MAX_GEN + 1):
        nouvelle_population = [min(population, key=fitness)]
        while len(nouvelle_population) < POP_SIZE:
            enfant = croisement(selection(population), selection(population))
            nouvelle_population.append(mutation(enfant))
        population = nouvelle_population
        enregistrer(gen, population)

        couts_str = "  ".join(str(fitness(ind)) for ind in population)
        print(f"Level {gen} (Gen {gen})       : {couts_str}")

    meilleur = min(population, key=fitness)
    print("=" * 50)
    print(f"Meilleure solution : {meilleur}  →  Coût = {fitness(meilleur)}")
    print("Détail :")
    for i, j in enumerate(meilleur):
        print(f"  Agent {i+1} → Tâche {j+1}  (coût = {cost_matrix[i][j]})")
    print("=" * 50)

    visualiser(historique_meilleur, historique_moyen, historique_pire, snapshots)

    return meilleur


def visualiser(meilleur_h, moyen_h, pire_h, snapshots):
    generations = list(range(len(meilleur_h)))

    BLEU   = "#2563EB"
    ORANGE = "#F59E0B"
    ROUGE  = "#EF4444"
    VERT   = "#10B981"
    GRIS   = "#6B7280"
    BG     = "#F8FAFC"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor=BG)
    fig.suptitle("Algorithme Génétique — Visualisation de la Convergence",
                 fontsize=15, fontweight='bold', color="#1E293B", y=1.02)

    # ── Graphe 1 : Évolution du coût ─────────────────────────────────────────
    ax1.set_facecolor(BG)
    ax1.plot(generations, pire_h,     color=ROUGE,  lw=1.2, alpha=0.5, label="Pire")
    ax1.fill_between(generations, pire_h, moyen_h,  color=ROUGE, alpha=0.07)
    ax1.plot(generations, moyen_h,    color=ORANGE, lw=1.5, alpha=0.8, label="Moyen")
    ax1.fill_between(generations, moyen_h, meilleur_h, color=BLEU, alpha=0.10)
    ax1.plot(generations, meilleur_h, color=BLEU,   lw=2.2, label="Meilleur")

    val_finale = meilleur_h[-1]
    ax1.annotate(f"  Optimal = {val_finale}",
                 xy=(generations[-1], val_finale),
                 xytext=(-80, 20), textcoords="offset points",
                 fontsize=9, color=BLEU,
                 arrowprops=dict(arrowstyle="->", color=BLEU, lw=1.2))

    ax1.set_title("Évolution du coût au fil des générations",
                  fontsize=12, fontweight='bold', color="#1E293B", pad=8)
    ax1.set_xlabel("Génération", fontsize=10, color=GRIS)
    ax1.set_ylabel("Coût", fontsize=10, color=GRIS)
    ax1.legend(fontsize=9, framealpha=0.8)
    ax1.grid(True, linestyle='--', alpha=0.4)
    ax1.spines[['top', 'right']].set_visible(False)

    # ── Graphe 2 : Distribution finale ───────────────────────────────────────
    ax2.set_facecolor(BG)
    data = snapshots.get(MAX_GEN, [])
    if data:
        ax2.hist(data, bins=20, color=VERT, alpha=0.75,
                 edgecolor='white', linewidth=0.5)
        med = np.median(data)
        ax2.axvline(min(data), color=BLEU, lw=1.5, linestyle='--',
                    label=f"Min = {min(data)}")
        ax2.axvline(med,       color=GRIS, lw=1.2, linestyle=':',
                    label=f"Méd = {med:.0f}")

    ax2.set_title(f"Distribution finale — Génération {MAX_GEN}",
                  fontsize=12, fontweight='bold', color="#1E293B", pad=8)
    ax2.set_xlabel("Coût", fontsize=10, color=GRIS)
    ax2.set_ylabel("Nombre d'individus", fontsize=10, color=GRIS)
    ax2.legend(fontsize=9, framealpha=0.8)
    ax2.grid(True, linestyle='--', alpha=0.3, axis='y')
    ax2.spines[['top', 'right']].set_visible(False)

    plt.tight_layout()
    plt.savefig("convergence_genetique.png", dpi=150, bbox_inches='tight',
                facecolor=BG)
    print("\n📊 Graphe sauvegardé → convergence_genetique.png")
    plt.show()


# ── Point d'entrée ────────────────────────────────────────────────────────────
algorithme_genetique()