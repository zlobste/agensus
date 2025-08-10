# agent-consensus

Lightweight consensus library for multi-agent LLM systems - fast, dependency-light, and easy to embed.

- Strategies: `overlap` (Jaccard token overlap), `rrf` (reciprocal rank fusion), and `llm_judge` (bring your own judge).
- Clean API: `Consensus(strategy=...).pick(candidates)` returns a `ConsensusResult`.
- Includes CLI for quick experiments and `examples/` for integration patterns.
- Pure Python. No heavy deps.

## Install
```bash
pip install -e .
```

## Quickstart
```python
from agent_consensus import Consensus

c = Consensus("overlap")
res = c.pick(["A reliable cost-effective option.", "Higher throughput but costly.", "Balanced trade-offs overall."])
print(res.index, res.scores)
```

## CLI
```bash
printf "A\nB more info\nC longest option" | agent-consensus --strategy overlap
# => {"index": 2, "scores": [0.33, 0.42, 0.55]}
```

## LLM judge hook
```python
from agent_consensus import Consensus

def judge_fn(cands: list[str]) -> dict:
    # Example - choose the longest. Replace with an LLM call if desired.
    best = max(range(len(cands)), key=lambda i: len(cands[i]))
    return {"index": best, "rationale": "Picked longest."}

c = Consensus("llm_judge", judge_fn=judge_fn)
print(c.pick(["A", "BBBB", "CCC"]).index)  # 1
```

See `docs/` for strategy details and API, and `examples/` for runnable demos.
