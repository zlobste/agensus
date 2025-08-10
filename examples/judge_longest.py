from __future__ import annotations

from typing import Sequence, Mapping, Any, TypedDict

from agensus import Consensus

class JudgeVerdict(TypedDict, total=False):
    index: int
    rationale: str


def judge_fn(candidates: Sequence[str]) -> JudgeVerdict:
    best = max(range(len(candidates)), key=lambda i: len(candidates[i]))
    return {"index": best, "rationale": "Picked longest."}


if __name__ == "__main__":
    consensus = Consensus("llm_judge", judge_fn=judge_fn)
    result = consensus.pick(["A", "BBBB", "CCC"])
    print("Winner:", result.index, "| Rationale:", result.rationale)
