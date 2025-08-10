from __future__ import annotations

from agent_consensus import Consensus


def test_rrf_basic_rank_validity() -> None:
    candidates = [
        "alpha beta gamma",
        "beta gamma delta",
        "gamma delta epsilon",
        "unrelated tokens here",
    ]
    result = Consensus("rrf").pick(candidates)
    assert 0 <= result.index < len(candidates)
    assert result.scores is not None and len(result.scores) == len(candidates)


def test_rrf_not_all_zero_scores() -> None:
    candidates = ["a b", "b c", "c d"]
    result = Consensus("rrf").pick(candidates)
    assert result.scores is not None
    assert any(score > 0 for score in result.scores)
