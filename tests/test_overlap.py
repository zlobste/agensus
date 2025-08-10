from __future__ import annotations

import pytest

from agensus import Consensus


def test_overlap_scores_len() -> None:
    consensus = Consensus("overlap")
    result = consensus.pick(["alpha beta", "beta gamma", "table desk"])
    assert result.scores is not None
    assert len(result.scores) == 3
    assert 0 <= result.index < 3


def test_overlap_identical_candidates_picks_first() -> None:
    candidates = ["same text" for _ in range(5)]
    result = Consensus("overlap").pick(candidates)
    # Tie broken deterministically by first index.
    assert result.index == 0
    assert result.scores is not None and len(result.scores) == len(candidates)
    assert len(set(result.scores)) == 1
