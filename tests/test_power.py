import pytest

from ttlab.power import binary_payoff_sd, events_needed


def test_smaller_edges_need_more_events() -> None:
    assert events_needed(0.5, 0.02) > events_needed(0.5, 0.05)


def test_known_value() -> None:
    # (1.6449 + 0.8416)^2 * (0.5 / 0.05)^2 = 618.3 -> 619
    assert events_needed(0.5, 0.05) == 619


def test_binary_sd_peaks_at_half() -> None:
    assert binary_payoff_sd(0.5) == pytest.approx(0.5)
    assert binary_payoff_sd(0.9) == pytest.approx(0.3)
