"""Pick the tier that answers a question, then answer it with citations from that tier."""

import re
from dataclasses import dataclass

import anthropic

from src.ingest import Chunk
from src.rerank import CANDIDATES, rerank
from src.retrieval import Index

MODEL = "claude-opus-5"
CORE_THRESHOLD = 0.55  # cosine similarity to the nearest core chunk; picked by hand on this corpus
TOP_K = 5

SYSTEM = ("Answer the question using only the numbered sources. Cite each source you rely on as [n] "
          "right after the claim it supports. If the sources do not contain the answer, say so.")


@dataclass
class Answer:
    tier: str  # "core" or "retrieved"
    similarity: float  # the number the routing decision was made on
    text: str
    cited: list[Chunk]


def route(query: str, core: Index, corpus: Index) -> tuple[str, float, list[Chunk]]:
    """Core tier: the whole core corpus goes into context and nothing is retrieved.

    The decision uses the same dense similarity the corpus tier ranks with, so the printed score
    is directly comparable across queries. A fixed threshold is cheap and inspectable; the cost
    is that questions phrased unlike the core documents fall through to retrieval even when the
    core could have answered them.
    """
    _, similarity = core.dense_search(query, 1)[0]
    if similarity >= CORE_THRESHOLD:
        return "core", similarity, core.chunks
    fused = corpus.hybrid_search(query, CANDIDATES)
    return "retrieved", similarity, [chunk for chunk, _ in rerank(query, fused, TOP_K)]


def answer(query: str, core: Index, corpus: Index) -> Answer:
    tier, similarity, chunks = route(query, core, corpus)
    sources = "\n\n".join(f"[{i}] {chunk.cite()}\n{chunk.text}" for i, chunk in enumerate(chunks, start=1))
    response = anthropic.Anthropic().messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Sources:\n\n{sources}\n\nQuestion: {query}"}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    cited_numbers = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
    cited = [chunk for i, chunk in enumerate(chunks, start=1) if i in cited_numbers]
    return Answer(tier, similarity, text, cited)
