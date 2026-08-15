# Requirement Analysis Prompt Contract

When an LLM adapter is added, instruct it to return structured JSON containing:

- requirement summary
- interfaces/components affected
- explicit acceptance criteria
- assumptions that require confirmation
- risks
- test objective
- data/privacy constraints

The model must not invent undocumented requirements. Unknowns should be surfaced as questions or assumptions.
