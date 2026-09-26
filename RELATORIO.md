# Relatório — Caatinga.AI, Sprint 1

Disciplina: Inteligência Artificial — Prof. Ronierison Maciel — UniRios — 2026.2
Dupla: Arthur Henrique (matrícula 241.14.056) e Elliton Luis (matrícula 241.14.013)
Matrícula-semente: **24114056**
Todos os números abaixo vêm da execução de `python src/main.py 24114056`.

---

## Parte 1 — O agente antes do código

### 1.1 Ficha PEAS

| Componente | Descrição |
|---|---|
| **P — Performance** | Custo total de deslocamento da rota (unidades de custo, conforme `Custo do caminho`) somado ao tempo gasto perseguindo alertas falsos (12 min por alerta falso), medido por rota completa/semana. Unidade: *unidades de custo + minutos/semana*. |
| **E — Ambiente** | Grade 12×12 do pomar (talhões `.`, `~`, `#`), leituras do sensor óptico, histórico de infestação por talhão, previsão de chuva 24h, nível de bateria (6h). |
| **A — Atuadores** | Motor/rodas para mover nas 4 direções ortogonais, disparo do sensor óptico, envio de alerta ao agrônomo. |
| **S — Sensores** | Sensor óptico de pragas, leitor de posição na grade, leitor do tipo de terreno do talhão atual, medidor de bateria, sensor/API de previsão de chuva. |

A métrica P é mensurável (unidades de custo + minutos), não um adjetivo como "eficiente".

### 1.2 Classificação do ambiente

| Dimensão | Classificação | Trecho do cenário que sustenta |
|---|---|---|
| Observável | **Parcialmente observável** (discutível) | O layout de terreno é conhecido via `gerador_pomar.py`, mas a presença real de praga em cada talhão só é conhecida após a leitura do "sensor óptico de detecção de pragas" |
| Determinístico | **Estocástico** | O sensor tem "sensibilidade" e "taxa de falso positivo" — a mesma ação (ler o sensor) pode dar resultados diferentes da realidade |
| Episódico/Sequencial | **Sequencial** | Cada movimento consome bateria e define a posição para a próxima decisão; o custo do caminho é acumulado |
| Estático/Dinâmico | **Estático** | Nada no enunciado indica que o layout de terrenos muda enquanto o agente se move dentro de uma mesma inspeção |
| Discreto/Contínuo | **Discreto** | Grade de 144 posições, 4 ações possíveis por estado, custo de passo em valores inteiros |
| Agente único/Multiagente | **Agente único** (discutível) | O enunciado descreve "o agente" no singular, mas não diz se outras equipes da cooperativa operam no mesmo pomar simultaneamente |

**Duas dimensões discutíveis:**
- *Observável* — depende de o agente receber o mapa completo de terrenos antes de navegar (aí seria observável quanto ao terreno, só não quanto à praga) ou descobrir o terreno célula a célula em tempo real (aí seria parcialmente observável também no terreno). O enunciado não deixa isso explícito.
- *Agente único* — depende de haver ou não mais de um robô/equipe atuando no mesmo pomar ao mesmo tempo, informação que o enunciado não fornece.

### 1.3 Tipo de agente

**Agente baseado em utilidade.** Um agente puramente baseado em objetivos bastaria se a única meta fosse "chegar a (11,11)", mas o próprio enunciado (Parte 3.3) pede para trocar garantia de otimalidade por velocidade sob uma condição de negócio — isso é uma troca de utilidade (custo de rota vs. tempo de resposta vs. confiabilidade do alerta), não uma simples satisfação de objetivo. O agente precisa comparar quantitativamente diferentes rotas e diferentes heurísticas, o que só faz sentido com uma função de utilidade.

### 1.4 Métrica perversa

**Métrica proposta pelo cliente:** "número de talhões inspecionados por hora".

