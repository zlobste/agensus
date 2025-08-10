from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any, Callable

TokenSet = set[str]

_token_pattern = re.compile(r"[a-zA-Z0-9]+")


def _tokens(text: str) -> TokenSet:
    return set(_token_pattern.findall(text.lower()))


def _jaccard(a: TokenSet, b: TokenSet) -> float:
    if not a and not b:
        return 1.0
    union_size = len(a | b)
    if union_size == 0:
        return 0.0
    return len(a & b) / union_size


def overlap(candidates: Sequence[str]) -> dict[str, Any]:
    sets = [_tokens(c) for c in candidates]
    n = len(sets)
    scores: list[float] = []
    for i in range(n):
        total = 0.0
        for j in range(n):
            if i == j:
                continue
            total += _jaccard(sets[i], sets[j])
        denom = n - 1 if n > 1 else 1
        scores.append(total / denom)
    best = max(range(n), key=scores.__getitem__) if scores else 0
    return {"index": best, "scores": scores}


def rrf(candidates: Sequence[str], k: float = 60.0) -> dict[str, Any]:
    sets = [_tokens(c) for c in candidates]
    n = len(sets)
    sim: list[list[float]] = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            sim[i][j] = _jaccard(sets[i], sets[j])

    scores = [0.0] * n
    for i in range(n):
        order = sorted(
            (j for j in range(n) if j != i), key=lambda j: sim[i][j], reverse=True
        )
        for rank, j in enumerate(order, start=1):
            scores[j] += 1.0 / (k + rank)
    best = max(range(n), key=scores.__getitem__) if scores else 0
    return {"index": best, "scores": scores}


def llm_judge(
    candidates: Sequence[str], judge_fn: Callable[[list[str]], dict[str, Any]]
) -> dict[str, Any]:
    verdict = judge_fn(list(candidates)) or {}
    index = int(verdict.get("index", 0)) if candidates else 0
    rationale = verdict.get("rationale", "")
    return {"index": index, "rationale": rationale}
