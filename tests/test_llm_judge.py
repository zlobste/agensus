from __future__ import annotations

from agensus import Consensus


def test_llm_judge_rationale() -> None:
    def judge_fn(cands: list[str]) -> dict:
        return {"index": 1, "rationale": "Middle is most balanced."}

    result = Consensus("llm_judge", judge_fn=judge_fn).pick(["A", "B", "C"])
    assert result.index == 1
    assert result.rationale == "Middle is most balanced."


def test_llm_judge_empty_rationale_defaults() -> None:
    def judge_fn(cands: list[str]) -> dict:
        return {"index": 0}

    result = Consensus("llm_judge", judge_fn=judge_fn).pick(["X", "Y"])  # rationale omitted
    assert result.index == 0
    assert result.rationale == ""  # explicit empty string propagation
