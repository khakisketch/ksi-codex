# Plugin Policy

Use plugins primarily for external development, deployment, database, hosting, observability, or project infrastructure integration.

A plugin should be added only when it provides access to an external system, external state, or external artifact that Codex cannot safely manage through local repo files.

## Recommended Categories

- Source control
- Database / BaaS
- Hosting / deployment
- Browser inspection
- Observability, only when already adopted

## Examples

- Source control: GitHub
- Database / BaaS: Supabase, Firebase
- Hosting / deployment: Vercel
- Browser inspection: Playwright / Browser tools
- Observability: Sentry, Logtail, Datadog, etc. only if the project actually uses them

## Avoid Plugins For

- generic planning loops
- autonomous development loops
- auto-commit or auto-push flows
- redundant wrappers around Codex `/goal`, `/plan`, skills, or repo tests
- workflows that can be a simple skill, `AGENTS.md` rule, local script, or repo-owned test
- external services the project does not actually use

## Excluded From v1 Recommendations

These services are not part of the default v1 recommendation set:
- Gmail
- Google Calendar
- Canva
- Figma
- Notion
- Linear

They can still be used by projects that actually depend on them.

## KSI v1 Default State

Keep only development-infrastructure plugins enabled by default.

Recommended:
- `github@openai-curated`, when GitHub PR, issue, CI, or release workflows are used

Disable by default:
- `gmail@openai-curated`
- `google-calendar@openai-curated`
- `canva@openai-curated`

These plugins are useful in their own domains, but they add non-development workflow surface area. KSI v1 keeps them off unless the user explicitly needs them.
