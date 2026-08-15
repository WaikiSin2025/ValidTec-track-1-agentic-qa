# Track 5 Integration Contract

Track 1 decides **what should be tested** and records QA approval. Track 5 provides deterministic automation that proves the behavior.

The handoff file is `04_automation_spec.json`.

A Track 5 adapter can:

1. Read approved tests.
2. Map `postman/newman` tests to a Postman collection or folder.
3. Map `playwright` tests to UI specifications.
4. Execute the deterministic suite in CI.
5. Return JUnit/HTML results to a reporting layer.

This keeps AI-assisted planning separate from pass/fail test execution.
