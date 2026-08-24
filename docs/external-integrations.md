# External Integrations

KSI Codex treats external integrations as explicit authority openings. They are not generic productivity boosters.

## Default Policy

- Do not auto-install MCP servers.
- Do not auto-connect external services.
- Prefer project-scoped access.
- Prefer read-only access.
- Prefer dev/staging over production.
- Treat production-connected tools as strict-mode work.
- Keep unused plugins disabled.

## Plugin Defaults

Recommended enabled by default:
- GitHub, when repository, PR, issue, or CI workflows are used.

Disabled by default:
- Gmail
- Google Calendar
- Canva
- Figma
- Notion
- Linear

Use those only when the project workflow actually depends on them.

## MCP / Service Priority

### Supabase

Use only when a project actually uses Supabase.

Recommended posture:
- dev/staging project
- `project_ref` scoped
- `read_only=true` by default
- production blocked unless the user explicitly accepts the risk
- production usage is strict-mode work

### Firebase

Use only when a project actually uses Firebase.

Recommended posture:
- project directory scoped
- activate only the feature groups in use
- avoid broad auth/user/storage access by default
- production-connected usage is strict-mode work

### Vercel

Use only for deployment, preview URL, environment, build status, and deployment log workflows.

Recommended posture:
- official Vercel MCP endpoint or Vercel CLI
- project-specific context where available
- human confirmation for changes
- avoid write-capable deployment changes unless explicitly requested

### Playwright / Browser

Use project-owned Playwright/Cypress tests first for durable regression coverage.

Prefer Chromium + Playwright for browser automation. Firefox is fallback only when explicitly requested or Chromium is blocked.

Use Playwright CLI, Browser MCP, or screenshots for:
- exploratory UI inspection
- runtime behavior
- console/network observation
- auth-flow debugging
- visual evidence for UI/UX review

For login, MFA, OAuth, cloud consoles, billing consoles, and admin screens:
- launch a visible Chromium window with a persistent profile
- let the user type credentials and approval codes directly
- continue automation only after login and only on non-secret UI state
- stop before billable, destructive, production, or irreversible external actions unless the user explicitly accepts that action

Do not launch browser automation for every UI task by default.

### Observability

Use Sentry, Datadog, Logtail, or similar tools only if the project already adopted them.

## Conditional Review Modes

External integrations can escalate review mode:

Security review mode:
- auth
- permissions
- tenant isolation
- secrets
- customer data
- file access
- signed URLs

Release review mode:
- deployment
- migration
- rollback
- billing
- observability
- customer-impacting rollout

Architecture review mode:
- new module boundary
- database schema design
- multi-tenant architecture
- AI pipeline architecture
- billing architecture
- realtime infrastructure design
