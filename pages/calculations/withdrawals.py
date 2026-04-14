import pandas as pd

from pages.calculations.rates import effective_monthly_rate


def withdraw_analysis(
    monthly_withdraw: float,
    total_savings: float,
    interest: float,
    inflation: float,
) -> pd.DataFrame:
    inflation_decimal = inflation / 100
    monthly_interest = effective_monthly_rate(interest)
    balance = total_savings
    months = 0
    total_withdrawn = 0
    balances = []

    if monthly_withdraw <= 0 or total_savings <= 0:
        return pd.DataFrame(
            columns=[
                "Year",
                "Balance",
                "Adjusted Balance",
                "Month",
                "Total Withdrawn",
            ]
        )

    while balance > 0:
        if months >= 1200:
            break

        withdrawal_amount = min(monthly_withdraw, balance)
        balance -= withdrawal_amount
        total_withdrawn += withdrawal_amount
        balance *= 1 + monthly_interest
        months += 1

        balances.append(
            {
                "Month": months,
                "Year": (months - 1) // 12 + 1,
                "Balance": balance,
                "Adjusted Balance": balance / (1 + inflation_decimal) ** (months / 12),
                "Total Withdrawn": total_withdrawn,
            }
        )

    df = pd.DataFrame(balances)
    return (
        df.groupby("Year")
        .agg(
            {
                "Balance": "last",
                "Adjusted Balance": "last",
                "Month": "last",
                "Total Withdrawn": "last",
            }
        )
        .reset_index()
    )