**Comportamento ruim que o agente aprenderia:** para maximizar a contagem de talhões/hora, o agente passaria a circular preferencialmente pelos talhões `.` (custo 1) próximos ao portão, evitando entrar nos talhões `~` (custo 4, solo encharcado/linhas de irrigação) — justamente onde a umidade favorece a proliferação de pragas. No nosso pomar, isso apareceria nos 52 talhões `~` (36% da grade): o agente otimizado por essa métrica tenderia a contorná-los sempre que uma rota alternativa mais barata existisse, deixando de inspecionar a área de maior risco.

**Correção:** substituir por "número de talhões efetivamente inspecionados, ponderado pelo histórico de risco de infestação, por unidade de custo gasto" — isso obriga o agente a cobrir também talhões caros/de risco, não só os baratos.

---

## Parte 2 — Formulação e busca cega

### 2.1 Componentes do problema de busca

- **Estado inicial:** posição `(0, 0)`.
- **Ações:** mover para Norte, Sul, Leste ou Oeste (para uma célula adjacente dentro da grade e não bloqueada).
- **Modelo de transição:** `resultado((r,c), ação) = (r±1, c)` ou `(r, c±1)`, válido apenas se a célula destino existir e não for `#`.
- **Teste de objetivo:** posição atual `== (11, 11)`.
- **Custo do caminho:** soma dos custos de entrada de cada talhão visitado (exceto o inicial): 1 para `.`, 4 para `~`.

**Tamanho do espaço de estados:** o estado é apenas a posição do agente na grade, logo o número de estados é o número de células não bloqueadas. Para a matrícula 24114056: grade 12×12 = 144 células, das quais 19 são `#` → **125 estados**.

### 2.2 Resultados (ordem de expansão N, S, L, O)

| Estratégia | Custo da rota | Nº de passos | Nós expandidos | Fronteira máx. | Ótima em custo? |
|---|---|---|---|---|---|
| BFS | 49 | 22 | 123 | 13 | Não |
| DFS | 126 | 54 | 74 | 48 | Não |
| UCS | 34 | 22 | 123 | 19 | Sim |

### 2.3 Por que a BFS não é um bug

A BFS devolveu uma rota com o **mesmo número de passos** da UCS (22), mas **mais cara** (49 vs. 34). Isso não é bug: a hipótese violada é a de **custo de passo uniforme** da Aula 03. BFS garante otimalidade apenas quando todas as ações têm o mesmo custo — nesse caso, encontrar o caminho com menos arestas é o mesmo que encontrar o de menor custo. Aqui, entrar num talhão `.` custa 1 e num `~` custa 4, então BFS (que só minimiza número de passos) pode escolher uma sequência de 22 passos com mais talhões caros.

Conferindo a composição real dos caminhos:

| Estratégia | Passos | Custo | Talhões `~` (custo 4) | Talhões `.` (custo 1) |
|---|---|---|---|---|
| BFS | 22 | 49 | 9 | 13 |
| UCS | 22 | 34 | 4 | 18 |

Mesmo número de passos, mas a BFS passou por mais que o dobro de talhões encharcados que a UCS — exatamente a assinatura de uma busca que ignora custo.

### 2.4 Escalabilidade (aumentando n)

| n | BFS (tempo) | DFS (tempo) | UCS (tempo) |
|---|---|---|---|
| 12 | 0,000 s | 0,000 s | 0,000 s |
| 40 | 0,002 s | 0,001 s | 0,003 s |
| 100 | 0,013 s | 0,001 s | 0,020 s |
| 200 | 0,044 s | 0,008 s | 0,090 s |
| 400 | 0,216 s | 0,021 s | 0,503 s |
| 800 | 1,103 s | 0,116 s | 2,025 s |
| 1500 | 3,752 s | 4,089 s | 7,986 s |
| 2500 | 10,897 s | 0,482 s | 24,395 s |
| 3000 | 26,4 s | 1,270 s | 59,5 s |
| 3500 | 35,6 s | 1,292 s | 80,4 s **FALHA (> 60 s)** |

