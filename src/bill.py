def calculate_tneb_bill(units):
    if units <= 200:
        return 0
    elif units <= 400:
        return (units - 200) * 4.70
    elif units <= 500:
        return (200 * 4.70) + (units - 400) * 6.30

    # Above 500 units, the free allowance returns to 100 units.
    remaining_units = units - 100
    bill = 0
    for slab_units, rate in (
        (300, 4.70),
        (100, 6.30),
        (100, 8.40),
        (200, 9.45),
        (200, 10.50),
    ):
        charged_units = min(remaining_units, slab_units)
        bill += charged_units * rate
        remaining_units -= charged_units
        if remaining_units <= 0:
            break

    return bill + remaining_units * 11.55