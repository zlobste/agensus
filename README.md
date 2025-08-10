# agensus

AI Agent Consensus framework - lightweight consensus library for multi-agent LLM systems - fast, dependency-light, and easy to embed.

- Strategies: `overlap` (Jaccard token overlap), `rrf` (reciprocal rank fusion), and `llm_judge` (bring your own judge).
- API: `Consensus(strategy=...).pick(candidates)` -> `ConsensusResult`.
- Includes advanced LLM integration example in `examples/llm_agents.py`.
- Pure Python. No heavy deps.

## Install
```bash
pip install -e .
```

## Advanced LLM agents example
See `examples/llm_agents.py` for full script pulling multiple model outputs and applying overlap and LLM-judge consensus.
```python
from agensus import Consensus
from examples.llm_agents import generate_candidates, llm_judge_builder

prompt = "Outline a zero-downtime deployment pipeline for a SaaS platform."
models = ["gpt-4o-mini", "gpt-4o"]
answers = generate_candidates(prompt, models)

# Overlap strategy
res_overlap = Consensus("overlap").pick(answers)
print("Overlap winner index:", res_overlap.index)
print("Scores:", res_overlap.scores)

# LLM judge strategy
judge_fn = llm_judge_builder("gpt-4o")
res_judge = Consensus("llm_judge", judge_fn=judge_fn).pick(answers)
print("LLM Judge winner index:", res_judge.index)
print("Rationale:", res_judge.rationale)
```

## CLI
```bash
printf "A\nB more info\nC longest option" | agensus --strategy overlap
```

## Tests
```bash
pytest -q
```

See `docs/` for deeper strategy notes.
