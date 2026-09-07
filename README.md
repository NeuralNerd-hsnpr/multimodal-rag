# multimodal-rag

A small, runnable demonstration of tiered hybrid retrieval over mixed file types, with the retrieval choices measured by an ablation rather than assumed.

## What it does

Two tiers hold the knowledge. A small, stable core corpus (`data/core/`, three short markdown files) is placed directly in the model's context. A larger corpus (`data/corpus/`, eighteen files) is retrieved from per query. A router decides which tier answers a given question.

Ingestion turns every file into the same chunk shape regardless of where it came from:

| source | how it becomes text | locator carried into the citation |
|---|---|---|
| markdown | read as is | none |
| PDF | text per page via pypdf | page number |
| image | caption from `data/corpus/captions.json` | none |
| audio | transcribed at ingest time with faster-whisper `tiny.en` | start time of the chunk |

A chunk is a document id, a source path, a modality, a locator and the text. Text is split into fixed windows of 120 words with 25 words of overlap, the same rule for every modality.

Retrieval over the corpus tier runs BM25 (rank-bm25) and dense cosine similarity (`all-MiniLM-L6-v2`) and fuses the two full rankings with reciprocal rank fusion. A cross-encoder (`ms-marco-MiniLM-L-6-v2`) then rescores the top twenty fused candidates and the top five go to the model.

The router embeds the question and compares its cosine similarity to the nearest core chunk against a fixed threshold of 0.55. At or above it, the whole core corpus goes into context and nothing is retrieved. Below it, the corpus tier answers. The similarity is printed with every decision so a reader can see how close the call was.

The answer step sends the numbered chunks and the question to the Anthropic Messages API and maps the `[n]` markers in the reply back to the chunks they cite. A cited audio chunk prints as its file and start time, a PDF chunk as its file and page.

## Running it

```
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python demo.py
```

`demo.py` is the only command. It exits with a clear message if `ANTHROPIC_API_KEY` is unset; that key is the only credential involved. All data is committed; nothing is downloaded at run time except model weights.

Three models are fetched by their libraries on first run and cached under the Hugging Face cache directory:

| model | purpose | approximate size |
|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | dense embeddings for both tiers and the router | 88 MB |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | reranking | 88 MB |
| `Systran/faster-whisper-tiny.en` | audio transcription | 75 MB |

Image captions are deliberately not produced at run time. `scripts/caption.py` captioned the three images once with `microsoft/git-base-coco` and the result is committed as `data/corpus/captions.json`; that model is a 674 MB download and buys captions that cannot read the text on a chart, so it was not worth putting on the first-run path, whereas transcription is cheap enough to run for real. The caption script needs `pip install -r requirements-dev.txt` and is only run again when the images change.

The retrieval ablation needs no API key and can be run on its own:

```
python -m src.ablation
```

Smoke tests, also key-free:

```
pip install -r requirements-dev.txt
python -m pytest -q
```

### What the demo prints

1. A count of chunks per tier and per modality.
2. The ablation table and per-query rank table shown below.
3. Two questions, one routed to each tier. For each: the tier chosen, the similarity the decision was made on next to the threshold, the model's answer, and the list of cited chunks with their locators.

The two demo questions are "Which planets are the inner planets?" and "How big is Deimos and how long does it take to orbit Mars?". The first is answerable from the core overview; the second is answerable only from a transcribed recording. No example answers are reproduced here because none were produced during development of this repository.

## Ablation

The same 26 queries were run against four strategies over the corpus tier: 18 documents, 34 chunks. Gold labels are at document level, so a strategy scores when any chunk of the right document appears at the given rank. Output of `python -m src.ablation`, copied verbatim:

```
Ablation: 26 queries over 18 documents (34 chunks), gold = source document, top 10 scored
strategy           hit@1  recall@5    mrr
bm25                0.81      0.88   0.84
dense               0.81      0.96   0.86
hybrid              0.73      0.92   0.83
hybrid + rerank     0.81      0.96   0.86

Rank of the gold document per query (0 = not in top 10)
                                                                   bm25  dense hybrid rerank
Which planet has the largest temperature swing between day and        1      1      1      1
Why is Venus hotter than Mercury even though it is farther fro        5      2      3      2
On which planet does the Sun rise in the west?                        1      5      1      1
What causes the seasons on Earth?                                     1      1      1      1
What is the tallest volcano in the Solar System?                      1      5      2      1
How long has the Great Red Spot been observed?                        1      3      2      1
What are Saturn's rings made of and how thick are they?               1      1      1      1
Why does a comet's tail point away from the Sun?                      1      1      1      1
What is the difference between a meteor and a meteorite?              1      1      1      1
How hot is the core of the Sun?                                       1      1      1      1
How long does sunlight take to reach Earth?                           1      1      1      1
Why does Uranus rotate on its side?                                   1      1      1      1
Who discovered Uranus and in what year?                               1      1      1      1
How was Neptune's position predicted before anyone observed it        1      1      1      1
Why was Pluto reclassified as a dwarf planet?                         1      1      1      1
What did New Horizons find on Pluto?                                  1      1      1      1
Which figure compares the sizes of the planets side by side?          8      1      2      5
Is there a chart of how far each planet is from the Sun?              0      1      0      0
Show me a picture of Saturn with its rings.                           8      6      6      5
How big is Deimos and how long does it take to orbit Mars?            1      1      1      1
Who discovered the moons of Mars?                                     1      1      1      1
Which moon of Jupiter is the most volcanically active?                1      1      1      1
Which is the largest moon in the Solar System?                        1      1      1      1
What did the Huygens probe do at Titan?                               1      1      1      1
Where do the geysers on Enceladus come from?                          2      1      2      2
What is the giant impact hypothesis for the origin of the Moon        1      1      1      1
```

