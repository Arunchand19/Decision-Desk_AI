import json
import pickle
import math
import re
from dataclasses import dataclass
from pathlib import Path

from .config import get_settings

ROOT = Path(__file__).resolve().parents[1]
KB_DIR = ROOT / "knowledge_base"
INDEX_PATH = ROOT / "retrieval_index.pkl"


@dataclass
class Chunk:
    source: str
    text: str


class Retriever:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.idf: dict[str, float] = {}
        self.matrix: list[dict[str, float]] = []
        self.load_or_build()

    def load_or_build(self) -> None:
        if INDEX_PATH.exists():
            with INDEX_PATH.open("rb") as file:
                self.chunks, self.idf, self.matrix = pickle.load(file)
            expected_sources = {path.name for path in KB_DIR.glob("*.md")}
            loaded_sources = {chunk.source for chunk in self.chunks}
            if expected_sources.issubset(loaded_sources) and len(self.matrix) == len(self.chunks):
                return
        self.build()

    def build(self) -> None:
        self.chunks = []
        for path in sorted(KB_DIR.glob("*.md")):
            paragraphs = [part.strip() for part in path.read_text(encoding="utf-8").split("\n\n") if part.strip()]
            for paragraph in paragraphs:
                self.chunks.append(Chunk(source=path.name, text=paragraph))
        if not self.chunks:
            raise RuntimeError(f"No knowledge-base documents found in {KB_DIR}")
        term_sets = [set(_tokens(chunk.text)) for chunk in self.chunks]
        document_frequency: dict[str, int] = {}
        for terms in term_sets:
            for term in terms:
                document_frequency[term] = document_frequency.get(term, 0) + 1
        document_count = len(self.chunks)
        self.idf = {term: math.log((1 + document_count) / (1 + frequency)) + 1 for term, frequency in document_frequency.items()}
        self.matrix = [_embed(_tokens(chunk.text), self.idf) for chunk in self.chunks]
        with INDEX_PATH.open("wb") as file:
            pickle.dump((self.chunks, self.idf, self.matrix), file)

    def retrieve(self, query: str, top_k: int | None = None) -> list[dict[str, str | float]]:
        query_vector = _embed(_tokens(query), self.idf)
        scores = [_cosine(query_vector, vector) for vector in self.matrix]
        count = min(top_k or get_settings().top_k, len(self.chunks))
        indexes = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)[:count]
        return [{"source": self.chunks[index].source, "text": self.chunks[index].text, "score": float(scores[index])} for index in indexes]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _embed(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    counts: dict[str, int] = {}
    for token in tokens:
        if token in idf:
            counts[token] = counts.get(token, 0) + 1
    return {token: count * idf[token] for token, count in counts.items()}


def _cosine(left: dict[str, float], right: dict[str, float]) -> float:
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    dot_product = sum(value * right.get(term, 0.0) for term, value in left.items())
    return dot_product / (left_norm * right_norm)


retriever = Retriever()
