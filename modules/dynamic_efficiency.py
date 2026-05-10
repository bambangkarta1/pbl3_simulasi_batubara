def dynamic_efficiency(
    choke_price,
    mc,
    discount_rate
):

    muc = choke_price - mc

    future_value = muc * (
        (1 + discount_rate) ** 10
    )

    return muc, future_value