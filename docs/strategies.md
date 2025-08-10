# Strategies

## overlap
Average Jaccard similarity over token sets. For each candidate i, compute
`score(i) = mean_j Jaccard(tokens(i), tokens(j))`. The highest score wins.

Pros: simple, fast, robust.  
Cons: lexical - does not understand semantics.

## rrf
Reciprocal Rank Fusion on lexical similarity rankings. For each voter i, rank
candidates j by similarity(i, j). Aggregate via
`score(j) = sum_i 1/(k + rank_i(j))`, where k controls the tail influence.

Pros: more robust to outliers than raw averaging.  
Cons: still lexical, depends on tokenization and k.

## llm_judge
Delegates to your own judge function, which can use an LLM with a rubric.
The library only expects `{"index": int, "rationale": str}`.
