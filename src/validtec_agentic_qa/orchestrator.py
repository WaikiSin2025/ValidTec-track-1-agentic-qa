from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .agents import AutomationSpecificationAgent, ReportingAgent, RequirementAnalysisAgent, TestDesignAgent
from .models import FeatureTicket


class ApprovalRequired(RuntimeError):
    pass


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


class QAOrchestrator:
    def __init__(self) -> None:
        self.requirements = RequirementAnalysisAgent()
        self.test_design = TestDesignAgent()
        self.automation = AutomationSpecificationAgent()
        self.reporting = ReportingAgent()

    def run(self, ticket: FeatureTicket, output_dir: Path, approved: bool = False) -> dict[str, Any]:
        output_dir.mkdir(parents=True, exist_ok=True)

        analysis = self.requirements.run(ticket)
        write_json(output_dir / "01_requirement_analysis.json", analysis)

        scenarios = self.test_design.run(ticket, analysis)
        scenario_dicts = [s.to_dict() for s in scenarios]
        write_json(output_dir / "02_test_scenarios.json", scenario_dicts)

        approval = {
            "ticket_id": ticket.id,
            "approved": approved,
            "approved_by": "QA engineer" if approved else None,
            "note": "Automation handoff is blocked until explicit QA approval." if not approved else "Scenario set approved for automation handoff.",
        }
        write_json(output_dir / "03_approval.json", approval)

        report = self.reporting.run(ticket, analysis, scenarios, approved)
        (output_dir / "05_qa_report.md").write_text(report, encoding="utf-8")

        if not approved:
            return {
                "status": "approval_required",
                "ticket_id": ticket.id,
                "scenario_count": len(scenarios),
                "output_dir": str(output_dir),
            }

        automation_spec = self.automation.run(ticket, scenarios)
        write_json(output_dir / "04_automation_spec.json", automation_spec)

        return {
            "status": "complete",
            "ticket_id": ticket.id,
            "scenario_count": len(scenarios),
            "automation_test_count": len(automation_spec["tests"]),
            "output_dir": str(output_dir),
        }
