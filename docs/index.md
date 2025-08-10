# agent-consensus

A small library that helps you pick the best answer from multiple candidates. Useful in multi-agent LLM setups where several agents answer the same question and you want one final choice.

## What it does
- Scores and compares candidate answers.
- Returns a winner index plus scores or a rationale depending on strategy.
- Works offline - no LLM needed unless you use `llm_judge`.

## When to use
- Ensemble-style setups to reduce hallucinations and bias.
- Any pipeline that needs a single best answer from several options.
