# KSI Codex Workflow

## Goal / Plan Operating Model

- `/goal` defines the work boundary.
- `/plan` designs implementation and verification before edits.
- Small clear edits can execute directly.
- Small but uncertain or risky edits should plan first.

## Power User Autonomy

For local development and dev/staging verification, KSI Codex should default to action instead of waiting for permission on every step. When the task is clear enough and the risk is local or reversible, main Codex should inspect files, make scoped edits, run project commands, start dev servers, run tests, use Chromium browser automation, take screenshots, and verify the result.

Ask only blocking questions. A question is blocking when the answer changes safety, data handling, cost, architecture, or acceptance.

Hard stops remain:
- passwords, OTPs, recovery codes, API secrets, private keys, and payment details
- production data or production writes
- billable cloud resource creation or deletion
- destructive filesystem changes
- irreversible external service mutations
- `git commit`, `git push`, tags, releases, or remote changes

## Use `/goal` When

- building a new feature
- touching multiple files or layers
- changing DB schema, API, UI, worker, queue, auth, permissions, or data model
- doing broad refactors
- work may lose direction midstream
- another agent or developer should be able to reproduce the intended outcome

## Use `/plan` Before Implementation When

- DB migration is involved
- API contracts or schemas change
- frontend state structure changes
- file ownership or architecture is unclear
- rollback would be expensive or annoying
- bug cause is unknown
- security, permissions, or data loss risk exists

## Execute Directly When

- typo/copy/CSS spacing
- simple import fix
- single function bug fix with known cause
- one small test
- log/message/label change

## Vibe Intake / Task Decomposition

KSI Codex is designed for users who often start with vague product or development intent:

- "This screen feels wrong."
- "Make this more product-ready."
- "Find what is missing and improve it."
- "This error happens; fix it."
- "Continue improving the harness."

Main Codex must convert this kind of request into bounded engineering work without demanding a perfect specification.

### Protocol

1. Intent capture
   - Restate the likely user outcome in one sentence.
   - Separate desired result from implementation guesses.

2. Work classification
   - small direct edit
   - discovery then direct edit
   - `/plan` needed
   - `/goal` + `/plan` + `.ai/` needed
   - strict-mode security, release, or architecture review needed
   - `.ai/` artifact ownership needed

3. Task decomposition
   - Discovery task: what must be found in the repo or docs
   - Decision task: what must be chosen before editing
   - Build task: the bounded implementation milestone
   - Verification task: smallest reliable checks
   - Acceptance task: what proves the work satisfies the request

4. Delegation decision
   - Use `ksi-explorer` only for bounded repo discovery.
   - Use `ksi-librarian` only for bounded official docs or external source lookup.
   - Use `ksi-acceptance-reviewer` only when meaningful acceptance evidence is useful.

5. Bounded build
   - Main Codex implements the selected milestone.
   - Do not broaden scope into later milestones.
   - If the plan becomes invalid, stop and return to planning.
   - Maintain context lock: one bounded milestone at a time.

6. Verification
   - Prefer project-owned typecheck, lint, and tests.
   - Use browser or screenshot evidence for UI/UX work when visual judgment matters.
   - Convert important recurring regressions into repo-owned tests.

7. Acceptance
   - Check intent alignment, plan adherence, verification adequacy, residual risk, and delivery readiness.
   - Activate conditional security, release, or architecture review modes when risk triggers appear.

### Question Policy

Ask only when the answer changes implementation, acceptance, or safety.

Default behavior:
- ask 0 questions when a safe assumption is enough
- ask 1-3 questions when truly blocked
- avoid broad questionnaires
- state assumptions and proceed when risk is low

### `.ai/` Artifact Ownership

Main Codex owns `.ai/` writes.

`ksi-goal-plan-handoff` is a declarative workflow skill: it tells main Codex how to create, update, and read artifacts. It is not a separate writer agent.

