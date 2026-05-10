def oligopoly_market(price, mc, firms):

    share = 1 / firms

    adjusted_price = price * (
        1 - (0.05 * firms)
    )

    profit = adjusted_price - mc

    return adjusted_price, profit, share