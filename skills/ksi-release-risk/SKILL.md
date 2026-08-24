---
name: ksi-release-risk
description: Use for production-readiness risk involving deploy, release, DB migration, data backfill, infra, CI/CD, billing/payment, rollback, observability, incidents, or customer-impacting rollout. Korean triggers include 배포, 운영, 릴리즈, DB migration, infra, 결제, rollback, 장애, observability.
---

# KSI Release Risk

Use this skill for material delivery, deployment, data, billing, or operational risk.

## Principles

- Delivery safety matters more than abstract architecture purity.
- Prefer concrete failure modes, blast radius, rollout order, and rollback plan.
- Distinguish local development risk from production risk.
- If evidence is insufficient, approval should be conditional or blocked.

## Checklist

- Scope and non-goals are clear?
- Backward and forward compatibility considered?
- Migration deploy order safe?
- Rollback plan exists and is realistic?
- Data backfill or cleanup needed?
- Observability/logging/metrics sufficient?
- Feature flag or phased rollout needed?
- Secrets/IAM/environment changes documented?
- Billing/customer impact understood?
- Existing integrations or adapters affected?
- Tests cover critical failure paths?

## Workflow

1. Identify the release unit and affected systems.
2. Identify data changes, dependencies, and rollout order.
3. Identify the failure modes and blast radius.
4. Define verification before and after release.
5. Define rollback or mitigation.
6. Decide `Approved`, `Needs changes`, or `Blocked`.

## Output

```md
## Release Verdict
Approved / Needs changes / Blocked

## Key Risks

## Required Changes Before Delivery

## Rollout Plan

## Rollback Plan

## Observability / Verification

## Residual Risks
```
