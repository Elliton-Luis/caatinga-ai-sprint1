# Caatinga.AI — Sprint 1

## 1. Identificação

- **Disciplina:** Inteligência Artificial — Prof. Ronierison Maciel — UniRios — 2026.2
- **Dupla:**
  - Arthur Henrique — matrícula 241.14.056
  - Elliton Luis — matrícula 241.14.013
- **Matrícula usada como semente (integrante mais velho):** `24114056`

## 2. O que este projeto faz

O Caatinga.AI é um agente que planeja a rota de um robô de inspeção em um pomar de manga
representado como uma grade 12×12, do portão `(0,0)` até o ponto de coleta `(11,11)`,
minimizando o custo de deslocamento entre talhões de custos diferentes (carreador firme,
solo encharcado e áreas bloqueadas). O projeto compara buscas cegas (BFS, DFS, UCS) e
informada (A* com três heurísticas), resolve um problema de busca local para escolher quais
talhões inspecionar com bateria limitada, implementa um pequeno sistema especialista com
encadeamento para trás para decidir o manejo de cada talhão, e aplica o Teorema de Bayes
para avaliar a confiabilidade do sensor óptico de pragas.

## 3. Como rodar

- **Python:** 3.10 ou superior
- **Ambiente virtual (recomendado):**

```bash
python -m venv venv
```

Ative conforme o SO:

| SO | Ativar | Desativar |
|---|---|---|
| Linux / macOS (bash/zsh) | `source venv/bin/activate` | `deactivate` |
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` | `deactivate` |
| Windows (cmd) | `venv\Scripts\activate.bat` | `deactivate` |

- **Instalação (com venv ativo):**

```bash
pip install -r requirements.txt
```

- **Execução (gera `pomar.txt`, `resultados.csv` e `grafico.png` do zero):**

```bash
python src/main.py 24114056
```

## 4. Tabela-resumo dos resultados (matrícula 24114056)

### Busca cega e A*

| Estratégia | Heurística | Custo da rota | Nº de passos | Nós expandidos | Fronteira máx. | Ótima em custo? |
|---|---|---|---|---|---|---|
| BFS | — | 49 | 22 | 123 | 13 | Não |
| DFS | — | 126 | 54 | 74 | 48 | Não |
| UCS | — | 34 | 22 | 123 | 19 | Sim |
| A* | h1 (=0) | 34 | 22 | 123 | 19 | Sim |
| A* | h2 (Manhattan) | 34 | 22 | 108 | 29 | Sim |
| A* | h3 (4×Manhattan) | 40 | 22 | 22 | 24 | Não |

### Busca local (K=15, 30 execuções)

| Algoritmo | Média | Desvio | Melhor |
|---|---|---|---|
| Subida de encosta | 35,77 | 0,05 | 35,8 |
| Têmpera simulada | 35,75 | 0,07 | 35,8 |

Tabelas completas (Bayes, sistema especialista, escalabilidade, auditoria do laudo) estão em
[`RELATORIO.md`](RELATORIO.md).

## 5. Ordem de expansão e reabertura de nós

- **Ordem de expansão dos vizinhos:** Norte, Sul, Leste, Oeste (`N, S, L, O`), fixa em todas
  as estratégias (`ORDEM_VIZINHOS` em `src/buscas.py`).
- **O A* reabre nós?** Sim. A implementação mantém `melhor_g[nó]` e, ao encontrar um `g`
  menor para um nó já expandido, atualiza `melhor_g` e reinsere o nó na fronteira (entradas
  obsoletas do heap são descartadas por comparação de `g` na hora do `pop`). Isso garante
  otimalidade mesmo com heurísticas não consistentes.

## 6. Mapa do repositório

| Arquivo | O que resolve |
|---|---|
| `src/gerador_pomar.py` | Gerador do pomar e dos parâmetros do sensor (intacto, não alterado) |
| `src/buscas.py` | BFS, DFS, UCS e A* (h1, h2, h3) |
| `src/busca_local.py` | Subida de encosta e têmpera simulada (Parte 3.4) |
| `src/especialista.py` | Sistema especialista com encadeamento para trás (Parte 4.1/4.2) |
| `src/bayes.py` | Cálculos de Bayes / PPV do sensor (Parte 4.3) |
| `src/main.py` | Roda tudo e gera `resultados/resultados.csv`, `resultados/grafico.png`, `resultados/pomar.txt` |
| [`RELATORIO.md`](RELATORIO.md) | Relatório completo com todas as tabelas das Partes 1 a 5 |
| [`ANEXO_IA.md`](ANEXO_IA.md) | Uso de assistentes de IA no trabalho (Parte 6) |

## 7. Limitações conhecidas

- A escalabilidade da Parte 2.4 foi medida até `n=3500` nesta máquina; a primeira falha
  foi da UCS em `n=3500` com 80,4 s (> 60 s, limite de tempo).
- O contraexemplo da "Liga de IA" (bônus DFS > 2× ótimo em grade 8×8) ainda não foi
  construído neste repositório.
- `requirements.txt` lista apenas `matplotlib`; nenhuma outra dependência externa é usada.
