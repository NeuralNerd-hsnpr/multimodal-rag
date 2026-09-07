"""Lexical and dense retrieval over chunks, fused with reciprocal rank fusion."""

import functools
import re

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from src.ingest import Chunk

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RRF_K = 60  # the constant from the original RRF paper; it dampens the weight of top ranks


@functools.cache
def embedder() -> SentenceTransformer:
    # About 88 MB, fetched on first run. Shared by both tiers so it loads once.
    return SentenceTransformer(EMBED_MODEL)


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class Index:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokenize(c.text) for c in chunks])
        self.vectors = embedder().encode([c.text for c in chunks], normalize_embeddings=True)

    def _ranked(self, scores: np.ndarray, k: int) -> list[tuple[Chunk, float]]:
        order = np.argsort(-scores)[:k]
        return [(self.chunks[i], float(scores[i])) for i in order]

    def bm25_search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        return self._ranked(self.bm25.get_scores(tokenize(query)), k)

    def dense_search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        q = embedder().encode(query, normalize_embeddings=True)
        return self._ranked(self.vectors @ q, k)  # cosine similarity, vectors are unit length

    def hybrid_search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        """Reciprocal rank fusion of the full BM25 and dense rankings.

        RRF only looks at ranks, so the two score scales never have to be reconciled. The
        tradeoff is that a strong top hit in one ranking is flattened to 1/(k+1) like any other.
        """
        fused = np.zeros(len(self.chunks))
        for scores in (self.bm25.get_scores(tokenize(query)),
                       self.vectors @ embedder().encode(query, normalize_embeddings=True)):
            for rank, i in enumerate(np.argsort(-scores), start=1):
                fused[i] += 1.0 / (RRF_K + rank)
        return self._ranked(fused, k)
