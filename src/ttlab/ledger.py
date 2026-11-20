"""Append-only, hash-chained forecast ledger.

Each entry stores the SHA-256 of the previous entry, so editing or deleting any
past forecast breaks every hash after it. Committing the ledger file to git
before an event resolves gives a public, timestamped record.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

GENESIS = "0" * 64


class LedgerTampered(ValueError):
    """Raised when the hash chain does not verify."""


@dataclass(frozen=True)
class Entry:
    prev_hash: str
    payload: dict[str, Any]

    @property
    def hash(self) -> str:
        body = json.dumps(
            {"prev_hash": self.prev_hash, "payload": self.payload},
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(body.encode()).hexdigest()

    def to_line(self) -> str:
        return json.dumps(
            {"prev_hash": self.prev_hash, "payload": self.payload, "hash": self.hash},
            sort_keys=True,
        )


def read(path: Path) -> list[Entry]:
    """Read and verify a ledger file. Missing file means an empty ledger."""
    if not path.exists():
        return []
    entries: list[Entry] = []
    prev = GENESIS
    for n, line in enumerate(path.read_text().splitlines(), start=1):
        raw = json.loads(line)
        entry = Entry(prev_hash=raw["prev_hash"], payload=raw["payload"])
        if entry.prev_hash != prev or entry.hash != raw["hash"]:
            raise LedgerTampered(f"hash chain breaks at line {n}")
        entries.append(entry)
        prev = entry.hash
    return entries


def append(path: Path, payload: dict[str, Any]) -> Entry:
    """Verify the existing chain, then append ``payload`` as a new entry."""
    entries = read(path)
    prev = entries[-1].hash if entries else GENESIS
    entry = Entry(prev_hash=prev, payload=payload)
    with path.open("a") as f:
        f.write(entry.to_line() + "\n")
    return entry
