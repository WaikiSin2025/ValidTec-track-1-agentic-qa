# Test Design Prompt Contract

Generate a small, risk-ranked scenario set traceable to the supplied requirements.

For every scenario return:

- scenario id
- source requirement
- risk
- priority
- preconditions
- steps
- expected result
- automation-candidate flag

Include positive, negative, authorization, data-integrity, and cleanup coverage where applicable. QA approval is required before downstream automation generation.
