from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Callable, Protocol


class StrategyFn(Protocol):
    def __call__(self, candidates: Sequence[str]) -> dict[str, Any]: ...  # noqa: D401


@dataclass(slots=True)
class ConsensusResult:
    index: int
    scores: list[float] | None = None
    rationale: str | None = None
    extra: dict[str, Any] | None = None


class Consensus:
    def __init__(
        self,
        strategy: str = "overlap",
        judge_fn: Callable[[list[str]], dict] | None = None,
    ) -> None:
        from . import strategies

        self.name = strategy
        self._judge_fn = judge_fn

        if strategy == "overlap":
            self._fn: StrategyFn = strategies.overlap  # type: ignore[assignment]
        elif strategy == "rrf":
            self._fn = strategies.rrf  # type: ignore[assignment]
        elif strategy == "llm_judge":
            if judge_fn is None:
                raise ValueError("llm_judge requires judge_fn")

            def _wrap(cands: Sequence[str]) -> dict[str, Any]:
                verdict = strategies.llm_judge(list(cands), judge_fn)
                return {
                    "index": verdict["index"],
                    "rationale": verdict.get("rationale", ""),
                }

            self._fn = _wrap
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def pick(self, candidates: Sequence[str]) -> ConsensusResult:
        if not isinstance(candidates, (list, tuple)) or not all(
            isinstance(x, str) for x in candidates
        ):
            raise TypeError("candidates must be a sequence of str")
        if not candidates:
            return ConsensusResult(
                index=0, scores=[], rationale="No candidates", extra={}
            )

        out = self._fn(candidates)
        index = int(out["index"]) if "index" in out else 0
        return ConsensusResult(
            index=index,
            scores=out.get("scores"),
            rationale=out.get("rationale"),
            extra={
                k: v
                for k, v in out.items()
                if k not in {"index", "scores", "rationale"}
            },
        )