A primeira falha foi da **UCS em `n=3500`, com 80,4 s (> 60 s)** — limite de **tempo** atingido. Nenhuma estourou memória ou pilha até lá (a DFS aqui é **iterativa**, com pilha explícita em lista, não recursiva — por isso não sofre `RecursionError`). A UCS cresce mais rápido que a BFS porque, além de expandir um número de nós parecido com o da BFS (o grid é denso e o objetivo fica no canto oposto), cada expansão custa `O(log |fronteira|)` por causa do heap de prioridade, contra `O(1)` amortizado da fila da BFS.

Isso se relaciona com a fórmula da Aula 03 de complexidade de busca em espaço `O(b^d)`: aqui `b≈4` (vizinhos) e o espaço de estados cresce com `n²`, então o custo de busca cresce quadraticamente com `n`, e o overhead logarítmico da fila de prioridade da UCS agrava isso a cada expansão.

---

## Parte 3 — Busca informada

### 3.1 A* com três heurísticas

| Heurística | Custo da rota | Nós expandidos | Admissível? |
|---|---|---|---|
| h1 (= 0) | 34 | 123 | Sim (trivialmente — nunca superestima) |
| h2 (Manhattan) | 34 | 108 | Sim (ver 3.2) |
| h3 (4×Manhattan) | 40 | 22 | Não (ver 3.2) |

### 3.2 Admissibilidade

**h2 é admissível.** O custo mínimo para entrar em qualquer talhão passável é 1 (talhão `.`). A distância de Manhattan é o número mínimo de passos necessários para ir de um ponto a outro numa grade sem obstáculos. Logo:

`custo_real(n, objetivo) = Σ custo_entrada(célula) ≥ Σ 1 = nº de passos do caminho real ≥ distância_Manhattan(n, objetivo) = h2(n)`

(a última desigualdade vale porque obstáculos só podem aumentar o número de passos necessário em relação ao caso sem obstáculos, nunca diminuir). Como `h2(n)` nunca é maior que o custo real, h2 é admissível.

**h3 superestima.** Par de talhões concreto: partindo de `(0, 0)` até o objetivo `(11, 11)`, o custo real ótimo (UCS) é **34**, mas `h3(0,0) = 4 × Manhattan((0,0),(11,11)) = 4 × 22 = 88`. Como `88 > 34`, h3 superestima o custo real nesse par — logo não é admissível.

### 3.3 A pergunta que separa quem rodou de quem entendeu

O custo de h3 (**40**) ficou **maior** que o da UCS (**34**).

- **Perda percentual:** `(40 − 34) / 34 = 17,6%` de rota mais cara.
- **Nós "comprados" com essa perda:** UCS expandiu 123 nós; h3 expandiu apenas 22 — uma redução de **101 nós** (≈ 82% menos expansões).

**Condição de negócio verificável para trocar otimalidade por velocidade:** vale a pena usar h3 quando o custo operacional de cada nó expandido (tempo de CPU/bateria do robô embarcado) for maior que o custo equivalente da rota extra — por exemplo, se o agente precisa decidir a rota em menos de 1 segundo antes de perder conectividade com a base, ou se cada nó expandido consome mais energia de bateria do que os 17,6% de deslocamento extra representam em custo operacional total.

### 3.4 Busca local

**Modelagem:** estado = conjunto de K=15 talhões livres a inspecionar; vizinhança = trocar um talhão do conjunto por outro fora dele; função objetivo = soma do valor de cada talhão escolhido (`~`=3, `.`=1) menos uma penalidade de deslocamento (`0,1 × (linha+coluna)` de cada talhão escolhido), favorecendo talhões valiosos e próximos do portão.

