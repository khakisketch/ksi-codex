## KSI Codex Strict Preset

Strict mode is for high-risk work, team handoff, and projects where delivery discipline matters more than speed.

- Risky work must have an explicit `/goal` and `/plan` before source edits.
- Plan must not edit source code.
- Build must not rewrite Plan-owned artifacts unless the user explicitly asks.
- Build must update `.ai/task-state.md` and `.ai/handoff.md` after meaningful non-trivial work.
- Review must stay read-only by default.
- Schema, API, auth, permission, data model, migration, deployment, billing, and production-data work require plan approval before implementation.
- Non-trivial handoffs must include scope, non-goals, changed or likely affected files, verification, risks, next phase, and stop condition.
