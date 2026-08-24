---
name: ksi-security-review
description: Use for security-sensitive planning or review involving auth, authorization, permissions, tenant isolation, secrets, customer data, file access, signed URLs, logs, privacy, or data exposure. Korean triggers include 보안, 인증, 인가, 권한, tenant, 멀티테넌시, 데이터 노출, secret, 고객 데이터.
---

# KSI Security Review

Use this skill as a security checklist and reasoning workflow. It does not replace current code inspection.

## Principles

- Current code, config, diff, and tests are the source of truth.
- Never read or print secret values from `.env*` files.
- Prefer concrete attack paths and data exposure scenarios over generic advice.
- Separate confirmed issues from plausible risks.
- If evidence is insufficient, mark the review as blocked or conditional.

## Planning Workflow

1. Identify protected assets and trust boundaries.
2. Identify actors, roles, tenants, and ownership rules.
3. Identify entry points and authorization decision points.
4. Define non-goals and implementation constraints.
5. Specify required verification before build starts.

## Review Workflow

1. Reconstruct intended security behavior from the request, plan, docs, and diff.
2. Inspect changed files and relevant auth/data-access paths.
3. Check server-side authorization and tenant filters.
4. Check whether sensitive data can leak through responses, logs, errors, cache, URLs, files, tests, or browser state.
5. Check whether verification covers allowed and denied cases.
6. Decide `Approved`, `Needs changes`, or `Blocked`.

## Checklist

- Authentication required where expected?
- Authorization enforced server-side?
- Tenant/customer/site filters applied consistently?
- Object IDs cannot access another tenant's data?
- Admin/service roles constrained?
- Secrets never logged, returned, committed, or printed?
- File upload/download validates ownership, type, size, and expiry?
- Error messages avoid leaking sensitive details?
- Tests cover forbidden, cross-tenant, and unauthenticated access?

## Output

```md
## Security Verdict
Approved / Needs changes / Blocked

## Protected Assets / Trust Boundaries

## Confirmed Issues

## Plausible Risks

## Required Fixes Or Acceptance Questions

## Verification Required

## Residual Risks
```
