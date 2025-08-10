# API

```python
from agensus import Consensus, ConsensusResult

c = Consensus(strategy="overlap")  # or "rrf" or "llm_judge" with judge_fn=...
res: ConsensusResult = c.pick(["A", "B", "C"])
print(res.index, res.scores, res.rationale)
```

`ConsensusResult`
- `index: int` - winning candidate index
- `scores: list[float] | None` - per-candidate scores (if strategy returns them)
- `rationale: str | None` - explanation from judge strategies
- `extra: dict | None` - passthrough metadata
