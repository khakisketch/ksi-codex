# LSP / Typecheck Policy

KSI Codex does not select or install a fixed LSP stack.

Instead, it detects and uses the user's existing project tooling:
- package scripts
- typecheck commands
- lint commands
- test commands
- local language server binaries
- project config files
- editor/LSP setup when surfaced through Codex tools

## Principle

LSP is not the agent's brain. It is a code-reality sensor.

Use it to reduce:
- hallucinated APIs
- broken imports
- missing references
- invalid renames
- type errors
- framework convention mistakes
- dead or unused code

## Default Policy

- Do not auto-install language servers in v1.
- Do not change editor settings automatically.
- Detect existing project tooling first.
- Prefer repo-owned commands over global binaries.
- Treat LSP diagnostics as advisory unless backed by project-owned commands or CI.
- Use the lightest reliable verification method.

## Detection Targets

KSI Codex can detect:
- `package.json` scripts: `typecheck`, `lint`, `test`, `test:e2e`
- `tsconfig.json`
- ESLint config
- Vitest, Playwright, Cypress config
- `pyproject.toml`, `pyrightconfig.json`, `mypy.ini`, `ruff.toml`
- `Cargo.toml`
- `go.mod`
- `compile_commands.json`
- common language-server binaries already on PATH

## Recommended Flow

After meaningful code changes:

1. Run the smallest relevant formatter/lint/typecheck command if available.
2. Run the smallest relevant test suite.
3. Use LSP diagnostics when available to catch symbol/type/reference mistakes.
4. Use Codex `/review` for code-diff review when useful.
5. Use `ksi-security-review`, `ksi-release-risk`, or `ksi-ui-ux-review` when the task demands it.

## Examples

```text
INFO TypeScript project detected.
INFO package.json has typecheck script: npm run typecheck.
INFO package.json has lint script: npm run lint.
WARN tsconfig.json detected but no typecheck script found.
```

```text
INFO Python project detected.
INFO pyrightconfig.json detected.
INFO ruff config detected.
INFO pyright binary found on PATH.
```
