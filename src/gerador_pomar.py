# gerador_pomar.py - NAO ALTERE ESTE ARQUIVO
import random
CUSTO = {".": 1, "~": 4} # carreador = 1, solo encharcado = 4
BLOQUEADO = "#"
def gerar_pomar(matricula: int, n: int = 12):
    rng = random.Random(matricula % 1_000_000)
    g = [[("#" if rng.random() < 0.20 else ("~" if rng.random() < 0.40 else "."))
        for _ in range(n)] for _ in range(n)]
    # garante ao menos um caminho do portao ate o ponto de coleta
    i = j = 0
    g[0][0] = "."
    while (i, j) != (n - 1, n - 1):
        if i == n - 1: j += 1
        elif j == n - 1: i += 1
        elif rng.random() < 0.5: i += 1
        else: j += 1
        if g[i][j] == BLOQUEADO:
            g[i][j] = "~"
    g[n - 1][n - 1] = "."
    return g
def parametros_sensor(matricula: int):
    rng = random.Random((matricula % 1_000_000) + 777)
    return {
        "prevalencia": round(rng.uniform(0.008, 0.05), 4),
        "sensibilidade": rng.choice([0.95, 0.97, 0.99]),
        "taxa_falso_positivo": rng.choice([0.03, 0.05, 0.08]),
        "talhoes_por_semana": rng.choice([800, 1200, 2000]),
    }
if __name__ == "__main__":
    import sys
    m = int(sys.argv[1])
    for linha in gerar_pomar(m):
        print(" ".join(linha))
    print(parametros_sensor(m))
