# ksi-codex

Private, portable KSI Codex configuration for reproducing the owner's active
Codex behavior on another personal computer.

The portable baseline is synchronized from the active source PC and targets
Codex CLI `0.155.1` behavior.
It installs only durable behavior configuration. Authentication, sessions,
memories, browser profiles, project trust paths, absolute machine paths, and
other local state are deliberately excluded.

## Managed baseline

- `~/.codex/AGENTS.md`: concise KSI global routing
- `~/.codex/agents/*.toml`: the complete configured role roster
- `~/.codex/rules/ksi-default.rules`: conservative command rules
- optional portable Codex config as either:
  - `~/.codex/ksi.config.toml` for `codex --profile ksi`
  - `~/.codex/config.toml` for matching default behavior
- Context7 MCP through portable `npx -y @upstash/context7-mcp` and Exa MCP URL
- plugin enable/disable preferences; plugin login and connection state are not copied

The repository's historical `skills/` and `presets/` remain reference material;
the active agent roster under `codex/agents/` is installed as a unit.

## Security boundary

The portable config intentionally reproduces the owner's current high-authority
local settings:

```toml
approval_policy = "never"
sandbox_mode = "danger-full-access"
```

Use config replacement only on a personal machine where this is intentional.
The safer profile installation does not replace the existing default config.

Never copy or commit any of the following:

- `~/.codex/auth.json`
- `~/.codex/config.toml` copied wholesale from a machine
- session, history, SQLite, memory, attachment, browser, or cache directories
- API keys, OAuth tokens, cookies, passwords, private keys, or `.env` files

## Install on another computer

Authenticate the computer to the GitHub account that can access the private repo,
then clone it:

```bash
gh auth login
gh repo clone khakisketch/ksi-codex ~/ksi-codex
cd ~/ksi-codex
```

Safe profile installation:

```bash
./install.sh --dry-run --mode copy --config-mode profile --backup
./install.sh --mode copy --config-mode profile --backup
python3 scripts/check.py --skip-mcp
codex --profile ksi
```

Exact portable default behavior on a dedicated personal PC:

```bash
./install.sh --dry-run --mode copy --config-mode replace --backup
./install.sh --mode copy --config-mode replace --backup
python3 scripts/check.py
```

Restart Codex after installation. Sign in to Codex and reconnect GitHub, Chrome,
browser, Sites, or other plugins on the new computer; their credentials are not
part of this repository.

## Verify and update

```bash
python3 -m py_compile scripts/apply.py scripts/check.py scripts/uninstall.py
python3 scripts/check.py --source-only --skip-mcp
./install.sh --dry-run --mode copy --config-mode replace --backup
```

For subsequent updates:

```bash
git pull --ff-only
./install.sh --dry-run --mode copy --config-mode replace --backup
./install.sh --mode copy --config-mode replace --backup
python3 scripts/check.py
```

See [CURRENT_STATE.md](CURRENT_STATE.md), [docs/install.md](docs/install.md), and
[INSTALL_PROMPT.md](INSTALL_PROMPT.md).
