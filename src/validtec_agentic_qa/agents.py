from __future__ import annotations

from collections import Counter
from typing import Any

from .models import FeatureTicket, Scenario


class RequirementAnalysisAgent:
    """Deterministic baseline for requirement decomposition."""

    RISK_KEYWORDS = {
        "auth": "authorization",
        "unauthorized": "authorization",
        "license": "entitlement",
        "role": "authorization",
        "email": "identity/data validation",
        "duplicate": "data integrity",
        "invite": "workflow state",
    }

    def run(self, ticket: FeatureTicket) -> dict[str, Any]:
        text = " ".join([ticket.title, ticket.description, *ticket.acceptance_criteria]).lower()
        risks = sorted({label for word, label in self.RISK_KEYWORDS.items() if word in text})
        if not risks:
            risks = ["functional regression"]
        return {
            "ticket_id": ticket.id,
            "summary": ticket.title,
            "interfaces": ticket.interfaces,
            "acceptance_criteria_count": len(ticket.acceptance_criteria),
            "identified_risks": risks,
            "data_policy": ticket.data_classification,
            "test_objective": "Verify acceptance criteria and high-risk negative paths with traceable evidence.",
        }


class TestDesignAgent:
    """Creates traceable positive and negative scenarios from acceptance criteria."""

    def run(self, ticket: FeatureTicket, analysis: dict[str, Any]) -> list[Scenario]:
        scenarios: list[Scenario] = []
        risks = analysis["identified_risks"]
        default_risk = risks[0] if risks else "functional regression"

        for idx, criterion in enumerate(ticket.acceptance_criteria, start=1):
            lower = criterion.lower()
            negative = any(word in lower for word in ("reject", "cannot", "unauthorized", "invalid", "duplicate"))
            scenarios.append(
                Scenario(
                    id=f"{ticket.id}-S{idx:02d}",
                    requirement=criterion,
                    risk="authorization" if "unauthorized" in lower or "role" in lower else default_risk,
                    priority="P0" if negative or "license" in lower else "P1",
                    preconditions=["Use isolated synthetic test data", "Target service is healthy"],
                    steps=[
                        f"Arrange data for: {criterion}",
                        "Execute the relevant API or UI action",
                        "Capture response, state transition, and identifiers",
                        "Verify the resulting system state",
                    ],
                    expected_result=criterion,
                    automation_candidate=True,
                )
            )

        # Always add a resilience/cleanup scenario because test-data control is part of the QA contract.
        scenarios.append(
            Scenario(
                id=f"{ticket.id}-S{len(scenarios)+1:02d}",
                requirement="Test data can be cleaned up after execution",
                risk="environment contamination",
                priority="P1",
                preconditions=["Synthetic organization and user records exist"],
                steps=["Delete or reset created test entities", "Query for residual test records"],
                expected_result="No synthetic records remain after cleanup",
                automation_candidate=True,
            )
        )
        return scenarios


class AutomationSpecificationAgent:
    """Transforms approved scenarios into framework-neutral automation contracts."""

    def run(self, ticket: FeatureTicket, scenarios: list[Scenario]) -> dict[str, Any]:
        tests = []
        for scenario in scenarios:
            framework = "postman/newman" if "REST API" in ticket.interfaces else "playwright"
            tests.append({
                "scenario_id": scenario.id,
                "framework": framework,
                "priority": scenario.priority,
                "setup": scenario.preconditions,
                "actions": scenario.steps,
                "assertions": [scenario.expected_result],
                "evidence": ["request/response or trace", "assertion result", "execution timestamp"],
            })
        return {
            "ticket_id": ticket.id,
            "contract_version": "1.0",
            "recommended_execution_order": [t["scenario_id"] for t in tests],
            "tests": tests,
            "release_gate": "All P0 tests must pass; P1 failures require QA review.",
        }


class ReportingAgent:
    def run(self, ticket: FeatureTicket, analysis: dict[str, Any], scenarios: list[Scenario], approved: bool) -> str:
        priorities = Counter(s.priority for s in scenarios)
        risks = ", ".join(analysis["identified_risks"])
        return f"""# QA Workflow Report — {ticket.id}\n\n## Feature\n{ticket.title}\n\n## QA decision\n- Scenario set approved: **{'YES' if approved else 'NO'}**\n- Scenario count: **{len(scenarios)}**\n- P0 scenarios: **{priorities.get('P0', 0)}**\n- P1 scenarios: **{priorities.get('P1', 0)}**\n\n## Identified risks\n{risks}\n\n## Control statement\nGenerated scenarios are advisory until reviewed by QA. Automation generation is blocked unless the approval gate is explicitly satisfied.\n"""
