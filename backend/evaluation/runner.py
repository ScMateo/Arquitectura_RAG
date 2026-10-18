"""Evaluation runner (PLAN_VALIDACION.md §7).

Indexes the synthetic corpus into a dedicated collection, runs the 40 cases
through the real retrieval + generation pipeline, measures per-stage latency and
resource usage with the non-invasive instrumentation (Option A) and computes the
retrieval and generation metrics.

Usage:
    cd Arquitectura_RAG
    PYTHONPATH=backend python scripts/evaluate.py
    PYTHONPATH=backend python scripts/evaluate.py --judge --limit 8
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.application.services.generation_service import GenerationService
from app.application.services.retrieval_service import RetrievalService
from app.core.config import get_settings
from app.domain.entities.chunk import Chunk
from app.domain.interfaces.llm_provider import ILLMProvider
from app.domain.value_objects.query_analysis import QueryAnalysis
from app.domain.value_objects.query_type import QueryType
from app.infrastructure.embeddings import Bm25SparseEncoder, HuggingFaceAdapter
from app.infrastructure.ingestion import (
    AcronymNormalizer,
    Cleaner,
    CsvIngestor,
    LogicalUnitChunker,
)
from app.infrastructure.llm import GeminiAdapter
from app.infrastructure.reranking import WeightedReranker
from app.infrastructure.vectorstore import QdrantAdapter
from qdrant_client import QdrantClient

from evaluation.cases import EvalCase, build_cases
from evaluation.corpus import THEMES, build_researchers, write_csv
from evaluation.judge import Judge
from evaluation.metrics import (
    mean,
    mrr_at_k,
    ndcg_at_k,
    percentile,
    precision_at_k,
    recall_at_k,
)
from evaluation.timing import ResourceMonitor, StageTimer, instrument

# HU-09 evidence-based mapping for the synthetic corpus (shared by documents and queries).
ACRONYM_MAPPING = {
    "UNAL": "Universidad Nacional de Colombia",
    "UdeA": "Universidad de Antioquia",
    "UIS": "Universidad Industrial de Santander",
    "Unicauca": "Universidad del Cauca",
    "INS": "Instituto Nacional de Salud",
    "UPTC": "Universidad Pedagógica y Tecnológica de Colombia",
}

DEFAULT_THRESHOLDS = {
    "faithfulness": 0.85,
    "answer_relevancy": 0.80,
    "answer_correctness": 0.70,
    "precision_5": 0.70,
    "recall_10": 0.85,
    "mrr_10": 0.75,
    "ndcg_10": 0.80,
    "rejection": 0.90,
}

_REJECTION_MARKERS = (
    "insuficiente",
    "no hay informaci",
    "no se encontr",
    "no se dispone",
    "no hay datos",
    "no aparece",
    "sin informaci",
    "no es posible responder",
)


class StubLLMProvider:
    """Deterministic stand-in (implements ILLMProvider) for quota-free runs.

    Classifies a query as specific when it contains a known researcher name and
    otherwise as general, so the retrieval metrics remain meaningful without
    consuming the LLM quota. Generation just echoes a fixed marker.
    """

    def __init__(self, researcher_names: list[str]) -> None:
        self._names = researcher_names

    def analyze_query(self, query: str) -> QueryAnalysis:
        lowered = query.lower()
        for name in self._names:
            if name.lower() in lowered:
                return QueryAnalysis(
                    query_type=QueryType.SPECIFIC,
                    researcher_name=name,
                )
        return QueryAnalysis(query_type=QueryType.GENERAL, researcher_name=None)

    def generate(self, prompt: str) -> str:
        return "respuesta simulada"

    def stream(self, prompt: str):
        yield "respuesta simulada"


@dataclass
class CaseResult:
    """Resultado de un caso de evaluación."""

    id: str
    kind: str
    query: str
    n_relevant: int
    n_retrieved: int
    precision_5: float
    precision_10: float
    recall_5: float
    recall_10: float
    mrr_10: float
    ndcg_10: float
    author_recall_10: float
    author_coverage: float
    rejected: int
    urls_valid: int
    ttft_ms: float
    gen_ms: float
    retrieval_ms: float
    faithfulness: float
    answer_relevancy: float
    answer_correctness: float
    answer: str
    sources: str
    error: str


def _select_per_kind(cases: list[EvalCase], per_kind: int) -> list[EvalCase]:
    """Selecciona hasta `per_kind` casos por tipo, de forma estratificada."""
    selected: list[EvalCase] = []
    for kind in ("puntual", "general", "relacional", "comparativa", "negativa"):
        selected.extend([case for case in cases if case.kind == kind][:per_kind])
    return selected


def _is_relevant(chunk: Chunk, case: EvalCase, authors: set[str]) -> bool:
    if chunk.author not in authors:
        return False
    if not case.expected_sections:
        return True
    return chunk.section.value in case.expected_sections


def _mentions(answer: str, name: str) -> bool:
    lowered = answer.lower()
    if name.lower() in lowered:
        return True
    return all(token in lowered for token in name.lower().split()[-2:])


def _author_recall_10(retrieved: list[Chunk], authors: set[str], case: EvalCase) -> float:
    """Cobertura de autores relevantes en los 10 primeros fragmentos.

    Para consultas abiertas ("¿quién trabaja en X?") el conjunto de fragmentos
    relevantes es enorme, por lo que la recuperación se mide a nivel de autor.
    """
    if not case.relevant_authors:
        return 0.0
    top_authors = {chunk.author for chunk in retrieved[:10] if chunk.author in authors}
    return len(top_authors) / len(case.relevant_authors)


def _author_coverage(answer: str, case: EvalCase) -> float:
    if not case.relevant_authors:
        return 1.0
    hits = sum(1 for name in case.relevant_authors if _mentions(answer, name))
    return hits / len(case.relevant_authors)


def _is_rejected(answer: str) -> int:
    lowered = answer.lower()
    return int(any(marker in lowered for marker in _REJECTION_MARKERS))


def _summarize(results: list[CaseResult], kinds: tuple[str, ...]) -> dict[str, float]:
    retrieval = [r for r in results if r.kind in kinds and r.n_relevant > 0]
    generation = [r for r in results if r.kind in kinds]
    summary = {
        "casos": float(len(generation)),
        "precision_5": mean([r.precision_5 for r in retrieval]),
        "precision_10": mean([r.precision_10 for r in retrieval]),
        "recall_5": mean([r.recall_5 for r in retrieval]),
        "recall_10": mean([r.recall_10 for r in retrieval]),
        "mrr_10": mean([r.mrr_10 for r in retrieval]),
        "ndcg_10": mean([r.ndcg_10 for r in retrieval]),
        "author_recall_10": mean([r.author_recall_10 for r in retrieval]),
        "cobertura_autores": mean([r.author_coverage for r in generation]),
        "faithfulness": mean([r.faithfulness for r in generation if r.faithfulness > 0]),
        "answer_relevancy": mean([r.answer_relevancy for r in generation if r.answer_relevancy > 0]),
        "answer_correctness": mean([r.answer_correctness for r in generation if r.answer_correctness > 0]),
    }
    negatives = [r for r in results if r.kind == "negativa"]
    if negatives:
        summary["rechazo_negativas"] = mean([float(r.rejected) for r in negatives])
    return summary


def _print_summary(
    results: list[CaseResult],
    thresholds: dict[str, float],
    timer: StageTimer,
    judge_enabled: bool,
) -> None:
    print("\n== Metricas de recuperacion (macro) ==")
    for label, kinds in (
        ("global", ("puntual", "general", "relacional", "comparativa")),
        ("puntual", ("puntual",)),
        ("general", ("general",)),
        ("relacional", ("relacional",)),
        ("comparativa", ("comparativa",)),
    ):
        summary = _summarize(results, kinds)
        if summary["casos"] == 0:
            continue
        print(
            f"{label:12s} P@5={summary['precision_5']:.3f} P@10={summary['precision_10']:.3f} "
            f"R@5={summary['recall_5']:.3f} R@10={summary['recall_10']:.3f} "
            f"MRR@10={summary['mrr_10']:.3f} nDCG@10={summary['ndcg_10']:.3f} "
            f"Raut@10={summary['author_recall_10']:.3f} cob_resp={summary['cobertura_autores']:.3f}"
        )

    negatives = [r for r in results if r.kind == "negativa"]
    if negatives:
        rate = mean([float(r.rejected) for r in negatives])
        print(f"rechazo en negativas: {rate:.3f} (objetivo >= {thresholds['rejection']:.2f})")

    print("\n== Metricas de generacion (juez) ==")
    if not judge_enabled:
        print("juez desactivado (ejecutar con --judge para faithfulness/relevancy/correctness)")
    else:
        summary = _summarize(results, ("puntual", "general", "relacional", "comparativa", "negativa"))
        print(
            f"faithfulness={summary['faithfulness']:.3f} (>= {thresholds['faithfulness']:.2f}) "
            f"relevancy={summary['answer_relevancy']:.3f} (>= {thresholds['answer_relevancy']:.2f}) "
            f"correctness={summary['answer_correctness']:.3f} (>= {thresholds['answer_correctness']:.2f})"
        )

    print("\n== Desempeno ==")
    ttfts = [r.ttft_ms for r in results]
    gens = [r.gen_ms for r in results]
    retrievals = [r.retrieval_ms for r in results]
    print(f"TTFT    media={mean(ttfts):8.1f} ms  P95={percentile(ttfts, 0.95):8.1f} ms")
    print(f"gen     media={mean(gens):8.1f} ms")
    print(f"retriev media={mean(retrievals):8.1f} ms")
    for stage in ("normalizacion", "clasificacion", "embedding", "busqueda", "reranking"):
        durations = timer.durations(stage)
        if durations:
            print(f"  {stage:14s} media={mean(durations) * 1000:7.1f} ms")


def _monkeypatch_indexer_stages(
    timer: StageTimer,
    normalizer: AcronymNormalizer,
    llm: Any,
    embedding: HuggingFaceAdapter,
    vector_store: QdrantAdapter,
    reranker: WeightedReranker,
) -> None:
    instrument(timer, normalizer, "normalize", "normalizacion")
    instrument(timer, llm, "analyze_query", "clasificacion")
    instrument(timer, embedding, "embed_query", "embedding")
    instrument(timer, vector_store, "search", "busqueda")
    instrument(timer, reranker, "rerank", "reranking")


def run(args: argparse.Namespace) -> int:
    settings = get_settings()
    thresholds = dict(DEFAULT_THRESHOLDS)
    if args.thresholds and Path(args.thresholds).exists():
        thresholds.update(json.loads(Path(args.thresholds).read_text(encoding="utf-8")))

    researchers = build_researchers()
    corpus_path = write_csv(researchers, args.corpus)
    cases = build_cases(researchers, THEMES)
    if args.per_kind:
        cases = _select_per_kind(cases, args.per_kind)
    elif args.limit:
        cases = cases[: args.limit]
    print(f"corpus: {corpus_path} ({len(researchers)} investigadores)")
    print(f"casos:  {len(cases)}")

    normalizer = AcronymNormalizer(ACRONYM_MAPPING)
    cleaner = Cleaner()
    chunker = LogicalUnitChunker(max_chunk_size=settings.chunk_size)
    ingestor = CsvIngestor(cleaner, normalizer, chunker)
    embedding = HuggingFaceAdapter(settings.embedding_model_name, settings.embedding_device)
    vector_store = QdrantAdapter(
        url=settings.qdrant_url,
        collection_name=args.collection,
        sparse_encoder=Bm25SparseEncoder(),
    )
    llm: ILLMProvider = (
        StubLLMProvider([researcher.name for researcher in researchers])
        if args.stub_llm
        else GeminiAdapter(
            api_key=settings.google_api_key.get_secret_value(),
            model=settings.gemini_model,
            timeout_ms=settings.llm_timeout_ms,
            analysis_temperature=settings.llm_temperature_analysis,
            generation_temperature=settings.llm_temperature_generation,
        )
    )
    reranker = WeightedReranker()

    timer = StageTimer()
    monitor = ResourceMonitor()
    monitor.start()

    client = QdrantClient(url=settings.qdrant_url)
    if client.collection_exists(args.collection):
        client.delete_collection(args.collection)

    print("indexando corpus de evaluacion...")
    index_start = time.perf_counter()
    chunks = list(ingestor.ingest(str(corpus_path)))
    vectors = embedding.embed_documents([chunk.content for chunk in chunks])
    vector_store.add(chunks, vectors)
    index_seconds = time.perf_counter() - index_start
    print(f"indexado: {len(chunks)} fragmentos en {index_seconds:.1f}s")

    _monkeypatch_indexer_stages(timer, normalizer, llm, embedding, vector_store, reranker)
    retrieval_service = RetrievalService(
        normalizer=normalizer,
        llm_provider=llm,
        embedding_provider=embedding,
        vector_store=vector_store,
        reranker=reranker,
        top_k_retrieval=settings.top_k_retrieval,
        top_k_final=settings.top_k_final,
    )
    generation_service = GenerationService(llm_provider=llm)
    judge = Judge(llm) if args.judge and not args.stub_llm else None

    results: list[CaseResult] = []
    for case in cases:
        authors = set(case.relevant_authors)
        error = ""
        retrieved: list[Chunk] = []
        answer = ""
        ttft_ms = 0.0
        gen_ms = 0.0
        retrieval_start = time.perf_counter()
        try:
            retrieved = retrieval_service.retrieve(case.query)
            retrieval_ms = (time.perf_counter() - retrieval_start) * 1000

            generation_start = time.perf_counter()
            pieces: list[str] = []
            for delta in generation_service.generate_stream(case.query, retrieved, []):
                if not pieces:
                    ttft_ms = (time.perf_counter() - generation_start) * 1000
                pieces.append(delta)
            gen_ms = (time.perf_counter() - generation_start) * 1000
            answer = "".join(pieces).strip()
        except Exception as exc:  # noqa: BLE001 - keep the run going on API/quota errors
            retrieval_ms = (time.perf_counter() - retrieval_start) * 1000
            error = f"{type(exc).__name__}: {exc}".splitlines()[0][:200]

        relevance = [_is_relevant(chunk, case, authors) for chunk in retrieved]
        total_relevant = sum(
            1 for chunk in chunks if _is_relevant(chunk, case, set(case.relevant_authors))
        )
        scores = (
            judge.evaluate(
                case.query,
                answer,
                "\n".join(chunk.content for chunk in retrieved),
                case.reference,
            )
            if judge
            else None
        )

        results.append(
            CaseResult(
                id=case.id,
                kind=case.kind,
                query=case.query,
                n_relevant=total_relevant,
                n_retrieved=len(retrieved),
                precision_5=precision_at_k(relevance, 5),
                precision_10=precision_at_k(relevance, 10),
                recall_5=recall_at_k(relevance, 5, total_relevant),
                recall_10=recall_at_k(relevance, 10, total_relevant),
                mrr_10=mrr_at_k(relevance, 10),
                ndcg_10=ndcg_at_k(relevance, 10, total_relevant),
                author_recall_10=_author_recall_10(retrieved, authors, case),
                author_coverage=_author_coverage(answer, case),
                rejected=_is_rejected(answer),
                urls_valid=int(all(chunk.url.value.startswith("http") for chunk in retrieved)),
                ttft_ms=ttft_ms,
                gen_ms=gen_ms,
                retrieval_ms=retrieval_ms,
                faithfulness=scores.faithfulness if scores else 0.0,
                answer_relevancy=scores.answer_relevancy if scores else 0.0,
                answer_correctness=scores.answer_correctness if scores else 0.0,
                answer=answer,
                sources="; ".join(sorted({chunk.url.value for chunk in retrieved})),
                error=error,
            )
        )
        status = f"error={error}" if error else f"ttft={ttft_ms:.0f}ms"
        print(
            f"  [{case.id}] {case.kind:11s} n_rel={total_relevant:3d} "
            f"R@10={results[-1].recall_10:.2f} nDCG@10={results[-1].ndcg_10:.2f} "
            f"cov={results[-1].author_coverage:.2f} {status}"
        )

    monitor.stop()
    _print_summary(results, thresholds, timer, judge_enabled=judge is not None)
    print(
        f"\nrecursos: CPU={monitor.cpu_percent:.1f}%  RAM pico={monitor.peak_rss_mb:.0f} MB  "
        f"wall={monitor.wall_seconds:.1f}s"
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(results[0]).keys()))
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))
    print(f"resultados: {output} ({len(results)} filas)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ejecuta la evaluacion del sistema RAG CvLAC.")
    parser.add_argument("--corpus", default="data/processed/eval_corpus.csv")
    parser.add_argument("--output", default="data/processed/evaluation_results.csv")
    parser.add_argument("--collection", default="cvlac_eval")
    parser.add_argument("--judge", action="store_true", help="Activa el juez LLM de generacion.")
    parser.add_argument(
        "--stub-llm",
        action="store_true",
        help="Usa un LLM simulado (sin cuota) para validar la mecanica del harness.",
    )
    parser.add_argument("--limit", type=int, default=0, help="Limita el numero de casos (0 = todos).")
    parser.add_argument(
        "--per-kind",
        type=int,
        default=0,
        help="Selecciona hasta N casos por tipo (0 = todos). Util para respetar la cuota de API.",
    )
    parser.add_argument("--thresholds", default=None, help="JSON con umbrales personalizados.")
    return run(parser.parse_args(argv))
