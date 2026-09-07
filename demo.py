"""One command: ingest both tiers, run the retrieval ablation, answer two routed queries."""

import os
import sys
from collections import Counter

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

from src.ablation import run  # noqa: E402
from src.ingest import load_dir  # noqa: E402
from src.retrieval import Index  # noqa: E402
from src.router import CORE_THRESHOLD, answer  # noqa: E402

QUERIES = [
    "Which planets are the inner planets?",
    "How big is Deimos and how long does it take to orbit Mars?",
]

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. It is the only credential the demo needs.")

    core = load_dir("data/core")
    corpus = load_dir("data/corpus")
    counts = Counter(c.modality for c in corpus)
    print(f"core tier: {len(core)} chunks from data/core")
    print(f"corpus tier: {len(corpus)} chunks from data/corpus "
          f"({', '.join(f'{m} {n}' for m, n in sorted(counts.items()))})\n")
    core_index, corpus_index = Index(core), Index(corpus)

    run(corpus_index)

    for query in QUERIES:
        result = answer(query, core_index, corpus_index)
        print(f"\nQuery: {query}")
        print(f"  tier: {result.tier}  (nearest core chunk {result.similarity:.2f}, threshold {CORE_THRESHOLD})")
        print(f"  answer: {result.text}")
        print("  cited: " + ("; ".join(c.cite() for c in result.cited) or "nothing"))
