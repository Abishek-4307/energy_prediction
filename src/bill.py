def calculate_tneb_bill(units):
    if units <= 100:
        return 0
    elif units <= 200:
        return (units - 100) * 2.25
    elif units <= 400:
        return (100 * 2.25) + (units - 200) * 4.50
    elif units <= 500:
        return (100 * 2.25) + (200 * 4.50) + (units - 400) * 6.00
    else:
        return (100 * 2.25) + (200 * 4.50) + (100 * 6.00) + (units - 500) * 8.00