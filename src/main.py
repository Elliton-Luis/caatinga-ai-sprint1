import csv
import sys
import time
from pathlib import Path

try:
    from gerador_pomar import gerar_pomar
    import buscas
    from busca_local import executar_experimento
except ModuleNotFoundError:
    from src.gerador_pomar import gerar_pomar
    from src import buscas
    from src.busca_local import executar_experimento

RAIZ = Path(__file__).resolve().parent.parent
RESULTADOS = RAIZ / "resultados"


def cronometrar(func, *args, **kwargs):
    t0 = time.perf_counter()
    res = func(*args, **kwargs)
    dt_ms = (time.perf_counter() - t0) * 1000
    return res, dt_ms


def main(matricula, n=12):
    grade = gerar_pomar(matricula, n=n)
    linhas = []
    jobs = [
        ("BFS", "", lambda: buscas.bfs(grade)),
        ("DFS", "", lambda: buscas.dfs(grade)),
        ("UCS", "", lambda: buscas.ucs(grade)),
        ("A*", "h1", lambda: buscas.astar(grade, heuristica="h1")),
        ("A*", "h2", lambda: buscas.astar(grade, heuristica="h2")),
        ("A*", "h3", lambda: buscas.astar(grade, heuristica="h3")),
    ]
    for estrategia, heuristica, fn in jobs:
        res, dt_ms = cronometrar(fn)
        linhas.append({
            "estrategia": estrategia,
            "heuristica": heuristica,
            "custo": res["custo"],
            "passos": res["passos"],
            "nos_expandidos": res["nos_expandidos"],
            "fronteira_max": res["fronteira_max"],
            "tempo_ms": round(dt_ms, 2),
        })
        print(f"{estrategia} {heuristica or '-'}: custo={res['custo']} "
              f"passos={res['passos']} exp={res['nos_expandidos']} "
              f"front={res['fronteira_max']} {dt_ms:.1f}ms")

    bl = executar_experimento(grade, seed=matricula % 1_000_000)
    for nome in ("encosta", "tempera"):
        r = bl[nome]
        print(f"busca_local {nome}: media={r['media']:.2f} "
              f"desvio={r['desvio']:.2f} melhor={r['melhor']:.2f}")

    RESULTADOS.mkdir(parents=True, exist_ok=True)
    with open(RESULTADOS / "resultados.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["estrategia", "heuristica", "custo",
                                          "passos", "nos_expandidos",
                                          "fronteira_max", "tempo_ms"])
        w.writeheader()
        w.writerows(linhas)

    with open(RESULTADOS / "pomar.txt", "w") as f:
        f.write(f"{matricula}\n")
        for linha in grade:
            f.write(" ".join(linha) + "\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rotulos = [f"{l['estrategia']}{'*' + l['heuristica'] if l['heuristica'] else ''}"
               for l in linhas]
    valores = [l["nos_expandidos"] for l in linhas]
    plt.figure()
    plt.bar(rotulos, valores)
    plt.xlabel("Estratégia")
    plt.ylabel("Nós expandidos (un)")
    plt.title(f"Nós expandidos por estratégia (matrícula {matricula})")
    plt.tight_layout()
    plt.savefig(RESULTADOS / "grafico.png")
    print(f"OK: {RESULTADOS / 'resultados.csv'}, {RESULTADOS / 'pomar.txt'}, "
          f"{RESULTADOS / 'grafico.png'}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python src/main.py <matricula> [n]")
        sys.exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 12)
