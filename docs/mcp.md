# MCP Policy

KSI Codex does not automatically install or connect MCP servers in v1.

MCP servers may expose access to databases, browsers, design files, repositories, customer data, secrets, or external SaaS APIs. MCP configuration must be explicit and user-controlled.

## Default Policy

- Do not auto-install MCP servers.
- Document recommended MCPs.
- Verify existing MCP configuration when present.
- Prefer official or actively maintained MCP servers.
- Prefer read-only access by default.
- Prefer project-scoped access over workspace/global access.
- Prefer dev/staging environments over production.
- Never connect to production data unless the user explicitly accepts the risk.
- Treat production-connected MCP usage as strict-mode work.

## Recommended Categories

### Supabase

- dev/staging only by default
- project-scoped with `project_ref` where possible
- `read_only=true` by default
- production access requires explicit approval and strict mode

### Playwright

- exploratory browser inspection
- screenshots, runtime behavior, console/network observation
- not a replacement for repo-owned Playwright/Cypress tests
- Chromium is the default browser target; Firefox is fallback only
- visible persistent Chromium profiles are preferred for login/MFA handoff
- credentials, OTPs, recovery codes, secrets, and payment details remain user-entered only

### Firebase

- optional, only when the project actually uses Firebase
- project directory scoped
- feature groups limited to what is needed
- avoid broad auth, user, or storage access by default
- production access requires explicit approval and strict mode

### Vercel

- optional, only when deployment or hosting state matters
- prefer official Vercel MCP or Vercel CLI
- prefer project-specific context
- human confirmation for write actions

### Figma

- optional
- only when a design source is actually involved
- prefer official or well-maintained implementations
- prefer file-scoped access when possible
- not part of the default v1 recommendation set

### Context7

- optional documentation lookup for current framework/library docs
- not a replacement for repo code or project docs

### OpenAI Docs

- optional documentation lookup for current OpenAI API/product behavior