| Algoritmo | Média (30 execuções) | Desvio | Melhor |
|---|---|---|---|
| Subida de encosta | 35,77 | 0,05 | 35,8 |
| Têmpera simulada | 35,75 | 0,07 | 35,8 |

A Aula 04 diz que aceitar piora de propósito (têmpera simulada) ajuda a escapar de ótimos locais. Nos nossos 30 resultados, o desvio-padrão da têmpera (0,068) é maior que o da subida de encosta (0,048) — sinal de que a têmpera explora mais estados diferentes (às vezes aceitando pioras), enquanto a subida de encosta converge de forma mais determinística para o primeiro ótimo local que encontra e para lá.

---

## Parte 4 — Regras e incerteza

Parâmetros do sensor para a matrícula 24114056: `prevalência=0,0168`, `sensibilidade=0,99`, `taxa_falso_positivo=0,03`, `talhões_por_semana=800`.

### 4.1 Sistema especialista (7 regras, encadeamento para trás)

```
R1: SE armadilha_positiva E umidade_alta E dias_desde_pulverizacao_maior_14 ENTAO inspecionar_prioridade_alta
R2: SE sensor_optico_positivo E historico_talhao_infestado ENTAO inspecionar_prioridade_alta
R3: SE sensor_optico_positivo E not:historico_talhao_infestado E umidade_baixa ENTAO monitorar
R4: SE lesao_foliar_visivel E praga_identificada_em_talhao_vizinho ENTAO aplicar_defensivo
R5: SE dias_desde_pulverizacao_maior_14 E not:sensor_optico_positivo E not:armadilha_positiva E umidade_alta ENTAO monitorar
R6: SE not:sensor_optico_positivo E not:armadilha_positiva E dias_desde_pulverizacao_maior_14 E not:umidade_alta ENTAO ignorar
R7: SE inspecionar_prioridade_alta E chuva_prevista_24h ENTAO aplicar_defensivo
```

Traço para `armadilha_positiva=True, umidade_alta=True, dias_desde_pulverizacao_maior_14=True`:

```
Conclusao 'inspecionar_prioridade_alta': SIM
Cadeia de regras que sustentou a conclusao:
  - R1: SE armadilha_positiva E umidade_alta E dias_desde_pulverizacao_maior_14 ENTAO inspecionar_prioridade_alta
```

### 4.2 Quebrando a própria base

**Caso legítimo mal classificado sem R2:** talhão com `sensor_optico_positivo=True` e `historico_talhao_infestado=True`, mas sem armadilha e sem umidade alta. Sem a regra R2, nenhuma regra cobre esse padrão:

```
--- ANTES (sem R2) ---
Conclusao: False — ERRADO: sensor positivo + histórico de infestação deveria ser prioridade alta

--- DEPOIS (com R2) ---
Conclusao 'inspecionar_prioridade_alta': SIM
  - R2: SE sensor_optico_positivo E historico_talhao_infestado ENTAO inspecionar_prioridade_alta
```

R2 corrige o caso sem contradizer R1, R3–R7 (antecedentes diferentes, mesmo consequente).

### 4.3 Bayes com os nossos números

**(a)** `P(+) = 0,99×0,0168 + 0,03×0,9832 = 0,046128`
`P(infestado | +) = (0,99×0,0168) / 0,046128 = 0,360562` → **≈ 36,06%**

**(b)** A cada 100 alertas do sistema, cerca de **63,9** serão falsos.

**(c)** Com 800 talhões/semana inspecionados pelo sensor:
- alertas/semana = `800 × 0,046128 = 36,90`
- alertas falsos/semana = `36,90 × (1 − 0,3606) = 23,60`
- tempo perdido = `23,60 × 12 min = 283,2 min = 4,72 h/semana`

