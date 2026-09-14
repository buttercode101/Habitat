# Habitat

**A local-first supervision and accountability runtime for autonomous agents.**

> Agents can tell you what they did. Habitat helps you verify it.

Habitat records trusted actions locally, accepts authenticated structured events, correlates work with run IDs, verifies claims against trusted actions or explicit external evidence, and raises supervision signals when behavior needs attention.

## Core model

```text
Agent → Event → Habitat ledger → Verification → Signal → Human
                         ↓
                       SQLite
```

## Requirements

- Python 3.10+
- No third-party runtime dependencies
- SQLite (included with Python)

## Development

```bash
python -m pytest -q
```

See `PROJECT.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, and `SECURITY.md` for the design and operating boundaries.

## License

MIT.
