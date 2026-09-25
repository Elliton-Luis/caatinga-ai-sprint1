try:
    from gerador_pomar import parametros_sensor
except ModuleNotFoundError:
    from src.gerador_pomar import parametros_sensor


def ppv(prevalencia, sensibilidade, fpr):
    p_pos_dado_infestado = sensibilidade
    p_infestado = prevalencia
    p_pos_dado_nao_infestado = fpr
    p_nao_infestado = 1 - prevalencia

    p_pos = (p_pos_dado_infestado * p_infestado +
             p_pos_dado_nao_infestado * p_nao_infestado)
    if p_pos <= 0:
        raise ValueError("P(+) == 0: prevalencia/sensibilidade/fpr degenerados")
    p_infestado_dado_pos = (p_pos_dado_infestado * p_infestado) / p_pos
    return p_infestado_dado_pos, p_pos


def relatorio(matricula):
    params = parametros_sensor(matricula)
    prev = params["prevalencia"]
    sens = params["sensibilidade"]
    fpr = params["taxa_falso_positivo"]
    talhoes_semana = params["talhoes_por_semana"]

    print("Parametros do sensor:", params)
    print()

    # (a)
    valor_ppv, p_pos = ppv(prev, sens, fpr)
    print("(a) Teorema de Bayes:")
    print(f"    P(+) = {sens}*{prev} + {fpr}*{1-prev:.4f} = {p_pos:.6f}")
    print(f"    P(infestado|+) = ({sens}*{prev}) / {p_pos:.6f} = {valor_ppv:.6f}")
    print()

    # (b)
    falsos_a_cada_100 = round((1 - valor_ppv) * 100, 1)
    print(f"(b) A cada 100 alertas do meu sistema, cerca de {falsos_a_cada_100} serao falsos.")
    print()

    # (c)
    alertas_por_semana = talhoes_semana * p_pos
    falsos_por_semana = alertas_por_semana * (1 - valor_ppv)
    minutos_por_semana = falsos_por_semana * 12
    horas_por_semana = minutos_por_semana / 60
    print(f"(c) Com {talhoes_semana} talhoes/semana inspecionados pelo sensor:")
    print(f"    alertas/semana = {talhoes_semana} * {p_pos:.6f} = {alertas_por_semana:.2f}")
    print(f"    alertas falsos/semana = {alertas_por_semana:.2f} * (1-{valor_ppv:.4f}) = {falsos_por_semana:.2f}")
    print(f"    tempo perdido = {falsos_por_semana:.2f} * 12 min = {minutos_por_semana:.1f} min "
          f"= {horas_por_semana:.2f} h/semana")
    print()

    # (d)
    nova_sens = 0.999
    novo_ppv, novo_p_pos = ppv(prev, nova_sens, fpr)
    print(f"(d) Aumentando sensibilidade para {nova_sens} (fpr mantido em {fpr}):")
    print(f"    novo P(infestado|+) = {novo_ppv:.6f}  (era {valor_ppv:.6f})")
    melhora_pp = (novo_ppv - valor_ppv) * 100
    print(f"    melhora de {melhora_pp:.3f} pontos percentuais no PPV")

    return {
        "params": params, "ppv": valor_ppv, "p_pos": p_pos,
        "falsos_a_cada_100": falsos_a_cada_100,
        "alertas_por_semana": alertas_por_semana,
        "falsos_por_semana": falsos_por_semana,
        "horas_por_semana": horas_por_semana,
        "novo_ppv": novo_ppv, "novo_p_pos": novo_p_pos,
    }


if __name__ == "__main__":
    import sys
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 24114056
    relatorio(m)
