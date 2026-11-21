"""Point-in-time discipline.

Every observation carries two clocks: when it became public, and when we received
it. A feature may be used for a decision only if both are at or before the
decision time. An unknown public time is never assumed to be early.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


class LookAheadError(ValueError):
    """Raised when an observation would leak information from after the decision."""


@dataclass(frozen=True)
class Observation:
    key: str
    value: float
    public_at: datetime | None
    received_at: datetime

    def __post_init__(self) -> None:
        for t in (self.public_at, self.received_at):
            if t is not None and t.tzinfo is None:
                raise ValueError("timestamps must be timezone-aware")


def usable_at(obs: Observation, decision_at: datetime) -> bool:
    """True if ``obs`` was both public and in hand by ``decision_at``."""
    if decision_at.tzinfo is None:
        raise ValueError("decision time must be timezone-aware")
    if obs.public_at is None:
        return False
    return obs.public_at <= decision_at and obs.received_at <= decision_at


def require_usable(observations: list[Observation], decision_at: datetime) -> None:
    """Raise ``LookAheadError`` naming the first observation that is not usable."""
    for obs in observations:
        if not usable_at(obs, decision_at):
            raise LookAheadError(
                f"{obs.key} not usable at {decision_at.isoformat()} "
                f"(public_at={obs.public_at}, received_at={obs.received_at})"
            )
