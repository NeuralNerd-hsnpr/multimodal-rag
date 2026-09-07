"""Turn a directory of mixed files into one flat list of text chunks with provenance."""

import json
from dataclasses import dataclass
from pathlib import Path

import pypdf
from faster_whisper import WhisperModel

CHUNK_WORDS = 120
OVERLAP_WORDS = 25


@dataclass
class Chunk:
    doc_id: str  # file name, the unit the ablation scores against
    source: str  # path relative to the repo root
    modality: str  # text, pdf, image or audio
    locator: str  # page or start time inside the source; empty when the whole file is the unit
    text: str

    def cite(self) -> str:
        return f"{self.source} {self.locator}".strip()


def split_words(text: str) -> list[str]:
    """Fixed-size word windows with overlap. Crude, but the same rule applies to every modality."""
    words = text.split()
    step = CHUNK_WORDS - OVERLAP_WORDS
    starts = range(0, max(len(words) - OVERLAP_WORDS, 1), step)
    return [" ".join(words[i : i + CHUNK_WORDS]) for i in starts]


def _text_chunks(path: Path, modality: str, text: str, locator: str = "") -> list[Chunk]:
    return [Chunk(path.name, str(path), modality, locator, t) for t in split_words(text)]


def _pdf_chunks(path: Path) -> list[Chunk]:
    chunks = []
    for number, page in enumerate(pypdf.PdfReader(path).pages, start=1):
        chunks += _text_chunks(path, "pdf", page.extract_text(), f"p.{number}")
    return chunks


def _audio_chunks(path: Path, model: WhisperModel) -> list[Chunk]:
    """Group transcript segments into chunks; the locator is the start time of the first segment.

    The transcript is used as Whisper produced it. Mis-heard proper nouns stay in, because
    that is the condition retrieval has to cope with on real recordings.
    """
    segments, _ = model.transcribe(str(path))
    chunks, words, start = [], [], 0.0
    for seg in segments:
        if not words:
            start = seg.start
        words += seg.text.split()
        if len(words) >= CHUNK_WORDS:
            chunks.append(Chunk(path.name, str(path), "audio", f"{start:.0f}s", " ".join(words)))
            words = []
    if words:
        chunks.append(Chunk(path.name, str(path), "audio", f"{start:.0f}s", " ".join(words)))
    return chunks


def load_dir(directory: str) -> list[Chunk]:
    """Chunk every supported file in a directory, in name order.

    Image captions are read from captions.json next to the images. They were produced once by
    scripts/caption.py and committed, so the demo does not download a captioning model.
    """
    root = Path(directory)
    captions = json.loads((root / "captions.json").read_text()) if (root / "captions.json").exists() else {}
    whisper = None
    chunks: list[Chunk] = []
    for path in sorted(root.iterdir()):
        suffix = path.suffix.lower()
        if suffix in (".md", ".txt"):
            chunks += _text_chunks(path, "text", path.read_text())
        elif suffix == ".pdf":
            chunks += _pdf_chunks(path)
        elif suffix in (".png", ".jpg", ".jpeg"):
            chunks.append(Chunk(path.name, str(path), "image", "", captions[path.name]))
        elif suffix == ".wav":
            # tiny.en is about 75 MB and is fetched on first run; int8 keeps CPU transcription fast.
            whisper = whisper or WhisperModel("tiny.en", device="cpu", compute_type="int8")
            chunks += _audio_chunks(path, whisper)
    return chunks
