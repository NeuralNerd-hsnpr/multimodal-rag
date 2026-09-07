"""Entry point. The ablation is added in the next branch; see README."""

import os
import sys
from collections import Counter

from src.ingest import load_dir
from src.retrieval import Index
from src.router import CORE_THRESHOLD, answer

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
          f"({', '.join(f'{m} {n}' for m, n in sorted(counts.items()))})")
    core_index, corpus_index = Index(core), Index(corpus)

    for query in QUERIES:
        result = answer(query, core_index, corpus_index)
        print(f"\nQuery: {query}")
        print(f"  tier: {result.tier}  (nearest core chunk {result.similarity:.2f}, threshold {CORE_THRESHOLD})")
        print(f"  answer: {result.text}")
        print("  cited: " + ("; ".join(c.cite() for c in result.cited) or "nothing"))
