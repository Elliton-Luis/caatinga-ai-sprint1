# ANEXO_IA — Uso de assistentes de IA

## A.1 — Ferramentas

- Muse Spark 1.3 (Opencode)
- Claude (Anthropic)

Uso por parte (a IA participou de tudo, seja como escritora ou analista de código):

- `src/buscas.py` (Parte 2 e 3.1): implementação de BFS, DFS, UCS e A* com os 4 contadores.
- `src/bayes.py` (Parte 4.3): implementação de `ppv()` e `relatorio()` com a semente 24114056.
- `src/especialista.py` (Parte 4.1 e 4.2): implementação das 7 regras, `prova()` e `explicar()`.

## A.2 — Prompts na íntegra e respostas recebidas

### A.2 - Prompt 1

> Considere os requisitos do arquivo `Atividade-Pratica.pdf`,
> dentro do arquivo `buscas.py`, implemente as buscas BFS, DFS,
> UCS e A*, avalie a implementação conforme os critérios do
> documento, após isso, me retorne uma avaliação de quais pontos
> dos requisitos foram cumpridos.

### Resposta - Prompt 1

- Houve alterações somente no arquivo requerido, `buscas.py`, onde as funções foram implementadas. A implementação será posteriormente verificada por meio dos experimentos e resultados exigidos pela atividade.

- Esse foi o retorno obtido pela IA:

>Avaliação por requisito
>Cumpridos (dentro de buscas.py):
>- §2 ordem de vizinhos declarada e uniforme; §4 item 2.2 instrumentação dos 4 contadores; BFS/DFS/UCS funcionais; §5 item 3.1 A* com h1/h2/h3 e suporte a reabertura.
>Ainda pendentes (fora do escopo de buscas.py, zeram/descontam se não feitos):
>1. Relatório/tabelas: preencher tabelas 2.2 e 3.1 com sua semente real, responder 2.3 (custo não-uniforme viola hipótese da Aula 03), 3.2 (prova de h2 via custo mínimo 1 + par de coordenadas onde h3 superestima), 3.3 (igualdade ≠ prova de admissibilidade).
>2. Item 2.4: experimento n=12→40→100 até falha >60s/memória, ligado à fórmula da Aula 03 — não feito.
>3. Item 3.4 + src/busca_local.py, src/especialista.py, src/bayes.py, src/main.py: inexistentes. Sem python src/main.py <matricula> o projeto perde 1,0 pt (§11).
>4. Repositório: faltam RELATORIO.md, resultados.csv, grafico.png, pomar.txt, README completo (§9.2: identificação, comando copiável, tabela-resumo, ordem, reabertura, mapa, limitações), ANEXO_IA.md específico (sem ele, não corrigido), 8 commits de ambos os membros, gerador_pomar.py intacto — este último ✅ ok, não alterado.
>5. Descontos a evitar: declarar ordem no README (−0,3), eixos do gráfico e unidades (−0,2 cada).
>Resumo: núcleo de busca correto e aferido; o risco agora é todo de entrega (relatório, artefatos, README, ANEXO_IA, main.py).

### A.2 - Prompt 2

> Considere os requisitos da Parte 4.3 do arquivo `Atividade-Pratica.pdf`, dentro do arquivo `bayes.py`, implemente os cálculos de Bayes com os parâmetros da minha semente (matrícula 24114056), avalie a implementação conforme os critérios do documento, após isso, me retorne uma avaliação de quais pontos dos requisitos foram cumpridos.

### Resposta - Prompt 2

- Houve alterações somente no arquivo requerido, `bayes.py`, implementando `ppv()` e `relatorio()` a partir de `parametros_sensor()` do arquivo `gerador_pomar.py`.

- Esse foi o retorno obtido pela IA:

>Avaliação por requisito
>Cumpridos (dentro de bayes.py):
>- §4.3(a) cálculo de P(infestado|+) via Teorema de Bayes, com a substituição explícita na fórmula; §4.3(b) conversão para "a cada 100 alertas, quantos serão falsos"; §4.3(c) alertas/semana, alertas falsos/semana e horas/semana perdidas, a partir de `talhoes_por_semana`; §4.3(d) recálculo do PPV com sensibilidade 99,9% mantendo a taxa de falso positivo, com comparação numérica ao valor original.
>Ainda pendentes (fora do escopo de bayes.py, zeram/descontam se não feitos):
>1. Relatório: transcrever os quatro parâmetros do sensor e os resultados de (a)-(d) para RELATORIO.md, com a análise textual de por que aumentar a sensibilidade não resolve o problema (dominância da taxa de falso positivo quando a prevalência é baixa) e qual parâmetro mexeria de fato (§4.3(d)) — cálculo pronto, redação ainda não.
>2. Item 4.4: decisão que deve ficar em regra explícita, não em modelo aprendido — é resposta textual/justificativa no relatório, não um cálculo de bayes.py.
>3. Item 4.1/4.2: sistema especialista com encadeamento para trás (`src/especialista.py`) — módulo separado, não coberto por este prompt.
>4. Parte 5 (auditoria do laudo): as afirmações 3 e 4 do fornecedor dependem diretamente destes números (PPV real vs. sensibilidade alegada; recálculo de duas confirmações positivas) — ainda precisam ser redigidas no relatório usando esses valores como evidência numérica.
>Resumo: cálculos de Bayes corretos e aferidos com a semente real; o risco agora é a redação/análise no relatório e a conexão desses números com a Parte 5 (auditoria).

