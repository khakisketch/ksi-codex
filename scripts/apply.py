#!/usr/bin/env python3
"""Install the portable KSI Codex configuration without copying local state."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class InstallAction:
    label: str
    source: Path
    target: Path
    mode: str


class Installer:
    def __init__(
        self,
        *,
        home: Path,
        mode: str,
        config_mode: str,
        dry_run: bool,
        backup: bool,
        force: bool,
    ) -> None:
        self.home = home
        self.mode = mode
        self.config_mode = config_mode
        self.dry_run = dry_run
        self.backup = backup
        self.force = force
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.conflicts: list[str] = []
        self.changed = 0
        self.skipped = 0

    @property
    def codex_home(self) -> Path:
        return self.home / ".codex"

    @property
    def backups_home(self) -> Path:
        return self.codex_home / "backups"

    def actions(self) -> list[InstallAction]:
        actions = [
            InstallAction(
                label="global AGENTS.md",
                source=REPO_ROOT / "codex" / "AGENTS.md",
                target=self.codex_home / "AGENTS.md",
                mode=self.mode,
            ),
            InstallAction(
                label="command rules",
                source=REPO_ROOT / "codex" / "rules" / "ksi-default.rules",
                target=self.codex_home / "rules" / "ksi-default.rules",
                mode=self.mode,
            ),
        ]
        actions.extend(
            InstallAction(
                label=f"agent {source.name}",
                source=source,
                target=self.codex_home / "agents" / source.name,
                mode=self.mode,
            )
            for source in sorted((REPO_ROOT / "codex" / "agents").glob("*.toml"))
        )

        if self.config_mode == "profile":
            actions.append(
                InstallAction(
                    label="portable config profile",
                    source=REPO_ROOT / "codex" / "config.portable.toml",
                    target=self.codex_home / "ksi.config.toml",
                    mode=self.mode,
                )
            )
        elif self.config_mode == "replace":
            actions.append(
                InstallAction(
                    label="portable default config",
                    source=REPO_ROOT / "codex" / "config.portable.toml",
                    target=self.codex_home / "config.toml",
                    mode=self.mode,
                )
            )
        return actions

    def run(self) -> int:
        if self.config_mode == "replace":
            print(
                "NOTICE: config replacement enables approval_policy=never and "
                "sandbox_mode=danger-full-access."
            )
        if self.force and not self.backup:
            print("WARNING: --force replaces conflicting targets without backup.")

        for action in self.actions():
            self.apply_action(action)

        if self.conflicts:
            print()
            print("Installation stopped because conflicting targets already exist:")
            for conflict in self.conflicts:
                print(f"- {conflict}")
            print()
            print("Use --backup to preserve existing targets before replacing them.")
            print("Use --force only when replacement without backup is intentional.")
            return 2

        print()
        if self.dry_run:
            print("Dry run complete. No files were modified.")
        else:
            print(f"Install complete: {self.changed} changed, {self.skipped} skipped.")
            print("Restart Codex to load the installed instructions and configuration.")
        return 0

    def apply_action(self, action: InstallAction) -> None:
        target = action.target
        if self.target_matches(action):
            self.skipped += 1
            print(f"SKIP {action.label}: already up to date ({target})")
            return

        if target.exists() or target.is_symlink():
            if not self.backup and not self.force:
                print(f"CONFLICT {action.label}: {target}")
                self.conflicts.append(str(target))
                return
            if self.backup:
                self.backup_target(target)
            else:
                print(f"REPLACE {action.label}: {target}")
                if not self.dry_run:
                    self.remove_target(target)

        if self.dry_run:
            verb = "LINK" if action.mode == "symlink" else "WRITE"
            print(f"DRY-RUN {verb} {action.label}: {target}")
            return

        target.parent.mkdir(parents=True, exist_ok=True)
        self.install_target(action)
        self.changed += 1
        print(f"OK {action.label}: {target}")

    def target_matches(self, action: InstallAction) -> bool:
        target = action.target
        if not target.exists() and not target.is_symlink():
            return False
        if action.mode == "symlink":
            return target.is_symlink() and target.resolve() == action.source.resolve()
        if action.source.is_dir():
            return target.is_dir() and digest_dir(action.source) == digest_dir(target)
        return target.is_file() and digest_file(action.source) == digest_file(target)

    def install_target(self, action: InstallAction) -> None:
        if action.mode == "symlink":
            os.symlink(action.source, action.target, target_is_directory=action.source.is_dir())
        elif action.source.is_dir():
            shutil.copytree(action.source, action.target)
        else:
            shutil.copy2(action.source, action.target)

    def backup_target(self, target: Path) -> None:
        backup_path = self.backup_path_for(target)
        print(f"BACKUP {target} -> {backup_path}")
        if self.dry_run:
            return
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(target), str(backup_path))

    def backup_path_for(self, target: Path) -> Path:
        candidate = self.backups_home / f"{target.name}.{self.timestamp}"
        counter = 1
        while candidate.exists():
            candidate = self.backups_home / f"{target.name}.{self.timestamp}.{counter}"
            counter += 1
        return candidate

    @staticmethod
    def remove_target(target: Path) -> None:
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)


def digest_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def digest_dir(path: Path) -> str:
    hasher = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        rel = item.relative_to(path).as_posix()
        if "__pycache__" in item.parts:
            continue
        hasher.update(rel.encode("utf-8"))
        if item.is_symlink():
            hasher.update(b"symlink")
            hasher.update(os.readlink(item).encode("utf-8"))
        elif item.is_file():
            hasher.update(b"file")
            hasher.update(digest_file(item).encode("ascii"))
        elif item.is_dir():
            hasher.update(b"dir")
    return hasher.hexdigest()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the portable KSI Codex configuration.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions only.")
    parser.add_argument(
        "--mode",
        choices=["copy", "symlink"],
        default="copy",
        help="Copy files for normal use or symlink them for repository development.",
    )
    parser.add_argument(
        "--config-mode",
        choices=["skip", "profile", "replace"],
        default="profile",
        help=(
            "skip config, install ~/.codex/ksi.config.toml for --profile ksi, "
            "or replace ~/.codex/config.toml"
        ),
    )
    parser.add_argument("--backup", action="store_true", help="Back up conflicts first.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace conflicts without backup. Use with care.",
    )
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory to install into. Defaults to the current user's home.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    installer = Installer(
        home=args.home.expanduser(),
        mode=args.mode,
        config_mode=args.config_mode,
        dry_run=args.dry_run,
        backup=args.backup,
        force=args.force,
    )
    return installer.run()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
