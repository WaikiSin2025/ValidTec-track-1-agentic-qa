# ValidTec Track 1 — Agentic QA Workflow

A portfolio-ready reference implementation showing how AI-assisted QA can move a feature requirement through **analysis → risk identification → test design → human approval → automation specification → QA reporting**.

The repository intentionally uses a deterministic local implementation by default so recruiters and engineers can run the demo without cloud credentials. The agent boundaries are designed so an LLM or Azure AI Foundry/Semantic Kernel adapter can be added later without changing the workflow contract.

## What this demonstrates

- Structured requirement analysis
- Risk-based test design
- Human-in-the-loop approval gate
- Traceability from requirement to test scenario
- Automation-ready test specifications
- Deterministic evidence artifacts
- CI validation of the orchestration logic

## Workflow

```text
Feature Ticket
    |
    v
Requirement Analysis Agent
    |
    v
Risk/Test Design Agent
    |
    v
Human Approval Gate --------- stop if not approved
    |
    v
Automation Specification Agent
    |
    v
Reporting Agent
    |
    v
QA Evidence Package
```

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -e .

# Run only through scenario generation; workflow stops at approval gate.
validtec-agentic-qa --ticket examples/feature_ticket.json --output output/review

# Run the complete demo with explicit QA approval.
validtec-agentic-qa --ticket examples/feature_ticket.json --output output/approved --approve
```

The completed run produces:

```text
output/approved/
├── 01_requirement_analysis.json
├── 02_test_scenarios.json
├── 03_approval.json
├── 04_automation_spec.json
└── 05_qa_report.md
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Why the approval gate matters

The workflow does **not** treat generated scenarios as automatically correct. A QA engineer must explicitly approve the scenario set before automation specifications are produced. This keeps judgment, risk acceptance, and release responsibility with the tester.

## Track 5 integration

`04_automation_spec.json` is deliberately shaped as a handoff contract. A downstream automation repository can read the approved steps and implement them as Postman, Playwright, Pytest, or another deterministic test framework. See `docs/track5-integration.md`.

## Portfolio demo

A five-minute recruiter demo is documented in `docs/recruiter-demo.md`.

## Disclaimer

This is an educational portfolio project. It does not contain employer source code, credentials, tickets, customer data, or proprietary test assets.
