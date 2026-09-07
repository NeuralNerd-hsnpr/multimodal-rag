"""Smoke tests over the committed corpus. Run from the repo root: python -m pytest -q"""

import json

import pytest

from src.ablation import gold_rank
from src.ingest import load_dir
from src.rerank import rerank
from src.retrieval import Index
from src.router import CORE_THRESHOLD, route


@pytest.fixture(scope="module")
def corpus():
    return load_dir("data/corpus")


@pytest.fixture(scope="module")
def index(corpus):
    return Index(corpus)


def test_every_modality_is_ingested_with_provenance(corpus):
    assert {c.modality for c in corpus} == {"text", "pdf", "image", "audio"}
    assert all(c.doc_id and c.source and c.text for c in corpus)
    assert all(c.locator.startswith("p.") for c in corpus if c.modality == "pdf")
    assert all(c.locator.endswith("s") for c in corpus if c.modality == "audio")
    assert all(c.cite().startswith("data/corpus/") for c in corpus)


def test_queries_point_at_existing_documents(corpus):
    docs = {c.doc_id for c in corpus}
    assert all(q["gold"] in docs for q in json.load(open("data/queries.json")))


def test_each_strategy_returns_ranked_chunks(index):
    query = "What are Saturn's rings made of?"
    for search in (index.bm25_search, index.dense_search, index.hybrid_search):
        results = search(query, 5)
        scores = [score for _, score in results]
        assert len(results) == 5 and scores == sorted(scores, reverse=True)
    assert len(rerank(query, index.hybrid_search(query, 20), 5)) == 5
    assert gold_rank(index.bm25_search(query, 10), "saturn.md") >= 1


def test_router_sends_each_demo_query_to_a_different_tier(index):
    core = Index(load_dir("data/core"))
    tier, similarity, chunks = route("Which planets are the inner planets?", core, index)
    assert tier == "core" and similarity >= CORE_THRESHOLD and chunks == core.chunks
    tier, similarity, chunks = route("How big is Deimos and how long does it take to orbit Mars?", core, index)
    assert tier == "retrieved" and similarity < CORE_THRESHOLD and len(chunks) == 5
