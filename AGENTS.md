# KSI Codex Repository Instructions

This repository is the source of truth for the portable KSI Codex baseline.

## Working Rules

- Keep the harness small and pragmatic.
- Prefer `AGENTS.md` for stable behavior, scripts for deterministic installation and checks, and MCP/plugins only for external systems.
- Do not add plugins, hooks, MCP servers, agents, or skills unless they solve a repeated problem.
- Keep global instructions concise because they are loaded for every Codex task.
- Keep skill `SKILL.md` files focused and progressively disclosed.
- Never add authentication, sessions, memories, browser profiles, absolute machine paths, or secrets.
- Never silently overwrite user configuration.

## Verification

After changing installer, config, agents, rules, or global guidance, run:

```bash
python3 -m py_compile scripts/apply.py scripts/check.py scripts/uninstall.py
python3 scripts/check.py --source-only --skip-mcp
./install.sh --dry-run --mode copy --config-mode replace --backup
```

Use `--mode symlink --config-mode profile --backup` only for repository development.
