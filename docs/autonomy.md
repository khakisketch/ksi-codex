# Autonomy Policy

KSI Codex is optimized for users who want AI to carry local development work through implementation and verification without excessive permission prompts.

## Default Action

For local development and dev/staging work, Codex should proceed when the task is clear enough and the risk is local or reversible:

- inspect repository structure and relevant files
- make scoped edits
- run typecheck, lint, tests, and project scripts
- start dev servers when needed
- run Playwright/Cypress/browser checks when runtime behavior matters
- capture screenshots for UI/UX or visual verification
- use existing project tooling before guessing
- update `.ai/` artifacts for non-trivial work

## Question Policy

Ask only blocking questions. A question is blocking when the answer materially changes:

- safety
- data handling
- cost
- architecture
- external service behavior
- acceptance criteria

When a safe assumption is enough, state it briefly and proceed.

## Hard Stops

Always stop for explicit user input before:

- asking for or handling passwords, OTPs, recovery codes, API secrets, private keys, or payment details
- accessing production data or performing production writes
- creating, deleting, or modifying billable cloud resources
- performing destructive filesystem changes
- making irreversible external service changes
- committing, amending, pushing, tagging, releasing, or changing git remotes

## Preset Shape

`standard` remains suitable for public/default use.

`power-user` is for a personal machine where the user wants proactive local/dev execution. It increases default action, not authority over secrets, production, billing, destructive operations, or git publishing.
