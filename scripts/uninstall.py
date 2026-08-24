#!/usr/bin/env python3
"""Conservatively remove files installed by the portable KSI Codex bundle."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def remove(path: Path, dry_run: bool) -> None:
    if not path.exists() and not path.is_symlink():
        print(f"SKIP missing: {path}")
        return
    print(f"REMOVE {path}")
    if dry_run:
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def remove_if_managed(target: Path, source: Path, dry_run: bool) -> None:
    if not target.exists() and not target.is_symlink():
        print(f"SKIP missing: {target}")
        return
    if target.is_symlink() and target.resolve() == source.resolve():
        remove(target, dry_run)
        return
    if target.is_file() and digest(target) == digest(source):
        remove(target, dry_run)
        return
    print(f"SKIP modified or unmanaged: {target}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Uninstall portable KSI Codex files.")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--remove-agents", action="store_true")
    parser.add_argument("--remove-config-profile", action="store_true")
    args = parser.parse_args(argv)

    home = args.home.expanduser()
    codex_home = home / ".codex"
    remove_if_managed(
        codex_home / "rules" / "ksi-default.rules",
        REPO_ROOT / "codex" / "rules" / "ksi-default.rules",
        args.dry_run,
    )
    remove_if_managed(
        codex_home / "agents" / "explorer.toml",
        REPO_ROOT / "codex" / "agents" / "explorer.toml",
        args.dry_run,
    )

    if args.remove_agents:
        remove_if_managed(
            codex_home / "AGENTS.md",
            REPO_ROOT / "codex" / "AGENTS.md",
            args.dry_run,
        )
    else:
        print("SKIP ~/.codex/AGENTS.md (pass --remove-agents to remove it)")

    if args.remove_config_profile:
        remove_if_managed(
            codex_home / "ksi.config.toml",
            REPO_ROOT / "codex" / "config.portable.toml",
            args.dry_run,
        )
    else:
        print("SKIP ~/.codex/ksi.config.toml (pass --remove-config-profile to remove it)")

    print("SKIP ~/.codex/config.toml: default config replacement is never auto-removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
