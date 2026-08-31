PONTOS_POR_REAL = 5  # 5 pontos = R$ 1,00

PONTOS_POR_CATEGORIA = {
    "econômico": 30,
    "economico": 30,
    "compacto": 30,
    "popular": 30,
    "suv": 30,
    "van": 30,
    "executivo": 50,
    "luxo": 50,
}

PONTOS_PADRAO = 30

PONTOS_AVALIACAO = 5

VOUCHERS_DISPONIVEIS = (
    {"valor_reais": 10, "pontos": 50, "descricao": "Voucher de abastecimento R$ 10"},
    {"valor_reais": 20, "pontos": 100, "descricao": "Voucher de abastecimento R$ 20"},
    {"valor_reais": 50, "pontos": 250, "descricao": "Voucher de abastecimento R$ 50"},
)


def pontos_por_categoria(categoria):
    if not categoria:
        return PONTOS_PADRAO
    return PONTOS_POR_CATEGORIA.get(str(categoria).strip().lower(), PONTOS_PADRAO)


def reais_equivalentes(pontos):
    return round((pontos or 0) / PONTOS_POR_REAL, 2)


def regras_fidelidade():
    return {
        "pontos_por_real": PONTOS_POR_REAL,
        "pontos_por_categoria": {
            "Econômico / Compacto / SUV / Van (populares)": 30,
            "Executivo / Luxo": 50,
        },
        "vouchers": list(VOUCHERS_DISPONIVEIS),
        "explicacao": "A cada 5 pontos você acumula o equivalente a R$ 1,00. Os pontos podem ser trocados por vouchers de abastecimento.",
    }
