# Tyler Trade Labs

Research code and website for Tyler Trade Labs, a public lab notebook that asks one question: when can data tell you something a market does not already know?

By Tyler Dial ([tylerdial.dev](https://tylerdial.dev)), Dialed Intelligence.

## Layout

| Path | Contents |
| --- | --- |
| `src/ttlab/` | Python package: as-of data rules, fee formulas, forecast ledger, power calculations |
| `tests/` | pytest suite, offline only |
| `specs/` | Pre-registrations, committed before any test data is examined |
| `site/` | Astro website: essays, method, experiments |

## Rules this code follows

- No code in this repository can place an order. It reads public market data only.
- Every observation records when it became public and when it was received. Neither may be later than the decision it feeds.
- Forecasts go into a hash-chained ledger committed to git before the event resolves.
- Results that depend on unknown fee rules or missing data are refused, not estimated.

## Development

```sh
uv sync
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run mypy

cd site && npm ci && npm run dev
```

## License

Code is MIT. Writing on the site is © Tyler Dial, all rights reserved.
