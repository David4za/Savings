import pandas as pd

from pages.calculations.rates import effective_monthly_rate


def future_value_annuity(
    monthly_contribution: float,
    lump_sums: tuple[tuple[float, int], ...],
    annual_rate: float,
    years: int,
) -> pd.DataFrame:
    """
    Return future value by year.

    Assumes the annual rate is an effective annual return, lump sums are
    invested at their chosen year, and fixed monthly savings are added at
    month-end.
    """
    periods_per_year = 12
    monthly_rate = effective_monthly_rate(annual_rate)
    values = []

    for year in range(1, years + 1):
        periods = periods_per_year * year
        annuity_value = (
            monthly_contribution * ((1 + monthly_rate) ** periods - 1) / monthly_rate
            if monthly_rate > 0
            else monthly_contribution * periods
        )
        lump_sum_value = 0
        for amount, years_from_now in lump_sums:
            lump_sum_periods = periods - years_from_now * periods_per_year
            if lump_sum_periods < 0:
                continue
            lump_sum_value += (
                amount * (1 + monthly_rate) ** lump_sum_periods
                if monthly_rate > 0
                else amount
            )
        total = annuity_value + lump_sum_value
        values.append(
            {
                "Year": year,
                "FV Annuity": annuity_value,
                "FV Lump Sum": lump_sum_value,
                "Total FV": total,
            }
        )

    return pd.DataFrame(values)


def inflation_adjustment(total_savings: float, inflation_rate: float, years: int) -> float:
    inflation_decimal = inflation_rate / 100
    return total_savings / ((1 + inflation_decimal) ** years)


def total_contributions(
    monthly_contribution: float,
    lump_sums: tuple[tuple[float, int], ...],
    years: int,
) -> float:
    lump_sum_contributions = sum(amount for amount, _ in lump_sums)
    return monthly_contribution * 12 * years + lump_sum_contributions
