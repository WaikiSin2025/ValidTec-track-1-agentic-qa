import json
import tempfile
import unittest
from pathlib import Path

from validtec_agentic_qa.models import FeatureTicket
from validtec_agentic_qa.orchestrator import QAOrchestrator


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.ticket = FeatureTicket(
            id="TEST-1",
            title="Invite user",
            description="Admin invites a user and assigns a license.",
            acceptance_criteria=[
                "Admin can invite a valid email address",
                "Duplicate invitation is rejected",
                "Unauthorized users cannot invite members",
            ],
            interfaces=["REST API"],
        )

    def test_unapproved_run_stops_before_automation_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = QAOrchestrator().run(self.ticket, out, approved=False)
            self.assertEqual(result["status"], "approval_required")
            self.assertTrue((out / "02_test_scenarios.json").exists())
            self.assertFalse((out / "04_automation_spec.json").exists())

    def test_approved_run_creates_automation_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = QAOrchestrator().run(self.ticket, out, approved=True)
            self.assertEqual(result["status"], "complete")
            spec = json.loads((out / "04_automation_spec.json").read_text())
            self.assertGreaterEqual(len(spec["tests"]), 4)
            self.assertTrue(all(t["framework"] == "postman/newman" for t in spec["tests"]))


if __name__ == "__main__":
    unittest.main()
