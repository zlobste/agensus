from __future__ import annotations

import sys
import json
import argparse
from typing import Sequence

from .core import Consensus


def _read_candidates(path: str | None) -> list[str]:
    if path:
        with open(path, "r", encoding="utf-8") as fh:
            return [ln.rstrip("\n") for ln in fh if ln.strip()]
    data = sys.stdin.read()
    return [ln for ln in data.splitlines() if ln.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Agensus - AI Agent Consensus framework CLI")
    parser.add_argument("--strategy", "-s", default="overlap", choices=["overlap", "rrf"], help="Consensus strategy")
    parser.add_argument("--file", "-f", help="File with one candidate per line. If omitted, read from stdin.")
    args = parser.parse_args()

    candidates = _read_candidates(args.file)
    consensus = Consensus(args.strategy)
    result = consensus.pick(candidates)
    print(
        json.dumps(
            {
                "index": result.index,
                "scores": result.scores,
                "rationale": result.rationale,
            }
        )
    )


if __name__ == "__main__":  # pragma: no cover
    main()
