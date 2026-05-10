def monopoly_market(price, mc):

    mr = price * 0.85

    profit = mr - mc

    if profit > 0:
        decision = "Kurangi output agar laba maksimum"

    else:
        decision = "Produksi tidak efisien"

    return mr, profit, decision