This is 26 hand-written queries over 18 documents. It is a check that the pipeline retrieves what it should, not a benchmark, and one query moving changes Hit@1 by about four points.

What the numbers say on this corpus:

- Dense retrieval alone and hybrid plus rerank tie on every metric. Reranking did not beat the best single retriever here; it recovered the ground that fusion lost.
- Plain reciprocal rank fusion scored below both of its inputs on Hit@1. On the volcano query, BM25 placed the gold chunk first and dense placed it fifth; fusion put ahead of it a chunk that was third in one ranking and second in the other. Rank fusion rewards being decent in both lists over being first in one, which is the known cost of fusing by rank alone.
- The three image queries account for most of the misses under every strategy. Captions of charts do not contain the numbers or labels drawn on them. The one image query that dense retrieval found at rank 1 fell outside BM25's top ten because the caption and the query share no content word: "far" against "distance", "planet" against "planets". The tokenizer does no stemming and no stopword removal, so only "of" and "the" matched.
- Whisper `tiny.en` mangles most proper nouns in the synthetic recordings: "Deimos" is transcribed as "Dados", "Enceladus" as "sell at us", "Ganymede" as "Can immediately", "Huygens" as "hydrogen". The transcripts are used as produced. The expectation was that a query naming one of these moons would be unreachable for BM25 and partly recoverable by dense retrieval. That is not what happened for Deimos: BM25 ranked the recording first anyway, carried by "Mars", "orbit", "moons" and "hours" in the same chunk. The Enceladus query is the only one where the pattern showed, and only by one rank: dense placed the recording first, BM25 second, and the reranker left it second.

## Design decisions and their tradeoffs

Fusion by rank rather than by score. Reciprocal rank fusion needs no calibration between BM25 scores and cosine similarities, which is why it is the default choice in small systems. The price is that it flattens confidence: a chunk that one retriever is sure about is worth exactly as much as any other first-place result. The ablation above shows that price being paid.

A threshold router rather than a model call. Routing on cosine similarity to the core chunks costs nothing extra and prints a number a reader can argue with. The threshold was picked by eye on this corpus, and questions phrased unlike the core documents fall through to retrieval even when the core could have answered them. A model-based router would be more forgiving of phrasing at the cost of a call per question and a decision that cannot be inspected.

Document-level gold labels. Labelling which document answers a query is unambiguous when facts are partitioned across documents, as they are here. It also means a strategy gets credit for returning the wrong chunk of the right document, which inflates every number equally.

## Limitations

- 18 documents and 26 queries. Differences of one or two queries are within what a single rewording could flip.
- The corpus was written for this repository. The facts are partitioned so that each query has exactly one gold document, which is cleaner than any real collection.
- The audio is synthetic speech from espeak-ng, and the transcription errors above come from that voice and a tiny model. Real recordings would fail differently.
- Image retrieval depends entirely on a one-line caption from a small captioning model. The captions in `data/corpus/captions.json` are generic and cannot see chart labels, so questions about what a chart shows mostly fail.
- The router threshold is a hand-picked constant for this corpus. Similarities for image questions sit close to those for genuinely core questions, so the margin is thin; the demo prints the score with each decision for that reason.
- The BM25 tokenizer lowercases and splits on non-alphanumerics; there is no stemming or stopword removal.
- The answer step was not run against the Anthropic API during development, only its routing, prompt construction and citation parsing.
- Everything is rebuilt on every run. There is no index cache, because at this size there is nothing to save.

## Layout

```
demo.py                 the one command
src/ingest.py           files -> chunks with provenance
src/retrieval.py        BM25, dense, reciprocal rank fusion
src/rerank.py           cross-encoder over fused candidates
src/router.py           tier decision and cited answering
src/ablation.py         four strategies, three metrics, per-query ranks
scripts/caption.py      offline image captioning, output committed
tests/test_smoke.py     ingestion, retrieval and routing checks on the committed corpus
data/core/              in-context tier
data/corpus/            retrieved tier, plus captions.json and queries.json alongside
```
