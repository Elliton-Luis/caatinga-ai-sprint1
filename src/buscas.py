from collections import deque
import heapq
import itertools

ORDEM_VIZINHOS = ['N', 'S', 'L', 'O']

DELTAS = {
    'N': (-1, 0),
    'S': (1, 0),
    'L': (0, 1),
    'O': (0, -1),
}

CUSTO_TERRENO = {".": 1, "~": 4}
BLOQUEADO = "#"


def _padrao_objetivo(grade, objetivo):
    if objetivo is None:
        n = len(grade)
        return (n - 1, n - 1)
    return tuple(objetivo)


def _passavel(grade, r, c):
    n = len(grade)
    if not (0 <= r < n and 0 <= c < n):
        return False
    return grade[r][c] != BLOQUEADO


def _custo_entrada(grade, r, c):
    return CUSTO_TERRENO[grade[r][c]]


def vizinhos(pos, grade):
    r, c = pos
    for d in ORDEM_VIZINHOS:
        dr, dc = DELTAS[d]
        nr, nc = r + dr, c + dc
        if _passavel(grade, nr, nc):
            yield (nr, nc)


def reconstruir_caminho(pais, inicio, objetivo):
    caminho = [objetivo]
    atual = objetivo
    while atual != inicio:
        atual = pais[atual]
        caminho.append(atual)
    caminho.reverse()
    return caminho


def calcular_custo(caminho, grade):
    if not caminho or len(caminho) == 1:
        return 0
    return sum(_custo_entrada(grade, r, c) for (r, c) in caminho[1:])


def _resultado(pais, inicio, objetivo, grade, nos_expandidos, fronteira_max,
               estrategia, heuristica=None, sucesso=True):
    if sucesso:
        caminho = reconstruir_caminho(pais, inicio, objetivo)
        custo = calcular_custo(caminho, grade)
        passos = len(caminho) - 1
    else:
        caminho, custo, passos = None, None, None
    return {
        "estrategia": estrategia,
        "heuristica": heuristica,
        "sucesso": sucesso,
        "caminho": caminho,
        "custo": custo,
        "passos": passos,
        "nos_expandidos": nos_expandidos,
        "fronteira_max": fronteira_max,
    }


def bfs(grade, inicio=(0, 0), objetivo=None):
    inicio = tuple(inicio)
    objetivo = _padrao_objetivo(grade, objetivo)

    if inicio == objetivo:
        return _resultado({}, inicio, objetivo, grade, 0, 1, "BFS")

    fronteira = deque([inicio])
    visitado = {inicio}
    pais = {}
    nos_expandidos = 0
    fronteira_max = 1

    while fronteira:
        atual = fronteira.popleft()
        if atual == objetivo:
            return _resultado(pais, inicio, objetivo, grade,
                              nos_expandidos, fronteira_max, "BFS")
        nos_expandidos += 1
        for viz in vizinhos(atual, grade):
            if viz not in visitado:
                visitado.add(viz)
                pais[viz] = atual
                fronteira.append(viz)
        fronteira_max = max(fronteira_max, len(fronteira))

    return _resultado(pais, inicio, objetivo, grade,
                      nos_expandidos, fronteira_max, "BFS", sucesso=False)


def dfs(grade, inicio=(0, 0), objetivo=None):
    inicio = tuple(inicio)
    objetivo = _padrao_objetivo(grade, objetivo)

    if inicio == objetivo:
        return _resultado({}, inicio, objetivo, grade, 0, 1, "DFS")

    fronteira = [inicio]
    visitado = {inicio}
    pais = {}
    nos_expandidos = 0
    fronteira_max = 1

    while fronteira:
        atual = fronteira.pop()
        if atual == objetivo:
            return _resultado(pais, inicio, objetivo, grade,
                              nos_expandidos, fronteira_max, "DFS")
        nos_expandidos += 1
        # pilha inverte a ordem, por isso empilha ao contrario
        for viz in reversed(list(vizinhos(atual, grade))):
            if viz not in visitado:
                visitado.add(viz)
                pais[viz] = atual
                fronteira.append(viz)
        fronteira_max = max(fronteira_max, len(fronteira))

    return _resultado(pais, inicio, objetivo, grade,
                      nos_expandidos, fronteira_max, "DFS", sucesso=False)


