from datetime import UTC, datetime, timedelta

import pytest

from ttlab.asof import LookAheadError, Observation, require_usable, usable_at

T = datetime(2026, 11, 19, 13, 30, tzinfo=UTC)


def obs(public: datetime | None, received: datetime) -> Observation:
    return Observation("x", 1.0, public, received)


def test_usable_when_both_clocks_precede_decision() -> None:
    assert usable_at(obs(T - timedelta(hours=1), T - timedelta(minutes=5)), T)


def test_not_usable_if_received_late() -> None:
    assert not usable_at(obs(T - timedelta(hours=1), T + timedelta(seconds=1)), T)


def test_unknown_public_time_is_never_usable() -> None:
    assert not usable_at(obs(None, T - timedelta(days=1)), T)


def test_require_usable_names_the_leak() -> None:
    with pytest.raises(LookAheadError, match="x not usable"):
        require_usable([obs(T + timedelta(minutes=1), T + timedelta(minutes=1))], T)


def test_naive_timestamps_rejected() -> None:
    with pytest.raises(ValueError):
        Observation("x", 1.0, datetime(2026, 1, 1), T)
