# Vibe Intake

KSI Codex expects vague, product-shaped, or founder-style requests. The goal is to turn the user's intent into bounded work without forcing the user to provide a perfect engineering spec.

## Main Rule

Main Codex is the orchestrator, planner, builder, tester, coordinator, and final owner.

Auxiliary agents are read-only sensors:
- `ksi-explorer`: repository discovery
- `ksi-librarian`: official docs and external source lookup
- `ksi-acceptance-reviewer`: final acceptance review

Do not add a standing builder, planner, architect, test-writer, security-reviewer, or release-reviewer in v1.

Main Codex also owns `.ai/` artifact writes. Skills provide templates and rules; auxiliary agents do not write persistent planning, state, or handoff files.

## Intake Steps

1. Restate the likely intent.
2. Classify scope and risk.
3. Split the request into bounded tasks.
4. Decide whether read-only delegation is useful.
5. Implement the current bounded task in main Codex.
6. Verify with the lightest reliable method.
7. Run acceptance review when the work is meaningful or risky.

## Classification

| Request Shape | Default Handling |
| --- | --- |
| Clear small edit | Execute directly |
| Vague but low-risk edit | State assumption, inspect, execute |
| Unknown-cause bug | Plan before editing |
| Multi-file feature | `/goal` + `/plan` |
| DB/API/auth/data-impacting change | `/goal` + `/plan` + strict ownership |
| Security/release/architecture risk | Conditional high-risk review mode |
| UI/UX request | Screenshot/browser evidence when visual judgment matters |

## Bounded Task Breakdown

Break vague work into:
- Discovery
- Decision
- Build
- Verification
- Acceptance

Only the current bounded task should be implemented. Later milestones should remain in the plan or handoff.

## Context Lock

Once the current bounded milestone is selected, main Codex should lock context around that milestone.

If the user adds a new request mid-build:
- incorporate it only if it is a small clarification of the current milestone
- queue it as a follow-up if it is related but not required now
- stop and re-plan if it changes scope, priority, safety, or acceptance criteria

For non-trivial work, queued follow-ups should be recorded in `.ai/handoff.md` or the final response.

## `.ai/` Artifact Ownership

Main Codex writes `.ai/` artifacts according to the active workflow.

Auxiliary agents are read-only:
- `ksi-explorer` returns repository findings
- `ksi-librarian` returns source findings
- `ksi-acceptance-reviewer` returns review findings

They do not update `.ai/`, source files, tests, migrations, or config.

## Memories

Vibe Intake may use Codex memories only for stable preferences, such as preferred workflow, communication style, or commonly used stacks.

Memories must not drive active task state. The current bounded milestone, queued follow-ups, task-state, and handoff belong in `.ai/` or the final response for small work.

Do not generate memories from sensitive vibe sessions involving production data, customer data, secrets, external SaaS data, or security-sensitive context.

## Delegation Rules

Delegate to `ksi-explorer` when:
- file ownership is unclear
- related tests or fixtures must be found
- call paths or symbols need tracing
- broad repo search would pollute main context

Delegate to `ksi-librarian` when:
- official docs may have changed
- SDK behavior differs by version
- deprecated behavior must be confirmed
- migration, security, permission, or billing guidance is needed

Delegate to `ksi-acceptance-reviewer` when:
- meaningful code was changed
- acceptance criteria matter
- verification adequacy is uncertain
- security, release, architecture, or UI/UX evidence must be checked

## Question Policy

Ask only blocking questions. Prefer 0 questions when safe assumptions are enough. Ask at most 1-3 questions when implementation, acceptance, or safety would change materially.

## Stop Conditions

Stop and return to planning when:
- the implementation invalidates the plan
- scope expands beyond the current milestone
- security/release/architecture risk appears unexpectedly
- verification cannot establish basic confidence
- the user intent is materially ambiguous
