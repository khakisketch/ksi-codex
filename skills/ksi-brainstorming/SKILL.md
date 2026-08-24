---
name: ksi-brainstorming
description: Use when the user asks for brainstorming, direction, product or development ideas, improvement options, vague requirements, vibe-to-task decomposition, next steps, or alternatives before implementation. Korean triggers include 브레인스토밍, 방향, 개선, 아이디어, 다음에 뭘, 뭐부터, 모호한 요구, 알아서, 제품답게, 이상한데.
---

# KSI Brainstorming

Use this skill to convert vague or open-ended product/development requests into concrete options, bounded task candidates, and next actions.

## Principles

- Do not demand a perfect specification.
- Reduce ambiguity with assumptions and options.
- Prefer 3-5 concrete paths over generic lists.
- Separate known facts, assumptions, risks, and unknowns.
- Recommend one next action.
- Do not edit code unless the user explicitly switches to implementation.
- Do not turn main Codex into a passive dispatcher. Main Codex remains the orchestrator and final owner.
- Use auxiliary agents only as read-only sensors for bounded discovery, source lookup, or acceptance review.
- Main Codex owns `.ai/` artifact writes. Skills provide templates and rules; auxiliary agents do not write persistent artifacts.
- After task breakdown, keep context locked to one bounded milestone at a time.

## Workflow

1. Restate the user's goal in one sentence.
2. Identify the decision space: product, UX, architecture, implementation, testing, security, release, or operations.
3. Classify the work:
   - direct small edit
   - discovery then direct edit
   - `/plan` needed
   - `/goal` + `/plan` + `.ai/` needed
   - strict security, release, or architecture review needed
4. Inspect local project context only when it materially changes the recommendation.
5. Generate options:
   - Minimal / safe
   - Balanced
   - Strategic / ambitious
6. Convert the recommended option into bounded task candidates:
   - Discovery task
   - Decision task
   - Build task
   - Verification task
   - Acceptance task
7. Decide whether read-only delegation is useful:
   - `ksi-explorer` for repo files, tests, fixtures, symbols, and call paths
   - `ksi-librarian` for official docs, SDK behavior, deprecations, and migration guidance
   - `ksi-acceptance-reviewer` after meaningful work when acceptance evidence matters
8. Define the context lock:
   - current bounded milestone
   - queued follow-ups
   - when to re-plan
9. Compare tradeoffs by impact, risk, cost, and reversibility.
10. Recommend one path and the next concrete step.
11. If implementation should follow, produce a `/goal`, `/plan`, or bounded build prompt.

## Output

```md
## Goal

## Current Understanding

## Classification

## Options
### A. Minimal / Safe
### B. Balanced
### C. Strategic

## Task Candidates

## Delegation Recommendation

## Context Lock

## Recommendation

## Next Actions

## Assumptions / Questions
```

## Escalation

If the brainstorm touches auth, permissions, tenant isolation, secrets, customer data, DB migrations, billing, deployment, or production operations, recommend `/goal` + `/plan` and a stricter review path before implementation.
