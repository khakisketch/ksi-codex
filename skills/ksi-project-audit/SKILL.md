---
name: ksi-project-audit
description: Use when the user asks for a broad project audit, missing parts, weak spots, quality review, structure review, refactoring opportunities, test gaps, or what to improve next. Korean triggers include 전체적으로 분석, 미비한 부분, 개선점, 품질 점검, 구조 점검, 리팩토링 포인트.
---

# KSI Project Audit

Use this skill to turn broad project improvement requests into prioritized, evidence-based findings and next tasks.

## Scope

Audit the current repository or requested subpath. Prefer concrete file evidence over general advice.

## Workflow

1. Identify project type and major entry points.
2. Read project guidance: `AGENTS.md`, README, and relevant docs when present.
3. Inspect build, package, test, and deployment configuration.
4. Check git status and current diff if relevant.
5. Locate core source directories and major flows.
6. Evaluate:
   - architecture and module boundaries
   - test coverage and reliability
   - error handling and observability
   - security and secret handling
   - auth, authorization, and tenant isolation when applicable
   - data model and migration risk when applicable
   - developer experience and documentation
   - existing typecheck, lint, test, and LSP diagnostics setup
   - UI/UX surface if the product is screen-driven
7. Prioritize findings by impact, confidence, and actionability.
8. Recommend the next 3 concrete tasks.

## Output

```md
## Executive Summary

## What I Inspected

## Findings
### High Priority
### Medium Priority
### Low Priority

## Recommended Next 3 Tasks

## Suggested Verification

## Risks / Unknowns
```

## Rules

- Do not pretend to inspect files that were not inspected.
- If the repo is too large, sample strategically and say what was sampled.
- Do not perform broad source edits during the audit.
- For security/auth/tenant/customer-data domains, pair with `ksi-security-review`.
- For DB/infra/billing/deployment/release domains, pair with `ksi-release-risk`.
