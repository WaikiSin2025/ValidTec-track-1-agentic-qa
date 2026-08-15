# Architecture

The project separates **reasoning responsibilities** from **workflow control**.

- `RequirementAnalysisAgent` identifies scope and risk.
- `TestDesignAgent` creates traceable scenarios.
- `QAOrchestrator` persists evidence and enforces the approval gate.
- `AutomationSpecificationAgent` is unavailable until approval succeeds.
- `ReportingAgent` summarizes the QA state.

This separation makes it possible to replace one deterministic agent with an LLM-backed adapter while retaining the same governance and evidence model.

## Design principles

1. Human approval before executable-test handoff.
2. Structured inputs/outputs instead of free-form agent chaining.
3. Synthetic test data only in the public portfolio repository.
4. Deterministic CI path that does not require model credentials.
5. Traceability from feature ticket to every generated scenario.