**(d)** Aumentando a sensibilidade para 99,9% (mantendo FPR=3%): novo PPV = **36,27%** (era 36,06%) — melhora de apenas **0,21 ponto percentual**. O problema **não** melhora de forma relevante, porque a prevalência (1,68%) domina a conta, não a sensibilidade. O parâmetro que de fato deveria ser reduzido é a **taxa de falsos positivos** (FPR): com prevalência tão baixa, é o FPR que mais influencia o PPV — reduzir de 3% para, por exemplo, 0,5% teria impacto muito maior no PPV do que qualquer ganho de sensibilidade.

### 4.4 A regra que salva o modelo

**Decisão que deve ficar em regra explícita:** a decisão de **aplicar defensivo químico** (R4/R7) nunca deve vir de um modelo aprendido (ex.: uma rede neural treinada em histórico), e sim de regras explícitas com os antecedentes documentados. Justificativa de **auditabilidade**: aplicação de agrotóxico tem implicações regulatórias, de segurança alimentar e de rastreabilidade — a cooperativa precisa poder mostrar, para um órgão fiscalizador ou para o comprador da manga, exatamente qual conjunto de evidências (lesão foliar visível + praga em talhão vizinho, por exemplo) motivou cada aplicação. Um modelo aprendido não oferece essa cadeia de justificativa verificável linha a linha.

---

## Parte 5 — Auditoria do laudo do fornecedor (AgroVision)

| # | Afirmação | Veredito | Justificativa (número medido) |
|---|---|---|---|
| 1 | "A* com h=4×Manhattan é comprovadamente ótimo" | **Incorreta** | A* só é ótimo com heurística admissível. h3 não é admissível (h3(0,0)=88 > custo real=34, Parte 3.2) e de fato devolveu rota de custo **40**, 17,6% mais cara que o ótimo (34, Parte 3.3). |
| 2 | "BFS→A* reduziu custo, provando que a heurística melhora a qualidade" | **Parcialmente correta** | A queda de custo (49→34 = 30,6%, não 38% como alegado) vem de trocar uma busca cega por uma busca sensível a custo — a **UCS sem heurística nenhuma** já atinge o mesmo custo ótimo 34 (Parte 2.2). A heurística (h2) só reduz **nós expandidos** (123→108, Parte 3.1), não muda o custo da rota ótima. |
| 3 | "Sensibilidade de 99% → 99% dos apontamentos são infestação real" | **Incorreta** | Confunde sensibilidade com PPV. Com nossos parâmetros, `P(infestado\|+) = 36,06%` (Parte 4.3a), bem distante de 99%. |
| 4 | "Dois testes positivos seguidos → confiança > 99%" | **Parcialmente correta** | Repetir o teste e atualizar o prior bayesiano de fato eleva a confiança (mecanismo correto), mas com nossos números o PPV após dois positivos sucessivos fica em **≈ 94,9%**, não acima de 99% — e a conta assume independência entre os dois testes, o que raramente vale para o mesmo sensor físico medindo o mesmo talhão nas mesmas condições. |
| 5 | "DFS usa menos memória e, como o ambiente é estático/observável, é suficiente" | **Incorreta** | Em teoria DFS usa menos memória (O(d)), mas nesta grade mediu fronteira máx. 48 vs. 19 da UCS (Parte 2.2), ou seja, maior; além disso "estático e observável" não tem relação com qualidade da solução — DFS devolveu custo **126**, 3,7× o ótimo (34), inaceitável para uma rota de produção. |

**Recomendação:** **contratar com ressalvas.** O laudo mistura afirmações corretas (uso de A*, uso de sensibilidade) com conclusões estatística e algoritmicamente erradas (confundir admissibilidade com otimalidade garantida, confundir sensibilidade com PPV). A condição técnica que mudaria a resposta: a AgroVision reapresentar a proposta com (i) prova de admissibilidade da heurística usada e (ii) o PPV real do sensor calculado com a prevalência real do pomar, não apenas a sensibilidade isolada.

---

*Números reproduzíveis executando `python src/main.py 24114056` a partir da raiz do repositório.*
