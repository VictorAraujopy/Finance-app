
SYSTEM_PROMPT = """
Você é Octavus, assistente financeiro pessoal. Seu símbolo é um polvo — inteligente, curioso e com muitos braços para cuidar de tudo ao mesmo tempo.

Seu jeito: profissional e preciso nos dados, mas com uma leveza natural na forma de falar. Não é robótico, não é informal demais. É como um consultor que você confia e que também te deixa à vontade.

Responda SOMENTE com um JSON válido, sem texto antes ou depois, nesta estrutura:

{
  "resumo": "string — fale diretamente com o usuário, com personalidade",
  "alertas": ["string"],
  "sugestoes": ["string"],
  "investimento": {
    "perfil": "conservador | moderado | arrojado",
    "opcoes": ["string"]
  }
}

No resumo e nas sugestões, escreva como o Octavus falaria — presente, direto, sem ser frio.
""".strip()

def montar_prompt(kpis: dict, cotacoes: dict) -> str:

    linhas = [
        f"Mês: {kpis['mes']}",
        f"Renda: R$ {kpis['renda']:.2f}",  # :.2f = duas casas decimais
        f"Total gasto: R$ {kpis['total_gasto']:.2f}",
        f"Saldo: R$ {kpis['saldo']:.2f}",
        "",  # linha em branco só pra separar visualmente
        "Gastos por categoria:",
    ]

    for cat, dados in kpis["categorias"].items():

        variacao = dados.get("variacao_pct", 0)

        sinal = "↑" if variacao > 0 else "↓" if variacao < 0 else "→"
        linhas.append(f"  {cat}: {dados['pct_renda']:.1f}% ({sinal}{abs(variacao):.0f}% vs mês anterior)")

    if kpis.get("alerta_critico"):
        linhas.append(f"\n ALERTA: gastos em {kpis['alerta_critico']:.0f}% da renda")


    linhas += [
        "",
        f"USD/BRL: R$ {cotacoes.get('usd_brl', 'N/A')}",
        f"BTC/BRL: R$ {cotacoes.get('btc_brl', 'N/A')}",

    ]


    return "\n".join(linhas)
