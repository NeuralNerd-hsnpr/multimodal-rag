"""Score four retrieval strategies on the same query set and print the comparison."""

import json

from src.ingest import Chunk
from src.rerank import CANDIDATES, rerank
from src.retrieval import Index

DEPTH = 10  # ranks beyond this count as a miss
RRF_SWEEP = (1, 5, 10, 20, 60)


def strategies(index: Index) -> dict:
    return {
        "bm25": lambda q: index.bm25_search(q, DEPTH),
        "dense": lambda q: index.dense_search(q, DEPTH),
        "hybrid": lambda q: index.hybrid_search(q, DEPTH),
        "hybrid + rerank": lambda q: rerank(q, index.hybrid_search(q, CANDIDATES), DEPTH),
    }


def gold_rank(results: list[tuple[Chunk, float]], gold: str) -> int:
    """1-based rank of the first chunk from the gold document, or 0 when absent from the top DEPTH."""
    return next((i for i, (chunk, _) in enumerate(results, start=1) if chunk.doc_id == gold), 0)


def metrics(ranks: list[int]) -> str:
    n = len(ranks)
    hit1 = sum(r == 1 for r in ranks) / n
    recall5 = sum(0 < r <= 5 for r in ranks) / n
    mrr = sum(1 / r for r in ranks if r) / n
    return f"{hit1:>7.2f}{recall5:>10.2f}{mrr:>7.2f}"


def run(index: Index, queries_path: str = "data/queries.json") -> None:
    queries = json.loads(open(queries_path).read())
    ranks = {name: [gold_rank(search(q["query"]), q["gold"]) for q in queries]
             for name, search in strategies(index).items()}

    docs = len({chunk.doc_id for chunk in index.chunks})
    print(f"Ablation: {len(queries)} queries over {docs} documents ({len(index.chunks)} chunks), "
          f"gold = source document, top {DEPTH} scored")
    print(f"{'strategy':<17}{'hit@1':>7}{'recall@5':>10}{'mrr':>7}")
    for name, rs in ranks.items():
        print(f"{name:<17}{metrics(rs)}")

    print(f"\nRank of the gold document per query (0 = not in top {DEPTH})")
    print(f"{'':<64}" + "".join(f"{n.split()[-1]:>7}" for n in ranks))
    for i, q in enumerate(queries):
        print(f"{q['query'][:62]:<64}" + "".join(f"{rs[i]:>7}" for rs in ranks.values()))

    # The RRF constant sets how much a top rank is worth relative to a middling one; the usual
    # 60 was chosen for lists of about a thousand, and this sweep shows what it does here.
    print(f"\nReciprocal rank fusion constant k, fused over all {len(index.chunks)} chunks")
    print(f"{'k':<7}{'hybrid hit@1':>13}{'recall@5':>10}{'mrr':>7}{'+rerank hit@1':>15}{'recall@5':>10}{'mrr':>7}")
    for k in RRF_SWEEP:
        fused = [gold_rank(index.hybrid_search(q["query"], DEPTH, rrf_k=k), q["gold"]) for q in queries]
        reranked = [gold_rank(rerank(q["query"], index.hybrid_search(q["query"], CANDIDATES, rrf_k=k), DEPTH),
                              q["gold"]) for q in queries]
        print(f"{k:<7}{metrics(fused):>30}{metrics(reranked):>32}")


if __name__ == "__main__":
    from src.ingest import load_dir

    run(Index(load_dir("data/corpus")))
