# Architecture

```text
                  ┌────────────────────┐
                  │ Agent / Job / Crew │
                  └─────────┬──────────┘
                            │
                    execute / report
                            │
                  ┌─────────▼──────────┐
                  │   Habitat Runtime  │
                  │ jobs • state • run │
                  └─────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
          Actions         State         Signals
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                 ┌────────────────────┐
                 │ Supervision Surface│
                 │  needs attention   │
                 └────────────────────┘
```

## Runtime boundaries

- `config.py`: load and validate configuration.
- `store.py`: SQLite persistence.
- `runtime.py`: execute jobs and record outcomes.
- `signals.py`: derive high-signal anomalies from persisted truth.
- `generate.py`: pure presentation of state; no agent decisions.
- `__main__.py`: CLI.

SQLite is used because it is included in the Python standard library and gives Habitat durable local state without a dependency-heavy database.
