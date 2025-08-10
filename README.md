# agensus

AI Agent Consensus framework - reduces bias and improves accuracy in multi-agent LLM systems by leveraging multiple perspectives to reach reliable consensus.

**Why Consensus?** Single LLMs can hallucinate, produce biased results, or generate false information. Agensus mitigates these issues by combining outputs from multiple agents using proven consensus algorithms.

- **Strategies**: `overlap` (Jaccard similarity), `rrf` (reciprocal rank fusion), `llm_judge` (meta-evaluation)
- **API**: `Consensus(strategy=...).pick(candidates)` → `ConsensusResult` 
- **Production-ready**: Fast, dependency-light, pure Python
- **Flexible**: CLI + Python API with LLM integration examples

## Install
```bash
pip install -e .
```

## Quick Start
```python
from agensus import Consensus

# Multiple AI responses to the same question
candidates = [
    "Deploy using blue-green strategy with load balancer switching",
    "Use rolling deployment with health checks and automatic rollback", 
    "Implement canary deployment with gradual traffic shifting"
]

# Find consensus using overlap similarity
result = Consensus("overlap").pick(candidates)
print(f"Best answer: {candidates[result.index]}")
print(f"Confidence scores: {result.scores}")
```

## Advanced Multi-Agent Example
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

## Research Background
Based on research showing that multi-agent consensus frameworks significantly reduce bias and improve accuracy in generative AI systems. Single LLMs are prone to hallucinations and biased outputs - agensus provides practical consensus mechanisms to address these reliability challenges.

## CLI
```bash
printf "A\nB more info\nC longest option" | agensus --strategy overlap
```

## Tests
```bash
pytest -q
```

See `docs/` for deeper strategy notes.
