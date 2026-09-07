"""Entry point. Reranking, routing and the ablation are added in later branches; see README."""

from collections import Counter

from src.ingest import load_dir
from src.retrieval import Index

if __name__ == "__main__":
    core = load_dir("data/core")
    corpus = load_dir("data/corpus")
    counts = Counter(c.modality for c in corpus)
    print(f"core tier: {len(core)} chunks from data/core")
    print(f"corpus tier: {len(corpus)} chunks from data/corpus "
          f"({', '.join(f'{m} {n}' for m, n in sorted(counts.items()))})")

    index = Index(corpus)
    query = "How big is Deimos and how long does it take to orbit Mars?"
    print(f"\nQuery: {query}")
    for name, search in (("bm25", index.bm25_search), ("dense", index.dense_search), ("hybrid", index.hybrid_search)):
        print(f"\n  {name}")
        for chunk, score in search(query, 3):
            print(f"    {score:6.3f}  {chunk.cite()}")
