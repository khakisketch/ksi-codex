---
name: ksi-ui-ux-review
description: Use when the user asks to review or improve a screen, dashboard, SaaS workflow, admin panel, B2B product UI, onboarding flow, data-heavy interface, Figma design, screenshot, or implemented frontend from a target-customer UX perspective. Korean triggers include UI, UX, 화면, 대시보드, 고객이 쓰기 어렵다, 플로우, 스크린샷, 디자인 개선.
---

# KSI UI / UX Review

Use this skill to review product screens from the target customer's perspective. This is a product-quality workflow, not a generic "make it pretty" pass.

## Evidence Sources

Use the best available evidence:
- screenshot or attached image
- running browser view
- Figma/design source when explicitly provided
- local frontend code and routes
- product requirements or user journey docs

Do not launch browser automation for every UI task by default. Prefer the lightest reliable evidence. If durable regression protection is needed, convert important findings into project-owned tests.

## Review Axes

- target user and job-to-be-done
- information hierarchy
- primary action clarity
- scanability for dense dashboards/admin tools
- form friction and validation feedback
- empty, loading, error, success, and permission states
- mobile and desktop responsiveness
- visual consistency and spacing rhythm
- accessibility basics: labels, contrast, focus, keyboard, semantics
- copy clarity and terminology
- trust, safety, auditability, and confidence cues for B2B/admin tools
- whether the screen supports repeated operational use

## Workflow

1. Identify target user, context, and intended task.
2. Inspect the evidence. If evidence is missing, review the visible code or ask for the minimum needed artifact.
3. Separate UX blockers from visual polish.
4. Recommend fixes in priority order.
5. When implementation is requested, translate findings into a bounded `/goal` or `/plan`.
6. If a recurring UI issue is likely, recommend a repo-owned test or screenshot check.

## Output

```md
## UX Verdict
Strong / Usable With Issues / Needs Rework / Blocked

## Target User And Task

## High-Impact Issues

## Medium-Impact Improvements

## Visual / Copy Polish

## Suggested Implementation Plan

## Verification
```

## Product Guidance

For SaaS, B2B, CRM, admin, operations, and engineering tools, prioritize dense but organized information, predictable navigation, clear controls, and repeated-use efficiency over decorative landing-page styling.
