import csv
import sys
import time
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from gerador_pomar import gerar_pomar
from buscas import bfs, dfs, ucs, astar
from busca_local import executar_experimento
import especialista
import bayes as bayes_mod


def main(matricula):
    raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_resultados = os.path.join(raiz, "resultados")
    os.makedirs(pasta_resultados, exist_ok=True)

    grade = gerar_pomar(matricula)

    # --- pomar.txt ---
    with open(os.path.join(pasta_resultados, "pomar.txt"), "w") as f:
        f.write(f"{matricula}\n")
        for linha in grade:
            f.write(" ".join(linha) + "\n")

    linhas_csv = []

    # --- busca cega (BFS, DFS, UCS) ---
    estrategias_cegas = [("BFS", bfs), ("DFS", dfs), ("UCS", ucs)]
    resultados_cegos = {}
    for nome, fn in estrategias_cegas:
        t0 = time.perf_counter()
        r = fn(grade)
        dt_ms = (time.perf_counter() - t0) * 1000
        resultados_cegos[nome] = r
        linhas_csv.append([nome, "-", r["custo"], r["passos"], r["nos_expandidos"],
                            r["fronteira_max"], round(dt_ms, 3)])
        print(f"{nome}: custo={r['custo']} passos={r['passos']} "
              f"nos_expandidos={r['nos_expandidos']} fronteira_max={r['fronteira_max']}")

    # --- busca informada (A* com h1, h2, h3) ---
    resultados_astar = {}
    for nome_h in ("h1", "h2", "h3"):
        t0 = time.perf_counter()
        r = astar(grade, heuristica=nome_h)
        dt_ms = (time.perf_counter() - t0) * 1000
        resultados_astar[nome_h] = r
        linhas_csv.append(["A*", nome_h, r["custo"], r["passos"], r["nos_expandidos"],
                            r["fronteira_max"], round(dt_ms, 3)])
        print(f"A* ({nome_h}): custo={r['custo']} passos={r['passos']} "
              f"nos_expandidos={r['nos_expandidos']}")

    with open(os.path.join(pasta_resultados, "resultados.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["estrategia", "heuristica", "custo", "passos", "nos_expandidos",
                    "fronteira_max", "tempo_ms"])
        w.writerows(linhas_csv)

    # --- grafico.png: nos expandidos x estrategia ---
    nomes = ["BFS", "DFS", "UCS", "A* (h1)", "A* (h2)", "A* (h3)"]
    valores = [resultados_cegos["BFS"]["nos_expandidos"],
               resultados_cegos["DFS"]["nos_expandidos"],
               resultados_cegos["UCS"]["nos_expandidos"],
               resultados_astar["h1"]["nos_expandidos"],
               resultados_astar["h2"]["nos_expandidos"],
               resultados_astar["h3"]["nos_expandidos"]]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    barras = ax.bar(nomes, valores, color=["#6b8e23", "#c0392b", "#2e86ab",
                                            "#8e44ad", "#8e44ad", "#8e44ad"])
    ax.set_xlabel("Estrategia de busca")
    ax.set_ylabel("Nos expandidos")
    ax.set_title(f"Nos expandidos por estrategia - pomar da matricula {matricula}")
    for b, v in zip(barras, valores):
        ax.text(b.get_x() + b.get_width() / 2, v, str(v), ha="center", va="bottom", fontsize=9)
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_resultados, "grafico.png"), dpi=150)
    plt.close()

    # --- busca local (Parte 3.4): K=15, 30 execucoes ---
    print("\n--- Busca local (K=15, 30 execucoes) ---")
    exp = executar_experimento(grade, k=15, repeticoes=30, seed=matricula % 1_000_000)
    print("Subida de encosta:", exp["encosta"])
    print("Tempera simulada:", exp["tempera"])

    # --- sistema especialista (Parte 4.1/4.2) ---
    print("\n--- Sistema especialista ---")
    especialista.explicar("inspecionar_prioridade_alta", {
        "armadilha_positiva": True,
        "umidade_alta": True,
        "dias_desde_pulverizacao_maior_14": True,
    })

    # --- bayes (Parte 4.3) ---
    print("--- Bayes ---")
    bayes_mod.relatorio(matricula)

    print(f"\nArquivos gerados em: {pasta_resultados}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("uso: python src/main.py <matricula>")
        sys.exit(1)
    main(int(sys.argv[1]))