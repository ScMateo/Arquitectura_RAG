"""Evaluation tests over the test query set (recall-oriented, HU-04/05).

These tests require the full system: an indexed corpus and the real LLM API.
They are skipped unless RUN_EVALUATION=1 is set, to avoid API usage by default.

Usage:
    RUN_EVALUATION=1 pytest -m evaluation
"""

import os

import pytest

from tests.evaluation.queries import EVALUATION_QUERIES

pytestmark = [
    pytest.mark.evaluation,
    pytest.mark.skipif(
        os.environ.get("RUN_EVALUATION") != "1",
        reason="Requiere sistema completo + API key (activar con RUN_EVALUATION=1)",
    ),
]


@pytest.mark.parametrize(
    "case",
    EVALUATION_QUERIES,
    ids=[f"{case.category}-{index}" for index, case in enumerate(EVALUATION_QUERIES)],
)
def test_query_retrieves_expected_authors(case) -> None:
    from app.api.dependencies import get_chat_use_case
    from app.application.dto.chat import ChatRequest

    use_case = get_chat_use_case()
    response = use_case.execute(ChatRequest(message=case.question))

    retrieved_authors = {source.author for source in response.sources}
    missing = set(case.expected_authors) - retrieved_authors
    assert not missing, f"No se recuperó(aron) {missing} para {case.question!r}"
