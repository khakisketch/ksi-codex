# KSI Codex Global Routing

## Goal and plan

- Use `/goal` and `/plan` before non-trivial, risky, ambiguous, or multi-file work.
- Execute small, clear, local changes directly.

## Subagents

- Use `explorer` only for bounded, read-only codebase discovery.
- Use the built-in `worker` for one clearly scoped implementation or testing task, including test code.
- Give a worker named ownership boundaries and validation; do not run concurrent writers against the same files.
- Do not add standing specialized agents by default.

## MCP routing

- Use Context7 for version-specific framework, library, or API behavior when relevant to the task.
- Use Local Codex only for an explicitly requested design workflow or an active Local Codex design project; do not use it for ordinary implementation tasks.