Ownership:
- main Codex writes `.ai/project-brief.md`, `.ai/plan.md`, `.ai/decisions.md`, `.ai/review-checklist.md`, `.ai/task-state.md`, and `.ai/handoff.md` when the active workflow allows it.
- `ksi-explorer` does not write `.ai/`.
- `ksi-librarian` does not write `.ai/`.
- `ksi-acceptance-reviewer` does not write `.ai/`; it reports findings for main Codex to apply.

Plan/Build/Review ownership still applies:
- planning artifacts are Plan-owned in strict workflows
- source edits, tests, task state, and handoff are Build-owned
- review remains read-only by default

### Context Lock

After task breakdown, main Codex locks onto the current bounded milestone.

Rules:
- implement one bounded milestone at a time
- do not silently absorb new scope while building
- if the user adds a related small clarification, incorporate it when safe
- if the user adds a new request, queue it as a follow-up
- if the new request changes scope, priority, safety, or acceptance criteria, stop and re-plan
- record queued follow-ups in `.ai/handoff.md` or the final response for non-trivial work

Context lock prevents vague requests from expanding into unbounded implementation loops.

### Delegation Examples

Use `ksi-explorer`:

```text
Find the files, tests, fixtures, and call path related to harness agent installation. Do not edit files.
```

Use `ksi-librarian`:

```text
Check the official Supabase MCP docs for read-only and project-scoped configuration guidance. Summarize only the constraints relevant to KSI.
```

Use `ksi-acceptance-reviewer`:

```text
Review the current implementation against the goal, plan, tests, and KSI acceptance criteria. Do not edit files.
```

### Output Shape For Vague Requests

```md
## Interpreted Intent

## Classification

## Task Breakdown

## Delegation

## Current Bounded Task

## Verification

## Assumptions
```

## Task Classification

| Work Type | `/goal` | `/plan` | Direct Execution |
| --- | --- | --- | --- |
| New feature | Required | Required | Not recommended |
| Large refactor | Required | Required | Not recommended |
| DB/API change | Recommended | Required | Not recommended |
| One UI screen | Recommended | Recommended | Possible |
| Single component edit | Not needed | Optional | Possible |
| CSS/copy change | Not needed | Not needed | Recommended |
| Unknown-cause bug | Optional | Required | Not recommended |
| Test addition | Not needed | Optional | Possible |
| Security/permission change | Required | Required | Not recommended |

## Persistent `.ai/` Artifacts

`.ai/` is for boundary, handoff, and recovery. It is not a log folder for every tiny edit.

Create `.ai/` only for non-trivial work:
- `/goal` or `/plan` needed
- multi-file or multi-layer work
- schema/API/auth/data-impacting changes
- rollback risk
- unknown-cause bug
- broad refactor
- release/security risk
- Plan/Build/Review separation
- explicit user request

Do not create `.ai/` for:
- typo/copy/CSS spacing
- single import or type error fix
- clear single-function bug fix
- small test
- log/message edit

## Memories

Codex memories are optional personal recall, not authoritative state.

Use memories for stable preferences and recurring workflow hints. Do not use memories for required rules, project contracts, secrets, customer data, production data, active task state, or security/release decisions.

Use `.ai/` for active goal, plan, decision, task-state, handoff, current milestone, and queued follow-up memory.

For sensitive threads involving external context, production data, customer data, secrets, security review, or private SaaS data, disable memory generation with `/memories` or set `disable_on_external_context = true`.

## Plan / Build / Review Ownership

Default is recommended ownership:
- Plan owns planning artifacts.
- Build owns source edits, tests, `.ai/task-state.md`, and `.ai/handoff.md`.
- Review is read-only by default and reports `Approved`, `Needs changes`, or `Blocked`.

Strict ownership applies when:
- DB migration is involved
- API/schema/auth/permission/data model changes
- multi-layer or multi-file architectural work
- bug cause is unknown
- data loss, security, or release risk exists
- handoff between agents/developers is expected

## Main Codex / Auxiliary Agent Model

KSI v1 uses one main owner and three auxiliary custom agents:

```text
main Codex
├─ ksi-explorer              # codebase exploration
├─ ksi-librarian             # official docs and external source lookup
└─ ksi-acceptance-reviewer   # final requirement and delivery readiness check
```

