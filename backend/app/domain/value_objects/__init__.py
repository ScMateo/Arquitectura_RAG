"""Domain value objects: inmutable types with validation."""

from .cvlac_url import CvLACUrl
from .message_role import MessageRole
from .query_analysis import QueryAnalysis
from .query_type import QueryType
from .section import Section

__all__ = ["CvLACUrl", "MessageRole", "QueryAnalysis", "QueryType", "Section"]
