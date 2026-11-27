#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DB="${TMPDIR:-/tmp}/habitat-playwright-e2e.db"
rm -f "$DB"
cd "$ROOT"
PYTHONPATH="$ROOT" python3 -m habitat --db "$DB" init --config examples/simple.yaml
PYTHONPATH="$ROOT" python3 -m habitat --db "$DB" demo
PYTHONPATH="$ROOT" python3 -m habitat --db "$DB" prove --run-id run-42 --claim "deployed v1.2.3 to production" -o "${DB}.proof.json" --card
exec env PYTHONPATH="$ROOT" python3 -m habitat --db "$DB" serve --host 127.0.0.1 --port 8787 --allow-unsigned
