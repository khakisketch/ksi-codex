---
name: ksi-goal-plan-handoff
description: Use when the user invokes /goal or /plan, asks to define work boundaries, decompose vague vibe requests into bounded tasks, create implementation plans, produce .ai artifacts, prepare Plan/Build/Review handoff, or structure non-trivial work before coding.
---

# KSI Goal / Plan / Handoff

Use this skill to turn non-trivial work into a bounded goal, implementation plan, verification strategy, and handoff.

## Operating Model

- `/goal` defines the work boundary.
- `/plan` designs implementation and verification before edits.
- Small clear edits can execute directly.
- Small but uncertain or risky edits should plan first.

## Vibe To Task

For vague product or development requests, main Codex should convert intent into a bounded execution path before editing.

1. Restate the likely intent.
2. Classify the work as direct, discovery-first, `/plan`, `/goal` + `/plan`, or strict-risk.
3. Split the work into:
   - Discovery
   - Decision
   - Build
   - Verification
   - Acceptance
4. Decide whether read-only delegation is useful:
   - `ksi-explorer` for repo paths, tests, fixtures, symbols, and call paths
   - `ksi-librarian` for official docs, SDK behavior, deprecations, and migration guidance
   - `ksi-acceptance-reviewer` for final acceptance after meaningful work
5. Keep implementation ownership with main Codex.
6. Keep `.ai/` artifact write ownership with main Codex.
7. Lock the build to one bounded milestone after task breakdown.
8. Ask only blocking questions, usually no more than 1-3.

## Create `.ai/` Only For Non-Trivial Work

Do not create `.ai/` for typo/copy changes, CSS spacing, simple import/type fixes, clear single-function bug fixes, small tests, or log/message edits.

Create `.ai/` when:
- `/goal` or `/plan` is needed
- work touches multiple files or layers
- schema/API/auth/permission/data-impacting behavior changes
- rollback risk exists
- bug cause is unknown
- refactor scope is broad
- release/security risk must be reviewed
- handoff is expected
- the user explicitly requests persistent artifacts

## Recommended Ownership

Use recommended ownership by default. Escalate to strict ownership for risky or non-trivial work.

- Plan owns `.ai/project-brief.md`, `.ai/plan.md`, `.ai/decisions.md`, and `.ai/review-checklist.md`.
- Build owns source edits, tests, `.ai/task-state.md`, and `.ai/handoff.md`.
- Review is read-only by default and reports `Approved`, `Needs changes`, or `Blocked`.

Strict mode applies when DB migration, API/schema/auth/permission/data model changes, multi-layer architecture work, unknown bug cause, data loss/security/release risk, or agent/developer handoff is involved.

This skill is declarative. It guides main Codex to create or update `.ai/` artifacts; it is not a separate writer. Auxiliary agents must not write `.ai/` artifacts.

## Context Lock

After a plan or task breakdown selects the current bounded milestone:

- implement only that milestone
- queue related follow-ups instead of absorbing them silently
- stop and re-plan if a new user request changes scope, priority, safety, or acceptance criteria
- record queued follow-ups in `.ai/handoff.md` for non-trivial work

## `/goal` Template

```md
# Project Goal

## Goal

## Scope

## Completion Criteria

## Non-Goals

## Constraints

## Risks

## Initial Task Breakdown

## Delegation Candidates

## Context Lock
```

## `/plan` Template

```md
# Implementation Plan

## Goal Reference

## Files To Modify

## Files To Add

## Data / Schema Changes

## API / Contract Changes

## Frontend State / UX Changes

## Implementation Steps

## Delegation Plan

State whether `ksi-explorer`, `ksi-librarian`, or `ksi-acceptance-reviewer` should be used. If not needed, say so.

## Context Lock

State the current bounded milestone, queued follow-ups, and re-plan triggers.

## Verification

Include the smallest relevant project-owned checks:
- typecheck/lint/test commands when available
- LSP/language-server diagnostics when available
- browser/screenshot evidence for UI work
- Codex `/review` for code-diff review when useful

## Risk Gates

## Stop Condition
```

## Build Handoff

```md
## Build Handoff
- Goal:
- Scope:
- Non-goals:
- Persistent artifacts read/updated:
- Files likely affected:
- Implementation steps:
- Delegation plan:
- Context lock:
- Queued follow-ups:
- Verification:
- Review focus:
- Risks:
- Acceptance criteria:
- Current phase: plan
- Completed:
- Blocked:
- Next recommended phase: build | review | plan
- Stop condition:
```
