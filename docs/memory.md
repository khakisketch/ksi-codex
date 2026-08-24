# Memory Policy

KSI Codex supports Codex Memories as a personal recall layer. Memories are useful, but they are not an authority layer.

## Authority Order

Use this order when sources disagree:

1. `AGENTS.md`
2. Repository docs and checked-in project conventions
3. KSI skills
4. `.ai/` artifacts for the active task
5. Codex memories

Memories can suggest preferences, but they must not override explicit instructions, project docs, security policy, or current task artifacts.

## What Belongs In Memory

Good memory candidates:
- stable user preferences
- recurring workflow habits
- preferred tech stacks
- repeated project conventions
- known personal operating preferences
- broad non-sensitive lessons learned

Examples:
- Korean-first responses
- concise pragmatic engineering style
- frequent `/goal` and `/plan` usage
- preference for Vibe Intake to Task Decomposition
- avoid plugin bloat
- main Codex owns implementation and final responsibility
- Supabase, Firebase, Vercel, GitHub are common development tools

## What Does Not Belong In Memory

Never store:
- secrets, credentials, tokens, or `.env` values
- customer data
- production DB contents or production operational state
- private external SaaS data
- security-sensitive findings
- current task progress
- one-off bug state
- release decisions or rollback details
- rules that must always apply

Use `AGENTS.md`, project docs, skills, or `.ai/` for those.

## `.ai/` Versus Memories

Use `.ai/` for active task state:
- goal
- plan
- decisions
- review checklist
- task-state
- handoff
- queued follow-ups
- current bounded milestone

Use memories for stable preferences that should carry across projects and sessions.

## Recommended Local Config

For a personal KSI Codex setup:

```toml
[features]
memories = true

[memories]
use_memories = true
generate_memories = true
disable_on_external_context = true
min_rate_limit_remaining_percent = 20
```

`disable_on_external_context = true` keeps threads that used external context, such as MCP or web/tool search, out of memory generation.

## Public Install Policy

KSI Codex does not auto-enable memories in v1.

The installer should document and verify memory settings, but memory activation remains user-controlled.

## Thread-Level Control

Use `/memories` in Codex to disable memory use or memory generation for sensitive threads.

Disable memory generation for:
- production incidents
- customer-data work
- secret or credential rotation
- sensitive security review
- external SaaS data exploration
- one-off private business context
