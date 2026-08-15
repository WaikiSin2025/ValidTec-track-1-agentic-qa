from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import FeatureTicket
from .orchestrator import QAOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the ValidTec Track 1 agentic QA workflow")
    parser.add_argument("--ticket", required=True, type=Path, help="Path to a feature-ticket JSON file")
    parser.add_argument("--output", required=True, type=Path, help="Directory for workflow evidence")
    parser.add_argument("--approve", action="store_true", help="Explicitly approve the scenario set for automation handoff")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data = json.loads(args.ticket.read_text(encoding="utf-8"))
    ticket = FeatureTicket.from_dict(data)
    result = QAOrchestrator().run(ticket, args.output, approved=args.approve)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
