# Decisions

## 2026-06-08: Source Of Truth

`ksi-codex/` is the source of truth. Global Codex files are installed outputs.

## 2026-06-08: Default Preset

Default preset is `standard`. `strict` is optional for high-risk/team workflows.

## 2026-06-08: Installer

Primary installer is `python3 scripts/apply.py`. `install.sh` is a wrapper.

## 2026-06-08: Existing Files

Existing different targets stop installation by default. No silent overwrite and no v1 auto-merge.

## 2026-06-08: `.ai/` Artifacts

`.ai/` artifacts are created only for non-trivial work.

## 2026-06-08: Skills

v1 ships six skills:
- `ksi-brainstorming`
- `ksi-project-audit`
- `ksi-goal-plan-handoff`
- `ksi-security-review`
- `ksi-release-risk`
- `ksi-ui-ux-review`

## 2026-06-08: MCP

No automatic MCP installation in v1. Document and verify only.

## 2026-06-08: LSP / Typecheck

KSI Codex does not prescribe or install a fixed LSP stack. It detects existing project tooling and installed language-server binaries, then treats diagnostics as advisory code-reality signals.

## 2026-06-08: Auxiliary Agents

v1 uses main Codex plus three read-only auxiliary custom agents:
- `ksi-explorer`
- `ksi-librarian`
- `ksi-acceptance-reviewer`

Main Codex owns planning, building, testing, coordination, and final user response. Do not add standing planner, architect, test-writer, debugger, refactorer, doc-writer, security-reviewer, or release-reviewer agents in v1.

## 2026-06-08: Model Tiering

Default auxiliary model policy:
- `ksi-explorer`: `gpt-5.4-mini`, low effort
- `ksi-librarian`: `gpt-5.4-mini`, medium effort
- `ksi-acceptance-reviewer`: `gpt-5.5`, high effort

xhigh review is reserved for failed gates, high-risk ambiguity, production data, security-sensitive changes, migration/rollback risk, or repeated review disagreement.

## 2026-06-08: Conditional Review Modes

Security, release, and architecture review are conditional modes, not standing v1 agents.

## 2026-06-08: Vibe Intake

KSI Codex treats vague product/development requests as normal input. Main Codex owns vibe intake, task decomposition, implementation, verification, coordination, and final responsibility. Auxiliary agents remain read-only and are used only for bounded discovery, official-source lookup, or acceptance review.

## 2026-06-08: Memories

Codex Memories are optional personal recall, not authoritative state. Required rules stay in `AGENTS.md`, repo docs, skills, or `.ai/` artifacts. KSI Codex documents and verifies memory settings but does not auto-enable memories for public installs.

## 2026-06-09: Power User Autonomy

KSI Codex supports a personal `power-user` preset for high-autonomy local development. Codex should proactively inspect, edit, run, test, start dev servers, automate Chromium, take screenshots, and verify when the task is local/dev and reversible. Hard stops remain for credentials, OTPs, secrets, payment details, production data, billable/destructive/irreversible external actions, and git publishing.

## 2026-06-09: Chromium Browser Automation

Default browser automation is Chromium + Playwright. Visible persistent Chromium profiles are preferred for login, MFA, OAuth, cloud consoles, billing consoles, and admin screens. Users enter credentials directly; Codex resumes after login on non-secret UI state. Firefox is fallback only when requested or Chromium is blocked.

## 2026-08-24: Portable Current Baseline

The default installer now reproduces the active owner configuration rather than
the earlier experimental harness. It installs the concise global routing file,
one read-only `explorer` agent, command rules, and an optional portable config.
The earlier KSI skills, presets, and `ksi-*` agents remain historical source only
and are not installed by default.

Portable config may be installed as a named `ksi` profile or as the default
config. Default replacement requires explicit `--config-mode replace` and keeps
the existing high-authority `approval_policy = "never"` plus
`sandbox_mode = "danger-full-access"`. Authentication and machine-local state
are never distributed.
