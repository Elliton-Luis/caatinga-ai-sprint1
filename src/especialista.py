REGRAS = [
    ("R1", ["armadilha_positiva", "umidade_alta", "dias_desde_pulverizacao_maior_14"],
     "inspecionar_prioridade_alta"),
    ("R2", ["sensor_optico_positivo", "historico_talhao_infestado"],
     "inspecionar_prioridade_alta"),
    ("R3", ["sensor_optico_positivo", "not:historico_talhao_infestado", "umidade_baixa"],
     "monitorar"),
    ("R4", ["lesao_foliar_visivel", "praga_identificada_em_talhao_vizinho"],
     "aplicar_defensivo"),
    ("R5", ["dias_desde_pulverizacao_maior_14", "not:sensor_optico_positivo",
            "not:armadilha_positiva"],
     "monitorar"),
    ("R6", ["not:sensor_optico_positivo", "not:armadilha_positiva",
            "dias_desde_pulverizacao_maior_14", "not:umidade_alta"],
     "ignorar"),
    ("R7", ["inspecionar_prioridade_alta", "chuva_prevista_24h"],
     "aplicar_defensivo"),
]


def _negado(nome):
    return nome.startswith("not:")


def _base(nome):
    return nome[4:] if _negado(nome) else nome


def prova(objetivo, fatos, regras=REGRAS, trilha=None, visitados=None):
    if trilha is None:
        trilha = []
    if visitados is None:
        visitados = set()

    if objetivo in fatos:
        return fatos[objetivo], trilha

    if objetivo in visitados:
        return False, trilha  # evita ciclo
    visitados.add(objetivo)

    for nome_regra, antecedentes, consequente in regras:
        if consequente != objetivo:
            continue
        todos_verdadeiros = True
        sub_trilha = []
        for ant in antecedentes:
            alvo = _base(ant)
            ok, t2 = prova(alvo, fatos, regras, [], visitados)
            if _negado(ant):
                ok = not ok
            sub_trilha.extend(t2)
            if not ok:
                todos_verdadeiros = False
                break
        if todos_verdadeiros:
            sub_trilha.append(f"{nome_regra}: SE {' E '.join(antecedentes)} ENTAO {consequente}")
            trilha.extend(sub_trilha)
            return True, trilha

    return False, trilha


def explicar(objetivo_desejado, fatos):
    ok, trilha = prova(objetivo_desejado, fatos)
    print(f"Fatos de entrada: {fatos}")
    print(f"Conclusao '{objetivo_desejado}': {'SIM' if ok else 'NAO provada com estes fatos'}")
    if ok:
        print("Cadeia de regras que sustentou a conclusao:")
        for passo in trilha:
            print("  -", passo)
    print()
    return ok


if __name__ == "__main__":
    # Caso 1: deve concluir inspecionar_prioridade_alta via R1
    explicar("inspecionar_prioridade_alta", {
        "armadilha_positiva": True,
        "umidade_alta": True,
        "dias_desde_pulverizacao_maior_14": True,
    })

    # 4.2 - Caso legitimo que a base classifica errado ANTES da correcao:
    # um talhao com sensor optico positivo e historico de infestacao,
    # mas SEM armadilha e SEM os dias de pulverizacao > 14 (ou seja,
    # nenhuma das regras R1/R2 originais cobria "sensor + historico"
    # se R2 nao existisse). Simulamos isso removendo R2 e mostrando que
    # a base fica "cega" para esse caso; depois religamos R2.
    regras_sem_r2 = [r for r in REGRAS if r[0] != "R2"]
    print("--- ANTES da correcao (sem R2) ---")
    ok_antes, trilha_antes = prova("inspecionar_prioridade_alta", {
        "sensor_optico_positivo": True,
        "historico_talhao_infestado": True,
        "armadilha_positiva": False,
        "umidade_alta": False,
    }, regras=regras_sem_r2)
    print("Conclusao (sem R2):", ok_antes, "- ERRADO: talhao com sensor positivo E "
          "historico de infestacao deveria ser prioridade alta.")

    print("--- DEPOIS da correcao (com R2) ---")
    explicar("inspecionar_prioridade_alta", {
        "sensor_optico_positivo": True,
        "historico_talhao_infestado": True,
        "armadilha_positiva": False,
        "umidade_alta": False,
    })