### A.2 - Prompt 3

> Considere os requisitos da Parte 4.1 e 4.2 do arquivo `Atividade-Pratica.pdf`, dentro do arquivo `especialista.py`, implemente de 5 a 8 regras SE...ENTÃO e um motor de encadeamento para trás que imprima a cadeia de regras que sustentou a conclusão, avalie a implementação conforme os critérios do documento, após isso, me retorne uma avaliação de quais pontos dos requisitos foram cumpridos.

### Resposta - Prompt 3

- Houve alterações somente no arquivo requerido, `especialista.py`, implementando 7 regras (`REGRAS`), a função `prova()` (encadeamento para trás recursivo) e `explicar()` (imprime fatos, conclusão e trilha de regras).

- Esse foi o retorno obtido pela IA:

>Avaliação por requisito
>Cumpridos (dentro de especialista.py):
>- §4.1 base com 7 regras (dentro do intervalo 5-8 pedido), no formato SE...ENTAO; encadeamento para trás funcional via `prova()`, com suporte a antecedentes negados (`not:`) e proteção contra ciclo (`visitados`); impressão da cadeia de regras que sustentou a conclusão (`explicar()`), respondendo o "por que você concluiu isso?" da Aula 05.
>- §4.2 caso legítimo que a base classifica errado sem R2 (sensor positivo + histórico de infestação, sem armadilha/umidade), com traço de execução antes (conclusão errada: False) e depois (R2 adicionada, conclusão correta), sem contradizer as demais regras.
>Ainda pendentes (fora do escopo de especialista.py, zeram/descontam se não feitos):
>1. Relatório: transcrever as 7 regras, o exemplo de execução com a trilha impressa, e o par de traços antes/depois de 4.2 para RELATORIO.md — o motor está pronto e testado, falta a redação.
>2. Item 4.3 (bayes.py) e 4.4: decisão que deve ficar em regra explícita — 4.4 é resposta textual/justificativa (ex.: aplicação de defensivo), não faz parte deste módulo.
>3. Cobertura da base: as 7 regras cobrem os casos usados nos testes, mas não há uma verificação sistemática de que toda combinação relevante de fatos (armadilha, sensor, histórico, umidade, dias de pulverização, chuva) leve a alguma conclusão — risco de "buracos" na base não testados que só apareceriam na arguição com uma semente nova.
>4. Parte 5 (auditoria do laudo): nenhuma das 5 afirmações do fornecedor trata do sistema especialista diretamente, então este módulo não alimenta a Parte 5 como bayes.py e buscas.py alimentam.
>Resumo: motor de encadeamento para trás e regras corretos e testados nos dois casos exigidos (4.1 e 4.2); o risco agora é cobertura de casos não testados e a transcrição para o relatório.

## A.3 — Erro do assistente com evidência experimental

Afirmação do assistente:

Afirmou que usar um conjunto global de visitados com visitados.add(objetivo) sem remoção tratava ciclos de forma correta e eficiente no encadeamento para trás de especialista.py.

O erro:

Confundiu detecção de ciclo com nós compartilhados em grafos de dedução (estrutura em diamante, como $A \leftarrow B \land C$, onde $B$ e $C$ dependem do mesmo fato intermediário $D$). Ao provar $B$, $D$ ficava gravado permanentemente em visitados; ao tentar provar $C$, o algoritmo considerava $D$ um ciclo e abortava a dedução prematuramente.

Evidência experimental:

Ao rodar o contraexemplo abaixo, a implementação da IA falhou:

```python
regras = [("RD", ["E"], "D"), ("RB", ["D"], "B"), ("RC", ["D"], "C"), ("RA", ["B", "C"], "A")]

prova("A", {"E": True}, regras)
# - Retorno da IA: (False, []) | Esperado: (True, [...])
```