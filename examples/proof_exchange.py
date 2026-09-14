"""Minimal proof exchange demo.

Producer side exports a Habitat proof bundle. Consumer side verifies the
bundle without importing Habitat's runtime or accessing the producer DB.

Usage:
    python examples/proof_exchange.py proof.json
"""
from __future__ import annotations

import json
import sys

from habitat.proof_verify import verify_file


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python examples/proof_exchange.py proof.json", file=sys.stderr)
        return 2

    path = sys.argv[1]
    result = verify_file(path)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
