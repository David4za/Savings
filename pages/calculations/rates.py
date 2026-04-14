def effective_monthly_rate(annual_rate: float) -> float:
    """Convert an effective annual return into an equivalent monthly return."""
    return (1 + annual_rate / 100) ** (1 / 12) - 1
