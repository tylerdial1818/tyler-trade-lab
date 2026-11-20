"""How many independent events a test needs before it can say anything."""

from __future__ import annotations

import math

from scipy.stats import norm


def events_needed(sd: float, edge: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Events needed for a one-sided test of mean ``edge`` > 0 with per-event ``sd``.

    Uses the normal approximation n = ((z_alpha + z_power) * sd / edge) ** 2.
    """
    if sd <= 0 or edge <= 0:
        raise ValueError("sd and edge must be positive")
    z = float(norm.ppf(1 - alpha)) + float(norm.ppf(power))
    return math.ceil((z * sd / edge) ** 2)


def binary_payoff_sd(price: float) -> float:
    """Standard deviation of a $1 binary contract's payoff when priced fairly at ``price``."""
    if not 0 < price < 1:
        raise ValueError("price must be strictly between 0 and 1")
    return math.sqrt(price * (1 - price))
