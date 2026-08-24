# Installation and portability

## Requirements

- A Linux, macOS, or WSL shell
- Git
- Python 3.11 or newer
- Codex CLI
- GitHub CLI for convenient access to the private repository
- Node.js and `npx` if Context7 MCP should be active

Use the same GitHub identity that has access to `khakisketch/ksi-codex`.

## Installer scope

The installer manages four files at most:

```text
~/.codex/AGENTS.md
~/.codex/agents/explorer.toml
~/.codex/rules/ksi-default.rules
~/.codex/ksi.config.toml or ~/.codex/config.toml
```

It does not inspect, copy, or export authentication and session state.

## Config modes

### `profile` (default and safest)

Installs `~/.codex/ksi.config.toml`. Start Codex with:

```bash
codex --profile ksi
```

### `replace`

Installs the portable config as `~/.codex/config.toml`. This reproduces the
owner's current portable defaults, including `approval_policy = "never"` and
`sandbox_mode = "danger-full-access"`. Always use `--backup` unless the target
does not exist.

### `skip`

Installs instructions, the explorer agent, and command rules without installing
a config file.

## Conflict and backup policy

The installer does not silently overwrite a different file. Without `--backup`
or `--force`, a conflict stops installation. Backups are written to:

```text
~/.codex/backups/<filename>.<timestamp>
```

`--force` replaces conflicting files without backup and should not be used for
normal installation.

## Machine-local follow-up

After the portable files are installed:

1. Sign in to Codex normally on the new PC.
2. Confirm `node` and `npx` exist for Context7.
3. Restart Codex.
4. Reconnect plugins and OAuth-backed apps manually.
5. Clone each project repository so its repository-owned `AGENTS.md` files are present.
6. Add project trust entries locally; do not copy another PC's absolute paths.

## Uninstall

Preview first:

```bash
python3 scripts/uninstall.py --dry-run --remove-agents --remove-config-profile
```

The uninstaller removes a managed file only when it still matches the repository
source. It never automatically removes `~/.codex/config.toml`.
