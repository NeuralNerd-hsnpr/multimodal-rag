"""Entry point. Retrieval, routing and the ablation are added in later branches; see README."""

from collections import Counter

from src.ingest import load_dir

if __name__ == "__main__":
    core = load_dir("data/core")
    corpus = load_dir("data/corpus")
    counts = Counter(c.modality for c in corpus)
    print(f"core tier: {len(core)} chunks from data/core")
    print(f"corpus tier: {len(corpus)} chunks from data/corpus "
          f"({', '.join(f'{m} {n}' for m, n in sorted(counts.items()))})")
    shown = set()
    for chunk in corpus:
        if chunk.modality not in shown:
            shown.add(chunk.modality)
            print(f"\n[{chunk.modality}] {chunk.cite()}\n  {chunk.text[:160]}...")
