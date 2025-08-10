from __future__ import annotations

from agensus import Consensus

if __name__ == "__main__":
    consensus = Consensus("overlap")
    result = consensus.pick([
        "Option A - reliable and cost-effective.",
        "Option B - higher throughput but higher cost.",
        "Option C - balanced trade-offs and moderate risk.",
    ])
    print("Winner index:", result.index)
    print("Scores:", result.scores)
