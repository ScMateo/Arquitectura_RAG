"""Unit tests for the domain exception hierarchy."""

from app.core.exceptions import (
    ConfigurationError,
    DomainError,
    IngestionError,
    RetrievalError,
)


def test_specific_errors_inherit_from_domain_error() -> None:
    assert issubclass(RetrievalError, DomainError)
    assert issubclass(ConfigurationError, DomainError)
    assert issubclass(IngestionError, DomainError)
