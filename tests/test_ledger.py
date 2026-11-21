from pathlib import Path

import pytest

from ttlab.ledger import GENESIS, LedgerTampered, append, read


def test_chain_links_entries(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    a = append(p, {"event": "A", "p": 0.6})
    b = append(p, {"event": "B", "p": 0.3})
    assert a.prev_hash == GENESIS
    assert b.prev_hash == a.hash
    assert [e.payload["event"] for e in read(p)] == ["A", "B"]


def test_editing_history_is_detected(tmp_path: Path) -> None:
    p = tmp_path / "ledger.jsonl"
    append(p, {"event": "A", "p": 0.6})
    append(p, {"event": "B", "p": 0.3})
    p.write_text(p.read_text().replace("0.6", "0.9"))
    with pytest.raises(LedgerTampered, match="line 1"):
        read(p)


def test_missing_file_is_empty(tmp_path: Path) -> None:
    assert read(tmp_path / "none.jsonl") == []