Main Codex owns:
- requirement interpretation
- planning
- implementation
- test execution and test writing
- self-check
- final user response
- final decision responsibility

Auxiliary agents are read-only and should be used only when they reduce context noise:
- `ksi-explorer` finds related code, tests, symbols, fixtures, and call paths.
- `ksi-librarian` checks official docs, source behavior, deprecations, and migration guidance.
- `ksi-acceptance-reviewer` checks whether the work satisfies the goal, plan, tests, security/release/UI evidence, and delivery readiness.

Do not add standing v1 agents for planner, architect, test-writer, debugger, refactorer, doc-writer, security-reviewer, or release-reviewer. Security, release, and architecture reviews are conditional modes activated by main Codex or `ksi-acceptance-reviewer` when risk triggers appear.

### Permission Matrix

| Agent | Read Code | Write Code | Execute Tests | Web | Final Decision |
| --- | --- | --- | --- | --- | --- |
| main Codex | Yes | Yes | Yes | Optional | Yes |
| `ksi-explorer` | Yes | No | No | No | No |
| `ksi-librarian` | Yes | No | No | Yes | No |
| `ksi-acceptance-reviewer` | Yes | No | No | No | No |

### Typical Flow

1. User request.
2. Main Codex interprets scope and decides whether auxiliary agents are useful.
3. `ksi-explorer` locates relevant code/tests when needed.
4. `ksi-librarian` checks official docs or external source facts when needed.
5. Main Codex implements, tests, and self-checks.
6. `ksi-acceptance-reviewer` reviews meaningful work when final acceptance evidence is useful.
7. Main Codex applies accepted fixes and returns the final response.

## Browser / E2E Policy

Project-owned tests are the primary durable regression layer.

Use the project's existing test stack first:
- Playwright
- Cypress
- Vitest
- Jest
- Testing Library
- framework-native test tools

Prefer Chromium for browser automation. Firefox is a fallback for explicit user requests or Chromium-specific blockers.

Use Browser MCP, interactive browser, or screenshots when:
- visual inspection is needed
- the issue is difficult to understand from code alone
- screenshots are required for UI/UX review
- reproducing a user flow requires exploration
- debugging layout, interaction, auth flow, or runtime behavior

For login/MFA/OAuth/cloud-console workflows, use a visible persistent Chromium profile. The user enters credentials directly in the browser. Codex resumes from the same session after login and should operate only on non-secret UI state.

Use Playwright for DOM-aware automation, screenshots, console and network inspection, and post-login verification. Use `wmctrl`, `xdotool`, ImageMagick, and `xclip` as fallbacks for visible-window focus, manual UI fallback, targeted screenshots, and non-secret clipboard handoff.

Screenshot-based review is acceptable for UI/UX analysis, but important recurring issues should become project-owned tests.

Do not launch browser automation for every UI task by default. Prefer the lightest reliable verification method.

## Codex `/review` Policy

Codex built-in `/review` is a code-diff review tool.

Use `/review` for:
- uncommitted working tree changes
- staged changes
- recent commits
- PR-style diffs when available
- implementation-level code quality issues

Do not use `/review` as the only review mechanism for:
- product UX review
- release risk review
- security review
- architecture review
- goal/plan/handoff verification

KSI Review phase may use Codex `/review` as one step, but final task approval should consider goal, plan, tests, artifacts, security risk, release risk, and UI/UX evidence where applicable.

## LSP / Typecheck Policy

Use project-owned typecheck, lint, and test commands as the primary code verification layer.

Use existing LSP or language-server diagnostics when available. Do not prescribe one fixed LSP stack. Detect the user's project tooling and installed language-server ecosystem, then use what already exists.

LSP is a code-reality sensor, not the agent's brain. It helps catch hallucinated APIs, broken imports, missing references, invalid renames, and type errors.

Do not automatically install language servers in v1. Detect and use existing project tooling first.

LSP diagnostics are advisory unless backed by project-owned commands or CI. Do not treat LSP output as the only source of truth.
