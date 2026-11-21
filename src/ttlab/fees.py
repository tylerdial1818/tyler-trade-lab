"""Kalshi trading fees.

Kalshi's published taker fee is ``rate * contracts * price * (1 - price)``, where
``price`` is the execution price in dollars, not the forecast. The exchange rounds
fees on its own rules (see https://docs.kalshi.com/getting_started/fee_rounding),
and rates and multipliers change over time and by series.

This module computes the *unrounded* fee from an explicitly versioned schedule.
Callers that need exact cents must apply the exchange's rounding for the period
in question; results that depend on an unknown schedule are refused rather than
guessed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


class UnknownFeeSchedule(LookupError):
    """Raised when no fee schedule covers the requested trade date."""


@dataclass(frozen=True)
class FeeSchedule:
    """One version of the fee formula, valid from ``effective`` until replaced."""

    effective: date
    taker_rate: Decimal
    source: str


def taker_fee(contracts: int, price: Decimal, schedule: FeeSchedule) -> Decimal:
    """Unrounded taker fee in dollars for ``contracts`` filled at ``price``.

    >>> s = FeeSchedule(date(2025, 1, 1), Decimal("0.07"), "example")
    >>> taker_fee(1, Decimal("0.42"), s)
    Decimal('0.017052')
    """
    if contracts <= 0:
        raise ValueError("contracts must be positive")
    if not Decimal(0) < price < Decimal(1):
        raise ValueError("price must be strictly between 0 and 1 dollar")
    return schedule.taker_rate * contracts * price * (1 - price)


def schedule_for(trade_date: date, schedules: list[FeeSchedule]) -> FeeSchedule:
    """Return the schedule in force on ``trade_date``.

    Raises ``UnknownFeeSchedule`` if the date precedes every known schedule.
    """
    valid = [s for s in schedules if s.effective <= trade_date]
    if not valid:
        raise UnknownFeeSchedule(f"no fee schedule known for {trade_date.isoformat()}")
    return max(valid, key=lambda s: s.effective)


def break_even_probability(price: Decimal, schedule: FeeSchedule) -> Decimal:
    """Win probability at which buying one contract at ``price`` has zero expected value."""
    return price + taker_fee(1, price, schedule)
