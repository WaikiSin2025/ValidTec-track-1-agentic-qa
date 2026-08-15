from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class FeatureTicket:
    id: str
    title: str
    description: str
    acceptance_criteria: list[str]
    interfaces: list[str] = field(default_factory=list)
    data_classification: str = "synthetic-only"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FeatureTicket":
        required = ["id", "title", "description", "acceptance_criteria"]
        missing = [key for key in required if not data.get(key)]
        if missing:
            raise ValueError(f"Missing required ticket fields: {', '.join(missing)}")
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            description=str(data["description"]),
            acceptance_criteria=list(data["acceptance_criteria"]),
            interfaces=list(data.get("interfaces", [])),
            data_classification=str(data.get("data_classification", "synthetic-only")),
        )


@dataclass
class Scenario:
    id: str
    requirement: str
    risk: str
    priority: str
    preconditions: list[str]
    steps: list[str]
    expected_result: str
    automation_candidate: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
