"""Entry point. Routing and the ablation are added in later branches; see README."""

from collections import Counter

from src.ingest import load_dir
from src.rerank import CANDIDATES, rerank
from src.retrieval import Index

if __name__ == "__main__":
    core = load_dir("data/core")
    corpus = load_dir("data/corpus")
    counts = Counter(c.modality for c in corpus)
    print(f"core tier: {len(core)} chunks from data/core")
    print(f"corpus tier: {len(corpus)} chunks from data/corpus "
          f"({', '.join(f'{m} {n}' for m, n in sorted(counts.items()))})")

    index = Index(corpus)
    query = "Where do the geysers on Enceladus come from?"
    print(f"\nQuery: {query}")
    fused = index.hybrid_search(query, CANDIDATES)
    for name, results in (("hybrid", fused[:3]), ("hybrid + rerank", rerank(query, fused, 3))):
        print(f"\n  {name}")
        for chunk, score in results:
            print(f"    {score:7.3f}  {chunk.cite()}")
