# Captured source state

Synchronized on 2026-09-22 from the owner's active Linux Codex environment.

## Reproduced by the installer

- Codex CLI behavior target: `0.155.1`
- Global instructions: exact file copy from `~/.codex/AGENTS.md`
- Configured role roster: exact `*.toml` copies from `~/.codex/agents/`
- KSI command rules: exact file copy
- Portable config values:
  - model and reasoning defaults
  - personality
  - approval and sandbox behavior
  - multi-agent limits, default subagent model and effort
  - plugin enable/disable preferences
  - memory feature preferences
  - Context7 MCP using portable `npx` and Exa MCP endpoint

## Deliberately not reproduced

- `auth.json`, OAuth, cookies, sessions, history, memories, attachments, and caches
- trusted project entries containing `/home/ksi/...`
- desktop appearance, notification, and per-window UI state
- hook trusted hashes
- app-specific approval records and generated app identifiers
- `node_repl` MCP because it is supplied by the local Codex app runtime
- `hooks.json` because its command points to a machine-local OpenCode harness path
- `open-design` / Local Codex MCP because it depends on a separate local design project
- browser profiles and existing signed-in sessions

## External components requiring separate installation or login

- GitHub, Browser, Chrome, Sites, Visualize, and Codex app tools are enabled in
  the portable config, but availability depends on the Codex installation.
- GitHub and other OAuth-backed integrations must be connected manually.
- The third-party `ui-ux-pro-max` skill was installed on the source PC from
  `nextlevelbuilder/ui-ux-pro-max-skill` at `v2.11.0`; it is not vendored here.
- The local `grill-me` skill is not part of the portable core release.

These exclusions prevent machine-local or sensitive state from being mistaken
for a safe cross-PC configuration.
