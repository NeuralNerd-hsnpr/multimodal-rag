"""Cross-encoder reranking over a candidate list."""

import functools

from sentence_transformers import CrossEncoder

from src.ingest import Chunk

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
CANDIDATES = 20  # how deep into the fused ranking the reranker looks


@functools.cache
def cross_encoder() -> CrossEncoder:
    # About 88 MB, fetched on first run.
    return CrossEncoder(RERANK_MODEL)


def rerank(query: str, candidates: list[tuple[Chunk, float]], k: int) -> list[tuple[Chunk, float]]:
    """Re-score candidates by reading query and chunk together, then keep the top k.

    A cross-encoder sees both texts in one forward pass, so it can weigh how the words interact
    rather than comparing two independent vectors. That costs one model call per candidate,
    which is why it runs over a short fused list and not the whole corpus.
    """
    chunks = [chunk for chunk, _ in candidates]
    scores = cross_encoder().predict([(query, chunk.text) for chunk in chunks])
    order = sorted(range(len(chunks)), key=lambda i: -scores[i])[:k]
    return [(chunks[i], float(scores[i])) for i in order]
