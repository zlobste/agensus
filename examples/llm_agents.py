from __future__ import annotations

"""
End-to-end examples showing how to use agensus with real LLM calls.

These examples assume you have an OpenAI-compatible endpoint and
OPENAI_API_KEY exported in your environment.

They are written to be minimal, dependency-light, and optional:
- If openai package is missing, a clear message is printed.
- Network calls are only made when you execute this file directly.

Two flows illustrated:
1. Aggregating multiple model answers ("overlap" strategy)
2. Letting an LLM act as the judge ("llm_judge" strategy)
"""

from typing import List, Dict, Any

try:  # Optional dependency
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - graceful fallback
    OpenAI = None  # type: ignore

from agensus import Consensus


def generate_candidates(prompt: str, model_ids: list[str]) -> list[str]:
    """Return one completion per model id. Falls back to synthetic strings if OpenAI missing."""
    if OpenAI is None:
        return [f"[mock:{m}] response about {prompt}" for m in model_ids]
    client = OpenAI()
    out: list[str] = []
    for m in model_ids:
        # Using the Chat Completions API; adjust to your provider as needed.
        resp = client.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=180,
            temperature=0.4,
        )
        content = resp.choices[0].message.content or ""
        out.append(content.strip())
    return out


def llm_judge_builder(model: str):
    """Return a judge_fn that queries a model to select best candidate.

    The model is prompted to output a tiny JSON object: {"index": <int>, "rationale": "..."}.
    Parsing is defensive: if parsing fails, we default to index 0.
    """

    def judge_fn(cands: List[str]) -> Dict[str, Any]:  # required signature for Consensus
        if OpenAI is None:
            # Deterministic fallback: chooses longest candidate
            best = max(range(len(cands)), key=lambda i: len(cands[i])) if cands else 0
            return {"index": best, "rationale": "Fallback length-based judge (no OpenAI)."}
        client = OpenAI()
        numbered = "\n".join(f"[{i}] {c}" for i, c in enumerate(cands))
        prompt = (
            "You are an expert evaluator. Given multiple model answers, pick the single best.\n"
            "Return ONLY a compact JSON object with keys index (integer) and rationale (string).\n"
            f"Candidates:\n{numbered}\n\nJSON:"
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.0,
        )
        raw = (resp.choices[0].message.content or "").strip()
        idx = 0
        rationale = ""
        try:
            import json

            data = json.loads(raw)
            if isinstance(data, dict) and "index" in data:
                idx = int(data.get("index", 0))
                rationale = str(data.get("rationale", ""))
        except Exception:  # pragma: no cover - parsing robustness
            rationale = f"Unparseable judge response: {raw[:80]}"
        if not (0 <= idx < len(cands)):
            idx = 0
        return {"index": idx, "rationale": rationale}

    return judge_fn


def demo_overlap() -> None:
    prompt = "Design a scalable logging architecture for a microservices platform."
    model_ids = [
        "gpt-4o-mini",  # Example; replace with models you have access to
        "gpt-4o",       # or other vendor-compatible names
        "gpt-3.5-turbo",  # legacy, if still accessible
    ]
    candidates = generate_candidates(prompt, model_ids)
    consensus = Consensus("overlap")
    result = consensus.pick(candidates)
    print("[Overlap] Winning index:", result.index)
    print("[Overlap] Scores:", result.scores)


def demo_llm_judge() -> None:
    prompt = "List three concrete, low-latency strategies to improve search ranking freshness."
    model_ids = ["gpt-4o-mini", "gpt-4o"]
    candidates = generate_candidates(prompt, model_ids)
    judge_fn = llm_judge_builder(model="gpt-4o")
    consensus = Consensus("llm_judge", judge_fn=judge_fn)
    result = consensus.pick(candidates)
    print("[LLM Judge] Winning index:", result.index)
    print("[LLM Judge] Rationale:", result.rationale)


if __name__ == "__main__":  # pragma: no cover
    demo_overlap()
    demo_llm_judge()
