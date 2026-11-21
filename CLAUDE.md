# Tyler Trade Labs

Public lab notebook: Python research package (`src/ttlab`) plus an Astro site (`site/`).

## Rules
- No order-placing code in this repository. Private trading lives in a separate private repo that imports this package.
- Every observation carries `public_at` and `received_at`; both must be at or before the decision time (`ttlab.asof`).
- Never put a number on the site that an experiment has not produced. Use the `Pending` component until it has.
- Specs in `specs/` are registered by a commit that sets `status: registered` before test data is examined. After that, append dated amendments; never edit above them.
- Site headings and titles are short and plain ("Method", "Results", "Limitations"). No clever headings.
- Analysis code stays simple and readable; package code is typed (mypy strict) and tested.

## Commands
- `uv run pytest -q`, `uv run ruff check . && uv run ruff format --check .`, `uv run mypy`
- `cd site && npm ci && npm run build`
