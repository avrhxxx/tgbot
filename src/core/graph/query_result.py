from dataclasses import dataclass, field


@dataclass
class GraphResult:
    found: bool

    entity_id: str | None = None
    entity_type: str | None = None

    entity_data: dict = field(default_factory=dict)
    relations: list[dict] = field(default_factory=list)

    meta: dict = field(default_factory=dict)