"""Indicative maturity calculator.

Mirrors the society's published RD schedule (simple-interest method):
    interest = monthly_amount * n(n+1)/2 * (annual_rate / 1200), n = months
Rates follow the official RD tenure tiers. Final values are subject to the
official plan terms (see disclaimer).
"""

from decimal import Decimal, ROUND_HALF_UP

DISCLAIMER = (
    "This calculation is indicative only. Final values are subject to official plan terms."
)

# Tenure (years) -> annual interest rate (%)
RD_RATE_TIERS = {6: 6, 8: 8, 10: 10, 12: 12, 15: 13, 18: 14, 21: 15, 24: 16}


def _rate_for(duration_years: int) -> float:
    if duration_years in RD_RATE_TIERS:
        return RD_RATE_TIERS[duration_years]
    lower = [y for y in sorted(RD_RATE_TIERS) if y <= duration_years]
    if lower:
        return RD_RATE_TIERS[lower[-1]]
    return RD_RATE_TIERS[min(RD_RATE_TIERS)]


def _round(value: float) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def calculate_maturity(plan_type: str, monthly_amount, duration_years: int) -> dict:
    amount = float(monthly_amount)
    months = duration_years * 12
    total_deposit = amount * months
    rate = _rate_for(duration_years)
    interest = amount * (months * (months + 1) / 2) * (rate / 1200)
    maturity = total_deposit + interest
    return {
        "total_deposit": _round(total_deposit),
        "estimated_maturity": _round(maturity),
        "estimated_benefit": _round(interest),
        "disclaimer": DISCLAIMER,
    }