def ucs(grade, inicio=(0, 0), objetivo=None):
    inicio = tuple(inicio)
    objetivo = _padrao_objetivo(grade, objetivo)

    if inicio == objetivo:
        return _resultado({}, inicio, objetivo, grade, 0, 1, "UCS")

    contador = itertools.count()
    fronteira = [(0, next(contador), inicio)]
    heapq.heapify(fronteira)
    melhor_g = {inicio: 0}
    pais = {}
    nos_expandidos = 0
    fronteira_max = 1

    while fronteira:
        g, _, atual = heapq.heappop(fronteira)
        # entrada obsoleta do heap: ja existe g menor, ignora sem expandir
        if g > melhor_g.get(atual, float("inf")):
            continue
        if atual == objetivo:
            return _resultado(pais, inicio, objetivo, grade,
                              nos_expandidos, fronteira_max, "UCS")
        nos_expandidos += 1
        for viz in vizinhos(atual, grade):
            novo_g = g + _custo_entrada(grade, *viz)
            if viz not in melhor_g or novo_g < melhor_g[viz]:
                melhor_g[viz] = novo_g
                pais[viz] = atual
                heapq.heappush(fronteira, (novo_g, next(contador), viz))
        fronteira_max = max(fronteira_max, len(fronteira))

    return _resultado(pais, inicio, objetivo, grade,
                      nos_expandidos, fronteira_max, "UCS", sucesso=False)


def h_nula(pos, objetivo):
    return 0


def h_manhattan(pos, objetivo):
    return abs(pos[0] - objetivo[0]) + abs(pos[1] - objetivo[1])


def h_manhattan_x4(pos, objetivo):
    return 4 * h_manhattan(pos, objetivo)


HEURISTICAS = {
    "h1": h_nula,
    "h2": h_manhattan,
    "h3": h_manhattan_x4,
}


def astar(grade, heuristica=h_manhattan, inicio=(0, 0), objetivo=None,
          nome_heuristica=None):
    inicio = tuple(inicio)
    objetivo = _padrao_objetivo(grade, objetivo)
    if isinstance(heuristica, str):
        nome_heuristica = nome_heuristica or heuristica
        heuristica = HEURISTICAS[heuristica]

    if inicio == objetivo:
        return _resultado({}, inicio, objetivo, grade, 0, 1, "A*",
                          heuristica=nome_heuristica)

    contador = itertools.count()
    h0 = heuristica(inicio, objetivo)
    fronteira = [(h0, next(contador), 0, inicio)]
    heapq.heapify(fronteira)
    melhor_g = {inicio: 0}
    pais = {}
    nos_expandidos = 0
    fronteira_max = 1

    while fronteira:
        f, _, g, atual = heapq.heappop(fronteira)
        # mesma reabertura lazy do UCS: descarta pop com g desatualizado
        if g > melhor_g.get(atual, float("inf")):
            continue
        if atual == objetivo:
            return _resultado(pais, inicio, objetivo, grade,
                              nos_expandidos, fronteira_max, "A*",
                              heuristica=nome_heuristica)
        nos_expandidos += 1
        for viz in vizinhos(atual, grade):
            novo_g = g + _custo_entrada(grade, *viz)
            if viz not in melhor_g or novo_g < melhor_g[viz]:
                melhor_g[viz] = novo_g
                pais[viz] = atual
                novo_f = novo_g + heuristica(viz, objetivo)
                heapq.heappush(fronteira, (novo_f, next(contador), novo_g, viz))
        fronteira_max = max(fronteira_max, len(fronteira))

    return _resultado(pais, inicio, objetivo, grade,
                      nos_expandidos, fronteira_max, "A*",
                      heuristica=nome_heuristica, sucesso=False)
