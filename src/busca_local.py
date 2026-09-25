import math
import random
import statistics

K_PADRAO = 15
REPETICOES_PADRAO = 30

VALOR_TALHAO = {"~": 3, ".": 1}
LAMBDA_DESLOC = 0.1


def talhoes_livres(grade):
    livres = []
    for r, linha in enumerate(grade):
        for c, t in enumerate(linha):
            if t != "#":
                livres.append((r, c))
    return livres


def valor_estado(estado, grade):
    return (sum(VALOR_TALHAO[grade[r][c]] for (r, c) in estado)
            - LAMBDA_DESLOC * sum(r + c for (r, c) in estado))


def estado_inicial(livres, k, rng):
    return tuple(sorted(rng.sample(livres, k)))


def gerar_vizinho(estado, livres_set, rng):
    estado_set = set(estado)
    fora = [t for t in livres_set if t not in estado_set]
    sai = rng.choice(estado)
    entra = rng.choice(fora)
    novo = set(estado_set)
    novo.remove(sai)
    novo.add(entra)
    return tuple(sorted(novo))


def subida_encosta(grade, k=K_PADRAO, max_iter=2000, rng=None, inicio=None):
    rng = rng or random.Random()
    livres = talhoes_livres(grade)
    if k > len(livres):
        raise ValueError(f"K={k} maior que talhoes livres={len(livres)}")
    livres_set = set(livres)
    atual = inicio if inicio is not None else estado_inicial(livres, k, rng)
    valor_atual = valor_estado(atual, grade)
    for _ in range(max_iter):
        viz = gerar_vizinho(atual, livres_set, rng)
        valor_viz = valor_estado(viz, grade)
        if valor_viz >= valor_atual:
            atual, valor_atual = viz, valor_viz
    return atual, valor_atual


def tempera_simulada(grade, k=K_PADRAO, max_iter=2000, t0=3.0, alfa=0.995, rng=None, inicio=None):
    rng = rng or random.Random()
    livres = talhoes_livres(grade)
    if k > len(livres):
        raise ValueError(f"K={k} maior que talhoes livres={len(livres)}")
    livres_set = set(livres)
    atual = inicio if inicio is not None else estado_inicial(livres, k, rng)
    valor_atual = valor_estado(atual, grade)
    melhor, valor_melhor = atual, valor_atual
    t = t0
    for _ in range(max_iter):
        viz = gerar_vizinho(atual, livres_set, rng)
        valor_viz = valor_estado(viz, grade)
        delta = valor_viz - valor_atual
        if delta >= 0 or rng.random() < math.exp(delta / t):
            atual, valor_atual = viz, valor_viz
            if valor_atual > valor_melhor:
                melhor, valor_melhor = atual, valor_atual
        t *= alfa
        if t < 1e-9:
            t = 1e-9
    return melhor, valor_melhor


def resumir(valores):
    return {
        "media": statistics.mean(valores),
        "desvio": statistics.stdev(valores) if len(valores) > 1 else 0.0,
        "melhor": max(valores),
        "valores": list(valores),
    }


def executar_experimento(grade, k=K_PADRAO, repeticoes=REPETICOES_PADRAO, seed=0):
    vals_encosta, vals_tempera = [], []
    livres = talhoes_livres(grade)
    for run in range(repeticoes):
        inicio = estado_inicial(livres, k, random.Random(seed * 1000 + run))
        rng1 = random.Random(seed * 1000 + 2 * run)
        rng2 = random.Random(seed * 1000 + 2 * run + 1)
        _, v1 = subida_encosta(grade, k=k, rng=rng1, inicio=inicio)
        _, v2 = tempera_simulada(grade, k=k, rng=rng2, inicio=inicio)
        vals_encosta.append(v1)
        vals_tempera.append(v2)
    return {
        "k": k,
        "repeticoes": repeticoes,
        "encosta": resumir(vals_encosta),
        "tempera": resumir(vals_tempera),
    }


if __name__ == "__main__":
    import sys
    try:
        from gerador_pomar import gerar_pomar
    except ModuleNotFoundError:
        from src.gerador_pomar import gerar_pomar
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 24114056
    g = gerar_pomar(m)
    res = executar_experimento(g, seed=m % 1_000_000)
    for nome in ("encosta", "tempera"):
        r = res[nome]
        print(f"{nome}: media={r['media']:.2f} desvio={r['desvio']:.2f} melhor={r['melhor']}")
