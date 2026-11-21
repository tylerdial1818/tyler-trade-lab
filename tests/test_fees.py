from datetime import date
from decimal import Decimal

import pytest

from ttlab.fees import (
    FeeSchedule,
    UnknownFeeSchedule,
    break_even_probability,
    schedule_for,
    taker_fee,
)

S1 = FeeSchedule(date(2024, 1, 1), Decimal("0.07"), "test")
S2 = FeeSchedule(date(2025, 6, 1), Decimal("0.05"), "test")


def test_fee_uses_execution_price() -> None:
    assert taker_fee(1, Decimal("0.42"), S1) == Decimal("0.017052")


def test_fee_is_symmetric_around_half() -> None:
    assert taker_fee(10, Decimal("0.30"), S1) == taker_fee(10, Decimal("0.70"), S1)


@pytest.mark.parametrize("price", [Decimal(0), Decimal(1), Decimal("-0.1")])
def test_fee_rejects_impossible_prices(price: Decimal) -> None:
    with pytest.raises(ValueError):
        taker_fee(1, price, S1)


def test_schedule_picks_latest_effective() -> None:
    assert schedule_for(date(2025, 7, 1), [S1, S2]) is S2
    assert schedule_for(date(2025, 5, 31), [S1, S2]) is S1


def test_unknown_schedule_is_refused() -> None:
    with pytest.raises(UnknownFeeSchedule):
        schedule_for(date(2023, 1, 1), [S1, S2])


def test_break_even_exceeds_price() -> None:
    assert break_even_probability(Decimal("0.42"), S1) == Decimal("0.437052")
