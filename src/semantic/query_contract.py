from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class QueryIntent(str, Enum):
    """
    High-level intent classification for user requests.
    """

    ENTITY_LOOKUP = "entity_lookup"
    ENTITY_DETAILS = "entity_details"
    RELATION_QUERY = "relation_query"
    SYSTEM_HELP = "system_help"
    UNKNOWN = "unknown"


@dataclass
class Query:
    """
    Canonical semantic query object shared across:
    - semantic layer
    - runtime pipeline
    - graph retrieval
    - AI narration
    """

    # tracing / observability
    trace_id: str

    # telegram / runtime identity
    user_id: str
    session_id: str

    # language detected from user input
    language: str

    # original telegram message
    raw_input: str

    # normalized form used for matching/cache
    normalized_input: str

    # semantic interpretation
    intent: QueryIntent

    # resolved graph entity
    entity_id: Optional[str] = None
    entity_type: Optional[str] = None

    # requested information
    requested_fields: list[str] = field(default_factory=list)
    requested_relations: list[str] = field(default_factory=list)

    # semantic confidence score
    confidence: float = 0.0

    # runtime/session context
    session_context: dict = field(default_factory=dict)

    # optional metadata
    metadata: dict = field(default_factory=dict)