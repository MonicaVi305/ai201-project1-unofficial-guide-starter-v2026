"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Split documents into sentence-based chunks without producing empty fragments."""
    import re

    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        text = re.sub(r"\r\n?", "\n", doc.text).strip()
        if not text:
            continue

        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
        doc_chunks: list[str] = []

        for para in paragraphs:
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", para) if s.strip()]
            if not sentences:
                sentences = [para]

            current = ""
            for sentence in sentences:
                if not sentence:
                    continue

                if not current:
                    current = sentence
                    continue

                candidate = f"{current} {sentence}".strip()
                if len(candidate) <= chunk_size:
                    current = candidate
                    continue

                if len(current) >= 200:
                    doc_chunks.append(current.strip())
                    current = sentence
                else:
                    # If the current chunk is too short to stand alone, keep it with the
                    # next sentence rather than producing a fragment that fails quality.
                    if len(current) + 1 + len(sentence) <= chunk_size:
                        current = f"{current} {sentence}".strip()
                    else:
                        doc_chunks.append(current.strip())
                        current = sentence

            if current.strip():
                doc_chunks.append(current.strip())

        # Merge tiny, low-value fragments into nearby chunks so the app doesn't emit
        # leftovers that are too short to be useful.
        merged: list[str] = []
        for piece in doc_chunks:
            if merged and len(piece) < 200 and len(merged[-1]) + 1 + len(piece) <= chunk_size:
                merged[-1] = (merged[-1] + " " + piece).strip()
            else:
                merged.append(piece)

        if merged and len(merged[0]) < 200 and len(merged) > 1:
            merged[1] = (merged[0] + " " + merged[1]).strip()
            merged = merged[1:]

        for idx, piece in enumerate(merged):
            chunks.append(
                Chunk(
                    text=piece.strip(),
                    source=doc.source,
                    index=idx,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
