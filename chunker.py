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


MAX_SECTION = 1200   # characters; above this a section gets split at a paragraph
MIN_SECTION = 150    # characters; below this a section merges into its neighbour


def _split_long_section(text: str) -> list[str]:
    """
    Cut an over-long section at paragraph breaks rather than mid-sentence.

    Only `guide_marchwood.md`'s district rundown and a couple of the
    cross-cutting guides reach MAX_SECTION. Splitting those on a blank line
    keeps whole paragraphs intact; splitting them at a character count is what
    produced "## Eat and drin" in the starter's output.
    """
    if len(text) <= MAX_SECTION:
        return [text]

    pieces: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) > MAX_SECTION and current:
            pieces.append(current)
            current = paragraph
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split each guide at its `##` headings, one section per chunk.

    These documents are travel guides divided into labelled sections —
    "Getting there", "Where to eat", "When to go". The answer to a question is
    almost always the whole of exactly one section, so the section is the
    natural unit and a character count is not.

    Every chunk keeps the heading it belongs to as its first line. That heading
    is real retrieval signal: "Getting there" in a chunk about buses is the
    difference between a chunk that reads as being about travel and one that
    reads as being about a timetable. The document title is prepended to every
    chunk for the same reason — a section that says "two inns on the square"
    has to carry the name of the town it's in, or it can't answer anything on
    its own.

    Overlap is zero, deliberately. Overlap exists to stop a sentence being cut
    in half, and cutting at headings means no sentence is ever cut at all.
    Repeating the tail of "Where to eat" at the top of "What to see" would
    make both chunks match both questions slightly, which is the problem
    overlap is supposed to prevent.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        lines = doc.text.split("\n")

        # The `# Title` line, so each chunk can say which town it's about.
        title = ""
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Walk the document, breaking a new section at every `## ` heading.
        # Anything before the first heading is the document's intro paragraph.
        sections: list[str] = []
        current: list[str] = []
        for line in lines:
            if line.startswith("## "):
                if current:
                    sections.append("\n".join(current).strip())
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append("\n".join(current).strip())

        sections = [s for s in sections if s]

        # Four of the cross-cutting guides (walking, eating, seasons,
        # regional transport) open with a `# Title` line and go straight into
        # the first `## ` heading with no intro paragraph. That leaves a
        # preamble that is nothing but the title — a 23-character chunk with
        # no content under it, which is the exact thing criterion 4 rules out.
        # Drop it: the title gets prepended to every chunk below anyway.
        if sections and not sections[0].startswith("## "):
            preamble_body = "\n".join(
                line for line in sections[0].split("\n") if not line.startswith("# ")
            ).strip()
            if not preamble_body:
                sections.pop(0)

        # Merge a section too short to stand alone into the one before it.
        # guide_givens_mill.md's 174-character "Where to stay" is complete as
        # written; the merge only catches headings with nothing under them.
        merged: list[str] = []
        for section in sections:
            if merged and len(section) < MIN_SECTION:
                merged[-1] = f"{merged[-1]}\n\n{section}"
            else:
                merged.append(section)

        index = 0
        for section in merged:
            for piece in _split_long_section(section):
                # Prepend the town name unless this chunk already opens with it.
                text = piece if piece.startswith("# ") else f"# {title}\n\n{piece}"
                chunks.append(
                    Chunk(
                        text=text.strip(),
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1

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
