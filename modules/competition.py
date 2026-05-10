def competitive_market(price, mc):

    profit = price - mc

    if profit > 0:
        decision = "Produksi meningkat"

    elif profit < 0:
        decision = "Produksi menurun"

    else:
        decision = "Pasar seimbang"

    return profit, decision