# Model Tiering

KSI Codex uses model and reasoning effort as routing controls, not as a status symbol.

## Default Structure

```text
main Codex
├─ ksi-explorer
├─ ksi-librarian
└─ ksi-acceptance-reviewer
```

Main Codex owns planning, building, testing, coordination, and final user response.

## Defaults

| Surface | Model | Reasoning Effort | Purpose |
| --- | --- | --- | --- |
| main Codex | `gpt-5.5` | high or xhigh by user/session setting | planning, implementation, coordination, final response |
| `/plan` | `gpt-5.5` | xhigh | implementation design and verification plan |
| `ksi-explorer` | `gpt-5.4-mini` | low | fast read-only codebase exploration |
| `ksi-librarian` | `gpt-5.4-mini` | medium | official docs, external source lookup, deprecation and migration checks |
| `ksi-acceptance-reviewer` | `gpt-5.5` | high | final acceptance and delivery readiness review |

## Escalation

Use xhigh only when the extra cost is justified:
- failed review gates
- high-risk ambiguity
- production data
- security-sensitive changes
- DB migration or rollback risk
- billing, tenant isolation, or permission risk
- repeated review disagreement
- architecture decisions that affect module boundaries, schema, realtime infra, AI pipelines, or multi-tenant behavior

## Librarian Medium Triggers

`ksi-librarian` defaults to `gpt-5.4-mini` medium because official-source research often needs careful synthesis.

Medium effort is especially useful when:
- official docs conflict
- SDK behavior differs by version
- deprecated behavior must be confirmed
- security, permission, or billing docs are involved
- migration guides require interpretation

## Non-Goals

Do not use deprecated Codex models.

Do not add standing v1 agents for:
- planner
- architect
- test-writer
- debugger
- refactorer
- doc-writer
- security-reviewer
- release-reviewer

Use conditional review modes instead.
