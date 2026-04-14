from pages.calculations.rates import effective_monthly_rate


def reverse_engineer_fixed_amount(future_value: float, annual_rate: float, years: int) -> float:
    periods = 12 * years
    monthly_rate = effective_monthly_rate(annual_rate)

    if future_value <= 0 or periods <= 0:
        return 0
    if monthly_rate == 0:
        return future_value / periods
    return (future_value * monthly_rate) / ((1 + monthly_rate) ** periods - 1)
